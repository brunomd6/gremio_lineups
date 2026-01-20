let seasonData;
const usedPlayers = new Set();

const pitch = document.getElementById("pitch");

/* =========================
   POSITION GROUPING
========================= */

const POSITION_GROUPS = {
  GK: "Goalkeepers",
  CB: "Defenders",
  LB: "Defenders",
  RB: "Defenders",
  DM: "Midfielders",
  CM: "Midfielders",
  AM: "Midfielders",
  LW: "Forwards",
  RW: "Forwards",
  CF: "Forwards"
};

document.addEventListener("DOMContentLoaded", loadSeasonData);

/* =========================
   LOAD JSON
========================= */

async function loadSeasonData() {
  try {
    const res = await fetch("../data/season_2026.json");
    seasonData = await res.json();

    renderRoster();
    renderCalendar();
  } catch (e) {
    console.error("Failed to load season JSON:", e);
  }
}

/* =========================
   CALENDAR
========================= */

function renderCalendar() {
  const list = document.getElementById("matchList");
  list.innerHTML = "";

  seasonData.matches.forEach(match => {
    const div = document.createElement("div");
    div.className = "match-item";
    div.textContent = `${match.date} – ${match.competition} vs ${match.opponent}`;
    list.appendChild(div);
  });
}

/* =========================
   ROSTER PANEL
========================= */

function renderRoster() {
  const rosterRoot = document.getElementById("rosterList");
  rosterRoot.innerHTML = "";

  const sections = {};

  seasonData.roster
    .filter(p => !usedPlayers.has(p.id))
    .forEach(player => {
      const group = POSITION_GROUPS[player.pos] || "Other";
      sections[group] ??= [];
      sections[group].push(player);
    });

  Object.entries(sections).forEach(([group, players]) => {
    const section = document.createElement("div");
    section.className = "roster-section";

    section.innerHTML = `<h3>${group}</h3>`;
    const list = document.createElement("div");
    list.className = "roster-list";

    players.forEach(player => {
      const div = document.createElement("div");
      div.className = "roster-player";
      div.draggable = true;

      div.innerHTML = `
        <div class="shirt"></div>
        <div>${player.nome}</div>
      `;

      div.addEventListener("dragstart", e => {
        e.dataTransfer.setData("playerId", player.id);
      });

      list.appendChild(div);
    });

    section.appendChild(list);
    rosterRoot.appendChild(section);
  });
}

/* =========================
   DROP ON PITCH
========================= */

pitch.addEventListener("dragover", e => e.preventDefault());

pitch.addEventListener("drop", e => {
  e.preventDefault();

  const playerId = e.dataTransfer.getData("playerId");
  if (usedPlayers.has(playerId)) return;

  const player = seasonData.roster.find(p => p.id === playerId);
  if (!player) return;

  const pt = pitch.createSVGPoint();
  pt.x = e.clientX;
  pt.y = e.clientY;
  const svgPt = pt.matrixTransform(pitch.getScreenCTM().inverse());

  createPlayerOnPitch(player, svgPt.x, svgPt.y);

  usedPlayers.add(playerId);
  renderRoster();
});

/* =========================
   PLAYERS ON PITCH
========================= */

function createPlayerOnPitch(player, x, y) {
  const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
  g.classList.add("player");
  g.dataset.playerId = player.id;

  const c = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  c.setAttribute("r", 3);

  const t = document.createElementNS("http://www.w3.org/2000/svg", "text");
  t.textContent = player.nome;

  g.appendChild(c);
  g.appendChild(t);
  pitch.appendChild(g);

  movePlayer(g, x, y);
  enableDrag(g);
}

function movePlayer(el, x, y) {
  x = Math.max(0, Math.min(100, x));
  y = Math.max(0, Math.min(150, y));

  el.children[0].setAttribute("cx", x);
  el.children[0].setAttribute("cy", y);
  el.children[1].setAttribute("x", x);
  el.children[1].setAttribute("y", y + 5);
}

function enableDrag(el) {
  let dragging = false;

  el.addEventListener("mousedown", () => dragging = true);

  pitch.addEventListener("mousemove", e => {
    if (!dragging) return;

    const pt = pitch.createSVGPoint();
    pt.x = e.clientX;
    pt.y = e.clientY;
    const svgPt = pt.matrixTransform(pitch.getScreenCTM().inverse());

    movePlayer(el, svgPt.x, svgPt.y);
  });

  window.addEventListener("mouseup", () => dragging = false);
}
