"""Systematic PubMed corpus of ML studies on hydrothermal conversion (HTL/HTC) and abstract-level screening.

Screening is keyword-based on titles/abstracts ONLY (full texts not inspected); results are
therefore a lower bound on the use of each practice and are reported as such.
"""
import json, re, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
E = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
TERM = ('("machine learning"[tiab] OR "deep learning"[tiab] OR "neural network"[tiab] OR "random forest"[tiab] '
        'OR "gradient boosting"[tiab] OR XGBoost[tiab]) AND ("hydrothermal liquefaction"[tiab] OR '
        '"hydrothermal carbonization"[tiab] OR "hydrothermal carbonisation"[tiab] OR hydrochar[tiab] OR biocrude[tiab] OR bio-crude[tiab])')
def get(u):
    for i in range(5):
        try: return urllib.request.urlopen(u, timeout=60).read()
        except Exception: time.sleep(2 ** i)
PAT = {
 "group_split": r"group(ed)?[- ]?(k[- ]?fold|cross|split|wise)|leave[- ]one[- ](study|paper|publication|source|feedstock|biomass|group)|study[- ]level|source[- ]level|out[- ]of[- ](study|sample feedstock)|unseen (feedstock|biomass|stud)|external (validation|test|data)",
 "random_split_or_cv": r"random(ly)? (split|divided|partition)|\b\d{2}\s?[:/]\s?\d{2}\b|train(ing)?[- ]test split|k[- ]?fold|cross[- ]validation",
 "uncertainty": r"conformal|prediction interval|uncertaint|bootstrap|monte carlo|bayesian",
 "physics_constraint": r"mass balance|mass[- ]conservation|element(al)? balance|carbon balance|physics[- ]informed|physic(s|ally)[- ](consistent|constrained|guided)|closure",
 "experimental_validation": r"experimental(ly)? (validat|verif)|verified experimentally|validation experiment",
}
if __name__ == "__main__":
    q = urllib.parse.urlencode(dict(db="pubmed", term=TERM, retmax=500, retmode="json", mindate="2015/01/01", maxdate="2026/11/10", datetype="pdat"))
    ids = json.loads(get(E + "esearch.fcgi?" + q))["esearchresult"]["idlist"]
    recs = []
    for i in range(0, len(ids), 200):
        root = ET.fromstring(get(E + "efetch.fcgi?" + urllib.parse.urlencode(dict(db="pubmed", id=",".join(ids[i:i+200]), retmode="xml"))))
        for a in root.findall(".//PubmedArticle"):
            t = "".join(a.find(".//ArticleTitle").itertext()) if a.find(".//ArticleTitle") is not None else ""
            ab = " ".join("".join(x.itertext()) for x in a.findall(".//Abstract/AbstractText"))
            doi = next((x.text for x in a.findall(".//ArticleId") if x.get("IdType") == "doi"), None)
            j = a.findtext(".//Journal/ISOAbbreviation"); y = a.findtext(".//JournalIssue/PubDate/Year") or a.findtext(".//ArticleDate/Year")
            pt = [x.text for x in a.findall(".//PublicationType")]
            text = (t + " " + ab).lower()
            recs.append(dict(pmid=a.findtext(".//PMID"), doi=doi, year=y, journal=j, title=t, review=("Review" in pt),
                             **{k: bool(re.search(p, text)) for k, p in PAT.items()}))
        time.sleep(0.4)
    json.dump(dict(query=TERM, retrieved=time.strftime("%Y-%m-%d"), records=recs), open("pubmed_ml_hydrothermal_corpus.json", "w"), indent=1)
    import collections
    prim = [r for r in recs if not r["review"]]
    print("total", len(recs), "primary", len(prim))
    for k in PAT: print(k, sum(r[k] for r in prim))
    print(collections.Counter(r["journal"] for r in prim).most_common(12))
    for r in prim:
        if r["group_split"] or r["physics_constraint"]: print("*", r["year"], r["journal"], r["doi"], r["title"][:110], "| G" if r["group_split"] else "", "| P" if r["physics_constraint"] else "")
