import os
from html import escape

os.makedirs("assets", exist_ok=True)


def write_svg(filename: str, content: str) -> None:
    path = os.path.join("assets", filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated {path}")


# ═══════════════════════════════════════════════════════════════════════
# 1. HERO BANNER: 3D Perspective Grid + Levitating Isometric Cube + HUD
# ═══════════════════════════════════════════════════════════════════════
def build_hero_svg() -> None:
    # Generate 3D vanishing-point grid lines
    v_lines = []
    for i in range(-10, 11):
        x_top = 600 + i * 28
        x_bot = 600 + i * 115
        v_lines.append(
            f'<line x1="{x_top}" y1="230" x2="{x_bot}" y2="380" stroke="#00F0FF" stroke-opacity="0.22" stroke-width="1"/>'
        )
    h_lines = []
    for idx, y in enumerate([238, 250, 266, 286, 312, 344, 378]):
        opacity = 0.14 + idx * 0.05
        h_lines.append(
            f'<line x1="0" y1="{y}" x2="1200" y2="{y}" stroke="#FF00A8" stroke-opacity="{opacity:.2f}" stroke-width="1"/>'
        )

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 380" width="100%">
  <defs>
    <radialGradient id="bgSpace" cx="72%" cy="42%" r="75%">
      <stop offset="0%" stop-color="#17123A"/>
      <stop offset="50%" stop-color="#0A0E24"/>
      <stop offset="100%" stop-color="#050714"/>
    </radialGradient>
    <linearGradient id="neonBorder" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF"/>
      <stop offset="50%" stop-color="#7B2CBF"/>
      <stop offset="100%" stop-color="#FF00A8"/>
    </linearGradient>
    <linearGradient id="holoTitle" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="45%" stop-color="#00F0FF"/>
      <stop offset="100%" stop-color="#FF00A8"/>
    </linearGradient>
    <linearGradient id="cubeTop" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#7B2CBF" stop-opacity="0.45"/>
    </linearGradient>
    <linearGradient id="cubeLeft" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#7B2CBF" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="#0B1026" stop-opacity="0.85"/>
    </linearGradient>
    <linearGradient id="cubeRight" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF00A8" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="#220D3A" stop-opacity="0.9"/>
    </linearGradient>
    <linearGradient id="scanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF" stop-opacity="0"/>
      <stop offset="50%" stop-color="#00F0FF" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#00F0FF" stop-opacity="0"/>
    </linearGradient>
    <filter id="glowCyan" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glowStrong" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="heroClip">
      <rect x="6" y="6" width="1188" height="368" rx="18"/>
    </clipPath>
    <style><![CDATA[
      .title-font {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; font-weight: 900; letter-spacing: 2px; }}
      .mono {{ font-family: 'Fira Code', 'JetBrains Mono', ui-monospace, monospace; }}
      .float-cube {{ animation: float3d 4.6s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite; }}
      .float-shadow {{ animation: shadowPulse 4.6s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite; transform-origin: 940px 292px; }}
      .ring-cw {{ animation: spinCW 18s linear infinite; transform-origin: 940px 185px; }}
      .ring-ccw {{ animation: spinCCW 12s linear infinite; transform-origin: 940px 185px; }}
      .pulse-dot {{ animation: pulseOrb 1.8s ease-in-out infinite; }}
      .scanline {{ animation: scanSweep 5.5s linear infinite; }}
      .flow-circuit {{ stroke-dasharray: 12 10; animation: dashFlow 2.4s linear infinite; }}
      .sheen-text {{ animation: chromaShift 4s ease-in-out infinite; }}

      @keyframes float3d {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-16px); }}
      }}
      @keyframes shadowPulse {{
        0%, 100% {{ transform: scale(1); opacity: 0.55; }}
        50% {{ transform: scale(0.76); opacity: 0.25; }}
      }}
      @keyframes spinCW {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
      }}
      @keyframes spinCCW {{
        from {{ transform: rotate(360deg); }}
        to {{ transform: rotate(0deg); }}
      }}
      @keyframes pulseOrb {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.3; }}
      }}
      @keyframes scanSweep {{
        0% {{ transform: translateY(-40px); }}
        100% {{ transform: translateY(420px); }}
      }}
      @keyframes dashFlow {{
        to {{ stroke-dashoffset: -44; }}
      }}
      @keyframes chromaShift {{
        0%, 100% {{ transform: translateX(0px); }}
        50% {{ transform: translateX(2.5px); }}
      }}
    ]]></style>
  </defs>

  <!-- Outer 3D Extruded Depth Plates -->
  <rect x="10" y="10" width="1186" height="366" rx="18" fill="none" stroke="#FF00A8" stroke-opacity="0.35" stroke-width="1.5"/>
  <rect x="6" y="6" width="1188" height="368" rx="18" fill="url(#bgSpace)" stroke="url(#neonBorder)" stroke-width="2"/>

  <g clip-path="url(#heroClip)">
    <!-- Ambient 3D Radial Glow Orbs -->
    <circle cx="940" cy="180" r="190" fill="#7B2CBF" fill-opacity="0.18" filter="url(#glowStrong)"/>
    <circle cx="240" cy="110" r="150" fill="#00F0FF" fill-opacity="0.09" filter="url(#glowStrong)"/>

    <!-- 3D Perspective Cyber Floor Grid -->
    <g>
      <rect x="0" y="229" width="1200" height="2" fill="#00F0FF" fill-opacity="0.6" filter="url(#glowCyan)"/>
      {''.join(v_lines)}
      {''.join(h_lines)}
    </g>

    <!-- Animated Circuit Accent Trace -->
    <path d="M 48 64 L 180 64 L 200 84 L 460 84" fill="none" stroke="#00F0FF" stroke-opacity="0.45" stroke-width="1.5" class="flow-circuit"/>
    <path d="M 48 326 L 260 326 L 284 304 L 540 304" fill="none" stroke="#FF00A8" stroke-opacity="0.4" stroke-width="1.5" class="flow-circuit"/>

    <!-- Corner HUD Brackets -->
    <path d="M 24 46 L 24 24 L 46 24" fill="none" stroke="#00F0FF" stroke-width="2.5"/>
    <path d="M 1154 24 L 1176 24 L 1176 46" fill="none" stroke="#FF00A8" stroke-width="2.5"/>
    <path d="M 24 334 L 24 356 L 46 356" fill="none" stroke="#FF00A8" stroke-width="2.5"/>
    <path d="M 1154 356 L 1176 356 L 1176 334" fill="none" stroke="#00F0FF" stroke-width="2.5"/>

    <!-- LEFT HUD TYPOGRAPHY -->
    <text x="56" y="54" class="mono" font-size="12" fill="#00F0FF" letter-spacing="3">REP-JULIAN // NEURAL DECK v5.0</text>

    <!-- 3D Chromatic Extruded Title Layers -->
    <text x="58" y="156" class="title-font sheen-text" font-size="54" fill="#FF00A8" fill-opacity="0.55">Hello, I'm Julian</text>
    <text x="54" y="152" class="title-font" font-size="54" fill="#00F0FF" fill-opacity="0.45">Hello, I'm Julian</text>
    <text x="56" y="154" class="title-font" font-size="54" fill="url(#holoTitle)" filter="url(#glowCyan)">Hello, I'm Julian</text>

    <text x="58" y="194" class="mono" font-size="16" font-weight="700" fill="#E8F7FF">AI Automation Architect · Full-Stack Builder · QCU</text>
    <text x="58" y="220" class="mono" font-size="13.5" fill="#9BB0DF">Engineering autonomous tools, real-time browser overlays &amp; futuristic UX.</text>

    <!-- Pulsing Holographic Status Pill -->
    <g transform="translate(56, 246)">
      <rect x="3" y="3" width="276" height="36" rx="18" fill="#FF00A8" fill-opacity="0.22"/>
      <rect x="0" y="0" width="276" height="36" rx="18" fill="#0B1026" stroke="#00F0FF" stroke-width="1.4"/>
      <circle cx="22" cy="18" r="5" fill="#00F0FF" filter="url(#glowCyan)" class="pulse-dot"/>
      <text x="38" y="22.5" class="mono" font-size="12" font-weight="700" fill="#E8F7FF" letter-spacing="1.5">SHIPPING AT NIGHT // LIVE</text>
    </g>

    <!-- Bottom Coordinates -->
    <text x="56" y="346" class="mono" font-size="11" fill="#7A8BB8" letter-spacing="2">COFFEE · CURIOSITY · AUTONOMOUS CODE</text>
    <text x="560" y="346" class="mono" font-size="11" fill="#00F0FF" fill-opacity="0.7" letter-spacing="1.5">LAT 14.6760° N · LON 121.0437° E</text>

    <!-- RIGHT 3D HOLOGRAPHIC CORE & ORBITING RINGS -->
    <!-- Ground Hologram Shadow -->
    <ellipse cx="940" cy="292" rx="82" ry="18" fill="#00F0FF" fill-opacity="0.25" filter="url(#glowStrong)" class="float-shadow"/>

    <!-- Counter-Rotating HUD Rings -->
    <g class="ring-cw">
      <circle cx="940" cy="185" r="118" fill="none" stroke="#00F0FF" stroke-opacity="0.45" stroke-width="1.5" stroke-dasharray="18 10 4 10"/>
      <circle cx="940" cy="67" r="4" fill="#00F0FF" filter="url(#glowCyan)"/>
      <circle cx="1058" cy="185" r="3.5" fill="#FF00A8" filter="url(#glowCyan)"/>
    </g>
    <g class="ring-ccw">
      <circle cx="940" cy="185" r="94" fill="none" stroke="#FF00A8" stroke-opacity="0.55" stroke-width="1.5" stroke-dasharray="32 14"/>
      <circle cx="940" cy="279" r="3.5" fill="#00F0FF" filter="url(#glowCyan)"/>
    </g>

    <!-- Floating 3D Isometric Hypercube -->
    <g class="float-cube" filter="url(#glowCyan)">
      <!-- Outer Isometric Cube -->
      <polygon points="940,108 1006,146 940,184 874,146" fill="url(#cubeTop)" stroke="#00F0FF" stroke-width="1.8"/>
      <polygon points="874,146 940,184 940,256 874,218" fill="url(#cubeLeft)" stroke="#00F0FF" stroke-width="1.5"/>
      <polygon points="1006,146 940,184 940,256 1006,218" fill="url(#cubeRight)" stroke="#FF00A8" stroke-width="1.5"/>
      <!-- Inner Floating Core Prism -->
      <polygon points="940,148 972,166 940,184 908,166" fill="#FFFFFF" fill-opacity="0.85"/>
      <polygon points="908,166 940,184 940,218 908,200" fill="#00F0FF" fill-opacity="0.65"/>
      <polygon points="972,166 940,184 940,218 972,200" fill="#FF00A8" fill-opacity="0.7"/>
      <!-- Wireframe Vertices -->
      <line x1="940" y1="108" x2="940" y2="148" stroke="#FFFFFF" stroke-opacity="0.6" stroke-width="1"/>
      <line x1="874" y1="218" x2="908" y2="200" stroke="#00F0FF" stroke-opacity="0.6" stroke-width="1"/>
      <line x1="1006" y1="218" x2="972" y2="200" stroke="#FF00A8" stroke-opacity="0.6" stroke-width="1"/>
    </g>
  </g>
