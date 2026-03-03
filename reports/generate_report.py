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

# Choose match
match = season["matches"]

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
lines.append(r"\usepackage{tabularx}")
lines.append(r"\usepackage{fontspec}")

lines.append(r"\graphicspath{{../assets/}}")
lines.append(r"\setmainfont{Latin Modern Roman}")
lines.append(r"\pagestyle{empty}")

lines.append(r"\newcommand{\teamjersey}{}")

# Player macro
lines.append(r"""
\newcommand{\player}[4]{%
  \begin{scope}[shift={(#1,#2)}]

    \node[anchor=center, inner sep=0] (shirt) at (0,0)
      {\includegraphics[width=1.2cm]{\teamjersey}};
      
    % Name above shirt
    \node[font=\small\bfseries, anchor=south]
      at ([yshift=-2pt]shirt.north) {#3};
      
    % Number below shirt
    \node[font=\footnotesize, anchor=north]
      at ([yshift=2pt]shirt.south) {#4};

  \end{scope}
}
""")

matches = season["matches"]

lines.append(r"\begin{document}")

for match in matches:

    competition = match.get("competition", "Unknown Competition")
    opponent = match.get("opponent", "Unknown Opponent")
    date = match.get("date", "Unknown Date")

    title = f"{competition} — {opponent} ({date})"
    subtitle = f"{match['stadium']} · Formation {match['formation']}"

    lines.append(rf"\section*{{{latex_escape(title)}}}")
    lines.append(rf"\textit{{{latex_escape(subtitle)}}}")
    lines.append(r"\vspace{0.5cm}")

    raw_jersey = match.get("jersey", "camisa/costas1.png")
    jersey_path = Path("../assets") / raw_jersey.lstrip("/").replace("\\", "/")
    lines.append(rf"\renewcommand{{\teamjersey}}{{{jersey_path.as_posix()}}}")

    lines.append(r"\begin{center}")
    lines.append(r"\begin{tikzpicture}")

    lines.append(
        r"\node[anchor=south west, inner sep=0] (pitch) at (0,0) "
        r"{\includegraphics[width=12cm]{pitch/pitch.png}};"
    )

    lines.append(
        r"\begin{scope}[x={(pitch.south east)}, y={(pitch.north west)}]"
    )

    for slot in match["lineup"]:
        player = roster[slot["player"]]

        x = slot["x"] / 100
        y = slot["y"] / 100

        name = latex_escape(player["nome"])
        number = player["numero"]

        lines.append(
            rf"\player{{{x}}}{{{y}}}{{{name}}}{{{number}}}"
        )

    lines.append(r"\end{scope}")
    lines.append(r"\end{tikzpicture}")
    lines.append(r"\end{center}")

    officials = match.get("officials", {})

    if officials:
        lines.append(r"\vspace{0.5cm}")
        lines.append(r"\begin{center}")
        lines.append(r"\begin{tabular}{ll}")

        label_map = {
            "referee": "Árbitro",
            "assistant1": "Assistente 1",
            "assistant2": "Assistente 2",
            "assistant3": "Quarto Árbitro",
            "assistant4": "Quinto Árbitro",
            "var": "VAR",
            "avar": "AVAR",
            "avar2": "AVAR 2",
            "var_observer": "Observador VAR",
            "pitch_observer": "Observador de Campo"
        }

        for key, label in label_map.items():
            value = officials.get(key)
            if value:   # Only print if present and not empty
                lines.append(
                    r"\textbf{" + label + r":} & "
                    + latex_escape(value) + r" \\"
                )

    lines.append(r"\end{tabular}")
    lines.append(r"\end{center}")

    bench_ids = match.get("bench", [])

    if bench_ids:
        lines.append(r"\vspace{0.5cm}")
        lines.append(r"\textbf{Bench:}")
        lines.append(r"\vspace{0.2cm}")
        lines.append(r"\begin{center}")
        lines.append(r"\begin{tabular}{cccccc}")

        row = []
        for i, pid in enumerate(bench_ids):
            player = roster.get(pid)
            if not player:
                continue

            name = latex_escape(player["nome"])
            number = player["numero"] if player["numero"] else ""

            row.append(f"{number} {name}")

            if len(row) == 6:
                lines.append(" & ".join(row) + r" \\")
                row = []

        if row:
            lines.append(" & ".join(row) + r" \\")

        lines.append(r"\end{tabular}")
        lines.append(r"\end{center}")

    lines.append(r"\newpage")   # 👈 one formation per page

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
