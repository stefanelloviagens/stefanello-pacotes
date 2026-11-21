// Prévia do link (WhatsApp/Facebook): entrega a foto do hotel pelo próprio domínio, reduzida pra 1200x630.
const map = require("./og-map.json");

module.exports = async (req, res) => {
  const item = map[String(req.query.s || "")];
  if (!item) { res.statusCode = 404; return res.end("not found"); }
  const log = [];
  for (const u of (Array.isArray(item) ? item : [item.resized, item.src])) {
    try {
      const r = await fetch(u, { signal: AbortSignal.timeout(4000), headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36", "Accept": "image/avif,image/webp,image/*,*/*;q=0.8" } });
      if (!r.ok) { log.push(u.slice(0, 40) + " " + r.status); continue; }
      const buf = Buffer.from(await r.arrayBuffer());
      res.setHeader("Content-Type", "image/jpeg");
      res.setHeader("Content-Length", buf.length);
      res.setHeader("Cache-Control", "public, max-age=86400, s-maxage=2592000, stale-while-revalidate=86400");
      return res.end(buf);
    } catch (e) { log.push(u.slice(0, 40) + " " + String(e && (e.cause || e.message) || e)); }
  }
  res.statusCode = 502; res.end("erro " + log.join(" | "));
};
