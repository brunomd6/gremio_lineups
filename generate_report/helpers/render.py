from pathlib import Path
from helpers.latex import latex_escape

def render_roster_grid(roster):

    lines = []

    cols = 3

    for i, player in enumerate(roster):

        lines.extend(render_player_card(player))

        if (i + 1) % cols == 0:
            lines.append(r"\vspace{0.5cm}")
            lines.append("")
        else:
            lines.append(r"\hfill")

    return lines

def render_player_card(player):

    lines = []

    player_id = player.get("id", "")

    nome = latex_escape(player.get("nome", ""))
    numero = player.get("numero")
    pos = latex_escape(player.get("pos", ""))

    image_path = Path("../assets/players") / f"{player_id}.png"

    lines.append(r"\begin{minipage}[t]{0.30\textwidth}")
    lines.append(r"\centering")

    if image_path.exists():
        lines.append(
            rf"\includegraphics[width=3cm]{{{image_path.as_posix()}}}\\"
        )

    lines.append(rf"\textbf{{{nome}}}\\")

    details = pos if numero is None else f"#{numero} --- {pos}"
    lines.append(latex_escape(details) + r"\\")

    lines.append(r"\vspace{0.2cm}")
    lines.append(r"\end{minipage}")

    return lines

def render_latex_preamble():

    lines = []

    lines.append(r"\documentclass[11pt]{article}")

    lines.append(r"\usepackage[margin=1.5cm]{geometry}")
    lines.append(r"\usepackage{tikz}")
    lines.append(r"\usepackage{graphicx}")
    lines.append(r"\usepackage{tabularx}")
    lines.append(r"\usepackage{fontspec}")
    lines.append(r"\usepackage{makeidx}")
    lines.append(r"\usepackage{multicol}")
    lines.append(r"\usepackage[hidelinks]{hyperref}")

    lines.append(r"\graphicspath{{../assets/}}")

    lines.append(r"\setmainfont{Latin Modern Roman}")

    lines.append(r"\pagestyle{empty}")

    lines.append(r"\makeindex")

    lines.append(
        r"\renewcommand{\indexname}{Índice de Partidas}"
    )

    lines.append(r"\newcommand{\teamjersey}{}")

    lines.extend(render_player_macro())

    return lines

def get_jersey_path(match):

    raw_jersey = match.get(
        "jersey",
        "camisa/costas1.png"
    )

    return (
        Path("../assets")
        / raw_jersey.lstrip("/").replace("\\", "/")
    )


def render_team_jersey_command(match):

    jersey_path = get_jersey_path(match)

    return [
        rf"\renewcommand{{\teamjersey}}{{{jersey_path.as_posix()}}}"
    ]

def render_match_header(match, round_name):

    lines = []

    competition = match.get("competition", "Unknown Competition")
    opponent = match.get("opponent", "Unknown Opponent")
    date = match.get("date", "Unknown Date")

    goals_for = match.get("goals_for", "?")
    goals_against = match.get("goals_against", "?")

    title = f"{date} - {competition} - {round_name}"
    subtitle = f"Grêmio {goals_for} x {goals_against} {opponent}"

    lines.append(
        rf"\section*{{{latex_escape(title)}}}"
    )

    lines.append(r"\phantomsection")

    entry = f"{date} - {round_name} - {opponent}"

    lines.append(
        rf"\index{{{latex_escape(competition)}!"
        rf"{date}@\mbox{{{latex_escape(entry)}}}}}"
    )

    lines.append(
        rf"\textbf{{{latex_escape(subtitle)}}}\\"
    )

    return lines

