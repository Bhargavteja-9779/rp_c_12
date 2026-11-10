"""Measure submission->acceptance (received->accepted) days from PubMed history dates."""
import sys, time, json, statistics, urllib.request, urllib.parse, xml.etree.ElementTree as ET, datetime as dt
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
def get(url):
    for i in range(4):
        try: return urllib.request.urlopen(url,timeout=60).read()
        except Exception as e: time.sleep(2**i)
    raise RuntimeError(url)
def measure(journal, mindate="2025/07/01", maxdate="2026/10/31", n=400):
    term=f'"{journal}"[jour] AND journal article[pt] NOT review[pt] NOT editorial[pt]'
    q=urllib.parse.urlencode(dict(db="pubmed",term=term,retmax=n,mindate=mindate,maxdate=maxdate,datetype="pdat",retmode="json",sort="pub_date"))
    ids=json.loads(get(E+"esearch.fcgi?"+q))["esearchresult"]["idlist"]
    days=[];rev=[]
    for i in range(0,len(ids),200):
        x=get(E+"efetch.fcgi?"+urllib.parse.urlencode(dict(db="pubmed",id=",".join(ids[i:i+200]),retmode="xml")))
        root=ET.fromstring(x)
        for art in root.findall(".//PubmedArticle"):
            d={}
            for p in art.findall(".//History/PubMedPubDate"):
                try: d[p.get("PubStatus")]=dt.date(int(p.findtext("Year")),int(p.findtext("Month")),int(p.findtext("Day")))
                except: pass
            if "received" in d and "accepted" in d:
                v=(d["accepted"]-d["received"]).days
                if 0<=v<1500: days.append(v)
        time.sleep(0.4)
    if not days: return dict(journal=journal,n_ids=len(ids),n=0)
    days.sort(); q=statistics.quantiles(days,n=4)
    return dict(journal=journal,n_ids=len(ids),n=len(days),median=statistics.median(days),q1=q[0],q3=q[2],
                pct_le_60=round(100*sum(v<=60 for v in days)/len(days),1),pct_le_72=round(100*sum(v<=72 for v in days)/len(days),1))
if __name__=="__main__":
    for j in sys.argv[1:]:
        print(json.dumps(measure(j)),flush=True)
