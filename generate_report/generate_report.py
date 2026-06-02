import json
import subprocess
from pathlib import Path

from helpers.bzz import (
    find_bzz_match,
)

from helpers.matches import (
    get_round_name,
)

from helpers.render import (
    render_team_jersey_command,
    render_roster_grid,
    render_latex_preamble,
    render_match_header,
    render_officials_table, 
    render_bench_table, 
    render_players,
    render_bzz_match_info
)

# =========================
# PATHS
# =========================

ROOT = Path(__file__).resolve().parent

DATA_DIR = ROOT.parent / "data"
REPORTS_DIR = ROOT.parent / "reports"

MY_DATA_FILE = DATA_DIR / "season_2026.json"

BZZOIRO_DATA_FILE = DATA_DIR / "bzzoiro_gremio_2026_detailed.json"

TEX_FILE = REPORTS_DIR / "lineup_report.tex"

# =========================
# LOAD JSON
# =========================

with open(MY_DATA_FILE, "r", encoding="utf-8") as f:
    season = json.load(f)

roster = {p["id"]: p for p in season["roster"]}

with open(BZZOIRO_DATA_FILE, "r", encoding="utf-8") as f:
    bzz_matches = json.load(f)

# =========================
# BUILD LATEX
# =========================

lines = []

lines.extend(render_latex_preamble())

lines.append(r"\begin{document}")

lines.append(r"\printindex")
lines.append(r"\newpage")

lines.append(r"\section*{Elenco}")
lines.extend(render_roster_grid(season["roster"]))
lines.append(r"\newpage")

matches = season["matches"]

for match in matches:

    match_id = match.get("id", "")

    if not match_id:
        continue

    round_name = get_round_name(match.get("round"))
    lines.extend(render_match_header(match, round_name))

    lines.append(r"\vspace{0.5cm}")

    lines.extend(render_team_jersey_command(match))

    lines.append(r"\begin{center}")

    # INIT PITCH
    lines.append(r"\begin{minipage}{0.4\textwidth}")
    lines.append(r"\raggedright")
    lines.append(r"\begin{tikzpicture}")

    lines.append(
        r"\node[anchor=south west, inner sep=0] (pitch) at (0,0) "
        r"{\includegraphics[width=9cm]{pitch/pitch.png}};"
    )

    lines.append(
        r"\begin{scope}[x={(pitch.south east)}, y={(pitch.north west)}]"
    )

    lines.extend(render_players(match.get("lineup"), roster))
    
    lines.append(r"\end{scope}")
    # END PITCH

    # INIT BENCH
    lines.append(r"\end{tikzpicture}")
    lines.append(r"\end{minipage}")
    lines.append(r"\hfill")

    lines.append(r"\begin{minipage}{0.25\textwidth}")
    lines.append(r"\raggedright")

    bench_ids = match.get("bench", [])
    lines.extend(render_bench_table(bench_ids, roster))

    lines.append(r"\end{minipage}")
    lines.append(r"\hfill")

    lines.append(r"\begin{minipage}{0.35\textwidth}")
    lines.append(r"\raggedright")

    lines.append(r"\end{minipage}")

    #END BENCH

    lines.append(r"\end{center}")

    lines.append(r"\vspace{0.5cm}")
    lines.append(r"\begin{minipage}{0.65\textwidth}")

    officials = match.get("officials", {})
    lines.extend(render_officials_table(officials))

    lines.append(r"\end{minipage}")

    lines.append(r"\begin{minipage}{0.3\textwidth}")
    bzz = find_bzz_match(match, bzz_matches)
    lines.extend(render_bzz_match_info(bzz))
    lines.append(r"\end{minipage}")

    lines.append(r"\newpage")   # 👈 one formation per page



lines.append(r"\end{document}")

TEX_FILE.write_text("\n".join(lines), encoding="utf-8")

subprocess.run(
    [
        "latexmk",
        "-lualatex",
        "-interaction=nonstopmode",
        str(TEX_FILE),
    ],
    cwd=REPORTS_DIR,
    check=True
)

print("PDF generated successfully:", TEX_FILE.with_suffix(".pdf"))
