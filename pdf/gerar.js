// Gera PDF de cada página listada em pdf/pedido.txt (uma URL por linha, sem query).
const { chromium } = require("playwright");
const fs = require("fs");
(async () => {
  const urls = fs.readFileSync("pdf/pedido.txt", "utf8").split("\n").map(s => s.trim()).filter(s => s.startsWith("http"));
  const b = await chromium.launch();
  for (const url of urls) {
    const p = await b.newPage({ viewport: { width: 1200, height: 900 } });
    await p.goto(url + "?pdf=" + Date.now(), { waitUntil: "networkidle", timeout: 90000 });
    await p.evaluate(async () => {
      document.querySelectorAll("img").forEach(i => (i.loading = "eager"));
      for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
      await Promise.all([...document.images].map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; })));
    });
    await p.waitForTimeout(1500);
    const slug = url.replace(/\/+$/, "").split("/").pop();
    await p.pdf({ path: `pdf/${slug}.pdf`, format: "A4", printBackground: true, margin: { top: "10mm", bottom: "10mm", left: "8mm", right: "8mm" } });
    console.log("ok", slug);
  }
  await b.close();
})();
