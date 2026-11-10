import sys,json,time,statistics,urllib.request,urllib.parse,datetime as dt
def get(u):
    for i in range(5):
        try: return json.loads(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"research-script/0.1"}),timeout=60).read())
        except Exception: time.sleep(2**i)
def P(x):
    x=x.strip()
    for f in ('%d %B %Y','%Y-%m-%d','%B %d, %Y'):
        try: return dt.datetime.strptime(x,f).date()
        except ValueError: pass
    raise ValueError(x)
def measure(issn,name):
    days=[];cursor="*";tot=0
    while len(days)<400 and cursor:
        q=urllib.parse.urlencode({"filter":"from-pub-date:2025-07-01,until-pub-date:2026-10-31,type:journal-article","rows":200,"cursor":cursor,"select":"DOI,assertion"})
        r=get(f"https://api.crossref.org/journals/{issn}/works?{q}")
        if not r: break
        items=r["message"]["items"]; cursor=r["message"].get("next-cursor") if items else None; tot+=len(items)
        for it in items:
            a={x.get("name"):x.get("value") for x in it.get("assertion",[])}
            try:
                v=(P(a["accepted"])-P(a["received"])).days
                if 0<=v<1500: days.append(v)
            except Exception: pass
        if tot>3000: break
    if not days: return dict(journal=name,n=0,scanned=tot)
    q=statistics.quantiles(days,n=4)
    return dict(journal=name,scanned=tot,n=len(days),median=statistics.median(days),q1=q[0],q3=q[2],pct_le_72=round(100*sum(v<=72 for v in days)/len(days),1))
for arg in sys.argv[1:]:
    issn,name=arg.split("=",1); print(json.dumps(measure(issn,name)),flush=True)
