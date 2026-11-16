import re
import markdown
from fpdf import FPDF


def to_latin1(s: str) -> str:
    """Map Unicode punctuation/whitespace to Latin-1-safe equivalents."""
    table = {
        "\u2014": "-",   # em dash
        "\u2013": "-",   # en dash
        "\u2018": "'",   # left single quote
        "\u2019": "'",   # right single quote
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "\u2026": "...", # ellipsis
        "\u2022": "*",   # bullet
        "\u2192": "->",  # right arrow
        "\u2190": "<-",  # left arrow
        "\u00b7": "*",   # middle dot
        "\u00d7": "x",   # multiplication sign
        "\u2264": "<=",  # ≤
        "\u2265": ">=",  # ≥
        "\u00a0": " ",   # non-breaking space
        "\u2009": " ",   # thin space
        "\u200b": "",    # zero-width space
    }
    for k, v in table.items():
        s = s.replace(k, v)
    # drop anything still outside Latin-1
    return s.encode("latin-1", errors="ignore").decode("latin-1")


with open("docs/Capstone_Report.md", encoding="utf-8") as f:
    md = f.read()

md = to_latin1(md)
html = markdown.markdown(md, extensions=["tables"])
text = re.sub(r"<[^>]+>", "", html)


class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, "Mini-Courier Planner - Capstone Report",
                  align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 8, f"Page {self.page_no()}", align="C")


pdf = PDF()
pdf.add_page()
pdf.set_font("Helvetica", size=10)
for line in text.split("\n"):
    line = line.strip()
    if line:
        pdf.multi_cell(0, 6, line)
        pdf.ln(1)

pdf.output("docs/Capstone_Report.pdf")
print("Wrote docs/Capstone_Report.pdf")