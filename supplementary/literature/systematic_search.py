"""Reproducible multi-database search (PubMed, OpenAlex, Crossref) of ML studies on hydrothermal conversion.

Search window: publications 2015-01-01 .. run date. Run date and raw records are stored with the outputs.
Eligibility (applied to title + abstract, rule-based and therefore reproducible):
  E1 contains a machine-learning term (ML_RE) and a hydrothermal-conversion term (HT_RE);
  E2 primary research (not a review/editorial/erratum: title/type);
  E3 predicts a product yield or product property (TARGET_RE);
  E4 published 2015 to the run year + 1 (journal issue years can run one year ahead of online publication). Records lacking an abstract are screened on the title only (flagged).
Extraction (abstract level): validation scheme, uncertainty quantification, physical constraints, external/locked test.
Outputs: search_records_raw.json, prisma_counts.json, included_studies.csv
"""
from __future__ import annotations

import datetime as dt, json, re, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
import pandas as pd

H = {"User-Agent": "systematic-search-script/1.0"}
ML_TERMS = ['"machine learning"', '"deep learning"', '"neural network"', '"random forest"', '"gradient boosting"', 'xgboost', '"support vector"']
HT_TERMS = ['"hydrothermal liquefaction"', '"hydrothermal carbonization"', '"hydrothermal carbonisation"', 'hydrochar', 'biocrude', '"bio-crude"']
ML_RE = r"machine learning|deep learning|neural network|random forest|gradient boost|xgboost|support vector|lightgbm|catboost|gaussian process"
HT_RE = r"hydrothermal liquefaction|hydrothermal carboni[sz]ation|hydrochar|biocrude|bio-crude|hydrothermal treatment|hydrothermal conversion"
TARGET_RE = r"yield|hhv|heating value|content|propert|composition|carbon|nitrogen|energy recovery|predict"
REVIEW_RE = r"\breview\b|perspective|editorial|erratum|corrigendum|retraction|state[- ]of[- ]the[- ]art"
EXTRACT = {
    "grouped_or_external": r"publication[- ](aware|level|wise|based|grouped)|group(ed)?[- ]?(k[- ]?fold|cross|split|wise)|leave[- ]one[- ](study|paper|publication|source|feedstock|biomass|group)|study[- ]level|unseen (feedstock|biomass|stud)|external (validation|test|data)|independent (test|validation|data)",
    "random_split": r"random(ly)? (split|divided|partition)|train(ing)?[- ]test split|\b[789]0\s?[:/]\s?[123]0\b|k[- ]?fold|cross[- ]validation",
    "uncertainty": r"conformal|prediction interval|uncertaint|bootstrap|monte carlo|bayesian",
    "physics": r"mass balance|conservation|physics[- ]informed|physic(s|ally)[- ](consistent|constrained|guided)|closure",
    "literature_data": r"literature|published (data|studies)|collected from|compiled|database",
}


def get(url, as_json=True):
    for i in range(6):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=90).read()
            return json.loads(r) if as_json else r
        except Exception:
            time.sleep(2 ** i)
    return None


def norm_doi(d):
    if not d:
        return None
    d = d.lower().strip()
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", d)


def pubmed(today):
    term = f"({' OR '.join(t + '[tiab]' for t in ML_TERMS)}) AND ({' OR '.join(t + '[tiab]' for t in HT_TERMS)})"
    q = urllib.parse.urlencode(dict(db="pubmed", term=term, retmax=2000, retmode="json", mindate="2015/01/01", maxdate=today.replace("-", "/"), datetype="pdat"))
    ids = get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + q)["esearchresult"]["idlist"]
    recs = []
    for i in range(0, len(ids), 200):
        root = ET.fromstring(get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + urllib.parse.urlencode(dict(db="pubmed", id=",".join(ids[i:i + 200]), retmode="xml")), as_json=False))
        for a in root.findall(".//PubmedArticle"):
            t = "".join(a.find(".//ArticleTitle").itertext()) if a.find(".//ArticleTitle") is not None else ""
            ab = " ".join("".join(x.itertext()) for x in a.findall(".//Abstract/AbstractText"))
            doi = next((x.text for x in a.findall(".//ArticleId") if x.get("IdType") == "doi"), None)
            pt = [x.text for x in a.findall(".//PublicationType")]
            recs.append(dict(source="PubMed", doi=norm_doi(doi), title=t, abstract=ab, year=a.findtext(".//JournalIssue/PubDate/Year"),
                             venue=a.findtext(".//Journal/ISOAbbreviation"), type="review" if "Review" in pt else "article"))
        time.sleep(0.4)
    return term, recs


