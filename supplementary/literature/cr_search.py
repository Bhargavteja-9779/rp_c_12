"""Crossref bibliographic search used to build/verify the literature matrix."""
import json, sys, time, urllib.parse, urllib.request
def q(query, rows=8, filt=None):
    p = {"query.bibliographic": query, "rows": rows, "select": "DOI,title,author,container-title,issued,type,is-referenced-by-count"}
    if filt: p["filter"] = filt
    u = "https://api.crossref.org/works?" + urllib.parse.urlencode(p)
    for i in range(5):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "lit-matrix-script/0.1"}), timeout=60).read())["message"]["items"]
        except Exception: time.sleep(2 ** i)
    return []
def fmt(it):
    a = it.get("author", [])
    au = (a[0].get("family", "") + (" et al." if len(a) > 1 else "")) if a else ""
    y = it.get("issued", {}).get("date-parts", [[None]])[0][0]
    return f"{it['DOI']} | {y} | {au} | {(it.get('title') or [''])[0][:130]} | {(it.get('container-title') or [''])[0][:45]} | cites={it.get('is-referenced-by-count')}"
if __name__ == "__main__":
    out = {}
    for query in sys.argv[1:]:
        items = q(query); out[query] = items
        print("==", query)
        for it in items: print("  ", fmt(it))
    json.dump(out, open(f"search_{int(time.time())}.json", "w"))
