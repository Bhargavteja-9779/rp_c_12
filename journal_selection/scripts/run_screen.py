"""Reproducible journal acceptance-time screen.

Measures received->accepted days from (a) PubMed History dates and (b) Crossref
'assertion' dates (Springer Nature).  Writes journal_selection/data/*.json.
Run:  python journal_selection/scripts/run_screen.py
"""
import json, os, sys, datetime as dt
sys.path.insert(0, os.path.dirname(__file__))
import pm_times, ml_subset
OUT = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT, exist_ok=True)
ALL = ["Bioresour Technol", "Anal Chim Acta", "Talanta", "Anal Bioanal Chem", "J Chem Inf Model",
       "Bioinformatics", "Brief Bioinform", "J Am Med Inform Assoc", "Nucleic Acids Res", "Gigascience",
       "Database (Oxford)", "NAR Genom Bioinform", "Bioinform Adv", "Comput Biol Med", "Neural Netw",
       "Artif Intell Med", "J Biomed Inform", "Comput Methods Programs Biomed", "Med Image Anal",
       "Water Res", "Environ Res", "J Hazard Mater", "Chemosphere", "Environ Pollut", "Environ Int",
       "Sci Total Environ", "Biosens Bioelectron", "Ultrason Sonochem", "Food Chem", "Food Res Int",
       "Spectrochim Acta A Mol Biomol Spectrosc", "J Pharm Biomed Anal", "Comput Struct Biotechnol J",
       "Int J Med Inform", "Methods", "Sci Rep", "npj Digit Med", "Patterns (N Y)", "J Cheminform",
       "Physiol Meas", "Anal Chem", "J Environ Manage", "Ecotoxicol Environ Saf", "Eur Heart J Digit Health",
       "Comput Med Imaging Graph", "Comput Biol Chem"]
ML = ["Bioresour Technol", "Anal Chim Acta", "Talanta", "Anal Bioanal Chem", "J Chem Inf Model",
      "Water Res", "Environ Res", "J Hazard Mater", "Biosens Bioelectron", "Ultrason Sonochem",
      "Environ Pollut", "Chemosphere", "J Pharm Biomed Anal", "Food Res Int", "Spectrochim Acta A Mol Biomol Spectrosc"]
if __name__ == "__main__":
    stamp = dt.date.today().isoformat()
    res = []
    for j in ALL:
        r = pm_times.measure(j); r["window"] = "pub 2025-07-01..2026-10-31, all research articles"; res.append(r); print(r, flush=True)
    json.dump(dict(retrieved=stamp, source="NCBI E-utilities PubMed History (received, accepted)", results=res),
              open(os.path.join(OUT, "pubmed_all_articles.json"), "w"), indent=1)
    import io, contextlib
    rows = []
    for j in ML:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            ml_subset.m(j, mindate="2025/07/01")
        for line in buf.getvalue().splitlines():
            try: rows.append(json.loads(line))
            except Exception: rows.append({"journal": j, "raw": line})
        print(rows[-1], flush=True)
    json.dump(dict(retrieved=stamp, query=ml_subset.ML, window="pub 2025-07-01..2026-10-31", results=rows),
              open(os.path.join(OUT, "pubmed_ml_subset.json"), "w"), indent=1)
