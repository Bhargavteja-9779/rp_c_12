"""Received->accepted days (PubMed history) for candidate fallback journals, research articles 2025-07-01..2026-10-31."""
import json, time, statistics, urllib.parse, urllib.request, xml.etree.ElementTree as ET, datetime as dt
H = {"User-Agent": "journal-timeline/1.0"}
def get(u, js=True):
    for i in range(6):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60).read(); return json.loads(r) if js else r
        except Exception: time.sleep(2 ** i)
out = {}
for j in ["Waste Manag", "Biotechnol Biofuels Bioprod", "Green Chem", "Bioresour Technol"]:
    q = f'"{j}"[ta] AND journal article[pt] NOT review[pt] AND 2025/07/01:2026/10/31[dp]'
    ids = get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urllib.parse.urlencode(dict(db="pubmed", term=q, retmax=400, retmode="json")))["esearchresult"]["idlist"]
    days = []
    for i in range(0, len(ids), 200):
        root = ET.fromstring(get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + urllib.parse.urlencode(dict(db="pubmed", id=",".join(ids[i:i+200]), retmode="xml")), js=False))
        for a in root.findall(".//PubmedArticle"):
            d = {x.get("PubStatus"): x for x in a.findall(".//PubMedPubDate")}
            if "received" in d and "accepted" in d:
                f = lambda e: dt.date(int(e.findtext("Year")), int(e.findtext("Month")), int(e.findtext("Day")))
                try: days.append((f(d["accepted"]) - f(d["received"])).days)
                except Exception: pass
        time.sleep(0.5)
    days = [x for x in days if x >= 0]
    out[j] = dict(n=len(days), median=statistics.median(days) if days else None, share_le72=sum(x <= 72 for x in days) / len(days) if days else None)
    print(j, out[j]); time.sleep(1)
json.dump(out, open("../data/fallback_timelines_v4.json", "w"), indent=1)
