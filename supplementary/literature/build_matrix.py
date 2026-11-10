"""Literature matrix of ML studies on hydrothermal conversion (abstract-level extraction).

Fields are extracted from PubMed titles/abstracts; 'n.s.' = not stated in abstract.
Full texts were not accessible (publisher blocks), which is a stated limitation.
"""
import json, re, csv, urllib.request, urllib.parse, xml.etree.ElementTree as ET, time
c = json.load(open("pubmed_ml_hydrothermal_corpus.json"))["records"]
ids = [r["pmid"] for r in c if not r["review"]]
root = ET.fromstring(urllib.request.urlopen("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + urllib.parse.urlencode(dict(db="pubmed", retmode="xml", id=",".join(ids))), timeout=120).read())
M = {"RF": r"random forest|\bRF\b", "XGB": r"xgboost|extreme gradient", "GBR/GBM": r"gradient boost|\bGBR\b|\bGBDT\b|lightgbm|catboost",
     "ANN/MLP": r"neural network|\bANN\b|\bMLP\b|multilayer perceptron", "SVR": r"support vector|\bSVR\b|\bSVM\b", "GPR": r"gaussian process", "DT": r"decision tree",
     "kNN": r"nearest neighbo", "linear/ridge": r"linear regression|ridge|lasso", "GNN": r"graph neural", "TabPFN/foundation": r"tabpfn|foundation model"}
T = {"bio-oil/biocrude yield": r"bio-?oil yield|bio-?crude yield|biocrude yield|yield of bio-?oil|bio-oil production", "hydrochar yield/properties": r"hydrochar", "HHV/energy": r"\bhhv\b|heating value|energy recovery|energy yield",
     "N content/heterocycles": r"nitrogen", "carbon recovery": r"carbon recovery|carbon yield|carbon retention|carbon balance", "adsorption": r"adsorption"}
rows = []
for a in root.findall(".//PubmedArticle"):
    t = "".join(a.find(".//ArticleTitle").itertext()); ab = " ".join("".join(x.itertext()) for x in a.findall(".//Abstract/AbstractText")); s = (t + " " + ab)
    sl = s.lower()
    pm = a.findtext(".//PMID"); rec = next(r for r in c if r["pmid"] == pm)
    au = a.find(".//AuthorList/Author"); first = au.findtext("LastName") if au is not None else ""
    n = re.findall(r"(\d{2,5})\s*(?:data ?points|data sets|datasets|samples|experiments|observations|records|data)", sl)
    r2 = re.findall(r"r\s?2\s?(?:value[s]?)?\s?(?:of|=|>|≥|:)?\s?(0\.\d{2,3})", sl)
    rows.append(dict(pmid=pm, doi=rec["doi"], year=rec["year"], venue=rec["journal"], first_author=first, title=t,
        problem="; ".join(k for k, p in T.items() if re.search(p, sl)) or "n.s.",
        dataset="literature-compiled" if re.search(r"literature|published|collected from|compiled", sl) else ("own experiments" if re.search(r"experiment(s|al) (were|was) (conducted|performed)", sl) else "n.s."),
        data_size=";".join(sorted(set(n), key=int)) or "n.s.",
        methods="; ".join(k for k, p in M.items() if re.search(p, sl)) or "n.s.",
        validation=("grouped/external" if rec["group_split"] else "") + ("random/k-fold" if rec["random_split_or_cv"] else "") or "n.s.",
        reported_R2=";".join(r2) or "n.s.",
        uncertainty="yes" if rec["uncertainty"] else "n.s.", physics_constraints="yes" if rec["physics_constraint"] else "n.s.",
        interpretability="SHAP/PDP/importance" if re.search(r"shap|partial dependence|feature importance|interpretab", sl) else "n.s.",
        experimental_validation="yes" if rec["experimental_validation"] else "n.s.",
        code_availability="n.s. (not checked in abstract)"))
    rows[-1]["research_gap_relative_to_this_work"] = ("does not evaluate transfer to unseen studies (abstract)" if not rec["group_split"] else "grouped/external validation reported")
rows.sort(key=lambda r: (r["year"] or "", r["pmid"]))
with open("literature_matrix_corpus.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows))
import collections
print("R2 reported:", sum(r["reported_R2"] != "n.s." for r in rows), "max R2 per paper median:",
      sorted(max(map(float, r["reported_R2"].split(";"))) for r in rows if r["reported_R2"] != "n.s.")[len([r for r in rows if r["reported_R2"]!="n.s."])//2])
print(collections.Counter(m for r in rows for m in r["methods"].split("; ")))
print(collections.Counter(r["dataset"] for r in rows)); print(collections.Counter(r["validation"] for r in rows))
