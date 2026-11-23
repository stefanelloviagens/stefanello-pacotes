"""Salva em og/<pacote>.jpg uma foto 1200x630 pra cada pacote do api/og-map.json (servida como arquivo estático)."""
import json, os, subprocess
m = json.load(open("api/og-map.json"))
os.makedirs("og", exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
for chave, cands in m.items():
    if isinstance(cands, dict): cands = [cands.get("resized"), cands.get("src")]
    dest = f"og/{chave}.jpg"
    if os.path.exists(dest) and os.path.getsize(dest) > 5000: continue
    for u in [c for c in cands if c and ("weserv" in c or "pexels" in c)]:
        r = subprocess.run(["curl", "-sSL", "-m", "40", "-A", UA, "-o", dest, "-w", "%{http_code} %{content_type}", u], capture_output=True, text=True)
        ok = r.stdout.startswith("200") and "image" in r.stdout and os.path.exists(dest) and os.path.getsize(dest) > 5000
        print(chave, r.stdout, "ok" if ok else "falhou")
        if ok: break
        if os.path.exists(dest): os.remove(dest)
