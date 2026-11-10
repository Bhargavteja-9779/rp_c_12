import pm_times, json, urllib.parse, statistics, datetime as dt, xml.etree.ElementTree as ET, sys
ML='"machine learning"[tiab] OR "deep learning"[tiab] OR chemometric*[tiab] OR "neural network"[tiab]'
def m(j,extra=ML,mindate="2024/07/01"):
    E=pm_times.E
    term=f'"{j}"[jour] AND journal article[pt] NOT review[pt] AND ({extra})'
    q=urllib.parse.urlencode(dict(db="pubmed",term=term,retmax=400,mindate=mindate,maxdate="2026/10/31",datetype="pdat",retmode="json"))
    ids=json.loads(pm_times.get(E+"esearch.fcgi?"+q))["esearchresult"]["idlist"]
    days=[]
    for i in range(0,len(ids),200):
        root=ET.fromstring(pm_times.get(E+"efetch.fcgi?"+urllib.parse.urlencode(dict(db="pubmed",id=",".join(ids[i:i+200]),retmode="xml"))))
        for art in root.findall(".//PubmedArticle"):
            d={}
            for p in art.findall(".//History/PubMedPubDate"):
                try:d[p.get("PubStatus")]=dt.date(int(p.findtext("Year")),int(p.findtext("Month")),int(p.findtext("Day")))
                except:pass
            if "received" in d and "accepted" in d: days.append((d["accepted"]-d["received"]).days)
    if len(days)<5: print(j,"n=",len(days)); return
    q=statistics.quantiles(days,n=4)
    print(json.dumps(dict(journal=j,subset="ML",n=len(days),median=statistics.median(days),q1=q[0],q3=q[2],pct_le_72=round(100*sum(v<=72 for v in days)/len(days),1))),flush=True)
if __name__ == "__main__":
    for j in sys.argv[1:]: m(j)