def render_bzz_match_info(bzz):

    if not bzz:
        return []

    lines = []

    stadium = bzz.get("venue", {}).get("name", "")

    if stadium:
        lines.append(
            rf"Estádio: {latex_escape(stadium)}\\"
        )

    lines.append(r"\begin{tabular}{lll}")

    home_goals = bzz.get("home_score")
    away_goals = bzz.get("away_score")
    if home_goals is not None and away_goals is not None:
        lines.append(
            rf"{latex_escape(home_goals)} & "
            rf"{latex_escape("Gols")} & "
            rf"{latex_escape(away_goals)} \\"
        )

    home_xg = bzz.get("actual_home_xg")
    away_xg = bzz.get("actual_away_xg")
    if home_xg is not None and away_xg is not None:
        lines.append(
            rf"{latex_escape(home_xg)} & "
            rf"{latex_escape("XG")} & "
            rf"{latex_escape(away_xg)} \\"
        )

    live_stats = bzz.get("live_stats") or {}
    home_stats = live_stats.get("home") or {}
    away_stats = live_stats.get("away") or {}

    home_passes = home_stats.get("passes")
    away_passes = away_stats.get("passes")

    if home_passes is not None and away_passes is not None:
        lines.append(
            rf"{latex_escape(home_passes)} & "
            rf"{latex_escape("Passes")} & "
            rf"{latex_escape(away_passes)} \\"
        )

    home_offsides = home_stats.get("offsides")
    away_offsides = away_stats.get("offsides")

    if home_offsides is not None and away_offsides is not None:
        lines.append(
            rf"{latex_escape(home_offsides)} & "
            rf"{latex_escape("Impedimentos")} & "
            rf"{latex_escape(away_offsides)} \\"
        )

    home_possession = home_stats.get("ball_possession")
    away_possession = away_stats.get("ball_possession")

    if home_possession is not None and away_possession is not None:
        lines.append(
            rf"{latex_escape(home_possession)} & "
            rf"{latex_escape("Posse")} & "
            rf"{latex_escape(away_possession)} \\"
        )

    home_saves = home_stats.get("goalkeeper_saves")
    away_saves = away_stats.get("goalkeeper_saves")

    if home_saves is not None and away_saves is not None:
        lines.append(
            rf"{latex_escape(home_saves)} & "
            rf"{latex_escape("Defesas")} & "
            rf"{latex_escape(away_saves)} \\"
        )

    


    lines.append(r"\end{tabular}")

    

    return lines

def render_player_macro():
    return [r"""
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
"""]

def render_players(lineup, roster):
    if not lineup:
        return []

    lines = []

    for slot in lineup:

        player = roster.get(slot["player"])

        if not player:
            continue

        x = slot["x"] / 100
        y = slot["y"] / 100

        name = latex_escape(player["nome"])
        number = player.get("numero", "")

        lines.append(
            rf"\player{{{x}}}{{{y}}}{{{name}}}{{{number}}}"
        )

    return lines

def render_officials_table(officials):
    if not officials:
        return []

    lines = []

    lines.append(r"\vspace{0.5cm}")
    lines.append(r"\begin{center}")
    lines.append(r"\begin{tabular}{ll}")

    label_map = {
        "referee": "Árbitro",
        "assistant1": "Assistente 1",
        "assistant2": "Assistente 2",
        "assistant3": "Quarto Árbitro",
        "quarto": "Quarto Árbitro",
        "assistant4": "Quinto Árbitro",
        "inspetor": "Inspetor",
        "assessor": "Assessor",
        "var": "VAR",
        "avar": "AVAR",
        "avar2": "AVAR 2",
        "var_observer": "Observador VAR",
        "pitch_observer": "Observador de Campo",
        "quality_observer": "Quality Observer"
    }

    for key, label in label_map.items():
        value = officials.get(key)

        if value:
            lines.append(
                rf"\textbf{{{latex_escape(label)}:}} & "
                rf"{latex_escape(value)} \\"
            )

    lines.append(r"\end{tabular}")
    lines.append(r"\end{center}")

    return lines

def render_bench_table(bench_ids, roster):
    if not bench_ids:
        return []

    lines = []

    lines.append(r"\textbf{Bench}")
    lines.append(r"\vspace{0.2cm}")
    lines.append(r"\begin{tabular}{c l}")
    lines.append(r"\renewcommand{\arraystretch}{1.3}")

    for pid in bench_ids:
        player = roster.get(pid)

        if not player:
            continue

        name = latex_escape(player["nome"])
        number = player["numero"] if player["numero"] else ""

        lines.append(
            r"\includegraphics[width=0.8cm]{\teamjersey} & "
            + f"{number} {name} \\\\"
        )

    lines.append(r"\end{tabular}")

    return lines