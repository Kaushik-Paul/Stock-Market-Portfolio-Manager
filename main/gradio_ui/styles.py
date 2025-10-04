# Additional modern CSS for the Gradio app with dark theme support
MODERN_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700;800&family=Manrope:wght@400;700;800&display=swap');

:root {
  --bg-primary: #f8fafc;
  --text-primary: #0b1220;
  --text-secondary: #334155;
  --panel-bg: #ffffff;
  --panel-border: rgba(2,6,23,.08);
  --panel-shadow: 0 2px 12px rgba(0,0,0,0.04);
  --chip-bg: linear-gradient(90deg, rgba(6,182,212,.08), rgba(167,139,250,.10));
  --chip-text: #0b1220;
  --chip-border: rgba(2,6,23,.08);
  --disclaimer-bg: #ffffff;
  --topbar-bg: rgba(255, 255, 255, 0.8);
  --note-color: #475569;
}

.dark {
  --bg-primary: #0f172a;
  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --panel-bg: #1e293b;
  --panel-border: rgba(148, 163, 184, 0.1);
  --panel-shadow: 0 2px 12px rgba(0,0,0,0.2);
  --chip-bg: linear-gradient(90deg, rgba(6,182,212,.15), rgba(167,139,250,.2));
  --chip-text: #e2e8f0;
  --chip-border: rgba(203, 213, 225, 0.1);
  --disclaimer-bg: #1e293b;
  --topbar-bg: rgba(30, 41, 59, 0.8);
  --note-color: #94a3b8;
}

html, body {
  background: radial-gradient(1000px 600px at 20% -10%, rgba(59,130,246,.12), transparent 60%),
              radial-gradient(800px 500px at 80% 0%, rgba(236,72,153,.10), transparent 55%),
              var(--bg-primary);
  color: var(--text-primary);
  font-family: Manrope, Inter, Helvetica, Arial, sans-serif;
  transition: background 0.3s ease, color 0.3s ease;
}

.gradio-container { 
  max-width: 100% !important; 
  width: 100% !important; 
  margin: 0 auto !important; 
  padding: 0 16px; 
}

.brand { 
  display: block; 
  text-align: center; 
  font-family: Space Grotesk, Manrope, Inter, sans-serif; 
  font-weight: 800; 
  font-size: 40px; 
  letter-spacing: .3px; 
  background: linear-gradient(90deg,#06b6d4 0%,#a78bfa 45%,#fb7185 100%); 
  -webkit-background-clip: text; 
  -webkit-text-fill-color: transparent; 
  text-shadow: 0 0 0 rgba(0,0,0,0), 0 6px 26px rgba(6,182,212,.28), 0 10px 46px rgba(167,139,250,.28), 0 14px 60px rgba(251,113,133,.22); 
  background-size: 200% 200%; 
  animation: brandGlow 8s ease-in-out infinite; 
}

@keyframes brandGlow { 
  0% { background-position: 0% 50%; } 
  50% { background-position: 100% 50%; } 
  100% { background-position: 0% 50%; } 
}

.subtitle { 
  margin: 8px auto 12px; 
  font-weight: 500; 
  letter-spacing: 0.03em; 
  line-height: 1.6; 
  max-width: 900px; 
  text-align: center; 
  font-size: 1.05rem; 
  color: var(--text-secondary);
  transition: color 0.3s ease;
}

.center-row { 
  display: flex; 
  justify-content: center; 
  gap: 10px; 
  margin: 0 auto; 
  width: fit-content; 
}

#run-btn, #run-btn button { 
  background: linear-gradient(90deg,#06b6d4,#a78bfa,#fb7185); 
  color: white; 
  padding: 10px 14px; 
  font-size: 14px; 
  border-radius: 12px; 
  border: none; 
  width: 120px; 
  box-shadow: 0 10px 30px rgba(6,182,212,.25), 0 2px 8px rgba(0,0,0,.06); 
  transition: transform .15s ease, box-shadow .2s ease; 
}

#run-btn button:hover { 
  transform: translateY(-1px); 
  box-shadow: 0 14px 36px rgba(6,182,212,.32), 0 3px 10px rgba(0,0,0,.08); 
}