def openalex(today):
    search = f"({' OR '.join(ML_TERMS)}) AND ({' OR '.join(HT_TERMS)})"
    recs, cursor = [], "*"
    while cursor:
        q = urllib.parse.urlencode({"filter": f"title_and_abstract.search:{search},from_publication_date:2015-01-01,to_publication_date:{today}",
                                    "per_page": 200, "cursor": cursor, "select": "doi,title,abstract_inverted_index,publication_year,type,primary_location"})
        r = get("https://api.openalex.org/works?" + q)
        if not r:
            break
        for w in r["results"]:
            inv = w.get("abstract_inverted_index") or {}
            pos = {p: wd for wd, ps in inv.items() for p in ps}
            src = ((w.get("primary_location") or {}).get("source") or {})
            recs.append(dict(source="OpenAlex", doi=norm_doi(w.get("doi")), title=w.get("title") or "", abstract=" ".join(pos[k] for k in sorted(pos)),
                             year=w.get("publication_year"), venue=src.get("display_name"), type=w.get("type")))
        cursor = r["meta"].get("next_cursor") if r["results"] else None
        time.sleep(0.3)
    return search, recs


def crossref(today):
    queries = [f"{m.strip(chr(34))} {h.strip(chr(34))}" for m in ['machine learning', 'neural network', 'random forest', 'gradient boosting']
               for h in ['hydrothermal liquefaction', 'hydrothermal carbonization', 'hydrochar', 'biocrude']]
    recs = []
    for qq in queries:
        p = {"query.bibliographic": qq, "rows": 200, "filter": f"from-pub-date:2015-01-01,until-pub-date:{today},type:journal-article",
             "select": "DOI,title,abstract,issued,container-title,type"}
        r = get("https://api.crossref.org/works?" + urllib.parse.urlencode(p))
        for it in (r or {}).get("message", {}).get("items", []):
            recs.append(dict(source="Crossref", doi=norm_doi(it.get("DOI")), title=(it.get("title") or [""])[0], abstract=re.sub("<[^>]+>", " ", it.get("abstract") or ""),
                             year=(it.get("issued", {}).get("date-parts", [[None]])[0][0]), venue=(it.get("container-title") or [""])[0], type=it.get("type")))
        time.sleep(0.5)
    return queries, recs


def main():
    import sys
    if "--from-raw" in sys.argv:  # re-apply the screening to the stored records of the last run (no new queries)
        R = json.load(open("search_records_raw.json")); today, raw = R["run_date"], R["records"]
    else:
        today = dt.date.today().isoformat()
        s_pm, r_pm = pubmed(today); s_oa, r_oa = openalex(today); s_cr, r_cr = crossref(today)
        raw = r_pm + r_oa + r_cr
        json.dump(dict(run_date=today, pubmed_query=s_pm, openalex_query=s_oa, crossref_queries=s_cr, records=raw), open("search_records_raw.json", "w"))
    df = pd.DataFrame(raw)
    df["title"] = df["title"].fillna("").str.replace(r"<[^>]+>", " ", regex=True)
    df["key"] = df["doi"].fillna(df["title"].str.lower().str.replace(r"[^a-z0-9]", "", regex=True).str[:80])
    n_identified = {s: int((df.source == s).sum()) for s in ["PubMed", "OpenAlex", "Crossref"]}
    # merge duplicates, keep the record with the longest abstract
    df["alen"] = df["abstract"].fillna("").str.len()
    dd = df.sort_values("alen", ascending=False).groupby("key").agg(
        doi=("doi", "first"), title=("title", "first"), abstract=("abstract", "first"), year=("year", "first"), venue=("venue", "first"), type=("type", "first"),
        sources=("source", lambda s: ";".join(sorted(set(s))))).reset_index()
    text = (dd.title.fillna("") + " " + dd.abstract.fillna("")).str.lower()
    e1 = text.str.contains(ML_RE) & text.str.contains(HT_RE)
    e2 = ~(dd.title.str.lower().str.contains(REVIEW_RE) | dd.type.fillna("").str.contains("review"))
    e3 = text.str.contains(TARGET_RE)
    try:
        yrs = pd.to_numeric(dd.year, errors="coerce"); e4 = yrs.between(2015, int(today[:4]) + 1)  # issue year can precede online year by one
    except Exception:
        e4 = True
    inc = dd[e1 & e2 & e3 & e4].copy()
    inc["abstract_available"] = inc.abstract.fillna("").str.len() > 50
    t2 = (inc.title.fillna("") + " " + inc.abstract.fillna("")).str.lower()
    for k, p in EXTRACT.items():
        inc[k] = t2.str.contains(p)
    inc.drop(columns=["key"]).to_csv("included_studies.csv", index=False)
    pr = dict(run_date=today, identified=n_identified, identified_total=int(len(df)), after_deduplication=int(len(dd)),
              excluded_no_ml_or_no_hydrothermal_term=int((~e1).sum()), excluded_review_or_non_primary=int((e1 & ~e2).sum()),
              excluded_no_prediction_target=int((e1 & e2 & ~e3).sum()), excluded_outside_window=int((e1 & e2 & e3 & ~e4).sum()),
              included=int(len(inc)), included_with_abstract=int(inc.abstract_available.sum()),
              included_in_bioresource_technology=int(inc.venue.fillna("").str.contains(r"Bioresource Technology|Bioresour Technol", case=False, regex=True).sum()),
              databases_unavailable=[s for s, n in n_identified.items() if n == 0],
              **{f"included_mentioning_{k}": int(inc[k].sum()) for k in EXTRACT})
    json.dump(pr, open("prisma_counts.json", "w"), indent=1)
    print(json.dumps(pr, indent=1))


if __name__ == "__main__":
    main()
