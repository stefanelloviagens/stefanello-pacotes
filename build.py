#!/usr/bin/env python3
"""Gera o site de pacotes da Stefanello Viagens a partir do pacotes.json.

Uso: python3 build.py   (gera index.html e <slug>.html na pasta do script)
Pacotes com data de ida já passada não entram no site.
"""
import json, html, datetime, pathlib, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent
cfg = json.loads((ROOT / "pacotes.json").read_text(encoding="utf-8"))
HOJE = datetime.date.today().isoformat()
WA = cfg["whatsapp"]
PIXEL = cfg["pixel"]
SITE = cfg["site"].rstrip("/")
GRUPO = cfg["grupo"]
INSTA = cfg["instagram"]

ativos = [p for p in cfg["pacotes"] if p.get("ida", "9999") >= HOJE and not p.get("esgotado")]
ativos.sort(key=lambda p: p["ida"])

e = lambda s: html.escape(str(s), quote=True)


def wa_link(msg):
    return f"https://wa.me/{WA}?text=" + urllib.parse.quote(msg)


def msg_pacote(p):
    return f"Oi! Vi no site o pacote {p['titulo']} ({p['idaTxt'].split(' (')[0]} a {p['voltaTxt'].split(' (')[0]}) e quero saber mais."


STAR = '<svg viewBox="0 0 100 100" aria-hidden="true"><path d="M50 0C50 27.6 72.4 50 100 50 72.4 50 50 72.4 50 100 50 72.4 27.6 50 0 50 27.6 50 50 27.6 50 0Z"/></svg>'
WA_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>'

