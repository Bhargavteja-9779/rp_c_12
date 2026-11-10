"""Fetch abstracts for DOIs from Crossref, falling back to OpenAlex (inverted index) and PubMed."""
import json, sys, time, re, urllib.parse, urllib.request
H = {"User-Agent": "lit-matrix-script/0.1"}
def get(u):
    for i in range(4):
        try: return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60).read())
        except Exception as e:
            time.sleep(2 ** i)
    return None
def abstract(doi):
    m = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
    meta = m["message"] if m else {}
    a = meta.get("abstract")
    src = "crossref"
    if not a:
        o = get("https://api.openalex.org/works/doi:" + doi)
        if o and o.get("abstract_inverted_index"):
            inv = o["abstract_inverted_index"]; pos = {}
            for w, ps in inv.items():
                for p in ps: pos[p] = w
            a = " ".join(pos[k] for k in sorted(pos)); src = "openalex"
    a = re.sub("<[^>]+>", " ", a or "")
    a = re.sub(r"\s+", " ", a).strip()
    au = ", ".join(f"{x.get('family','')} {x.get('given','')[:1]}" for x in meta.get("author", []))
    return dict(doi=doi, title=(meta.get("title") or [""])[0], authors=au, venue=(meta.get("container-title") or [""])[0],
                year=(meta.get("issued", {}).get("date-parts", [[None]])[0][0]), volume=meta.get("volume"), page=meta.get("page") or meta.get("article-number"),
                abstract=a, abstract_source=src if a else None)
if __name__ == "__main__":
    out = []
    for d in sys.argv[1:]:
        r = abstract(d); out.append(r)
        print(f"### {r['doi']} | {r['year']} | {r['venue']} | {r['title']}\n{r['authors']}\n{r['abstract'][:1800]}\n")
    try: prev = json.load(open("abstracts.json"))
    except Exception: prev = {}
    prev.update({r["doi"]: r for r in out}); json.dump(prev, open("abstracts.json", "w"), indent=1)