</svg>
"""
    write_svg("profile-hero-3d.svg", svg)


# ═══════════════════════════════════════════════════════════════════════
# 2. ANIMATED PLASMA ENERGY DIVIDER
# ═══════════════════════════════════════════════════════════════════════
def build_divider_svg() -> None:
    svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 28" width="100%">
  <defs>
    <linearGradient id="railGrad" gradientUnits="userSpaceOnUse" x1="20" y1="14" x2="880" y2="14">
      <stop offset="0%" stop-color="#00F0FF" stop-opacity="0" />
      <stop offset="28%" stop-color="#00F0FF" stop-opacity="0.9" />
      <stop offset="50%" stop-color="#FF00A8" stop-opacity="1" />
      <stop offset="72%" stop-color="#00F0FF" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#00F0FF" stop-opacity="0" />
    </linearGradient>
    <style><![CDATA[
      .pulse-beam { stroke-dasharray: 65 200; animation: beamMove 2.6s linear infinite; }
      .pulse-beam-rev { stroke-dasharray: 65 200; animation: beamMoveRev 2.6s linear infinite; }
      .core-spin { transform-origin: 450px 14px; animation: spinDiamond 6s linear infinite; }
      @keyframes beamMove { from { stroke-dashoffset: 265; } to { stroke-dashoffset: 0; } }
      @keyframes beamMoveRev { from { stroke-dashoffset: 0; } to { stroke-dashoffset: 265; } }
      @keyframes spinDiamond { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    ]]></style>
  </defs>

  <rect x="20" y="13" width="860" height="2" rx="1" fill="url(#railGrad)" />

  <path d="M 40 14 L 432 14" fill="none" stroke="#00F0FF" stroke-width="6" stroke-opacity="0.25" stroke-linecap="round" class="pulse-beam" />
  <path d="M 40 14 L 432 14" fill="none" stroke="#00F0FF" stroke-width="2.5" stroke-linecap="round" class="pulse-beam" />
  <path d="M 40 14 L 432 14" fill="none" stroke="#FFFFFF" stroke-width="1" stroke-linecap="round" class="pulse-beam" />

  <path d="M 468 14 L 860 14" fill="none" stroke="#FF00A8" stroke-width="6" stroke-opacity="0.25" stroke-linecap="round" class="pulse-beam-rev" />
  <path d="M 468 14 L 860 14" fill="none" stroke="#FF00A8" stroke-width="2.5" stroke-linecap="round" class="pulse-beam-rev" />
  <path d="M 468 14 L 860 14" fill="none" stroke="#FFFFFF" stroke-width="1" stroke-linecap="round" class="pulse-beam-rev" />

  <g class="core-spin">
    <circle cx="450" cy="14" r="8" fill="#00F0FF" fill-opacity="0.2" />
    <polygon points="450,5 459,14 450,23 441,14" fill="#0B1026" stroke="#00F0FF" stroke-width="1.8" />
    <circle cx="450" cy="14" r="2.5" fill="#FF00A8" />
  </g>
</svg>
"""
    write_svg("divider-3d.svg", svg)


