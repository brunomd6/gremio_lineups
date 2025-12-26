const players = [
  { nome: "Marchesín", x: 50, y: 10 },
  { nome: "Geromel", x: 60, y: 30 },
  { nome: "Kannemann", x: 40, y: 30 },
  { nome: "Villasanti", x: 50, y: 55 },
  { nome: "Cristaldo", x: 50, y: 80 }
];

const svg = document.getElementById("pitch");

players.forEach(p => {
  const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
  g.classList.add("player");

  const c = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  c.setAttribute("cx", p.x);
  c.setAttribute("cy", p.y);
  c.setAttribute("r", 3);
  c.setAttribute("fill", "white");

  const t = document.createElementNS("http://www.w3.org/2000/svg", "text");
  t.setAttribute("x", p.x);
  t.setAttribute("y", p.y + 5);
  t.setAttribute("font-size", "3");
  t.setAttribute("text-anchor", "middle");
  t.textContent = p.nome;

  g.appendChild(c);
  g.appendChild(t);
  svg.appendChild(g);

  enableDrag(g, p);
});

function enableDrag(el, player) {
  let dragging = false;

  el.addEventListener("mousedown", e => dragging = true);
  svg.addEventListener("mousemove", e => {
    if (!dragging) return;

    const pt = svg.createSVGPoint();
    pt.x = e.clientX;
    pt.y = e.clientY;
    const svgPt = pt.matrixTransform(svg.getScreenCTM().inverse());

    player.x = Math.max(0, Math.min(100, svgPt.x));
    player.y = Math.max(0, Math.min(150, svgPt.y));

    el.children[0].setAttribute("cx", player.x);
    el.children[0].setAttribute("cy", player.y);
    el.children[1].setAttribute("x", player.x);
    el.children[1].setAttribute("y", player.y + 5);
  });

  window.addEventListener("mouseup", () => dragging = false);
}

function exportYAML() {
  let yaml = "jogadores:\n";
  players.forEach(p => {
    yaml += `  - nome: ${p.nome}\n`;
    yaml += `    x: ${p.x.toFixed(1)}\n`;
    yaml += `    y: ${p.y.toFixed(1)}\n`;
  });

  document.getElementById("output").value = yaml;
}
