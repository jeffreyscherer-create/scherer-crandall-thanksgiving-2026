// Shared helpers used by every page's inline script.

async function getState() {
  const res = await fetch("/api/state", { credentials: "same-origin" });
  if (!res.ok) throw new Error("state fetch failed");
  return res.json();
}

function pollState(onState, intervalMs) {
  intervalMs = intervalMs || 6000;
  let stopped = false;
  async function tick() {
    if (stopped) return;
    try {
      const state = await getState();
      onState(state);
    } catch (e) {
      console.error(e);
    }
    if (!stopped) setTimeout(tick, intervalMs);
  }
  tick();
  return () => { stopped = true; };
}

function teamLabel(team) {
  return team === "team1" ? "Team 1: The Idiots" : team === "team2" ? "Team 2: The Wise" : team;
}

function teamPillHtml(team) {
  return `<span class="pill ${team}">${teamLabel(team)}</span>`;
}

function flagPillHtml(flag) {
  if (!flag) return "";
  const map = {
    showdown: ["SHOWDOWN", "flag-showdown"],
    "21+": ["21+", "flag-21"],
    italiano: ["ITALIANO", "flag-italiano"],
  };
  const entry = map[flag];
  if (!entry) return "";
  return `<span class="pill ${entry[1]}">${entry[0]}</span>`;
}

function startCountdown(targetIso, el, onZero) {
  const target = new Date(targetIso).getTime();
  function render() {
    const now = Date.now();
    let diff = Math.max(0, target - now);
    const totalSeconds = Math.floor(diff / 1000);
    const days = Math.floor(totalSeconds / 86400);
    const hours = Math.floor((totalSeconds % 86400) / 3600);
    const mins = Math.floor((totalSeconds % 3600) / 60);
    const secs = totalSeconds % 60;
    el.innerHTML = `
      <div class="unit"><span class="num">${days}</span><span class="label">days</span></div>
      <div class="unit"><span class="num">${hours}</span><span class="label">hrs</span></div>
      <div class="unit"><span class="num">${mins}</span><span class="label">min</span></div>
      <div class="unit"><span class="num">${secs}</span><span class="label">sec</span></div>
    `;
    if (diff <= 0 && onZero) onZero();
  }
  render();
  const id = setInterval(render, 1000);
  return () => clearInterval(id);
}

async function postForm(url, fields) {
  const fd = new FormData();
  Object.entries(fields).forEach(([k, v]) => {
    if (v !== undefined && v !== null) fd.append(k, v);
  });
  const res = await fetch(url, { method: "POST", body: fd, credentials: "same-origin" });
  return res;
}

async function adminCheck() {
  const res = await fetch("/api/admin/check", { credentials: "same-origin" });
  const j = await res.json();
  return j.logged_in;
}

async function adminLogin(password) {
  const res = await postForm("/api/admin/login", { password });
  return res.ok;
}

async function adminLogout() {
  await fetch("/api/admin/logout", { method: "POST", credentials: "same-origin" });
}

function setActiveTab() {
  const path = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll("nav.tabs a").forEach((a) => {
    const href = a.getAttribute("href");
    if (href === path || (path === "" && href === "index.html")) {
      a.classList.add("active");
    }
  });
}

document.addEventListener("DOMContentLoaded", setActiveTab);
