"""Build Final_Manuscript.docx/.pdf and cover_letter.docx for Bioresource Technology.

* {{token}}           -> value from manuscript_values.compute() (all from generated result files)
* {{TABLE:name}}      -> editable Word table from tables/<name>.csv (caption from tables/<name>.md)
* {{FIG:name|caption}}-> figure from figures/<name>.png with caption
* [@Key; @Key2]       -> author–year citation, resolved ONLY against references.json (verified metadata)
Unresolved tokens or citations abort the build.
"""
from __future__ import annotations

import json, os, re, subprocess, sys
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(REPO, "manuscript")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, "code"))
from manuscript_values import compute  # noqa: E402

REFS = json.load(open(os.path.join(HERE, "references.json")))
PARTS = ["part0_front.md", "part1_intro_methods.md", "part2_results.md", "part3_back.md"]


def cite(m, used):
    keys = [k.strip().lstrip("@") for k in m.group(1).split(";")]
    out = []
    for k in keys:
        if k not in REFS:
            raise KeyError(f"unverified citation key: {k}")
        used.append(k) if k not in used else None
        out.append(REFS[k]["cite"])
    return "(" + "; ".join(out) + ")"


TAB = os.environ.get("STRATA_TABLES", os.path.join(REPO, "tables"))
FIG = os.environ.get("STRATA_FIGURES", os.path.join(REPO, "figures"))
OUT = os.environ.get("STRATA_OUT", OUT)


def table_md(name, tlabel):
    df = pd.read_csv(os.path.join(TAB, f"{name}.csv"))
    cap = open(os.path.join(TAB, f"{name}.md")).read().splitlines()[0].strip("*")
    cap = re.sub(r"^Table \w+\.\s*", "", cap)
    df = df.fillna("")
    head = "| " + " | ".join(str(c) for c in df.columns) + " |\n|" + "|".join(["---"] * len(df.columns)) + "|\n"
    body = "".join("| " + " | ".join(str(v) for v in r) + " |\n" for r in df.itertuples(index=False))
    return f"\n**{tlabel}.** {cap}\n\n{head}{body}\n"


def render(values, parts=PARTS, table_prefix="Table ", fig_prefix="Fig. "):
    used, text = [], ""
    for p in parts:
        text += open(os.path.join(HERE, p)).read() + "\n\n"
    tcount = [0]

    def tab(m):
        tcount[0] += 1
        return table_md(m.group(1), f"{table_prefix}{tcount[0]}")
    text = re.sub(r"\{\{TABLE:([\w\-]+)\}\}", tab, text)
    fcount = [0]

    def fig(m):
        fcount[0] += 1
        name, cap = m.group(1), m.group(2)
        return f"\n![**{fig_prefix}{fcount[0]}.** {cap}]({os.path.join(FIG, name + '.png')}){{width=16cm}}\n"
    text = re.sub(r"\{\{FIG:([\w\-]+)\|(.+?)\}\}", fig, text)

    def tok(m):
        k = m.group(1)
        if k not in values:
            if os.environ.get("STRATA_ALLOW_MISSING") == "1":  # render-testing only; final build is strict
                return f"[[MISSING:{k}]]"
            raise KeyError(f"unresolved token {{{{{k}}}}}")
        return str(values[k])
    text = re.sub(r"\{\{([\w\.\-]+)\}\}", tok, text)
    text = re.sub(r"\[(@[\w]+(?:\s*;\s*@[\w]+)*)\]", lambda m: cite(m, used), text)
    if "{{" in text or "[@" in text:
        raise ValueError("unresolved placeholders remain")
    refs = sorted(set(used), key=lambda k: REFS[k]["text"].lower())
    text = text.replace("<<REFERENCES>>", "\n".join(f"::: {{custom-style=\"Bibliography\"}}\n{REFS[k]['text']}\n:::\n" for k in refs))
    return text, refs