CSS = """
:root{--ink:#111111;--paper:#FAF7F0;--card:#FFFFFF;--muted:#5d5a54;--line:#E7E1D4;--sun:#FFD400;--wa:#1FA855;--wa-d:#178a45;--sea:#0E6E7E}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--paper);color:var(--ink);line-height:1.5;font-size:16px}
img{max-width:100%;height:auto;display:block}
a{color:inherit}
.wrap{max-width:1120px;margin:0 auto;padding:0 16px}
h1,h2,h3,.display{font-family:'Archivo',Inter,sans-serif;letter-spacing:-.01em;line-height:1.1}
/* topo */
.top{position:sticky;top:0;z-index:20;background:rgba(250,247,240,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;height:64px;gap:12px}
.brand{display:flex;align-items:center;gap:8px;text-decoration:none;font-family:'Archivo',sans-serif;font-weight:800;font-size:18px}
.logo{height:40px;width:auto}.logo-ft{height:36px;width:auto;margin-bottom:4px}
.brand small{display:block;font:500 11px Inter,sans-serif;color:var(--muted);letter-spacing:.04em;text-transform:uppercase}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:48px;padding:0 20px;border-radius:999px;font-weight:700;text-decoration:none;font-size:15px;border:0;cursor:pointer;transition:transform .15s,background .15s}
.btn:active{transform:scale(.98)}
.btn svg{width:20px;height:20px;fill:currentColor}
.btn-wa{background:var(--wa);color:#fff}.btn-wa:hover{background:var(--wa-d)}
.btn-ghost{background:transparent;color:var(--ink);border:2px solid var(--ink)}
.btn-ghost:hover{background:var(--ink);color:#fff}
.btn-sm{min-height:40px;padding:0 14px;font-size:14px}
/* hero */
.hero{background:var(--ink);color:#fff;padding:40px 0 44px}
.hero .tag{display:inline-block;background:var(--sun);color:var(--ink);font-weight:800;font-size:13px;letter-spacing:.06em;padding:6px 14px;border-radius:999px;text-transform:uppercase}
.hero h1{font-size:clamp(32px,6vw,56px);font-weight:800;margin:16px 0 12px;max-width:760px}
.hero h1 em{font-style:normal;color:var(--sun)}
.hero p{color:#d9d6cf;max-width:620px;font-size:17px}
.hero .cta{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}
.hero .btn-ghost{color:#fff;border-color:#fff}.hero .btn-ghost:hover{background:#fff;color:var(--ink)}
.trust{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:26px;color:#bdb9b0;font-size:14px}
.trust b{color:#fff}
/* grade */
.sec{padding:40px 0}
.sec h2{font-size:clamp(24px,4vw,34px);font-weight:800;margin-bottom:6px}
.sec .sub{color:var(--muted);margin-bottom:24px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
.card{background:var(--card);border:1px solid var(--line);border-radius:20px;overflow:hidden;display:flex;flex-direction:column;text-decoration:none;transition:transform .2s,box-shadow .2s}
.card:hover{transform:translateY(-3px);box-shadow:0 14px 34px rgba(17,17,17,.10)}
.card .art{aspect-ratio:4/5;background:#eee;object-fit:cover;width:100%;height:auto}
.fake-art{aspect-ratio:4/5;background:radial-gradient(120% 80% at 80% 0%,#1d5f6b 0%,#111 70%);color:#fff;display:flex;flex-direction:column;justify-content:space-between;padding:22px}
.fake-art .bf{align-self:center;background:var(--sun);color:var(--ink);font-weight:800;font-size:14px;padding:6px 16px;border-radius:999px}
.fake-art .d{font-family:Archivo,sans-serif;font-weight:800;font-size:44px;color:var(--sun);text-align:center;line-height:1}
.fake-art .s{text-align:center;font-weight:700;font-size:15px;margin-top:10px}
.fake-art .pr{background:#000;border:1px solid #333;border-radius:16px;padding:14px;text-align:center}
.fake-art .pr b{font-family:Archivo,sans-serif;font-size:30px;color:var(--sun);display:block}
.fake-art .pr span{font-size:13px;color:#ddd}
.card .body{padding:16px 18px 18px;display:flex;flex-direction:column;gap:8px;flex:1}
.card h3{font-size:19px;font-weight:800}
.meta{display:flex;flex-wrap:wrap;gap:6px}
.chip{font-size:12.5px;font-weight:600;background:#F2EDE2;border-radius:999px;padding:4px 10px}
.chip.bf{background:var(--ink);color:var(--sun)}
.price{margin-top:auto;padding-top:8px;border-top:1px dashed var(--line)}
.price .p1{font-size:14px;color:var(--muted)}
.price .p1 b{font-size:22px;color:var(--ink);font-family:Archivo,sans-serif}
.price .p2{font-size:13.5px;color:var(--muted)}
.more{font-weight:700;font-size:14px;color:var(--sea)}
/* faixa grupo */
.band{background:var(--sun);border-radius:24px;padding:28px 24px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px}
.band h2{font-size:clamp(22px,3.4vw,30px)}
.band p{max-width:560px}
/* página do pacote */
.pk{padding:28px 0 40px;display:grid;grid-template-columns:1fr;gap:28px}
@media(min-width:900px){.pk{grid-template-columns:minmax(0,460px) 1fr;gap:44px;align-items:start}.pk .media{position:sticky;top:84px}}
.pk .media img,.pk .media .fake-art{border-radius:20px;box-shadow:0 18px 40px rgba(17,17,17,.14)}
.back{display:inline-block;margin-top:18px;font-size:14px;font-weight:600;color:var(--muted);text-decoration:none}
.pk h1{font-size:clamp(28px,4.6vw,44px);font-weight:800;margin:12px 0 10px}
.pk .lead{font-size:17px;color:var(--muted)}
.selo{display:inline-block;margin-left:6px;background:#E53935;color:#fff;font-weight:700;font-size:12.5px;border-radius:999px;padding:4px 10px}
.facts{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:22px 0}
.fact{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px;text-align:center}
.fact b{display:block;font-family:Archivo,sans-serif;font-size:18px}
.fact span{font-size:12.5px;color:var(--muted)}
.box{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:20px;margin-bottom:16px}
.box h2{font-size:18px;margin-bottom:12px}
.datas p{display:flex;gap:10px;padding:6px 0}
.inc{list-style:none;display:grid;gap:10px}
.inc li{display:flex;gap:12px;align-items:flex-start}
.inc li span:first-child{font-size:20px;line-height:1.3}
.pbox{background:var(--ink);color:#fff;border-radius:20px;padding:22px;margin-bottom:16px;position:relative}
.pbox .lbl{position:absolute;top:-13px;left:22px;background:var(--sun);color:var(--ink);font-weight:800;font-size:13px;padding:4px 14px;border-radius:999px;letter-spacing:.04em}
.pbox .row{display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:center;text-align:center}
.pbox .v{font-family:Archivo,sans-serif;font-weight:800;font-size:clamp(19px,5.2vw,30px);color:var(--sun);line-height:1.1;white-space:nowrap}
.pbox small{display:block;font-size:12.5px;color:#cfcac0;margin-top:4px}
.pbox .ou{width:40px;height:40px;border-radius:50%;background:var(--sun);color:var(--ink);font-weight:800;display:grid;place-items:center;font-size:14px}
.outras{background:#FFF4BF;border:1px solid #F1DC6A;border-radius:14px;padding:12px 14px;font-weight:600;margin-bottom:16px}
.ctas{display:grid;gap:10px}
.ctas .btn{width:100%;min-height:54px;font-size:16px}
.aviso{font-size:13px;color:var(--muted);margin-top:14px}
.sticky{position:fixed;left:0;right:0;bottom:0;z-index:30;background:rgba(250,247,240,.96);border-top:1px solid var(--line);padding:10px 16px calc(10px + env(safe-area-inset-bottom));display:flex;gap:10px;align-items:center}
.sticky .t{flex:1;font-size:13px;line-height:1.25}
.sticky .t b{font-size:16px;font-family:Archivo,sans-serif}
@media(min-width:900px){.sticky{display:none}}
.has-sticky{padding-bottom:84px}
@media(min-width:900px){.has-sticky{padding-bottom:0}}
/* rodapé */
footer{background:var(--ink);color:#bdb9b0;padding:32px 0;font-size:14px;margin-top:20px}
footer .wrap{display:grid;gap:10px}
footer a{color:#fff}
.empty{background:var(--card);border:1px dashed var(--line);border-radius:20px;padding:28px;text-align:center;color:var(--muted)}
"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'


def pixel(extra=""):
    return f"""<script>
