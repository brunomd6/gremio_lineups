import svgwrite
import yaml

with open("lineups/11_01_2026 - Gremio vs .yml") as f:
    jogo = yaml.safe_load(f)

dwg = svgwrite.Drawing("formacao.svg", size=("800px", "1200px"))

# campo
dwg.add(dwg.rect(insert=(0,0), size=("800px","1200px"),
                 fill="#1f7a1f"))

for j in jogo["jogadores"]:
    x = j["x"] * 8
    y = 1200 - j["y"] * 12
    dwg.add(dwg.circle(center=(x, y), r=18, fill="white"))
    dwg.add(dwg.text(j["nome"], insert=(x, y+35),
                     text_anchor="middle"))

dwg.save()