def make_reference_docx(path):
    subprocess.run(["pandoc", "-o", path, "--print-default-data-file", "reference.docx"], check=True)
    from docx import Document
    from docx.shared import Pt
    from docx.enum.text import WD_LINE_SPACING
    d = Document(path)
    for st in d.styles:
        try:
            if st.type != 1:
                continue
        except Exception:
            continue
        f = st.font
        f.name = "Times New Roman"; f.color.rgb = None
        rpr = st.element.get_or_add_rPr()
        rfonts = rpr.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rFonts")
        if rfonts is not None:
            for a in ["ascii", "hAnsi", "cs", "eastAsia"]:
                rfonts.set(f"{{http://schemas.openxmlformats.org/wordprocessingml/2006/main}}{a}", "Times New Roman")
            for a in ["asciiTheme", "hAnsiTheme", "cstheme", "eastAsiaTheme"]:
                k = f"{{http://schemas.openxmlformats.org/wordprocessingml/2006/main}}{a}"
                if k in rfonts.attrib:
                    del rfonts.attrib[k]
    sizes = {"Normal": 12, "Body Text": 12, "First Paragraph": 12, "Compact": 10, "Title": 16, "Heading 1": 13, "Heading 2": 12,
             "Heading 3": 12, "Abstract": 12, "Image Caption": 11, "Table Caption": 11, "Bibliography": 11}
    for name, sz in sizes.items():
        try:
            st = d.styles[name]
        except KeyError:
            continue
        st.font.size = Pt(sz)
        if name.startswith("Heading") or name == "Title":
            st.font.bold = True; st.font.italic = name == "Heading 3"
        pf = st.paragraph_format
        if name in ("Normal", "Body Text", "First Paragraph", "Abstract", "Bibliography"):
            pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    d.save(path)


def postprocess(path):
    from docx import Document
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    from docx.shared import Pt, Cm
    d = Document(path)
    for s in d.sections:
        s.page_width, s.page_height = Cm(21.0), Cm(29.7)  # A4
        s.left_margin = s.right_margin = Cm(2.5); s.top_margin = s.bottom_margin = Cm(2.5)
        ln = OxmlElement("w:lnNumType"); ln.set(qn("w:countBy"), "1"); ln.set(qn("w:restart"), "continuous"); ln.set(qn("w:distance"), "283")
        s._sectPr.append(ln)
        p = s.footer.paragraphs[0]; p.alignment = 1
        r = p.add_run()
        for t, txt in [("begin", None), (None, "PAGE"), ("end", None)]:
            if t:
                e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), t); r._r.append(e)
            else:
                e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = txt; r._r.append(e)
    for t in d.tables:
        t.style = d.styles["Table"] if "Table" in [s.name for s in d.styles] else t.style
        for row in t.rows:
            for c in row.cells:
                for p in c.paragraphs:
                    p.paragraph_format.line_spacing = 1.0
                    for r in p.runs:
                        r.font.size = Pt(8.5)
        tbl = t._tbl; tblPr = tbl.tblPr
        b = OxmlElement("w:tblBorders")
        for edge in ["top", "bottom", "insideH"]:
            e = OxmlElement(f"w:{edge}"); e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "4"); e.set(qn("w:color"), "808080"); b.append(e)
        tblPr.append(b)
    d.save(path)


def to_pdf(path):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(path), path], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def build(parts, name, values, table_prefix="Table ", fig_prefix="Fig. ", pdf=True):
    text, refs = render(values, parts, table_prefix, fig_prefix)
    md = os.path.join(OUT, f"{name}.md"); open(md, "w").write(text)
    ref = os.path.join(HERE, "reference.docx"); make_reference_docx(ref)
    docx = os.path.join(OUT, f"{name}.docx")
    subprocess.run(["pandoc", md, "-f", "markdown+tex_math_dollars+pipe_tables+fenced_divs+implicit_figures+superscript+subscript", "-o", docx,
                    f"--reference-doc={ref}", "--resource-path", REPO], check=True)
    postprocess(docx)
    if pdf:
        to_pdf(docx)
    return refs


def main():
    values = compute()
    refs = build(PARTS, "Final_Manuscript", values)
    srefs = build(["supp.md"], "Supplementary_Material", values, table_prefix="Table S", fig_prefix="Fig. S")
    build(["cover_letter.md"], "cover_letter", values, pdf=False)
    json.dump(dict(cited_keys=refs, supplementary_cited=srefs, n_refs=len(refs), values=values), open(os.path.join(OUT, "build_log.json"), "w"),
              indent=1, default=str)
    print(f"built manuscript ({len(refs)} references), supplementary, cover letter; {len(values)} values")


if __name__ == "__main__":
    main()