!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init','{PIXEL}');fbq('track','PageView');{extra}
</script><noscript><img height="1" width="1" style="display:none" alt="" src="https://www.facebook.com/tr?id={PIXEL}&ev=PageView&noscript=1"/></noscript>"""


# Script comum: origem do anúncio na mensagem do WhatsApp + evento Lead + esconder vencidos
JS = """<script>
(function(){
  var q=new URLSearchParams(location.search);var camp=q.get('utm_campaign')||q.get('utm_source')||'';
  document.querySelectorAll('a[data-wa]').forEach(function(a){
    if(camp){try{var u=new URL(a.href);var t=u.searchParams.get('text')||'';u.searchParams.set('text',t+' (origem: '+camp+')');a.href=u.toString();}catch(e){}}
    a.addEventListener('click',function(){if(window.fbq){fbq('track','Lead',{content_name:a.getAttribute('data-wa')||'geral'});}});
  });
  document.querySelectorAll('a[data-grupo]').forEach(function(a){a.addEventListener('click',function(){if(window.fbq){fbq('trackCustom','EntrarGrupo');}});});
  var hoje=new Date().toISOString().slice(0,10);
  document.querySelectorAll('[data-ida]').forEach(function(c){if(c.getAttribute('data-ida')<hoje){c.remove();}});
})();
</script>"""


def head(title, desc, url, img):
    og_img = f"{SITE}/{img}" if img else f"{SITE}/img/og.jpg"
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{e(url)}">
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{e(url)}"><meta property="og:image" content="{e(og_img)}"><meta property="og:locale" content="pt_BR">
<meta name="theme-color" content="#111111"><link rel="icon" type="image/png" href="/img/icone.png"><link rel="apple-touch-icon" href="/img/icone.png">
{FONTS}<style>{CSS}</style>"""


def topo():
    return f"""<header class="top"><div class="wrap"><a class="brand" href="/" aria-label="Stefanello Viagens - início"><img src="/img/logo.png" alt="Stefanello Viagens" width="178" height="40" class="logo"></a>
<a class="btn btn-wa btn-sm" data-wa="topo" href="{e(wa_link('Oi! Vim pelo site de pacotes da Stefanello Viagens e quero ajuda com uma viagem.'))}" target="_blank" rel="noopener">{WA_ICON}<span>WhatsApp</span></a></div></header>"""


