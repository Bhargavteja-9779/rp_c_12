"""Fetch abstracts of Bioresource Technology papers (2023-2026) on machine learning for hydrothermal / thermochemical conversion (PubMed)."""
import json, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
H = {"User-Agent": "bt-benchmark/1.0"}
def get(u):
    for i in range(6):
        try: return urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60).read()
        except Exception: time.sleep(2 ** i)
Q = {"htl_htc_ml": '"Bioresour Technol"[ta] AND ("machine learning"[tiab] OR "deep learning"[tiab] OR "neural network"[tiab] OR "random forest"[tiab] OR xgboost[tiab] OR "gradient boosting"[tiab]) AND (hydrothermal[tiab] OR hydrochar[tiab] OR biocrude[tiab] OR "bio-crude"[tiab])',
     "meta_analysis": '"Bioresour Technol"[ta] AND ("meta-analysis"[tiab] OR "meta analysis"[tiab])',
     "thermo_ml": '"Bioresour Technol"[ta] AND ("machine learning"[tiab]) AND (pyrolysis[tiab] OR gasification[tiab] OR biochar[tiab]) AND 2025:2026[dp]'}
out = {}
for k, q in Q.items():
    ids = json.loads(get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urllib.parse.urlencode(dict(db="pubmed", term=q + " AND 2022:2027[dp]", retmax=300, retmode="json"))))["esearchresult"]["idlist"]
    recs = []
    for i in range(0, len(ids), 100):
        time.sleep(0.5)
        root = ET.fromstring(get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + urllib.parse.urlencode(dict(db="pubmed", id=",".join(ids[i:i+100]), retmode="xml"))))
        for a in root.findall(".//PubmedArticle"):
            recs.append(dict(pmid=a.findtext(".//PMID"), title="".join(a.find(".//ArticleTitle").itertext()), year=a.findtext(".//JournalIssue/PubDate/Year"),
                             doi=next((x.text for x in a.findall(".//ArticleId") if x.get("IdType") == "doi"), None),
                             abstract=" ".join("".join(x.itertext()) for x in a.findall(".//Abstract/AbstractText")),
                             keywords=[x.text for x in a.findall(".//Keyword")],
                             dates={d.get("PubStatus"): f"{d.findtext('Year')}-{d.findtext('Month')}-{d.findtext('Day')}" for d in a.findall(".//PubMedPubDate")}))
    out[k] = recs; print(k, len(ids)); time.sleep(1)
json.dump(out, open("bt_abstracts.json", "w"), indent=1)
