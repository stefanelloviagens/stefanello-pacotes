// Prévia do link (WhatsApp/Facebook): entrega a foto do hotel pelo próprio domínio, reduzida pra 1200x630.
const map = require("./og-map.json");

module.exports = async (req, res) => {
  const item = map[String(req.query.s || "")];
  if (!item) { res.statusCode = 404; return res.end("not found"); }
  for (const u of [item.resized, item.src]) {
    try {
      const r = await fetch(u, { headers: { "User-Agent": "Mozilla/5.0 StefanelloOG" } });
      if (!r.ok) continue;
      const buf = Buffer.from(await r.arrayBuffer());
      res.setHeader("Content-Type", "image/jpeg");
      res.setHeader("Content-Length", buf.length);
      res.setHeader("Cache-Control", "public, max-age=86400, s-maxage=2592000, stale-while-revalidate=86400");
      return res.end(buf);
    } catch (e) { /* tenta a próxima */ }
  }
  res.statusCode = 502; res.end("erro");
};