def rodape():
    return f"""<footer><div class="wrap"><img src="/img/logo-branca.png" alt="Stefanello Viagens" width="160" height="36" class="logo-ft">
<p>Stefanello Viagens LTDA · CNPJ 54.630.293/0001-10 · Rua José Felice, nº 30, Centro, São João do Polêsine - RS</p>
<p><a href="{e(INSTA)}" target="_blank" rel="noopener">Instagram @stefanelloviagens</a> · <a href="https://stefanelloviagens.com.br/">stefanelloviagens.com.br</a> · <a href="{e(GRUPO)}" data-grupo target="_blank" rel="noopener">Grupo de promoções</a></p>
<p>*Valores sujeitos a disponibilidade e alteração a qualquer momento.</p></div></footer>"""


def fake_art(p):
    return f"""<div class="fake-art" role="img" aria-label="{e(p['titulo'])}"><span class="bf">🔥 BLACK FRIDAY</span><div><div class="d">{e(p['destino'].upper())}</div><div class="s">{p['dias']} dias · {p['noites']} noites · {p['pessoas']} pessoas</div></div><div class="pr"><b>R$ {e(p['pix'])}</b><span>no PIX ou {p['parcelas']}x de R$ {e(p['parcela'])}</span></div></div>"""


def card(p):
    art = f'<img class="art" src="/{e(p["img"])}" alt="{e(p["titulo"])}" loading="lazy" width="960" height="1200">' if p.get("img") else fake_art(p)
    chips = (['<span class="chip bf">BLACK FRIDAY</span>'] if p.get("black") else []) + [f'<span class="chip">{p["dias"]} dias / {p["noites"]} noites</span>', f'<span class="chip">{p["pessoas"]} pessoas</span>']
    return f"""<a class="card" href="/{e(p['slug'])}" data-ida="{e(p['ida'])}">{art}<div class="body"><div class="meta">{''.join(chips)}</div><h3>{e(p['titulo'])}</h3>
<p style="font-size:14px;color:var(--muted)">📅 {e(p['idaTxt'])} → {e(p['voltaTxt'].split(' (')[0])}</p>
<div class="price"><div class="p1"><b>R$ {e(p['pix'])}</b> no PIX</div><div class="p2">ou {p['parcelas']}x de R$ {e(p['parcela'])} sem juros</div></div><span class="more">Ver o pacote →</span></div></a>"""


def index():
    cards = "".join(card(p) for p in ativos) or '<div class="empty">Novos pacotes chegando. Me chama no WhatsApp que eu te mando as ofertas de hoje.</div>'
    tem_black = any(p.get("black") for p in ativos)
    desc = "Pacotes com aéreo, hotel e transfer saindo de Porto Alegre, com preço no PIX e até 15x sem juros. Atendimento direto pelo WhatsApp."
    body = f"""<body>{topo()}
<section class="hero"><div class="wrap">{'<span class="tag">🖤💛 Black Friday</span>' if tem_black else ''}
<h1>Pacotes de viagem saindo de <em>Porto Alegre</em></h1>
<p>Aéreo, hotel e transfer no mesmo pacote, com preço no PIX ou parcelado em até 15x sem juros. Tu escolhe, me chama no WhatsApp e eu cuido do resto.</p>
<div class="cta"><a class="btn btn-wa" data-wa="hero" href="{e(wa_link('Oi! Vi os pacotes no site da Stefanello Viagens e quero saber mais.'))}" target="_blank" rel="noopener">{WA_ICON}Falar no WhatsApp</a><a class="btn btn-ghost" href="{e(GRUPO)}" data-grupo target="_blank" rel="noopener">Entrar no grupo de promoções</a></div>
<div class="trust"><span>✔ <b>CNPJ</b> 54.630.293/0001-10</span><span>✔ Agência do <b>RS</b></span><span>✔ Atendimento <b>humano</b> do começo ao fim</span></div></div></section>
<main><section class="sec"><div class="wrap"><h2>Pacotes da semana</h2><p class="sub">Valores para o número de pessoas indicado em cada pacote. Tem outras datas? Me pergunta.</p>
<div class="grid">{cards}</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="band"><div><h2>Quer receber as promoções primeiro?</h2><p>Entra no grupo de WhatsApp da Stefanello Viagens. Só ofertas, sem spam.</p></div><a class="btn" style="background:var(--ink);color:#fff" href="{e(GRUPO)}" data-grupo target="_blank" rel="noopener">Entrar no grupo</a></div></div></section></main>
{rodape()}{JS}</body></html>"""
    return head("Pacotes de viagem saindo de Porto Alegre | Stefanello Viagens", desc, SITE + "/", ativos[0]["img"] if ativos and ativos[0].get("img") else "") + pixel() + "</head>" + body


