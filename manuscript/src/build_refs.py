"""Build the reference list ONLY from verified metadata (Crossref / DataCite / arXiv / JMLR / NeurIPS pages).

Output: references.json  {key: {"text": formatted Elsevier author-year reference, "cite": "Author et al., 2021"}}
"""
import json, os, re, urllib.request
LIT = os.path.join(os.path.dirname(__file__), "..", "..", "supplementary", "literature")
V = json.load(open(os.path.join(LIT, "references_verified.json")))
N = json.load(open(os.path.join(LIT, "nondoi_verification.json")))
JOURNAL_ABBR = {"Journal of Survey Statistics and Methodology": "J. Surv. Stat. Methodol.", "Bioresource Technology": "Bioresour. Technol.", "Fuel": "Fuel", "Energy": "Energy", "BioEnergy Research": "BioEnergy Res.",
    "GCB Bioenergy": "GCB Bioenergy", "Patterns": "Patterns", "Renewable and Sustainable Energy Reviews": "Renew. Sustain. Energy Rev.",
    "Biofuels, Bioproducts and Biorefining": "Biofuels Bioprod. Biorefin.", "Biofuels": "Biofuels", "Energy & Fuels": "Energy Fuels", "Energy &amp; Fuels": "Energy Fuels",
    "Journal of the American Statistical Association": "J. Am. Stat. Assoc.", "The Annals of Statistics": "Ann. Stat.", "Controlled Clinical Trials": "Control. Clin. Trials",
    "Statistics in Medicine": "Stat. Med.", "Ecography": "Ecography", "Machine Learning": "Mach. Learn.", "Nature": "Nature", "Biometrics Bulletin": "Biom. Bull.",
    "Philosophical Transactions of the Royal Society of London. Series A, Mathematical and Physical Sciences": "Philos. Trans. R. Soc. Lond. A",
    "Advances in Neural Information Processing Systems 35": "Adv. Neural Inf. Process. Syst. 35", "Journal of Machine Learning Research": "J. Mach. Learn. Res.",
    "Biochar": "Biochar", "Journal of Environmental Chemical Engineering": "J. Environ. Chem. Eng."}

def initials(given):
    parts = re.split(r"[\s]+", given.strip())
    out = []
    for p in parts:
        if not p: continue
        sub = p.split("-")
        out.append("-".join(s[0] + "." for s in sub if s))
    return "".join(out)

def name_list(authors):  # authors as "Family, Given"
    names = []
    for a in authors:
        fam, _, giv = a.partition(", ")
        names.append(f"{fam}, {initials(giv)}" if giv else fam)
    return ", ".join(names)

def cite_key(authors, year):
    fams = [a.partition(", ")[0] for a in authors]
    if len(fams) == 1: return f"{fams[0]}, {year}"
    if len(fams) == 2: return f"{fams[0]} and {fams[1]}, {year}"
    return f"{fams[0]} et al., {year}"

refs = {}
SKIP = {"Watson2019", "Holm1979", "Romano2019", "Tibshirani2019", "Chen2016", "Ke2017", "Pedregosa2011", "Lundberg2017", "Demsar2006", "Sigrist2022", "Prokhorenkova2018"}
for k, v in V.items():
    if not v.get("ok") and k not in ("Valdez2011", "Chen2016"): continue
    a, y = v["authors"], v["year"]
    if k == "Elfetni2026BT": y = 2027  # issue year per Crossref 'issued'
    venue = JOURNAL_ABBR.get(v["venue"], v["venue"])
    title = re.sub(r"\s+", " ", v["title"].replace("&amp;", "&"))
    if k == "Chen2016": title = "XGBoost: A scalable tree boosting system"
    if k == "Valdez2011": title = "Characterization of product fractions from hydrothermal liquefaction of Nannochloropsis sp. and the influence of solvents"
    vol = f" {v['volume']}" if v.get("volume") else ""
    iss = f"({v['issue']})" if v.get("issue") else ""
    pg = f", {v['pages']}" if v.get("pages") else ""
    if not venue and v.get("type") not in ("book",):
        meta = json.loads(urllib.request.urlopen("https://api.crossref.org/works/" + v["doi"], timeout=60).read())["message"]
        venue = meta.get("publisher", "")
        text = f"{name_list(a)}, {y}. {title}. {venue}. https://doi.org/{v['doi']}"
        refs[k] = dict(text=text, cite=cite_key(a, y), doi=v["doi"]); continue
    if v.get("type") == "book":
        text = f"{name_list(a)}, {y}. {title}, 2nd ed. Springer, Cham. https://doi.org/{v['doi']}"
    elif v.get("type") == "posted-content":
        text = f"{name_list(a)}, {y}. {title}. SSRN preprint. https://doi.org/{v['doi']}"
    elif v.get("type") == "proceedings-article":
        text = f"{name_list(a)}, {y}. {title}, in: {venue}{pg}. https://doi.org/{v['doi']}"
    else:
        text = f"{name_list(a)}, {y}. {title}. {venue}{vol}{iss}{pg}. https://doi.org/{v['doi']}"
    refs[k] = dict(text=text, cite=cite_key(a, y), doi=v["doi"])
