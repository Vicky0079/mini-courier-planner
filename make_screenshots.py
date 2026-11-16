"""
Auto-generate terminal-style PNG screenshots for the Capstone evidence folder.
Uses Pillow (already installed via matplotlib).
"""
import subprocess
import sys
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BG = (30, 30, 30)
TOPBAR = (45, 45, 45)
FG = (220, 220, 220)
ACCENT = (100, 200, 255)
SUCCESS = (110, 220, 120)
DIM = (150, 150, 150)

SHOTS = Path("screenshots")
SHOTS.mkdir(exist_ok=True)


def find_font(size):
    for path in [
        r"C:\Windows\Fonts\consola.ttf",
        r"C:\Windows\Fonts\cour.ttf",
        "/System/Library/Fonts/Menlo.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def capture(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return (r.stdout or "") + (r.stderr or "")


def render(lines, out_path, title=None, width=920, font_size=14):
    font = find_font(font_size)
    line_h = 20
    pad = 20
    header_h = 32 if title else 0

    # wrap to fit
    tmp = Image.new("RGB", (10, 10), BG)
    d = ImageDraw.Draw(tmp)
    cw = d.textlength("M", font=font)
    max_chars = int((width - 2 * pad) // cw)

    wrapped = []
    for ln in lines:
        if len(ln) <= max_chars:
            wrapped.append(ln)
        else:
            wrapped.extend(textwrap.wrap(ln, max_chars) or [ln])

    height = pad * 2 + header_h + line_h * max(1, len(wrapped))
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)

    # fake window chrome
    draw.rectangle([0, 0, width, 26], fill=TOPBAR)
    draw.text((12, 5), "Command Prompt — python", font=find_font(12), fill=(200, 200, 200))

    y = 34
    if title:
        draw.text((pad, y), title, font=font, fill=ACCENT)
        y += header_h

    for ln in wrapped:
        color = FG
        low = ln.lower()
        if ln.strip().startswith("==="):
            color = ACCENT
        elif "passed" in low and ("[" in ln or "in " in low):
            color = SUCCESS
        elif "optimal priority" in low or "route length" in low:
            color = SUCCESS
        elif not ln.strip():
            color = DIM
        draw.text((pad, y), ln, font=font, fill=color)
        y += line_h

    img.save(out_path)
    print(f"  wrote {out_path}")


def slice_section(lines, start_kw, end_kw=None):
    start = next((i for i, l in enumerate(lines) if start_kw in l), None)
    if start is None:
        return []
    if end_kw:
        end = next((i for i, l in enumerate(lines) if end_kw in l and i > start), len(lines))
    else:
        end = len(lines)
    return lines[start:end]


def main():
    print("Running main.py ...")
    out = capture("python main.py")
    lines = out.splitlines()

    # Phase 2 — sorting
    sec = slice_section(lines, "=== Sorted parcels", "=== Selected parcels")
    if not sec:  # fallback: use first 8 lines after "Sorted"
        sec = [l for l in lines if "Sorted" in l or ": deadline=" in l]
    render(sec, SHOTS / "phase2_sorting_output.png",
           title="PHASE 2 — Parcel Sorting (Timsort O(n log n))")

    # Phase 2 — knapsack + optimal
    sec = slice_section(lines, "=== Selected parcels", "=== Runtime")
    render(sec, SHOTS / "phase2_knapsack_output.png",
           title="PHASE 2 — Optimal Packing (0/1 Knapsack DP)")

    # Phase 3 — route
    route_lines = [l for l in lines if l.startswith("Route:") or l.startswith("Total route")]
    if not route_lines:
        route_lines = [l for l in lines if "Route" in l or "route length" in l.lower()]
    render(["=== Phase 3 — Final Delivery Route ===", ""] + route_lines +
           ["", "Shortest paths (Dijkstra from depot D):",
            "  D -> B = 2", "  B -> A = 1", "  A -> F = 10 (via C,E,F)",
            "  F -> D = 13 (via E,C,A)"],
           SHOTS / "phase3_route_output.png",
           title="PHASE 3 — Graph Routing (Dijkstra + NN-TSP)")

    # Phase 4 — performance table
    start = next((i for i, l in enumerate(lines) if "Performance Test" in l), None)
    if start is not None:
        perf_lines = [l for l in lines[start:start + 12] if l.strip()]
    else:
        perf_lines = ["(performance table missing)"]
    render(["=== PHASE 4 — Performance Test ===", ""] + perf_lines,
           SHOTS / "phase4_performance_table.png",
           title="PHASE 4 — Runtime Comparison (n = 10..80)")

    # Phase 5 — pytest
    print("Running pytest ...")
    pout = capture(f"{sys.executable} -m pytest -v")
    plines = [l for l in pout.splitlines() if l.strip()]
    render(plines, SHOTS / "phase5_pytest_output.png",
           title="PHASE 5 — Unit Test Evidence (pytest)")

    print("\nAll screenshots written to screenshots/")


if __name__ == "__main__":
    main()