def pagina(p):
    url = f"{SITE}/{p['slug']}"
    msg = msg_pacote(p)
    media = f'<img src="/{e(p["img"])}" alt="{e(p["titulo"])}" width="960" height="1200">' if p.get("img") else fake_art(p)
    inc = "".join(f"<li><span>{i}</span><span>{e(t)}</span></li>" for i, t in p["inclui"])
    selo = f'<span class="selo">{e(p["selo"])}</span>' if p.get("selo") else ""
    outras = f'<div class="outras">📆 {e(p["outrasDatas"])} Me chama que eu te mando as opções.</div>' if p.get("outrasDatas") else ""
    desc = f"{p['titulo']}: {p['dias']} dias / {p['noites']} noites para {p['pessoas']} pessoas. R$ {p['pix']} no PIX ou {p['parcelas']}x de R$ {p['parcela']} sem juros."
    vc = f"fbq('track','ViewContent',{{content_name:{json.dumps(p['titulo'])},content_ids:[{json.dumps(p['slug'])}],content_type:'product'}});"
    body = f"""<body class="has-sticky">{topo()}
<main class="wrap"><a class="back" href="/">← Todos os pacotes</a>
<div class="pk"><div class="media">{media}</div>
<div><span class="chip bf">{'🖤💛 BLACK FRIDAY' if p.get('black') else 'PACOTE'}</span>{selo}
<h1>{e(p['titulo'])}</h1><p class="lead">{e(p['chamada'])}</p>
<div class="facts"><div class="fact"><b>{p['pessoas']}</b><span>pessoas</span></div><div class="fact"><b>{p['dias']} dias</b><span>{p['noites']} noites</span></div><div class="fact"><b>Saída</b><span>Porto Alegre</span></div></div>
<div class="box datas"><h2>Datas</h2><p>📅 <span><b>Ida:</b> {e(p['idaTxt'])}</span></p><p>📅 <span><b>Retorno:</b> {e(p['voltaTxt'])}</span></p></div>
<div class="box"><h2>O pacote inclui</h2><ul class="inc">{inc}</ul></div>
<div class="pbox"><span class="lbl">{'PREÇO BLACK FRIDAY' if p.get('black') else 'INVESTIMENTO'}</span><div class="row"><div><div class="v">R$ {e(p['pix'])}</div><small>já com desconto no PIX</small></div><div class="ou">OU</div><div><div class="v">{p['parcelas']}x R$ {e(p['parcela'])}</div><small>sem juros no cartão</small></div></div></div>
{outras}
<div class="ctas"><a class="btn btn-wa" data-wa="{e(p['slug'])}" href="{e(wa_link(msg))}" target="_blank" rel="noopener">{WA_ICON}Quero esse pacote</a>
<a class="btn btn-ghost" href="{e(GRUPO)}" data-grupo target="_blank" rel="noopener">Entrar no grupo de promoções</a></div>
<p class="aviso">*Valores sujeitos a disponibilidade e alteração a qualquer momento. O valor só fica garantido na reserva.</p></div></div></main>
<div class="sticky"><div class="t">{e(p['destino'])}<br><b>R$ {e(p['pix'])}</b> no PIX</div><a class="btn btn-wa" data-wa="{e(p['slug'])}-barra" href="{e(wa_link(msg))}" target="_blank" rel="noopener">{WA_ICON}Quero</a></div>
{rodape()}{JS}</body></html>"""
    return head(f"{p['titulo']} | Stefanello Viagens", desc, url, p.get("img", "")) + pixel(vc) + "</head>" + body


# limpa páginas antigas geradas
for f in ROOT.glob("*.html"):
    f.unlink()
(ROOT / "index.html").write_text(index(), encoding="utf-8")
for p in ativos:
    (ROOT / f"{p['slug']}.html").write_text(pagina(p), encoding="utf-8")
print("ativos:", [p["slug"] for p in ativos])
