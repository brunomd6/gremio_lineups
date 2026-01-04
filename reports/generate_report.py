from pylatex import Document, NoEscape, Section, NewPage
from pylatex.utils import escape_latex
import json

with open("../data/season_2026.json", encoding="utf-8-sig") as f:
    data = json.load(f)

doc = Document()

doc.preamble.append(NoEscape(r"\usepackage{graphicx}"))
doc.preamble.append(NoEscape(r"\usepackage[percent]{overpic}"))

doc.append(NoEscape(r"\section*{Grêmio 2026 — Lineups}"))

for match in data["matches"]:
    doc.append(NoEscape(r"\subsection*{"))
    doc.append(
        f'{escape_latex(match["competition"])} — '
        f'{escape_latex(match["date"])} — '
        f'vs {escape_latex(match["opponent"])}'
    )
    doc.append(NoEscape(r"}"))

    # Pitch with overlay
    doc.append(NoEscape(r"""
\begin{center}
\begin{overpic}[width=0.8\textwidth]{../assets/pitch/pitch.png}
"""))

    for p in match["lineup"]:
        x = p["x"]
        y = p["y"]

        # Overpic uses bottom-left origin
        doc.append(
            NoEscape(
                rf"\put({x},{y}){{\circle*{{3}}}}"
            )
        )

    doc.append(NoEscape(r"""
\end{overpic}
\end{center}
"""))

    doc.append(NewPage())

doc.generate_pdf("lineup_report", clean_tex=False)
