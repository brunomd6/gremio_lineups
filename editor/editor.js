/* =========================================================
   Globals
   ========================================================= */

let seasonData = null;
let currentLineup = [];
const svg = document.getElementById("pitch");

/* =========================================================
   DOM Ready
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  console.log("Editor loaded");
  console.log("Roster element:", document.getElementById("rosterList"));

  loadSeasonData();
});

/* =========================================================
   Load JSON
   ========================================================= */

async function loadSeasonData() {
  try {
    const response = await fetch("../data/season_2026.json");
    seasonData = await response.json();

    console.log("Season data loaded:", seasonData);

    renderRoster(seasonData.roster);
  } catch (err) {
    console.error("Failed to load season JSON:", err);
  }
}

/* =========================================================
   Roster (available players)
   ========================================================= */

function renderRoster(roster) {
  const rosterEl = document.getElementById("rosterList");
  rosterEl.innerHTML = "";

  roster.forEach(player => {
    const div = document.createElement("div");
    div.className = "roster-player";
    div.textContent = `${player.numero} — ${player.nome}`;
    div.dataset.playerId = player.id;

    div.addEventListener("click", () => {
      addPlayerToPitch(player);
    });

    rosterEl.appendChild(div);
  });
}

/* =========================================================
   Pitch / Players
   ========================================================= */

function addPlayerToPitch(player) {
  const instance = {
    id: player.id,
    nome: player.nome,
    x: 50,
    y: 75
  };

  currentLineup.push(instance);
  drawPlayer(instance);
}

function drawPlayer(player) {
  const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
  g.classList.add("player");

  const c = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  c.setAttribute("r", 3);
  c.setAttribute("fill", "white");

  const t = document.createElementNS("http://www.w3.org/2000/svg", "text");
  t.setAttribute("font-size", "3");
  t.setAttribute("text-anchor", "middle");
  t.setAttribute("fill", "white");
  t.textContent = player.nome;

  g.appendChild(c);
  g.appendChild(t);
  svg.appendChild(g);

  updatePlayerPosition(g, player);
  enableDrag(g, player);
}

function updatePlayerPosition(el, player) {
  el.children[0].setAttribute("cx", player.x);
  el.children[0].setAttribute("cy", player.y);
  el.children[1].setAttribute("x", player.x);
  el.children[1].setAttribute("y", player.y + 5);
}

/* =========================================================
   Dragging
   ========================================================= */

function enableDrag(el, player) {
  let dragging = false;

  el.addEventListener("mousedown", e => {
    dragging = true;
    e.stopPropagation();
  });

  svg.addEventListener("mousemove", e => {
    if (!dragging) return;

    const pt = svg.createSVGPoint();
    pt.x = e.clientX;
    pt.y = e.clientY;

    const svgPt = pt.matrixTransform(svg.getScreenCTM().inverse());

    player.x = Math.max(0, Math.min(100, svgPt.x));
    player.y = Math.max(0, Math.min(150, svgPt.y));

    updatePlayerPosition(el, player);
  });

  window.addEventListener("mouseup", () => {
    dragging = false;
  });
}

/* =========================================================
   Export lineup as JSON (optional)
   ========================================================= */

function exportLineup() {
  const data = currentLineup.map(p => ({
    player: p.id,
    x: Number(p.x.toFixed(1)),
    y: Number(p.y.toFixed(1))
  }));

  document.getElementById("output").value =
    JSON.stringify(data, null, 2);
}
