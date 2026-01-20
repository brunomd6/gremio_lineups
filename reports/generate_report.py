import json
import subprocess
from pathlib import Path

# =========================
# PATHS
# =========================

ROOT = Path(__file__).resolve().parent           # /app/reports
DATA_FILE = ROOT / "../data/season_2026.json"
OUTPUT_DIR = ROOT
TEX_FILE = OUTPUT_DIR / "lineup_report.tex"

# =========================
# LOAD JSON
# =========================

with open(DATA_FILE, "r", encoding="utf-8") as f:
    season = json.load(f)

roster = {p["id"]: p for p in season["roster"]}

# Choose match (for now: first one)
match = season["matches"][0]

# =========================
# LATEX HELPERS
# =========================

def latex_escape(text: str) -> str:
    return (
        text.replace("&", r"\&")
            .replace("%", r"\%")
            .replace("_", r"\_")
    )

# =========================
# BUILD LATEX
# =========================

lines = []

lines.append(r"\documentclass[11pt]{article}")
lines.append(r"\usepackage[margin=1.5cm]{geometry}")
lines.append(r"\usepackage{tikz}")
lines.append(r"\usepackage{graphicx}")
lines.append(r"\graphicspath{{../assets/}}")
lines.append(r"\usepackage{fontspec}")
lines.append(r"\setmainfont{Latin Modern Roman}")
lines.append(r"\pagestyle{empty}")

# 🔑 Assets live in ../assets relative to /app/reports
lines.append(r"\graphicspath{{../assets/}}")

lines.append(r"\newcommand{\teamjersey}{}")

# Player macro
lines.append(r"""
\newcommand{\player}[4]{%
  \begin{scope}[shift={(#1,#2)}]
    \node at (0,0) {\includegraphics[width=1.2cm]{\teamjersey}};
    \node[font=\small\bfseries] at (0,0.9) {#3};
    \node[font=\footnotesize] at (0,-0.9) {#4};
  \end{scope}
}
""")

lines.append(r"\begin{document}")

# =========================
# TITLE
# =========================

title = f"{match['competition']} — {match['opponent']} ({match['date']})"
subtitle = f"{match['stadium']} · Formation {match['formation']}"

lines.append(rf"\section*{{{latex_escape(title)}}}")
lines.append(rf"\textit{{{latex_escape(subtitle)}}}")
lines.append(r"\vspace{0.5cm}")

# =========================
# JERSEY
# =========================

raw_jersey = match.get("jersey", "camisa/costas1.png")

# Force jersey path to be relative to /app/reports
jersey_path = Path("../assets") / raw_jersey.lstrip("/").replace("\\", "/")

lines.append(rf"\renewcommand{{\teamjersey}}{{{jersey_path.as_posix()}}}")



# =========================
# PITCH + PLAYERS
# =========================

lines.append(r"\begin{center}")
lines.append(r"\begin{tikzpicture}[x=0.1cm,y=0.1cm]")

# NOTE: no "assets/" prefix anymore
lines.append(r"\node at (50,75) {\includegraphics[width=10cm]{pitch/pitch.png}};")

for slot in match["lineup"]:
    player = roster[slot["player"]]

    x = slot["x"]
    y = 150 - slot["y"]  # invert Y for TikZ

    name = latex_escape(player["nome"])
    number = player["numero"]

    lines.append(
        rf"\player{{{x}}}{{{y}}}{{{name}}}{{{number}}}"
    )

lines.append(r"\end{tikzpicture}")
lines.append(r"\end{center}")

lines.append(r"\end{document}")

# =========================
# WRITE FILE
# =========================

TEX_FILE.write_text("\n".join(lines), encoding="utf-8")

# =========================
# COMPILE PDF
# =========================

subprocess.run(
    ["latexmk", "-lualatex", "-interaction=nonstopmode", TEX_FILE.name],
    check=True
)

print("PDF generated successfully:", TEX_FILE.with_suffix(".pdf"))