#reset-btn, #reset-btn button { 
  background: var(--panel-bg); 
  color: #2563eb; 
  padding: 10px 14px; 
  font-size: 14px; 
  border-radius: 12px; 
  border: 1px solid var(--panel-border); 
  width: 120px; 
  box-shadow: 0 6px 18px rgba(2,6,23,.06); 
  transition: all 0.3s ease;
}

#stop-btn, #stop-btn button { 
  background: linear-gradient(90deg,#ef4444,#f97316); 
  color: white; 
  padding: 8px 12px; 
  font-size: 13px; 
  border-radius: 10px; 
  border: none; 
  box-shadow: 0 8px 22px rgba(239,68,68,.2); 
  width: 100px; 
}

.disclaimer { 
  background: var(--disclaimer-bg); 
  border: 1px solid var(--panel-border); 
  border-radius: 14px; 
  padding: 14px 18px; 
  max-width: 900px; 
  margin: 16px auto 0; 
  display: flex; 
  align-items: flex-start; 
  gap: 12px; 
  box-shadow: 0 12px 28px rgba(2,6,23,.08); 
  position: relative; 
  overflow: hidden; 
  transition: all 0.3s ease;
}

.disclaimer:before { 
  content:""; 
  position:absolute; 
  inset:-1px; 
  background: linear-gradient(120deg, rgba(6,182,212,.25), rgba(167,139,250,.22), rgba(251,113,133,.22)); 
  filter: blur(24px); 
  opacity: .35; 
  pointer-events:none; 
}

.disclaimer .icon { 
  width: 28px; 
  height: 28px; 
  border-radius: 9999px; 
  background: #facc15; 
  display: inline-flex; 
  align-items: center; 
  justify-content: center; 
  color: #0b1220; 
  font-weight: 800; 
}

.disclaimer .text { 
  color: var(--text-secondary); 
  line-height: 1.55; 
  transition: color 0.3s ease;
}

.topbar { 
  display: flex; 
  align-items: center; 
  justify-content: space-between; 
  padding: 10px 12px; 
  margin: 0 auto 12px; 
  max-width: 800px; 
  background: var(--topbar-bg); 
  border-radius: 12px; 
  box-shadow: var(--panel-shadow);
  backdrop-filter: blur(8px);
  transition: all 0.3s ease;
}

.note, .center-note { 
  color: var(--note-color); 
  font-size: 13px; 
  text-align: center; 
  margin: 6px auto 4px; 
  max-width: 500px; 
  line-height: 1.5; 
  font-weight: 500; 
  opacity: 0.9; 
  transition: color 0.3s ease;
}

.center-note { 
  margin: 4px 0 8px; 
}

#stop-btn button:disabled { 
  cursor: not-allowed !important; 
  opacity: .7 !important; 
}

/* Soft glow for panels */
.gr-box, .gr-panel, .gradio-plot { 
  background: var(--panel-bg) !important;
  color: var(--text-primary) !important;
  border: 1px solid var(--panel-border) !important;
  box-shadow: 0 16px 40px rgba(30,64,175,.08), 0 2px 10px rgba(2,6,23,.04) !important; 
  border-radius: 14px !important; 
  transition: all 0.3s ease !important;
}

/* Plot container polish */
.wrap, .container { 
  backdrop-filter: saturate(110%) blur(2px); 
}

/* Feature chips */
.features { 
  display:flex; 
  flex-wrap:wrap; 
  gap:10px; 
  align-items:center; 
  justify-content:center; 
  margin: 6px auto 4px; 
}

.chip { 
  padding:6px 10px; 
  border-radius:9999px; 
  background: var(--chip-bg); 
  color: var(--chip-text); 
  border:1px solid var(--chip-border); 
  box-shadow: 0 6px 18px rgba(2,6,23,.06); 
  font-size: 13px;
  transition: all 0.3s ease;
}

/* Dataframe styles */
.dataframe-fix, .dataframe-fix-small {
  background: var(--panel-bg) !important;
  color: var(--text-primary) !important;
  border: 1px solid var(--panel-border) !important;
}

.dataframe-fix th, .dataframe-fix-small th {
  background: var(--panel-bg) !important;
  color: var(--text-primary) !important;
  border-bottom: 1px solid var(--panel-border) !important;
}

.dataframe-fix td, .dataframe-fix-small td {
  border-bottom: 1px solid var(--panel-border) !important;
  color: var(--text-secondary) !important;
}

/* Scrollbar styling */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--panel-bg);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #666;
}
"""