# ═══════════════════════════════════════════════════════════════════════
# 3. 3D GLASSMORPHIC CONFIG TERMINAL WITH BOOT TRANSITIONS
# ═══════════════════════════════════════════════════════════════════════
def build_terminal_svg() -> None:
    svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 360" width="100%">
  <defs>
    <linearGradient id="termBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0D1430"/>
      <stop offset="100%" stop-color="#050714"/>
    </linearGradient>
    <linearGradient id="termBorder" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF"/>
      <stop offset="55%" stop-color="#7B2CBF"/>
      <stop offset="100%" stop-color="#FF00A8"/>
    </linearGradient>
    <linearGradient id="glassSheen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="50%" stop-color="#00F0FF" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <filter id="tGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="termClip">
      <rect x="8" y="8" width="736" height="336" rx="14"/>
    </clipPath>
    <style><![CDATA[
      .code { font-family: 'Fira Code', 'JetBrains Mono', ui-monospace, monospace; font-size: 13.5px; }
      .k { fill: #FF00A8; font-weight: 700; }
      .v { fill: #E8F7FF; }
      .p { fill: #00F0FF; }
      .s { fill: #A7F3D0; }
      .m { fill: #7A8BB8; }
      .cursor { animation: blink 1s step-end infinite; }
      .sheen { animation: sweepX 6.5s ease-in-out infinite; }
      .line1 { animation: bootIn 0.8s ease-out both; }
      .line2 { animation: bootIn 1.1s ease-out both; }
      .line3 { animation: bootIn 1.4s ease-out both; }
      .line4 { animation: bootIn 1.7s ease-out both; }
      .line5 { animation: bootIn 2.0s ease-out both; }
      @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
      @keyframes sweepX {
        0%, 60% { transform: translateX(-420px) skewX(-20deg); }
        100% { transform: translateX(920px) skewX(-20deg); }
      }
      @keyframes bootIn {
        0% { opacity: 0.15; transform: translateX(-6px); }
        100% { opacity: 1; transform: translateX(0px); }
      }
    ]]></style>
  </defs>

  <!-- 3D Extruded Depth Plates -->
  <rect x="16" y="16" width="736" height="336" rx="14" fill="#FF00A8" fill-opacity="0.16" stroke="#FF00A8" stroke-opacity="0.45" stroke-width="1"/>
  <rect x="12" y="12" width="736" height="336" rx="14" fill="#00F0FF" fill-opacity="0.12" stroke="#00F0FF" stroke-opacity="0.4" stroke-width="1"/>

  <!-- Primary Glassmorphic Terminal Frame -->
  <rect x="8" y="8" width="736" height="336" rx="14" fill="url(#termBg)" stroke="url(#termBorder)" stroke-width="1.8"/>

  <g clip-path="url(#termClip)">
    <!-- Top Header Bar -->
    <rect x="8" y="8" width="736" height="42" fill="#10183A" fill-opacity="0.9"/>
    <line x1="8" y1="50" x2="744" y2="50" stroke="#00F0FF" stroke-opacity="0.35" stroke-width="1"/>
    <circle cx="32" cy="29" r="5.5" fill="#FF00A8" filter="url(#tGlow)"/>
    <circle cx="52" cy="29" r="5.5" fill="#7B2CBF"/>
    <circle cx="72" cy="29" r="5.5" fill="#00F0FF" filter="url(#tGlow)"/>
    <rect x="278" y="18" width="196" height="22" rx="6" fill="#050714" stroke="#00F0FF" stroke-opacity="0.4"/>
    <text x="376" y="33" text-anchor="middle" class="code" font-size="11.5" fill="#00F0FF">julian.config.ts // 3D</text>

    <!-- Code Body -->
    <g transform="translate(32, 82)">
      <text y="0" class="code line1"><tspan class="k">export const</tspan> <tspan class="p">engineer</tspan> <tspan class="v">=</tspan> <tspan class="m">{</tspan></text>
      <text x="20" y="28" class="code line1"><tspan class="p">name</tspan><tspan class="m">:</tspan> <tspan class="s">"Julian Agustino"</tspan><tspan class="m">,</tspan></text>
      <text x="20" y="54" class="code line2"><tspan class="p">handle</tspan><tspan class="m">:</tspan> <tspan class="s">"@REP-Julian"</tspan><tspan class="m">,</tspan></text>
      <text x="20" y="80" class="code line2"><tspan class="p">focus</tspan><tspan class="m">:</tspan> <tspan class="s">"AI Automation, Userscripts &amp; Tooling"</tspan><tspan class="m">,</tspan></text>
      <text x="20" y="106" class="code line3"><tspan class="p">coreStack</tspan><tspan class="m">:</tspan> <tspan class="m">[</tspan><tspan class="s">"Python"</tspan><tspan class="m">, </tspan><tspan class="s">"JavaScript"</tspan><tspan class="m">, </tspan><tspan class="s">"Playwright"</tspan><tspan class="m">, </tspan><tspan class="s">"Ollama"</tspan><tspan class="m">],</tspan></text>
      <text x="20" y="132" class="code line3"><tspan class="p">shippingNow</tspan><tspan class="m">:</tspan> <tspan class="s">"QCU-WEEK-2-PROJECT 🚀"</tspan><tspan class="m">,</tspan></text>
      <text x="20" y="158" class="code line4"><tspan class="p">fuel</tspan><tspan class="m">:</tspan> <tspan class="s">"Dark Roast + 24/7 Neural Lo-Fi"</tspan><tspan class="m">,</tspan></text>
      <text x="20" y="184" class="code line4"><tspan class="p">philosophy</tspan><tspan class="m">:</tspan> <tspan class="s">"Useful first. Intuitive always."</tspan></text>
      <text y="210" class="code line5"><tspan class="m">};</tspan></text>

      <!-- Live Command Prompt -->
      <text y="244" class="code line5">
        <tspan fill="#FF00A8" font-weight="700">julian@neural</tspan><tspan class="m">:</tspan><tspan class="p">~</tspan><tspan class="v">$ pnpm run make-magic</tspan>
      </text>
      <rect x="332" y="230" width="9" height="17" fill="#00F0FF" filter="url(#tGlow)" class="cursor"/>
    </g>

    <!-- Diagonal Glass Sheen Transition -->
    <rect x="0" y="0" width="220" height="360" fill="url(#glassSheen)" class="sheen"/>
  </g>
</svg>
"""
    write_svg("terminal-card-3d.svg", svg)


# ═══════════════════════════════════════════════════════════════════════
# 4. 3D NEURAL LO-FI AUDIO VISUALIZER DECK
# ═══════════════════════════════════════════════════════════════════════
def build_audio_hud_svg() -> None:
    bars = []
    heights = [22, 42, 30, 56, 48, 26, 62, 38, 52, 28, 60, 44, 32, 54, 40, 24]
    for i, h in enumerate(heights):
        x = 840 + i * 19
        color = "#00F0FF" if i % 2 == 0 else "#FF00A8"
        dur = 0.85 + (i % 5) * 0.18
        delay = (i % 4) * 0.12
        bars.append(
            f'<rect x="{x}" y="{75 - h/2:.1f}" width="9" height="{h}" rx="4" fill="{color}" '
            f'style="transform-origin:{x+4.5}px 75px; animation: eqPulse {dur:.2f}s ease-in-out {delay:.2f}s infinite;"/>'
        )

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 150" width="100%">
  <defs>
    <linearGradient id="audBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0B1026"/>
      <stop offset="50%" stop-color="#140E30"/>
      <stop offset="100%" stop-color="#070B1E"/>
    </linearGradient>
    <linearGradient id="audBorder" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00F0FF"/>
      <stop offset="50%" stop-color="#7B2CBF"/>
      <stop offset="100%" stop-color="#FF00A8"/>
    </linearGradient>
    <linearGradient id="progGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00F0FF"/>
      <stop offset="100%" stop-color="#FF00A8"/>
    </linearGradient>
    <filter id="aGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <style><![CDATA[
      .title {{ font-family: 'Segoe UI', system-ui, sans-serif; font-weight: 800; }}
      .mono {{ font-family: 'Fira Code', ui-monospace, monospace; }}
      .disc {{ transform-origin: 76px 75px; animation: spinDisc 7s linear infinite; }}
      .live-dot {{ animation: liveBlink 1.4s ease-in-out infinite; }}
      .progress-dot {{ animation: slideProg 9s linear infinite; }}
      @keyframes spinDisc {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
      @keyframes liveBlink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.25; }} }}
      @keyframes eqPulse {{
        0%, 100% {{ transform: scaleY(0.32); opacity: 0.65; }}
        50% {{ transform: scaleY(1.05); opacity: 1; }}
      }}
      @keyframes slideProg {{
        0% {{ transform: translateX(0px); }}
        100% {{ transform: translateX(298px); }}
      }}
    ]]></style>
  </defs>

  <!-- 3D Extruded Back Layer -->
  <rect x="12" y="12" width="1182" height="132" rx="18" fill="#FF00A8" fill-opacity="0.12" stroke="#FF00A8" stroke-opacity="0.35"/>
  <!-- Main Deck -->
  <rect x="6" y="6" width="1182" height="132" rx="18" fill="url(#audBg)" stroke="url(#audBorder)" stroke-width="1.8"/>

  <!-- Spinning 3D Holo-Disc -->
  <g class="disc" filter="url(#aGlow)">
    <circle cx="76" cy="75" r="42" fill="#050714" stroke="#00F0FF" stroke-width="2" stroke-dasharray="14 6"/>
    <circle cx="76" cy="75" r="28" fill="none" stroke="#FF00A8" stroke-width="1.5" stroke-dasharray="8 8"/>
    <circle cx="76" cy="75" r="10" fill="#00F0FF"/>
    <circle cx="76" cy="75" r="4" fill="#050714"/>
  </g>

  <!-- Track Metadata -->
  <text x="148" y="54" class="title" font-size="24" fill="#E8F7FF">Late Night Neural Lo-Fi</text>
  <g transform="translate(454, 34)">
    <rect width="74" height="24" rx="12" fill="#050714" stroke="#FF00A8" stroke-width="1.2"/>
    <circle cx="15" cy="12" r="4" fill="#FF00A8" filter="url(#aGlow)" class="live-dot"/>
    <text x="26" y="16" class="mono" font-size="11" font-weight="700" fill="#FF00A8">LIVE</text>
  </g>
  <text x="148" y="80" class="mono" font-size="13.5" fill="#9BB0DF">Julian's Radio · 24/7 Autonomous Coding Session</text>

  <!-- Progress Track -->
  <rect x="148" y="102" width="520" height="6" rx="3" fill="#1C284D"/>
  <rect x="148" y="102" width="320" height="6" rx="3" fill="url(#progGrad)" filter="url(#aGlow)"/>
  <circle cx="170" cy="105" r="6" fill="#FFFFFF" stroke="#00F0FF" stroke-width="2" class="progress-dot"/>
  <text x="148" y="126" class="mono" font-size="11" fill="#00F0FF">02:58 // ∞ LOOP</text>

  <!-- 16-Band Animated 3D Equalizer -->
  <g>
    {''.join(bars)}
  </g>
</svg>
"""
    write_svg("audio-hud-3d.svg", svg)


# ═══════════════════════════════════════════════════════════════════════
# 5. SIX BESPOKE 3D HOLOGRAPHIC PROJECT CARDS (STAGGERED SHEEN)
# ═══════════════════════════════════════════════════════════════════════
PROJECTS = [
    {
        "file": "card-gforms-3d.svg",
        "title": "Google-Forms-Universal-AI-Assistant",
        "category": "AI OVERLAY // AUTOMATION",
        "desc1": "Real-time AI browser overlay & auto-fill engine for Google Forms.",
        "desc2": "Parses questions live, links custom LLMs & suggests smart answers.",
        "tags": ["JavaScript", "AI Overlay", "Auto-Fill"],
        "accent": "#00F0FF",
        "secondary": "#7B2CBF",
        "delay": "0s",
    },
    {
        "file": "card-classcompanion-3d.svg",
        "title": "Meet & Teams Class Companion",
        "category": "USERSCRIPT // AI VISION",
        "desc1": "Tampermonkey copilot for online lectures & live video meetings.",
        "desc2": "Real-time audio transcription, slide AI vision & instant answers.",
        "tags": ["JavaScript", "Tampermonkey", "AI Vision"],
        "accent": "#FF00A8",
        "secondary": "#00F0FF",
        "delay": "0.8s",
    },
    {
        "file": "card-videoaudio-3d.svg",
        "title": "Video-to-Audio-Converter-Offline",
        "category": "AUDIO ENGINE // DESKTOP",
        "desc1": "Offline video to high-fidelity MP3 converter & USB optimizer.",
        "desc2": "Auto-bitrate tuning (4GB-128GB+) engineered for car stereos.",
        "tags": ["Python", "FFmpeg", "USB Storage"],
        "accent": "#A855F7",
        "secondary": "#00F0FF",
        "delay": "1.6s",
    },
    {
        "file": "card-smar-3d.svg",
        "title": "Social-Media-Autonomous-Report-V2",
        "category": "AUTONOMOUS DEFENSE // AGENTS",
        "desc1": "Autonomous desktop & web defense tool detecting malicious profiles.",
        "desc2": "Automates abusive account reporting via Playwright agent pipelines.",
        "tags": ["Python", "Playwright", "Anti-Abuse"],
        "accent": "#00F5A0",
        "secondary": "#00D9F5",
        "delay": "2.4s",
    },
    {
        "file": "card-sqlcli-3d.svg",
        "title": "sql-cli",
        "category": "MYSQL TERMINAL // OLLAMA AI",
        "desc1": "Developer-friendly Python MySQL terminal built for XAMPP.",
        "desc2": "Live schema autocomplete powered by a local Ollama SQL copilot.",
        "tags": ["Python", "MySQL", "Ollama AI"],
        "accent": "#FACC15",
        "secondary": "#FF00A8",
        "delay": "3.2s",
    },
    {
        "file": "card-stepup-3d.svg",
        "title": "StepUp-X-Google-Fit",
        "category": "FITNESS CLOUD // CADENCE",
        "desc1": "Cloud step synchronizer & natural walking cadence injector.",
        "desc2": "Gaussian human pacing with zero-lag sync for Google Fit & StepUp.",
        "tags": ["Python", "Google Fit", "Cloud Sync"],
        "accent": "#38BDF8",
        "secondary": "#FF00A8",
        "delay": "4.0s",
    },
]


def build_project_cards() -> None:
    for idx, p in enumerate(PROJECTS):
        accent = p["accent"]
        sec = p["secondary"]
        tag_svg = []
        tx = 28
        for tag in p["tags"]:
            w = max(72, len(tag) * 8.4 + 22)
            tag_svg.append(
                f'<rect x="{tx}" y="176" width="{w:.0f}" height="24" rx="6" fill="#050714" stroke="{accent}" stroke-opacity="0.55" stroke-width="1"/>'
                f'<text x="{tx + w/2:.1f}" y="192" text-anchor="middle" class="mono" font-size="11" fill="#E8F7FF">{escape(tag)}</text>'
            )
            tx += w + 10

        svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 580 230" width="100%">
  <defs>
    <linearGradient id="cBg{idx}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0E1535"/>
      <stop offset="100%" stop-color="#050714"/>
    </linearGradient>
    <linearGradient id="cBorder{idx}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{accent}"/>
      <stop offset="100%" stop-color="{sec}"/>
    </linearGradient>
    <linearGradient id="cSheen{idx}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="50%" stop-color="{accent}" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <filter id="cGlow{idx}" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="cClip{idx}">
      <rect x="6" y="6" width="560" height="210" rx="14"/>
    </clipPath>
    <style><![CDATA[
      .title {{ font-family: 'Segoe UI', system-ui, sans-serif; font-weight: 800; }}
      .mono {{ font-family: 'Fira Code', ui-monospace, monospace; }}
      .sheen {{ animation: cardSweep 5.8s ease-in-out {p["delay"]} infinite; }}
      .node-pulse {{ animation: nPulse 2.2s ease-in-out {p["delay"]} infinite; }}
      .arrow-move {{ animation: arrowNudge 2s ease-in-out infinite; }}
      @keyframes cardSweep {{
        0%, 62% {{ transform: translateX(-260px) skewX(-22deg); }}
        100% {{ transform: translateX(740px) skewX(-22deg); }}
      }}
      @keyframes nPulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
      @keyframes arrowNudge {{
        0%, 100% {{ transform: translate(0px, 0px); }}
        50% {{ transform: translate(3px, -2px); }}
      }}
    ]]></style>
  </defs>

  <!-- 3D Isometric Extruded Depth Layers -->
  <rect x="14" y="14" width="560" height="210" rx="14" fill="{sec}" fill-opacity="0.15" stroke="{sec}" stroke-opacity="0.4"/>
  <rect x="10" y="10" width="560" height="210" rx="14" fill="{accent}" fill-opacity="0.12" stroke="{accent}" stroke-opacity="0.35"/>

  <!-- Main Glassmorphic Plate -->
  <rect x="6" y="6" width="560" height="210" rx="14" fill="url(#cBg{idx})" stroke="url(#cBorder{idx})" stroke-width="1.6"/>

  <g clip-path="url(#cClip{idx})">
    <!-- Top Accent Glow Bar -->
    <rect x="28" y="6" width="120" height="3" fill="{accent}" filter="url(#cGlow{idx})"/>

    <!-- Isometric Mini-Cube Icon -->
    <g transform="translate(28, 28)" filter="url(#cGlow{idx})">
      <polygon points="16,0 32,9 16,18 0,9" fill="{accent}" fill-opacity="0.8"/>
      <polygon points="0,9 16,18 16,35 0,26" fill="{sec}" fill-opacity="0.6"/>
      <polygon points="32,9 16,18 16,35 32,26" fill="{accent}" fill-opacity="0.35"/>
    </g>

    <!-- Title & Category -->
    <text x="74" y="42" class="title" font-size="18.5" fill="#FFFFFF">{escape(p["title"])}</text>
    <circle cx="78" cy="59" r="3.2" fill="{accent}" filter="url(#cGlow{idx})" class="node-pulse"/>
    <text x="89" y="63" class="mono" font-size="10.5" font-weight="700" fill="{accent}" letter-spacing="1.4">{escape(p["category"])}</text>

    <!-- Description -->
    <text x="28" y="106" class="mono" font-size="12.5" fill="#CBD7F6">{escape(p["desc1"])}</text>
    <text x="28" y="128" class="mono" font-size="12.5" fill="#9BB0DF">{escape(p["desc2"])}</text>

    <!-- Subtle Circuit Separator -->
    <line x1="28" y1="156" x2="544" y2="156" stroke="{accent}" stroke-opacity="0.2" stroke-width="1"/>

    <!-- Tech Pills -->
    {''.join(tag_svg)}

    <!-- Animated Launch Indicator -->
    <g class="arrow-move">
      <text x="540" y="193" text-anchor="end" class="mono" font-size="12" font-weight="700" fill="{accent}">LAUNCH ↗</text>
    </g>

    <!-- Holographic Sheen Transition -->
    <rect x="0" y="0" width="180" height="230" fill="url(#cSheen{idx})" class="sheen"/>
  </g>
</svg>
"""
        write_svg(p["file"], svg)


# ═══════════════════════════════════════════════════════════════════════
# 6. 3D TELEMETRY BENTO DASHBOARD WITH ANIMATED NEON BARS
# ═══════════════════════════════════════════════════════════════════════
def build_stats_bento_svg() -> None:
    langs = [
        ("JavaScript", "42%", 265, "#00F0FF", "0.2s"),
        ("CSS", "20%", 148, "#FF00A8", "0.4s"),
        ("Python", "15%", 118, "#A855F7", "0.6s"),
        ("Local AI & Cloud APIs", "8%", 82, "#00F5A0", "0.8s"),
    ]
    lang_rows = []
    for i, (name, pct, width, color, delay) in enumerate(langs):
        y = 92 + i * 50
        lang_rows.append(
            f"""
            <text x="438" y="{y}" class="mono" font-size="13" font-weight="700" fill="#E8F7FF">{escape(name)}</text>
            <text x="774" y="{y}" text-anchor="end" class="mono" font-size="12.5" font-weight="700" fill="{color}">{pct}</text>
            <rect x="438" y="{y+10}" width="336" height="8" rx="4" fill="#172042"/>
            <rect x="438" y="{y+10}" width="{width}" height="8" rx="4" fill="{color}" filter="url(#sGlow)"
                  style="transform-origin: 438px {y+14}px; animation: growBar 1.6s cubic-bezier(0.22, 1, 0.36, 1) {delay} both;"/>
            """
        )

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 310" width="100%">
  <defs>
    <linearGradient id="sBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0E1536"/>
      <stop offset="100%" stop-color="#050714"/>
    </linearGradient>
    <linearGradient id="sBorder" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF"/>
      <stop offset="50%" stop-color="#7B2CBF"/>
      <stop offset="100%" stop-color="#FF00A8"/>
    </linearGradient>
    <filter id="sGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="3.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <style><![CDATA[
      .title {{ font-family: 'Segoe UI', system-ui, sans-serif; font-weight: 900; }}
      .mono {{ font-family: 'Fira Code', ui-monospace, monospace; }}
      .radar {{ animation: radarPing 2s ease-out infinite; transform-origin: 856px 90px; }}
      @keyframes growBar {{
        from {{ transform: scaleX(0); opacity: 0.2; }}
        to {{ transform: scaleX(1); opacity: 1; }}
      }}
      @keyframes radarPing {{
        0% {{ transform: scale(0.7); opacity: 0.9; }}
        100% {{ transform: scale(2.2); opacity: 0; }}
      }}
    ]]></style>
  </defs>

  <!-- Outer Frame -->
  <rect x="6" y="6" width="1188" height="298" rx="18" fill="#050714" stroke="url(#sBorder)" stroke-width="1.8"/>

  <!-- PANEL 1: DEVELOPER TELEMETRY -->
  <rect x="30" y="30" width="368" height="254" rx="14" fill="#00F0FF" fill-opacity="0.1"/>
  <rect x="24" y="24" width="368" height="254" rx="14" fill="url(#sBg)" stroke="#00F0FF" stroke-opacity="0.6" stroke-width="1.4"/>
  <text x="48" y="56" class="mono" font-size="12" font-weight="700" fill="#00F0FF" letter-spacing="2">DEVELOPER TELEMETRY</text>

  <text x="48" y="122" class="title" font-size="40" fill="#FFFFFF" filter="url(#sGlow)">22</text>
  <text x="48" y="144" class="mono" font-size="12" fill="#9BB0DF">Public Repositories</text>

  <text x="218" y="122" class="title" font-size="40" fill="#00F0FF" filter="url(#sGlow)">405+</text>
  <text x="218" y="144" class="mono" font-size="12" fill="#9BB0DF">Git Contributions</text>

  <text x="48" y="220" class="title" font-size="38" fill="#FF00A8" filter="url(#sGlow)">99%</text>
  <text x="48" y="242" class="mono" font-size="12" fill="#9BB0DF">Commit Consistency</text>

  <text x="218" y="220" class="title" font-size="38" fill="#A855F7" filter="url(#sGlow)">100%</text>
  <text x="218" y="242" class="mono" font-size="12" fill="#9BB0DF">Open Source Focus</text>

  <!-- PANEL 2: CORE LANGUAGE STACK -->
  <rect x="420" y="30" width="380" height="254" rx="14" fill="#7B2CBF" fill-opacity="0.12"/>
  <rect x="414" y="24" width="380" height="254" rx="14" fill="url(#sBg)" stroke="#7B2CBF" stroke-opacity="0.7" stroke-width="1.4"/>
  <text x="438" y="56" class="mono" font-size="12" font-weight="700" fill="#E8F7FF" letter-spacing="2">CORE LANGUAGE STACK</text>
  {''.join(lang_rows)}

  <!-- PANEL 3: ACTIVE HORIZON -->
  <rect x="822" y="30" width="354" height="254" rx="14" fill="#FF00A8" fill-opacity="0.12"/>
  <rect x="816" y="24" width="354" height="254" rx="14" fill="url(#sBg)" stroke="#FF00A8" stroke-opacity="0.65" stroke-width="1.4"/>
  <text x="840" y="56" class="mono" font-size="12" font-weight="700" fill="#FF00A8" letter-spacing="2">ACTIVE HORIZON</text>

  <!-- Live Radar Ping -->
  <circle cx="856" cy="90" r="6" fill="none" stroke="#00F5A0" stroke-width="1.8" class="radar"/>
  <circle cx="856" cy="90" r="4.5" fill="#00F5A0" filter="url(#sGlow)"/>
  <text x="874" y="94" class="mono" font-size="12" font-weight="700" fill="#00F5A0" letter-spacing="1.5">IN PRODUCTION</text>

  <!-- Highlighted 3D Project Box -->
  <rect x="844" y="118" width="302" height="78" rx="10" fill="#00F0FF" fill-opacity="0.1"/>
  <rect x="840" y="114" width="302" height="78" rx="10" fill="#090F29" stroke="#00F0FF" stroke-opacity="0.55"/>
  <text x="858" y="142" class="title" font-size="15.5" fill="#FFFFFF">QCU-WEEK-2-PROJECT</text>
  <text x="858" y="164" class="mono" font-size="11.5" fill="#9BB0DF">AI browser overlay &amp; real-time</text>
  <text x="858" y="180" class="mono" font-size="11.5" fill="#00F0FF">automation engine 🚀</text>

  <text x="842" y="220" class="mono" font-size="11.5" fill="#9BB0DF">Status: <tspan fill="#E8F7FF">Public Release</tspan></text>
  <text x="842" y="240" class="mono" font-size="11.5" fill="#9BB0DF">Focus: <tspan fill="#E8F7FF">Vision &amp; Overlays</tspan></text>
  <text x="842" y="260" class="mono" font-size="11.5" fill="#00F0FF" font-weight="700">Branch: main ↗</text>
</svg>
"""
    write_svg("stats-bento-3d.svg", svg)


if __name__ == "__main__":
    build_hero_svg()
    build_divider_svg()
    build_terminal_svg()
    build_audio_hud_svg()
    build_project_cards()
    build_stats_bento_svg()
    print("\nAll 11 Cyber-Sovereign 3D animated SVGs are ready in assets/.")