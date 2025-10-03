# Additional modern CSS for the Gradio app
MODERN_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700;800&family=Manrope:wght@400;700;800&display=swap');
html, body {
  background: radial-gradient(1000px 600px at 20% -10%, rgba(59,130,246,.12), transparent 60%),
              radial-gradient(800px 500px at 80% 0%, rgba(236,72,153,.10), transparent 55%),
              #f8fafc;
  color: #0b1220;
  font-family: Manrope, Inter, Helvetica, Arial, sans-serif;
}
.gradio-container { max-width: 100% !important; width: 100% !important; margin: 0 auto !important; padding: 0 16px; }
.brand { display:block; text-align:center; font-family: Space Grotesk, Manrope, Inter, sans-serif; font-weight: 800; font-size: 40px; letter-spacing: .3px; background: linear-gradient(90deg,#06b6d4 0%,#a78bfa 45%,#fb7185 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 0 0 rgba(0,0,0,0), 0 6px 26px rgba(6,182,212,.28), 0 10px 46px rgba(167,139,250,.28), 0 14px 60px rgba(251,113,133,.22); background-size: 200% 200%; animation: brandGlow 8s ease-in-out infinite; }
@keyframes brandGlow { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
.subtitle { margin: 8px auto 12px; font-weight: 500; letter-spacing: 0.03em; line-height: 1.6; max-width: 900px; text-align: center; font-size: 1.05rem; color: #334155; }
.center-row { display: flex; justify-content: center; gap: 10px; margin: 0 auto; width: fit-content; }
#run-btn, #run-btn button { background: linear-gradient(90deg,#06b6d4,#a78bfa,#fb7185); color: white; padding: 10px 14px; font-size: 14px; border-radius: 12px; border: none; width: 120px; box-shadow: 0 10px 30px rgba(6,182,212,.25), 0 2px 8px rgba(0,0,0,.06); transition: transform .15s ease, box-shadow .2s ease; }
#run-btn button:hover { transform: translateY(-1px); box-shadow: 0 14px 36px rgba(6,182,212,.32), 0 3px 10px rgba(0,0,0,.08); }
#reset-btn, #reset-btn button { background: #ffffff; color: #2563eb; padding: 10px 14px; font-size: 14px; border-radius: 12px; border: 1px solid rgba(2,6,23,.12); width: 120px; box-shadow: 0 6px 18px rgba(2,6,23,.06); }
#stop-btn, #stop-btn button { background: linear-gradient(90deg,#ef4444,#f97316); color: white; padding: 8px 12px; font-size: 13px; border-radius: 10px; border: none; box-shadow: 0 8px 22px rgba(239,68,68,.2); width: 100px; }
.disclaimer { background: #ffffff; border: 1px solid rgba(2,6,23,.08); border-radius: 14px; padding: 14px 18px; max-width: 900px; margin: 16px auto 0; display: flex; align-items: flex-start; gap: 12px; box-shadow: 0 12px 28px rgba(2,6,23,.08); position: relative; overflow: hidden; }
.disclaimer:before { content:""; position:absolute; inset:-1px; background: linear-gradient(120deg, rgba(6,182,212,.25), rgba(167,139,250,.22), rgba(251,113,133,.22)); filter: blur(24px); opacity: .35; pointer-events:none; }
.disclaimer .icon { width: 28px; height: 28px; border-radius: 9999px; background: #facc15; display: inline-flex; align-items: center; justify-content: center; color: #0b1220; font-weight: 800; }
.disclaimer .text { color: #334155; line-height: 1.55; }
.topbar { display: flex; align-items: center; justify-content: space-between; padding: 10px 12px; margin: 0 auto 12px; max-width: 800px; background: rgba(255, 255, 255, 0.8); border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.04); }
.note { color: #475569; font-size: 13px; text-align: center; margin: 6px auto 4px; max-width: 500px; line-height: 1.5; font-weight: 500; opacity: 0.9; }
.center-note { text-align: center; color: #475569; font-size: 13px; margin: 4px 0 8px; line-height: 1.5; font-weight: 500; opacity: 0.9; }
#stop-btn button:disabled { cursor: not-allowed !important; opacity: .7 !important; }
/* Soft glow for panels */
.gr-box, .gr-panel { box-shadow: 0 16px 40px rgba(30,64,175,.08), 0 2px 10px rgba(2,6,23,.04) !important; border-radius: 14px !important; }
/* Plot container polish */
.wrap, .container { backdrop-filter: saturate(110%) blur(2px); }
/* Feature chips */
.features { display:flex; flex-wrap:wrap; gap:10px; align-items:center; justify-content:center; margin: 6px auto 4px; }
.chip { padding:6px 10px; border-radius:9999px; background: linear-gradient(90deg, rgba(6,182,212,.08), rgba(167,139,250,.10)); color:#0b1220; border:1px solid rgba(2,6,23,.08); box-shadow: 0 6px 18px rgba(2,6,23,.06); font-size: 13px; }
"""
