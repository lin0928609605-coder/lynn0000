from http.server import HTTPServer, BaseHTTPRequestHandler


PAGE = """<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>我是加鹽</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      overflow: hidden;
      display: grid;
      place-items: center;
      color: #fff;
      font-family: "Microsoft JhengHei", system-ui, sans-serif;
      background: radial-gradient(circle at 50% 20%, #27205e 0, #090b1a 45%, #03030a 100%);
    }
    body::selection { background: #f0abfc; color: #080615; }
    body::before, body::after {
      content: "";
      position: fixed;
      width: 46vmax;
      height: 46vmax;
      border-radius: 50%;
      filter: blur(32px);
      opacity: .68;
      animation: drift 9s ease-in-out infinite alternate;
    }
    body::before { background: #6d28d9; top: -20vmax; left: -12vmax; }
    body::after { background: #0891b2; right: -14vmax; bottom: -22vmax; animation-delay: -6s; }
    .grid {
      position: fixed;
      inset: -30%;
      z-index: 0;
      background-image: linear-gradient(rgba(103,232,249,.13) 1px, transparent 1px), linear-gradient(90deg, rgba(103,232,249,.13) 1px, transparent 1px);
      background-size: 52px 52px;
      transform: perspective(420px) rotateX(63deg) translateY(12%);
      mask-image: linear-gradient(to bottom, transparent 18%, #000 56%, transparent 92%);
      animation: gridMove 3s linear infinite;
    }
    .scanline {
      position: fixed;
      z-index: 2;
      inset: 0;
      pointer-events: none;
      background: linear-gradient(transparent 48%, rgba(255,255,255,.04) 50%, transparent 52%);
      background-size: 100% 6px;
      mix-blend-mode: overlay;
    }
    .orb {
      position: fixed;
      z-index: 1;
      width: 11px;
      height: 11px;
      border-radius: 50%;
      background: #fff;
      box-shadow: 0 0 12px 4px #67e8f9, 0 0 28px 8px #a855f7;
      animation: float 5s ease-in-out infinite alternate;
    }
    .orb.one { top: 18%; left: 14%; }
    .orb.two { right: 17%; bottom: 18%; width: 7px; height: 7px; animation-delay: -2s; }
    .orb.three { top: 22%; right: 24%; width: 5px; height: 5px; animation-delay: -4s; }
    .dino {
      position: fixed;
      z-index: 3;
      right: clamp(1rem, 8vw, 8rem);
      bottom: clamp(1rem, 7vh, 4rem);
      font-size: clamp(5rem, 13vw, 10rem);
      line-height: 1;
      filter: drop-shadow(0 0 7px #bbf7d0) drop-shadow(0 0 24px #22c55e) drop-shadow(0 0 46px #d946ef);
      transform-origin: 55% 85%;
      animation: dinoDance 1.35s ease-in-out infinite alternate;
      user-select: none;
    }
    .dino::after {
      content: "+10 可愛值";
      position: absolute;
      top: -1.2rem;
      right: -1.6rem;
      padding: .35rem .6rem;
      border: 1px solid #f0abfc;
      border-radius: 999px;
      color: #fff;
      background: rgba(126,34,206,.75);
      font: 700 .8rem "Microsoft JhengHei", sans-serif;
      letter-spacing: .05em;
      box-shadow: 0 0 18px #d946ef;
      animation: badgePop 1.35s ease-in-out infinite alternate;
    }
    main {
      position: relative;
      z-index: 1;
      width: min(88vw, 720px);
      padding: clamp(2rem, 7vw, 5rem);
      text-align: center;
      border: 1px solid rgba(125,211,252,.55);
      border-radius: 32px;
      background: linear-gradient(135deg, rgba(20, 22, 62, .9), rgba(8, 10, 30, .68));
      box-shadow: 0 0 0 1px rgba(217,70,239,.3), 0 0 44px rgba(34,211,238,.35), 0 30px 90px rgba(0,0,0,.65), inset 0 1px rgba(255,255,255,.22);
      backdrop-filter: blur(18px);
      animation: cardFloat 4s ease-in-out infinite alternate;
    }
    .badge { color: #a5f3fc; font-weight: 700; letter-spacing: .35em; font-size: .8rem; text-shadow: 0 0 14px #22d3ee; }
    h1 {
      margin: .7rem 0 1rem;
      font-size: clamp(3rem, 11vw, 7rem);
      letter-spacing: .08em;
      background: linear-gradient(100deg, #fff, #67e8f9 22%, #f0abfc 48%, #c4b5fd 70%, #fff);
      background-size: 200% auto;
      -webkit-background-clip: text;
      color: transparent;
      filter: drop-shadow(0 0 12px #22d3ee) drop-shadow(0 0 30px #d946ef);
      animation: shine 2.8s linear infinite;
    }
    p { margin: 0; color: #dbeafe; font-size: clamp(1rem, 2.5vw, 1.3rem); text-shadow: 0 0 14px #60a5fa; }
    .spark { font-size: 2rem; display: block; margin-top: 1.5rem; color: #f0abfc; text-shadow: 0 0 20px #f0abfc; animation: pulse 1.2s ease-in-out infinite; }
    @keyframes drift { to { transform: translate(10vmax, 8vmax) scale(1.15); } }
    @keyframes shine { to { background-position: 200% center; } }
    @keyframes pulse { 50% { transform: scale(1.25) rotate(12deg); } }
    @keyframes gridMove { to { background-position: 0 52px, 52px 0; } }
    @keyframes float { to { transform: translate(28px, -36px) scale(1.7); } }
    @keyframes cardFloat { to { transform: translateY(-13px) rotateX(1deg) rotateY(-1deg); } }
    @keyframes dinoDance { to { transform: translateY(-22px) rotate(-9deg) scale(1.08); } }
    @keyframes badgePop { to { transform: translateY(-10px) scale(1.15); } }
  </style>
</head>
<body>
  <div class="grid"></div>
  <div class="scanline"></div>
  <div class="orb one"></div><div class="orb two"></div><div class="orb three"></div>
  <div class="dino" aria-label="可愛恐龍">🦖</div>
  <main>
    <div class="badge">HELLO, WORLD</div>
    <h1>我是加鹽</h1>
    <p>一點鹽，讓每個回應都更有味道。</p>
    <span class="spark">✦</span>
  </main>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):                    # 有人用 GET 來敲門時，執行這裡
        self.send_response(200)          # 狀態碼：成功
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()               # 標頭結束，接下來是 Body
        self.wfile.write(PAGE.encode("utf-8"))


if __name__ == "__main__":
    print("聽在 http://127.0.0.1:8000  （按 Ctrl+C 結束）")
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