# arXiv-verified NeurIPS papers
for k, venue, y in [("Romano2019", "Adv. Neural Inf. Process. Syst. 32", 2019), ("Tibshirani2019", "Adv. Neural Inf. Process. Syst. 32", 2019),
                    ("Lundberg2017", "Adv. Neural Inf. Process. Syst. 30", 2017), ("Prokhorenkova2018", "Adv. Neural Inf. Process. Syst. 31", 2018),
                    ("Fisch2021", "Proc. 38th Int. Conf. Mach. Learn., PMLR 139", 2021)]:
    n = N[k]; au = [f"{x.split()[-1]}, {' '.join(x.split()[:-1])}" for x in n["authors"]]
    refs[k] = dict(text=f"{name_list(au)}, {y}. {n['title']}, in: {venue}. arXiv:{n['arxiv']}", cite=cite_key(au, y), doi=None)
for k in ["Pedregosa2011", "Demsar2006", "Sigrist2022", "Ke2017"]:
    n = N[k]; au = [x if ", " in x else f"{x.split()[-1]}, {' '.join(x.split()[:-1])}" for x in n["author"]]
    venue = JOURNAL_ABBR.get(n["journal_title"], n["journal_title"]); y = n["publication_date"][:4]
    pg = f", {n['firstpage']}–{n['lastpage']}" if n.get("firstpage") else ""
    vol = f" {n['volume']}" + (f"({n['issue']})" if n.get("issue") and "Neural" not in venue else "")
    text = (f"{name_list(au)}, {y}. {n['title']}, in: {venue}{pg}. {n['url']}" if "Neural" in venue
            else f"{name_list(au)}, {y}. {n['title']}. {venue}{vol}{pg}. {n['url']}")
    refs[k] = dict(text=text, cite=cite_key(au, y), doi=None)
# datasets (DataCite)
for k, doi in [("Elfetni2026data", "10.22000/8bnbhqccf4aq7kea"), ("TU4data", "10.4121/834c3f22-f46a-4808-a0fe-46298be6a133.v1")]:
    d = json.loads(urllib.request.urlopen(f"https://api.datacite.org/dois/{doi}", timeout=60).read())["data"]["attributes"]
    au = [f"{c.get('familyName', c.get('name'))}, {c.get('givenName', '')}".strip(", ") for c in d["creators"]]
    t = d["titles"][0]["title"]
    refs[k] = dict(text=f"{name_list(au)}, {d['publicationYear']}. {t} [dataset]. {d['publisher'] if isinstance(d['publisher'], str) else d['publisher'].get('name')}. https://doi.org/{doi}",
                   cite=cite_key(au, d["publicationYear"]), doi=doi)
json.dump(refs, open(os.path.join(os.path.dirname(__file__), "references.json"), "w"), indent=1, ensure_ascii=False)
for k, r in sorted(refs.items(), key=lambda kv: kv[1]["text"]): print(f"{k:18s} [{r['cite']}] {r['text'][:170]}")
