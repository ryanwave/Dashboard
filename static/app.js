/* DocHub — engineering document workspace (vanilla JS, no build step) */
"use strict";

// ---------------------------------------------------------------- icons
const I = {
  home: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10.5L12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/></svg>',
  folder: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>',
  folderOpen: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8V6a2 2 0 0 1 2-2h4l2 2h7a2 2 0 0 1 2 2v1"/><path d="M3.5 20h14.3a2 2 0 0 0 1.9-1.4L22 11H6.2a2 2 0 0 0-1.9 1.4L2 19a1 1 0 0 0 1 1z"/></svg>',
  collapse: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 20l5-5 5 5M7 4l5 5 5-5"/></svg>',
  fit: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3M21 8V5a2 2 0 0 0-2-2h-3M3 16v3a2 2 0 0 0 2 2h3M16 21h3a2 2 0 0 0 2-2v-3"/></svg>',
  folderPlus: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M12 11v5M9.5 13.5h5"/></svg>',
  upload: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 16v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3M12 3v13M7 8l5-5 5 5"/></svg>',
  download: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 16v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3M12 3v13M7 11l5 5 5-5"/></svg>',
  save: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3h11l5 5v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/><path d="M7 3v5h8M7 21v-7h10v7"/></svg>',
  history: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5M12 7v5l3 2"/></svg>',
  undo: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 14L4 9l5-5"/><path d="M4 9h10.5a5.5 5.5 0 0 1 0 11H11"/></svg>',
  redo: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14l5-5-5-5"/><path d="M20 9H9.5a5.5 5.5 0 0 0 0 11H13"/></svg>',
  search: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>',
  minus: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M5 12h14"/></svg>',
  plus: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>',
  x: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M18 6L6 18M6 6l12 12"/></svg>',
  check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>',
  alert: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 9v4M12 17h.01"/><path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg>',
  info: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></svg>',
  edit: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/></svg>',
  restore: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></svg>',
  eye: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12z"/><circle cx="12" cy="12" r="3"/></svg>',
  file: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/></svg>',
  layers: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l10 5-10 5L2 7z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/></svg>',
  users: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/></svg>',
  git: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3.5"/><path d="M12 3v5.5M12 15.5V21"/></svg>',
  shield: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>',
  copy: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>',
  more: '<svg viewBox="0 0 24 24" fill="currentColor"><circle cx="5" cy="12" r="1.8"/><circle cx="12" cy="12" r="1.8"/><circle cx="19" cy="12" r="1.8"/></svg>',
  chevDown: '<svg viewBox="0 0 10 6"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.6" fill="none"/></svg>',
  chevRight: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg>',
  arrowLeft: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>',
  flag: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1zM4 22v-7"/></svg>',
  grid: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/></svg>',
};

// ---------------------------------------------------------------- utils
const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]));
const enc = encodeURIComponent;
const colName = (c) => { let s = ""; while (c > 0) { const m = (c - 1) % 26; s = String.fromCharCode(65 + m) + s; c = Math.floor((c - 1) / 26); } return s; };
const initials = (name) => (name || "?").split(/[\s._-]+/).filter(Boolean).slice(0, 2).map((p) => p[0].toUpperCase()).join("") || "?";
const statusClass = (s) => "st-" + String(s || "Draft").toLowerCase().replace(/\s+/g, "-");
const plural = (n, w) => `${n} ${w}${n === 1 ? "" : "s"}`;
const fmtSize = (b) => (b > 1048576 ? (b / 1048576).toFixed(1) + " MB" : Math.max(1, Math.round(b / 1024)) + " KB");

function timeAgo(iso) {
  if (!iso) return "";
  const d = new Date(iso), s = (Date.now() - d.getTime()) / 1000;
  if (s < 45) return "just now";
  if (s < 3600) return `${Math.round(s / 60)} min ago`;
  if (s < 86400) return `${Math.round(s / 3600)} h ago`;
  if (s < 172800) return "yesterday";
  if (s < 604800) return `${Math.round(s / 86400)} days ago`;
  return d.toLocaleDateString(undefined, { day: "numeric", month: "short", year: d.getFullYear() === new Date().getFullYear() ? undefined : "numeric" });
}
const fullTime = (iso) => (iso ? new Date(iso).toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" }) : "");

async function api(url, opts = {}) {
  const init = { ...opts };
  if (opts.json !== undefined) {
    init.method = init.method || "POST";
    init.headers = { "Content-Type": "application/json" };
    init.body = JSON.stringify(opts.json);
  }
  const res = await fetch(url, init);
  if (!res.ok) {
    let data = {};
    try { data = await res.json(); } catch (_) { /* not json */ }
    const err = new Error(data.error || `Request failed (${res.status})`);
    err.status = res.status;
    err.data = data;
    throw err;
  }
  return res;
}
const getJSON = async (url) => (await api(url)).json();
const postJSON = async (url, body) => (await api(url, { json: body })).json();

async function download(url, body, fallbackName) {
  const res = body ? await api(url, { json: body }) : await api(url);
  const blob = await res.blob();
  const cd = res.headers.get("Content-Disposition") || "";
  const m = /filename\*=UTF-8''([^;]+)/.exec(cd) || /filename="?([^";]+)"?/.exec(cd);
  const name = m ? decodeURIComponent(m[1]) : fallbackName;
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = name;
  document.body.appendChild(a);
  a.click();
  setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
}

let toastTimer;
function toast(msg, type = "ok") {
  const t = $("#toast");
  t.className = `toast show ${type}`;
  t.innerHTML = (type === "error" ? I.alert : I.check) + `<span>${esc(msg)}</span>`;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove("show"), type === "error" ? 6000 : 3200);
}

function modal({ title, text = "", body = "", icon = I.info, iconStyle = "", actions = [], onOpen, wide = false }) {
  return new Promise((resolve) => {
    const root = $("#modalRoot");
    const wrap = document.createElement("div");
    wrap.className = "backdrop";
    wrap.innerHTML = `<div class="modal" role="dialog" aria-modal="true" style="${wide ? "width:min(760px,calc(100vw - 32px))" : ""}">
      <div class="modal-head"><div class="mi" style="${iconStyle}">${icon}</div><div><h3>${esc(title)}</h3>${text ? `<p>${text}</p>` : ""}</div></div>
      ${body ? `<div class="modal-body">${body}</div>` : '<div style="height:18px"></div>'}
      <div class="modal-foot">${actions.map((a, i) => `<button class="btn ${a.primary ? "primary" : ""} ${a.danger ? "danger" : ""}" data-i="${i}">${a.label}</button>`).join("")}</div>
    </div>`;
    const close = (val) => { wrap.remove(); document.removeEventListener("keydown", onKey, true); resolve(val); };
    const onKey = (e) => {
      if (e.key === "Escape") { e.stopPropagation(); close(null); }
      if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { const p = actions.findIndex((a) => a.primary); if (p >= 0) wrap.querySelector(`[data-i="${p}"]`).click(); }
    };
    document.addEventListener("keydown", onKey, true);
    wrap.addEventListener("mousedown", (e) => { if (e.target === wrap) close(null); });
    wrap.querySelectorAll(".modal-foot button").forEach((b) => b.addEventListener("click", async () => {
      const a = actions[+b.dataset.i];
      if (a.handler) {
        b.disabled = true;
        try {
          const v = await a.handler(wrap);
          if (v !== false) close(v === undefined ? a.value ?? true : v);
        } catch (err) { toast(err.message, "error"); }
        b.disabled = false;
      } else close(a.value ?? (a.primary ? true : null));
    }));
    root.appendChild(wrap);
    if (onOpen) onOpen(wrap);
    const first = wrap.querySelector("input, textarea, select");
    (first || wrap.querySelector(".btn.primary") || wrap.querySelector("button"))?.focus();
  });
}

// ---------------------------------------------------------------- state
const S = {
  tree: null,
  user: localStorage.getItem("dochub:user") || "",
  sel: { model: "", milestone: "", variant: "" },
  doc: null,
  sheetIdx: 0,
  edits: {},
  undo: [],
  redo: [],
  cur: { r: 1, c: 1 },
  zoom: 1,
  zoomMode: "fit",
  drawer: false,
  history: [],
  openRev: null,
  hl: null,
  find: { q: "", hits: [], i: -1 },
  tdMap: new Map(),
  open: new Set((() => { try { return JSON.parse(localStorage.getItem("dochub:tree") || "[]"); } catch (_) { return []; } })()),
  docSort: { key: "name", dir: 1 },
};

function allDocs() {
  const out = (S.tree?.rootDocuments || []).map((d) => ({ ...d, model: "", milestone: "", variant: "" }));
  for (const m of S.tree?.models || []) {
    for (const d of m.documents || []) out.push({ ...d, model: m.name, milestone: "", variant: "" });
    for (const ms of m.milestones) {
      for (const d of ms.documents || []) out.push({ ...d, model: m.name, milestone: ms.name, variant: "" });
      for (const v of ms.variants) for (const d of v.documents) out.push({ ...d, model: m.name, milestone: ms.name, variant: v.name });
    }
  }
  return out;
}
const xlIcon = (d, lg) => `<span class="xl-icon${lg ? " lg" : ""}${d && d.supported === false ? " legacy" : ""}" title="${d ? esc(d.file) : ""}">${d && d.supported === false ? d.format.toUpperCase() : "X"}</span>`;
const docWhere = (d) => [d.model, d.milestone, d.variant, d.folder].filter(Boolean).join(" › ") || "Top folder";
function findNode(model, milestone, variant) {
  const m = S.tree?.models.find((x) => x.name === model);
  const ms = m?.milestones.find((x) => x.name === milestone);
  const v = ms?.variants.find((x) => x.name === variant);
  return { m, ms, v };
}
async function loadTree() { S.tree = await getJSON("/api/tree"); }

// ---------------------------------------------------------------- user
function paintUser() {
  $("#userAvatar").textContent = initials(S.user);
  $("#userName").textContent = S.user || "Sign in";
}
async function askUser(force = false) {
  if (S.user && !force) return;
  const name = await modal({
    title: S.user ? "Change your name" : "Welcome to DocHub",
    text: "Your name is recorded against every change you save, so the team always knows who changed what.",
    icon: I.users,
    body: `<div class="field"><label>Your name</label><input id="uName" value="${esc(S.user)}" placeholder="e.g. Rayan M." maxlength="60"></div>`,
    actions: [
      ...(S.user ? [{ label: "Cancel" }] : []),
      { label: "Continue", primary: true, handler: (w) => { const v = $("#uName", w).value.trim(); if (!v) { $("#uName", w).focus(); return false; } return v; } },
    ],
    onOpen: (w) => $("#uName", w).addEventListener("keydown", (e) => { if (e.key === "Enter") w.querySelector(".btn.primary").click(); }),
  });
  if (name) { S.user = name; localStorage.setItem("dochub:user", name); paintUser(); }
}

function folderHash(parts) { return "#/f/" + parts.filter(Boolean).map(enc).join("/"); }

// ---------------------------------------------------------------- search
function bindSearch() {
  const input = $("#search"), box = $("#searchResults");
  let active = 0, results = [];
  const paint = () => {
    const q = input.value.trim().toLowerCase();
    if (!q) { box.hidden = true; return; }
    const terms = q.split(/\s+/);
    results = allDocs().filter((d) => terms.every((t) => `${d.name} ${d.model} ${d.milestone} ${d.variant} ${d.folder || ""}`.toLowerCase().includes(t))).slice(0, 12);
    active = Math.min(active, Math.max(0, results.length - 1));
    box.innerHTML = results.length
      ? results.map((d, i) => `<div class="sr ${i === active ? "active" : ""}" data-i="${i}">${xlIcon(d)}<div><div>${esc(d.name)}</div><small>${esc(docWhere(d))}</small></div></div>`).join("")
      : `<div class="empty">No documents match “${esc(input.value)}”</div>`;
    box.hidden = false;
  };
  const go = (d) => { if (!d) return; input.value = ""; box.hidden = true; input.blur(); openDoc(d.path); };
  input.addEventListener("input", () => { active = 0; paint(); });
  input.addEventListener("focus", paint);
  input.addEventListener("blur", () => setTimeout(() => (box.hidden = true), 150));
  input.addEventListener("keydown", (e) => {
    if (e.key === "ArrowDown") { active = Math.min(active + 1, results.length - 1); paint(); e.preventDefault(); }
    if (e.key === "ArrowUp") { active = Math.max(active - 1, 0); paint(); e.preventDefault(); }
    if (e.key === "Enter") go(results[active]);
    if (e.key === "Escape") { input.value = ""; box.hidden = true; input.blur(); }
  });
  box.addEventListener("mousedown", (e) => { const el = e.target.closest(".sr"); if (el) go(results[+el.dataset.i]); });
  document.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") { e.preventDefault(); input.focus(); input.select(); }
  });
}

// ---------------------------------------------------------------- routing
function openDoc(path, rev) {
  location.hash = "#/d/" + enc(path) + (rev != null ? `?rev=${rev}` : "");
}
function parseHash() {
  const h = location.hash.slice(1) || "/";
  const [p, qs] = h.split("?");
  const parts = p.split("/").filter(Boolean);
  const params = new URLSearchParams(qs || "");
  if (parts[0] === "d") return { view: "doc", path: decodeURIComponent(parts.slice(1).join("/")), rev: params.has("rev") ? +params.get("rev") : null };
  if (parts[0] === "f") return { view: "folder", parts: parts.slice(1).map(decodeURIComponent) };
  return { view: "home" };
}

let leaving = false;
async function route() {
  const r = parseHash();
  if (S.doc && pendingCount() && !(r.view === "doc" && r.path === S.doc.path) && !leaving) {
    saveDraft();
  }
  closeFloating();
  if (r.view === "doc") {
    const d = allDocs().find((x) => x.path === r.path);
    const segs = r.path.split("/").slice(0, -1);
    S.sel = d ? { model: d.model, milestone: d.milestone, variant: d.variant }
      : { model: segs[0] || "", milestone: segs[1] || "", variant: segs[2] || "" };
    const segsAll = r.path.split("/").slice(0, -1);
    for (let i = 1; i <= segsAll.length; i++) S.open.add(segsAll.slice(0, i).join("/"));
    saveOpen();
    renderSidebar(r.path);
    await showEditor(r.path, r.rev);
  } else {
    S.doc = null;
    if (r.view === "folder") {
      const [model = "", milestone = "", variant = ""] = r.parts;
      S.sel = { model, milestone, variant };
    } else S.sel = { model: "", milestone: "", variant: "" };
    if (r.view === "folder") for (let i = 1; i <= r.parts.length; i++) S.open.add(r.parts.slice(0, i).join("/"));
    saveOpen();
    renderSidebar();
    if (r.view === "folder") renderFolder(r.parts); else await renderHome();
  }
}

// ---------------------------------------------------------------- sidebar (folder tree)
function saveOpen() { try { localStorage.setItem("dochub:tree", JSON.stringify([...S.open])); } catch (_) { /* ignore */ } }

/** Model › Milestone › Variant › (sub-folders) › documents, as generic nodes. */
function buildTree() {
  const mk = (name, parts, kind) => ({ name, parts, kind, id: parts.join("/"), folders: [], docs: [] });
  const root = mk("", [], "root");
  root.docs = S.tree?.rootDocuments || [];
  for (const m of S.tree?.models || []) {
    const nm = mk(m.name, [m.name], "model");
    nm.docs = m.documents || [];
    for (const ms of m.milestones) {
      const nms = mk(ms.name, [m.name, ms.name], "milestone");
      nms.docs = ms.documents || [];
      for (const v of ms.variants) {
        const nv = mk(v.name, [m.name, ms.name, v.name], "variant");
        for (const d of v.documents) {
          let node = nv;
          for (const part of (d.folder || "").split("/").filter(Boolean)) {
            let child = node.folders.find((f) => f.name === part);
            if (!child) { child = mk(part, [...node.parts, part], "sub"); node.folders.push(child); }
            node = child;
          }
          node.docs.push(d);
        }
        nms.folders.push(nv);
      }
      nm.folders.push(nms);
    }
    root.folders.push(nm);
  }
  const count = (n) => (n.count = n.docs.length + n.folders.reduce((a, f) => a + count(f), 0));
  count(root);
  return root;
}

const KIND_LABEL = { model: "Model", milestone: "Milestone", variant: "Variant", sub: "Folder" };

function treeHtml(node, depth, active) {
  let html = "";
  for (const f of node.folders) {
    const open = S.open.has(f.id);
    const current = active.folder === f.id;
    html += `<div class="tn">
      <div class="trow folder ${open ? "open" : ""} ${current ? "current" : ""}" style="--d:${depth}" data-id="${esc(f.id)}" data-kind="${f.kind}" title="${esc(KIND_LABEL[f.kind])}: ${esc(f.name)}">
        <span class="tw">${I.chevRight}</span>
        <span class="ti">${open ? I.folderOpen : I.folder}</span>
        <span class="nm">${esc(f.name)}</span><span class="ct">${f.count}</span>
      </div>
      ${open ? `<div class="tkids">${treeHtml(f, depth + 1, active)}${!f.folders.length && !f.docs.length ? `<div class="tempty" style="--d:${depth + 1}">Empty</div>` : ""}</div>` : ""}
    </div>`;
  }
  for (const d of node.docs) {
    html += `<div class="trow doc ${active.doc === d.path ? "current" : ""}" style="--d:${depth}" data-path="${esc(d.path)}" title="${esc(d.file)}\n${esc(d.status)} · edited ${esc(fullTime(d.editedAt))} by ${esc(d.editedBy || "—")}">
      <span class="tw"></span>${xlIcon(d)}<span class="nm">${esc(d.name)}</span>
      ${d.supported === false ? `<span class="tdot" style="background:#dc6803" title="Old format"></span>` : `<span class="tdot ${statusClass(d.status)}" title="${esc(d.status)}"></span>`}
    </div>`;
  }
  return html;
}

function renderSidebar(activePath) {
  const sb = $("#sidebar");
  const r = parseHash();
  const home = r.view === "home";
  const active = { doc: activePath || null, folder: r.view === "folder" ? r.parts.join("/") : null };
  const tree = buildTree();
  const keepScroll = $(".side-scroll", sb)?.scrollTop || 0;
  const { v } = findNode(S.sel.model, S.sel.milestone, S.sel.variant);
  const depth = [S.sel.model, S.sel.milestone, S.sel.variant].filter(Boolean).length;
  const newLabel = ["Model", "Milestone", "Variant"][depth];
  sb.innerHTML = `<div class="side-section">
      <button class="nav-item ${home ? "active" : ""}" data-href="#/">${I.home}Overview</button>
    </div>
    <div class="side-title tree-title"><span>Explorer</span>
      <button class="btn sm icon ghost" id="treeCollapse" title="Collapse all">${I.collapse}</button></div>
    <div class="side-scroll tree" role="tree">${treeHtml(tree, 0, active) || `<div class="side-empty">No folders found under ${esc(S.tree?.root || "")}.</div>`}</div>
    <div class="side-foot">
      ${v ? `<button class="btn sm primary" id="sbUpload">${I.upload}Upload Excel</button>` : ""}
      ${newLabel ? `<button class="btn sm" id="sbNew">${I.folderPlus}New ${newLabel}</button>` : ""}
    </div>
    <div class="resizer" id="sbResize" title="Drag to resize"></div>`;
  $(".side-scroll", sb).scrollTop = keepScroll;
  sb.querySelector("[data-href]").addEventListener("click", () => (location.hash = "#/"));
  $("#treeCollapse").addEventListener("click", () => { S.open.clear(); saveOpen(); renderSidebar(activePath); });
  sb.querySelectorAll(".trow.folder").forEach((el) => el.addEventListener("click", (e) => {
    const id = el.dataset.id;
    const parts = id.split("/");
    const navigable = el.dataset.kind !== "sub";
    const isCurrent = r.view === "folder" && r.parts.join("/") === id;
    if (e.target.closest(".tw") || !navigable) {
      S.open.has(id) ? S.open.delete(id) : S.open.add(id);
      saveOpen();
      renderSidebar(activePath);
      return;
    }
    if (S.open.has(id) && isCurrent) { S.open.delete(id); saveOpen(); renderSidebar(activePath); return; }
    S.open.add(id);
    saveOpen();
    if (isCurrent) renderSidebar(activePath); else location.hash = folderHash(parts);
  }));
  sb.querySelectorAll(".trow.doc").forEach((el) => el.addEventListener("click", () => openDoc(el.dataset.path)));
  sb.querySelector(".trow.current")?.scrollIntoView({ block: "nearest" });
  $("#sbUpload")?.addEventListener("click", () => uploadDialog());
  $("#sbNew")?.addEventListener("click", () => newFolderDialog());
  bindResizer();
}

function bindResizer() {
  const h = $("#sbResize");
  h.addEventListener("mousedown", (e) => {
    e.preventDefault();
    const move = (ev) => {
      const w = Math.max(220, Math.min(560, ev.clientX));
      document.documentElement.style.setProperty("--sidebar", w + "px");
    };
    const up = () => {
      document.removeEventListener("mousemove", move);
      document.removeEventListener("mouseup", up);
      try { localStorage.setItem("dochub:sidebar", getComputedStyle(document.documentElement).getPropertyValue("--sidebar").trim()); } catch (_) { /* ignore */ }
    };
    document.addEventListener("mousemove", move);
    document.addEventListener("mouseup", up);
  });
}
function countDocs(node) {
  let n = (node.documents || []).length;
  if (node.variants) n += node.variants.reduce((a, v) => a + v.documents.length, 0);
  if (node.milestones) n += node.milestones.reduce((a, ms) => a + countDocs(ms), 0);
  return n;
}

// ---------------------------------------------------------------- home
function greeting() {
  const h = new Date().getHours();
  return h < 12 ? "Good morning" : h < 17 ? "Good afternoon" : "Good evening";
}
async function renderHome() {
  const main = $("#main");
  main.innerHTML = `<div class="loading"><div class="spinner"></div>Loading overview…</div>`;
  const st = await getJSON("/api/stats");
  const approved = (st.byStatus.Approved || 0) + (st.byStatus.Released || 0);
  const pct = st.documents ? Math.round((approved / st.documents) * 100) : 0;
  const top = st.topContributors[0];
  main.innerHTML = `<div class="page">
    <section class="hero">
      <div>
        <h1>${greeting()}${S.user ? ", " + esc(S.user.split(" ")[0]) : ""}</h1>
        <p>Every engineering sheet in one place. Open a <b>Model → Milestone → Variant</b> in the explorer on the left, click a document to edit it like Excel, and DocHub records every change automatically.</p>
        <div class="path-chip">${I.folder.replace("<svg", '<svg width="14" height="14"')} ${esc(st.root)}</div>
      </div>
      <button class="btn" id="heroBrowse">${I.search}Find a document</button>
    </section>

    <div class="kpis">
      ${kpi("Documents", st.documents, `across ${plural(st.models, "model")} · ${plural(st.variants, "variant")}`, I.file, "#eff4ff", "#155eef")}
      ${kpi("Revisions tracked", st.revisions, `${st.cellsChanged.toLocaleString()} cell changes logged`, I.history, "#f4f3ff", "#7a5af8")}
      ${kpi("Contributors", st.contributors, top ? `Most active: ${esc(top[0])}` : "No edits yet", I.users, "#fdf2fa", "#dd2590")}
      ${kpi("Approved / Released", pct + "%", `${approved} of ${st.documents} documents`, I.shield, "#ecfdf3", "#12b76a")}
    </div>

    <div class="grid-2">
      <div class="card"><div class="card-head"><h3>Editing activity</h3><span>Last 14 days</span></div>
        <div class="card-body">${barChart(st.daily)}</div></div>
      <div class="card"><div class="card-head"><h3>Document status</h3><span>${plural(st.documents, "document")}</span></div>
        <div class="card-body">${statusBars(st.byStatus, st.documents)}
          ${st.topContributors.length ? `<div class="contrib">${st.topContributors.map(([n, c]) => `<div class="contrib-row"><span class="avatar sm">${esc(initials(n))}</span><span>${esc(n)}</span><span>${plural(c, "action")}</span></div>`).join("")}</div>` : ""}
        </div></div>
    </div>

    <div class="grid-2b">
      <div class="card"><div class="card-head"><h3>Recent activity</h3><span>Audit trail</span></div>
        <div class="card-body">${feed(st.activity.slice(0, 9))}</div></div>
      <div class="card"><div class="card-head"><h3>Recently updated documents</h3><span></span></div>
        <div class="card-body"><ul class="feed">${st.recentDocs.map((d) => `<li>
          ${xlIcon(d)}
          <div class="ft"><a href="#/d/${enc(d.path)}">${esc(d.name)}</a><small>${esc(d.path.split("/").slice(0, -1).join(" › "))}</small></div>
          <span class="when"><span class="pill ${statusClass(d.status)}">${esc(d.status)}</span></span></li>`).join("") || "<li>No documents yet.</li>"}</ul></div></div>
    </div>
  </div>`;
  $("#heroBrowse").addEventListener("click", () => $("#search").focus());
}
function kpi(label, value, sub, icon, bg, fg) {
  return `<div class="card kpi"><div class="label">${label}</div><div class="ico" style="background:${bg};color:${fg}">${icon}</div>
    <div class="value">${typeof value === "number" ? value.toLocaleString() : value}</div><div class="sub">${sub}</div></div>`;
}
function barChart(daily) {
  const W = 640, H = 190, pad = { l: 28, r: 6, t: 10, b: 24 };
  const max = Math.max(4, ...daily.map((d) => d.count));
  const step = Math.ceil(max / 4);
  const top = step * 4;
  const bw = (W - pad.l - pad.r) / daily.length;
  let g = "";
  for (let i = 0; i <= 4; i++) {
    const y = pad.t + (H - pad.t - pad.b) * (1 - i / 4);
    g += `<line class="gl" x1="${pad.l}" x2="${W - pad.r}" y1="${y}" y2="${y}"/><text class="axis" x="${pad.l - 8}" y="${y + 3.5}" text-anchor="end">${step * i}</text>`;
  }
  daily.forEach((d, i) => {
    const h = ((H - pad.t - pad.b) * d.count) / top;
    const x = pad.l + i * bw + bw * 0.18;
    const y = H - pad.b - h;
    const date = new Date(d.date + "T00:00:00");
    g += `<rect class="bar" x="${x}" y="${y}" width="${bw * 0.64}" height="${Math.max(h, d.count ? 2 : 0)}" rx="4"><title>${date.toLocaleDateString(undefined, { weekday: "short", day: "numeric", month: "short" })}: ${plural(d.count, "action")}</title></rect>`;
    if (i % 2 === daily.length % 2 || i === daily.length - 1)
      g += `<text class="axis" x="${x + bw * 0.32}" y="${H - 7}" text-anchor="middle">${i === daily.length - 1 ? "Today" : date.toLocaleDateString(undefined, { day: "numeric", month: "short" })}</text>`;
  });
  return `<svg class="chart" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none">${g}</svg>`;
}
function statusBars(by, total) {
  const colors = { Draft: "#98a2b3", "In Review": "#f79009", Approved: "#12b76a", Released: "#155eef" };
  return `<div class="status-bars">${Object.keys(colors).map((k) => {
    const n = by[k] || 0;
    return `<div class="sb-row"><span>${k}</span><div class="sb-track"><div class="sb-fill" style="width:${total ? (n / total) * 100 : 0}%;background:${colors[k]}"></div></div><b>${n}</b></div>`;
  }).join("")}</div>`;
}
const ACT = {
  edit: { icon: I.edit, bg: "#eff4ff", fg: "#155eef", verb: (a) => `saved <b>Rev ${a.rev}</b> of` },
  restore: { icon: I.restore, bg: "#f4f3ff", fg: "#7a5af8", verb: (a) => `restored an older version of` },
  external: { icon: I.alert, bg: "#fffaeb", fg: "#f79009", verb: () => `detected an edit made outside DocHub in` },
  status: { icon: I.flag, bg: "#ecfdf3", fg: "#12b76a", verb: (a) => `changed status (${esc(a.note)}) of` },
  upload: { icon: I.upload, bg: "#f0f9ff", fg: "#0086c9", verb: () => `uploaded` },
  folder: { icon: I.folderPlus, bg: "#f2f4f7", fg: "#475467", verb: () => `created folder` },
};
function feed(items) {
  if (!items.length) return `<div class="empty-state" style="padding:30px">No activity yet — changes will appear here as soon as someone saves.</div>`;
  return `<ul class="feed">${items.map((a) => {
    const t = ACT[a.action] || ACT.edit;
    const name = a.path.split("/").pop().replace(/\.xls[xm]$/i, "");
    const target = a.action === "folder" ? `<b>${esc(a.path)}</b>` : `<a href="#/d/${enc(a.path)}">${esc(name)}</a>`;
    const extra = a.action === "edit" || a.action === "external" || a.action === "restore"
      ? `<small>${plural(a.count || 0, "cell")} changed${a.note && a.action === "edit" ? ` · <span class="note">“${esc(a.note)}”</span>` : ""}</small>` : "";
    return `<li><span class="fi" style="background:${t.bg};color:${t.fg}">${t.icon}</span>
      <div class="ft"><b>${esc(a.user)}</b> ${t.verb(a)} ${target}${extra}</div><span class="when" title="${esc(fullTime(a.time))}">${timeAgo(a.time)}</span></li>`;
  }).join("")}</ul>`;
}

// ---------------------------------------------------------------- folders
function renderFolder(parts) {
  const main = $("#main");
  const { m, ms, v } = findNode(...parts);
  if (!m || (parts[1] && !ms) || (parts[2] && !v)) {
    main.innerHTML = `<div class="page"><div class="empty-state"><div class="big">${I.folder}</div><h3>Folder not found</h3><p>It may have been renamed or moved on the server.</p><a class="btn" href="#/">Back to overview</a></div></div>`;
    return;
  }
  const crumbs = [`<a href="#/">Home</a>`];
  parts.forEach((p, i) => crumbs.push(`<span class="sep">/</span>`, i === parts.length - 1 ? `<span>${esc(p)}</span>` : `<a href="${folderHash(parts.slice(0, i + 1))}">${esc(p)}</a>`));
  const head = (title, sub, actions) => `<div class="page-head"><div><div class="crumbs">${crumbs.join("")}</div><h1>${esc(title)}</h1><p>${sub}</p></div><div style="display:flex;gap:8px">${actions}</div></div>`;

  if (v) {
    main.innerHTML = `<div class="page">${head(v.name, `${plural(v.documents.length, "document")} in ${esc(m.name)} › ${esc(ms.name)}`,
      `<button class="btn" id="fNew">${I.folderPlus}New variant</button><button class="btn primary" id="fUpload">${I.upload}Upload Excel</button>`)}
      ${v.documents.length ? `<div id="docTable"></div>`
        : `<div class="card empty-state"><div class="big">${I.upload}</div><h3>No documents yet</h3><p>Upload an Excel workbook, or copy one from another variant.</p><button class="btn primary" id="fUpload2">${I.upload}Upload Excel</button></div>`}
    </div>`;
    $("#fUpload").addEventListener("click", () => uploadDialog());
    $("#fUpload2")?.addEventListener("click", () => uploadDialog());
    $("#fNew").addEventListener("click", () => newFolderDialog(2));
    if (v.documents.length) renderDocTable($("#docTable"), v.documents);
    return;
  }
  const children = ms ? ms.variants : m.milestones;
  const childLabel = ms ? "Variant" : "Milestone";
  main.innerHTML = `<div class="page">${head(ms ? ms.name : m.name,
    ms ? `${plural(children.length, "variant")} · ${plural(countDocs(ms), "document")}` : `${plural(children.length, "milestone")} · ${plural(countDocs(m), "document")}`,
    `<button class="btn primary" id="fNew">${I.folderPlus}New ${childLabel.toLowerCase()}</button>`)}
    <div class="doc-grid">${children.map((c) => {
      const docs = c.documents || c.variants.flatMap((x) => x.documents);
      const sub = c.variants ? `${plural(c.variants.length, "variant")} · ${plural(docs.length, "document")}` : plural(docs.length, "document");
      const chips = c.variants ? c.variants.map((x) => `<span class="pill rev">${esc(x.name)}</span>`).join("") :
        docs.slice(0, 3).map((d) => `<span class="pill ${statusClass(d.status)}">${esc(d.name.length > 26 ? d.name.slice(0, 24) + "…" : d.name)}</span>`).join("");
      const last = docs.slice().sort((a, b) => (b.modified > a.modified ? 1 : -1))[0];
      return `<div class="card doc-card" data-href="${folderHash([...parts, c.name])}">
        <div class="top"><span class="xl-icon lg" style="background:#eff4ff;color:#155eef">${I.folder.replace("<svg", '<svg width="22" height="22"')}</span>
        <div><h4>${esc(c.name)}</h4><div class="path">${childLabel} · ${sub}</div></div></div>
        <div class="meta">${chips || '<span style="color:var(--faint)">Empty</span>'}</div>
        <div class="foot"><span>${last ? "Updated " + timeAgo(last.modified) : "No documents yet"}</span>${I.chevRight.replace("<svg", '<svg width="16" height="16"')}</div></div>`;
    }).join("") || `<div class="card empty-state" style="grid-column:1/-1"><div class="big">${I.folder}</div><h3>No ${childLabel.toLowerCase()}s yet</h3><p>Create one to start organising documents.</p></div>`}</div>
    ${(ms || m).documents?.length ? `<h3 style="margin:28px 0 12px;font-size:16px">Documents in this folder</h3><div id="docTable"></div>` : ""}</div>`;
  $("#fNew").addEventListener("click", () => newFolderDialog());
  if ((ms || m).documents?.length) renderDocTable($("#docTable"), (ms || m).documents);
  $$(".doc-card[data-href]", main).forEach((el) => el.addEventListener("click", () => (location.hash = el.dataset.href)));
}
const SORTERS = {
  name: (d) => (d.folder ? d.folder + "/" : "") + d.name.toLowerCase(),
  edited: (d) => d.editedAt || "",
  by: (d) => (d.editedBy || "").toLowerCase(),
  status: (d) => ["Draft", "In Review", "Approved", "Released"].indexOf(d.status),
  rev: (d) => d.rev,
};
function fmtDate(iso) {
  if (!iso) return "—";
  const d = new Date(iso);
  return d.toLocaleDateString(undefined, { day: "2-digit", month: "short", year: "numeric" }) + ", " +
    d.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
}
/** Documents as wide rows: full name · last edited · edited by · sign-off status. */
function renderDocTable(el, docs) {
  const { key, dir } = S.docSort;
  const sorted = docs.slice().sort((a, b) => {
    const x = SORTERS[key](a), y = SORTERS[key](b);
    return (x < y ? -1 : x > y ? 1 : 0) * dir;
  });
  const th = (k, label) => `<button class="dt-h ${key === k ? "on" : ""}" data-sort="${k}">${label}${key === k ? `<span class="arr">${dir > 0 ? "▲" : "▼"}</span>` : ""}</button>`;
  el.innerHTML = `<div class="doc-table card" role="table">
    <div class="dt-head" role="row">${th("name", "Document name")}${th("edited", "Last edited")}${th("by", "Edited by")}${th("status", "Sign-off status")}${th("rev", "Rev")}<span></span></div>
    ${sorted.map((d) => `<div class="dt-row" role="row" tabindex="0" data-path="${esc(d.path)}" title="Open ${esc(d.file)}">
      <div class="dt-name">${xlIcon(d, true)}<div><div class="fn">${esc(d.name)}<span class="ext">.${esc(d.format)}</span></div>
        <small>${d.folder ? `${I.folder.replace("<svg", '<svg width="12" height="12"')} ${esc(d.folder)} · ` : ""}${fmtSize(d.size)}${d.supported === false ? " · old format — click to convert" : ""}</small></div></div>
      <div class="dt-date"><div>${fmtDate(d.editedAt)}</div><small>${timeAgo(d.editedAt)}</small></div>
      <div class="dt-by">${d.editedBy && d.editedBy !== "—" ? `<span class="avatar sm">${esc(initials(d.editedBy))}</span><span>${esc(d.editedBy)}</span>` : '<span class="muted">—</span>'}</div>
      <div class="dt-status">${d.supported === false ? `<span class="pill st-in-review nodot">.${esc(d.format)}</span>` : `<span class="pill ${statusClass(d.status)}">${esc(d.status)}</span>`}</div>
      <div class="dt-rev">${d.supported === false ? "—" : `Rev ${d.rev}`}</div>
      <div class="dt-go">${I.chevRight}</div>
    </div>`).join("")}
  </div>`;
  el.querySelectorAll(".dt-h").forEach((b) => b.addEventListener("click", () => {
    S.docSort = { key: b.dataset.sort, dir: S.docSort.key === b.dataset.sort ? -S.docSort.dir : b.dataset.sort === "edited" ? -1 : 1 };
    renderDocTable(el, docs);
  }));
  el.querySelectorAll(".dt-row").forEach((r) => {
    r.addEventListener("click", () => openDoc(r.dataset.path));
    r.addEventListener("keydown", (e) => { if (e.key === "Enter") openDoc(r.dataset.path); });
  });
}

// ---------------------------------------------------------------- dialogs
async function uploadDialog() {
  const folder = [S.sel.model, S.sel.milestone, S.sel.variant].join("/");
  let files = [];
  const ok = await modal({
    title: "Upload Excel documents",
    text: `Files are added to <b>${esc(folder.replace(/\//g, " › "))}</b> and tracked from their first version.`,
    icon: I.upload,
    body: `<label class="dropzone" id="dz"><input type="file" id="fileIn" accept=".xlsx,.xlsm" multiple hidden>
      <div style="margin-bottom:6px">${I.upload.replace("<svg", '<svg width="28" height="28" style="color:var(--primary)"')}</div>
      <div><b>Click to choose</b> or drag &amp; drop .xlsx files here</div><div id="dzList" style="margin-top:10px;color:var(--ink)"></div></label>`,
    actions: [{ label: "Cancel" }, {
      label: "Upload", primary: true, handler: async () => {
        if (!files.length) { toast("Choose at least one file", "error"); return false; }
        let last;
        for (const f of files) {
          const fd = new FormData();
          fd.append("file", f); fd.append("folder", folder); fd.append("user", S.user);
          last = await (await api("/api/upload", { method: "POST", body: fd })).json();
        }
        return last.path;
      },
    }],
    onOpen: (w) => {
      const dz = $("#dz", w), inp = $("#fileIn", w);
      const show = () => ($("#dzList", w).innerHTML = files.map((f) => `<div>📄 ${esc(f.name)}</div>`).join(""));
      inp.addEventListener("change", () => { files = Array.from(inp.files); show(); });
      dz.addEventListener("dragover", (e) => { e.preventDefault(); dz.classList.add("over"); });
      dz.addEventListener("dragleave", () => dz.classList.remove("over"));
      dz.addEventListener("drop", (e) => { e.preventDefault(); dz.classList.remove("over"); files = Array.from(e.dataTransfer.files).filter((f) => /\.xls[xm]$/i.test(f.name)); show(); });
    },
  });
  if (ok) { await loadTree(); toast("Upload complete"); openDoc(ok); }
}
async function newFolderDialog(depthOverride) {
  const parts = [S.sel.model, S.sel.milestone, S.sel.variant].filter(Boolean);
  const depth = depthOverride ?? parts.length;
  const parent = parts.slice(0, depth);
  const label = ["Model", "Milestone", "Variant"][depth];
  if (!label) return;
  const where = parent.length ? ` inside <b>${esc(parent.join(" › "))}</b>` : "";
  const created = await modal({
    title: `New ${label.toLowerCase()}`,
    text: `Creates a folder on the server${where}.`,
    icon: I.folderPlus,
    body: `<div class="field"><label>${label} name</label><input id="fName" placeholder="${["e.g. P301", "e.g. M2 - Design Signoff", "e.g. DC_NFB_4WD_1.25T"][depth]}"></div>`,
    actions: [{ label: "Cancel" }, {
      label: "Create", primary: true, handler: async (w) => {
        const name = $("#fName", w).value.trim();
        if (!name) return false;
        await postJSON("/api/folder", { parent: parent.join("/"), name, user: S.user });
        return [...parent, name];
      },
    }],
    onOpen: (w) => $("#fName", w).addEventListener("keydown", (e) => { if (e.key === "Enter") w.querySelector(".btn.primary").click(); }),
  });
  if (created) { await loadTree(); toast(`${label} created`); location.hash = folderHash(created); }
}
async function copyDialog() {
  const d = S.doc;
  const models = S.tree.models;
  const ok = await modal({
    title: "Copy to another variant",
    text: "Creates a new, independently tracked document from the current saved version — ideal for starting a new variant from an existing sheet.",
    icon: I.copy,
    body: `<div class="field"><label>Model</label><select id="cM">${models.map((m) => `<option>${esc(m.name)}</option>`).join("")}</select></div>
      <div class="field"><label>Milestone</label><select id="cMs"></select></div>
      <div class="field"><label>Variant</label><select id="cV"></select></div>
      <div class="field"><label>New document name</label><input id="cN" value="${esc(d.name)}"></div>`,
    actions: [{ label: "Cancel" }, {
      label: "Copy document", primary: true, handler: async (w) => {
        const folder = [$("#cM", w).value, $("#cMs", w).value, $("#cV", w).value].join("/");
        const r = await postJSON("/api/copy", { path: d.path, folder, name: $("#cN", w).value.trim(), user: S.user });
        return r.path;
      },
    }],
    onOpen: (w) => {
      const fillMs = () => {
        const m = models.find((x) => x.name === $("#cM", w).value);
        $("#cMs", w).innerHTML = m.milestones.map((x) => `<option>${esc(x.name)}</option>`).join("");
        fillV();
      };
      const fillV = () => {
        const m = models.find((x) => x.name === $("#cM", w).value);
        const ms = m.milestones.find((x) => x.name === $("#cMs", w).value);
        $("#cV", w).innerHTML = (ms?.variants || []).map((x) => `<option>${esc(x.name)}</option>`).join("");
      };
      $("#cM", w).value = S.sel.model; fillMs();
      $("#cMs", w).value = S.sel.milestone; fillV();
      $("#cM", w).addEventListener("change", fillMs);
      $("#cMs", w).addEventListener("change", fillV);
    },
  });
  if (ok) { await loadTree(); toast("Document copied"); openDoc(ok); }
}

// ================================================================ EDITOR
const sheet = () => S.doc.sheets[S.sheetIdx];
const readOnly = () => S.doc && S.doc.viewingRev != null;
const pendingCount = () => Object.values(S.edits).reduce((a, m) => a + Object.keys(m).length, 0);
const draftKey = (p) => "dochub:draft:" + p;

function saveDraft() {
  if (!S.doc || readOnly()) return;
  try {
    if (pendingCount()) localStorage.setItem(draftKey(S.doc.path), JSON.stringify({ edits: S.edits, baseRev: S.doc.rev, time: new Date().toISOString() }));
    else localStorage.removeItem(draftKey(S.doc.path));
  } catch (_) { /* storage unavailable */ }
}

async function showEditor(path, rev) {
  const main = $("#main");
  const same = S.doc && S.doc.path === path && (S.doc.viewingRev ?? null) === (rev ?? null);
  if (!same) {
    const file = path.split("/").pop();
    main.innerHTML = `<div class="loading"><div class="spinner"></div><div>Opening <b>${esc(file)}</b>…</div><small id="openTimer" style="color:var(--faint)"></small></div>`;
    const t0 = Date.now();
    const timer = setInterval(() => {
      const el = $("#openTimer");
      if (!el) return clearInterval(timer);
      const sec = Math.round((Date.now() - t0) / 1000);
      if (sec >= 3) el.textContent = `${sec}s — large workbooks can take a little while the first time`;
    }, 1000);
    let doc;
    try {
      doc = await getJSON(`/api/document?path=${enc(path)}${rev != null ? `&rev=${rev}` : ""}`);
    } catch (err) {
      clearInterval(timer);
      if (parseHash().path !== path) return;
      renderOpenError(path, err);
      return;
    }
    clearInterval(timer);
    if (parseHash().view !== "doc" || parseHash().path !== path) return;
    const keepSheet = S.doc && S.doc.path === path ? sheet()?.name : null;
    const prevPath = S.doc?.path;
    S.doc = doc;
    if (prevPath !== path) { S.edits = {}; S.undo = []; S.redo = []; S.hl = null; S.openRev = null; S.find = { q: "", hits: [], i: -1 }; }
    const visible = doc.sheets.findIndex((s) => s.name === (keepSheet || doc.active) && s.state === "visible");
    S.sheetIdx = visible >= 0 ? visible : Math.max(0, doc.sheets.findIndex((s) => s.state === "visible"));
    if (prevPath !== path) { S.cur = { r: 1, c: 1 }; S.zoomMode = "fit"; }
  }
  renderEditor();
  if (!same && !readOnly()) offerDraft();
}

function renderOpenError(path, err) {
  const main = $("#main");
  const data = err.data || {};
  const file = path.split("/").pop();
  const legacy = data.code === "legacy";
  const titles = {
    legacy: "Old Excel format", encrypted: "This workbook is protected", locked: "The file is in use",
    corrupt: "Not a valid Excel file", unreadable: "The file could not be read", parse: "The workbook could not be read",
  };
  main.innerHTML = `<div class="page"><div class="card open-error">
    <div class="big">${legacy ? I.file : I.alert}</div>
    <h3>${esc(titles[data.code] || "Could not open this document")}</h3>
    <div class="fname">${xlIcon({ file, supported: !legacy, format: file.split(".").pop() })}<span>${esc(path.split("/").join(" › "))}</span></div>
    <p>${esc(err.message)}</p>
    ${data.hint ? `<p class="hint">${I.info}<span>${esc(data.hint)}</span></p>` : ""}
    ${data.detail ? `<details><summary>Technical details</summary><pre>${esc(data.detail.join("\n"))}</pre></details>` : ""}
    <div class="actions">
      <a class="btn" href="${folderHash([S.sel.model, S.sel.milestone, S.sel.variant])}">${I.arrowLeft}Back</a>
      <button class="btn" id="oeDownload">${I.download}Download file</button>
      <button class="btn" id="oeRetry">${I.restore}Try again</button>
      ${legacy ? `<button class="btn primary" id="oeConvert">${I.copy}Convert to .xlsx</button>` : ""}
    </div></div></div>`;
  $("#oeDownload").addEventListener("click", () => download(`/api/export?path=${enc(path)}`, null, file).catch((e) => toast(e.message, "error")));
  $("#oeRetry").addEventListener("click", () => { S.doc = null; showEditor(path, parseHash().rev); });
  $("#oeConvert")?.addEventListener("click", async (e) => {
    e.currentTarget.disabled = true;
    e.currentTarget.innerHTML = `<span class="spinner" style="width:16px;height:16px;border-width:2px"></span>Converting…`;
    try {
      const r = await postJSON("/api/convert", { path, user: S.user });
      await loadTree();
      toast("Converted — the original .xls is kept alongside");
      openDoc(r.path);
    } catch (ex) {
      renderOpenError(path, ex);
    }
  });
}

async function offerDraft() {
  let draft;
  try { draft = JSON.parse(localStorage.getItem(draftKey(S.doc.path)) || "null"); } catch (_) { draft = null; }
  if (!draft || !draft.edits || pendingCount()) return;
  const n = Object.values(draft.edits).reduce((a, m) => a + Object.keys(m).length, 0);
  if (!n) return;
  const stale = draft.baseRev !== S.doc.rev;
  const ans = await modal({
    title: "Restore unsaved changes?",
    text: `You have <b>${plural(n, "unsaved edit")}</b> from ${esc(timeAgo(draft.time))} on this document.` +
      (stale ? ` The document has been updated to Rev ${S.doc.rev} since then — your edits will be applied on top of the latest version.` : ""),
    icon: I.restore,
    actions: [{ label: "Discard", value: "discard" }, { label: "Restore edits", primary: true, value: "restore" }],
  });
  if (ans === "restore") { S.edits = draft.edits; renderEditor(); toast(`${plural(n, "edit")} restored — remember to save`); }
  else if (ans === "discard") localStorage.removeItem(draftKey(S.doc.path));
}

function renderEditor() {
  const d = S.doc;
  const main = $("#main");
  const ro = readOnly();
  const segs = d.path.split("/").slice(0, -1);
  const crumbHtml = segs.map((p, i) => `<span class="sep">/</span><a href="${folderHash(segs.slice(0, Math.min(i + 1, 3)))}">${esc(p)}</a>`).join("");
  const statuses = S.tree?.statuses || ["Draft", "In Review", "Approved", "Released"];
  main.innerHTML = `<div class="editor">
    <div class="ed-head">
      <div class="ed-title">
        <div class="crumbs"><a href="#/">Home</a>${crumbHtml}</div>
        <h2><span class="xl-icon">X</span><span class="name" title="${esc(d.file)}">${esc(d.name)}</span>
          ${ro ? `<span class="pill rev nodot">Viewing Rev ${d.viewingRev}</span>` : `<select class="status-select pill ${statusClass(d.status)}" id="edStatus">${statuses.map((s) => `<option ${s === d.status ? "selected" : ""}>${s}</option>`).join("")}</select>`}
        </h2>
        <div class="ed-meta"><span class="pill rev">Rev ${d.rev}</span><span>Last saved by <b>${esc(d.lastUser)}</b> · <span title="${esc(fullTime(d.lastTime))}">${timeAgo(d.lastTime)}</span></span></div>
      </div>
      <div class="ed-actions">
        <button class="btn ${S.drawer ? "tb-toggle on" : ""}" id="edHistory">${I.history}History<span class="badge" style="background:#f2f4f7;color:var(--ink-2)">${d.revisions}</span></button>
        <button class="btn" id="edExport">${I.download}Export</button>
        <button class="btn icon" id="edMore" title="More">${I.more}</button>
        ${ro ? "" : `<button class="btn primary" id="edSave" ${pendingCount() ? "" : "disabled"}>${I.save}Save<span class="badge" id="saveCount" ${pendingCount() ? "" : "hidden"}>${pendingCount()}</span></button>`}
      </div>
    </div>
    ${ro ? `<div class="banner info">${I.eye}<span>You are viewing <b>revision ${d.viewingRev}</b> (read-only). The current version is Rev ${d.rev}.</span>
        <button class="btn sm" id="bnRestore">${I.restore}Restore this version</button><a class="btn sm primary" href="#/d/${enc(d.path)}">Back to latest</a></div>` : ""}
    <div class="toolbar">
      <button class="btn sm icon ghost" id="tbUndo" title="Undo (Ctrl+Z)" ${ro ? "disabled" : ""}>${I.undo}</button>
      <button class="btn sm icon ghost" id="tbRedo" title="Redo (Ctrl+Y)" ${ro ? "disabled" : ""}>${I.redo}</button>
      <span class="sep"></span>
      <input class="namebox" id="nameBox" title="Go to cell (type e.g. D12 and press Enter)">
      <div class="fx"><i>fx</i><input id="fxInput" ${ro ? "disabled" : ""} placeholder="${ro ? "Read-only revision" : "Select a cell to edit its value"}"></div>
      <span class="sep"></span>
      <div class="findbox"><input id="findInput" placeholder="Find in sheet…  Ctrl F" value="${esc(S.find.q)}"><small id="findCount"></small>
        <button class="btn sm icon ghost" id="findPrev" title="Previous">${I.chevDown.replace("<svg", '<svg style="transform:rotate(180deg);width:11px"')}</button>
        <button class="btn sm icon ghost" id="findNext" title="Next">${I.chevDown.replace("<svg", '<svg style="width:11px"')}</button></div>
      <span class="sep"></span>
      <div class="zoom"><button class="btn sm icon ghost" id="zOut" title="Zoom out">${I.minus}</button><button class="zval" id="zVal" title="Reset to 100%">${Math.round(S.zoom * 100)}%</button><button class="btn sm icon ghost" id="zIn" title="Zoom in">${I.plus}</button>
        <button class="btn sm ghost tb-toggle ${S.zoomMode === "fit" ? "on" : ""}" id="zFit" title="Fit the sheet width to the window">${I.fit}Fit</button></div>
    </div>
    <div class="ed-body">
      <div class="grid-wrap" id="gridWrap" tabindex="0"><div class="grid-zoom" id="gridZoom"></div></div>
      ${S.drawer ? `<aside class="drawer" id="drawer"></aside>` : ""}
    </div>
    <div class="sheet-tabs" id="sheetTabs"></div>
  </div>`;

  $("#edStatus")?.addEventListener("change", async (e) => {
    const status = e.target.value;
    try {
      await postJSON("/api/status", { path: d.path, status, user: S.user });
      d.status = status; e.target.className = `status-select pill ${statusClass(status)}`;
      await loadTree(); renderSidebar(d.path); toast(`Status set to ${status}`);
    } catch (err) { toast(err.message, "error"); }
  });
  $("#edHistory").addEventListener("click", toggleDrawer);
  $("#edExport").addEventListener("click", (e) => exportMenu(e.currentTarget));
  $("#edMore").addEventListener("click", (e) => moreMenu(e.currentTarget));
  $("#edSave")?.addEventListener("click", saveDialog);
  $("#bnRestore")?.addEventListener("click", () => restoreRev(d.viewingRev));
  $("#tbUndo").addEventListener("click", undo);
  $("#tbRedo").addEventListener("click", redo);
  $("#zOut").addEventListener("click", () => setZoom(S.zoom - 0.1));
  $("#zIn").addEventListener("click", () => setZoom(S.zoom + 0.1));
  $("#zVal").addEventListener("click", () => setZoom(1));
  $("#zFit").addEventListener("click", () => setZoom(fitZoom(), "fit"));
  $("#gridWrap").addEventListener("wheel", (e) => {
    if (!e.ctrlKey) return;  // Ctrl + mouse wheel zooms the sheet, like Excel
    e.preventDefault();
    setZoom(S.zoom * (e.deltaY < 0 ? 1.1 : 1 / 1.1));
  }, { passive: false });
  bindFx();
  bindFind();
  bindGrid();
  renderSheet();
  renderTabs();
  if (S.drawer) renderDrawer();
}

function sheetWidth(sh) {
  let w = 44;
  for (let c = 1; c <= sh.maxCol; c++) if (!sh.hiddenCols.includes(c)) w += sh.colWidths[c] || 0;
  return w;
}
/** Zoom that shows the whole sheet width (never above the sheet's own Excel zoom or 100%). */
function fitZoom() {
  const sh = sheet(), wrap = $("#gridWrap");
  const avail = (wrap?.clientWidth || 1200) - 8;
  const own = Math.min(1, (sh.zoom || 100) / 100);
  // Very wide sheets stop at 65% (still readable) and scroll sideways instead.
  return Math.max(0.65, Math.min(own, avail / (sheetWidth(sh) + 12)));
}
function setZoom(z, mode = "manual") {
  S.zoom = Math.min(2, Math.max(0.4, Math.round(z * 100) / 100));
  S.zoomMode = mode;
  const el = $("#gridZoom");
  if (el) el.style.zoom = S.zoom;
  if ($("#zVal")) $("#zVal").textContent = Math.round(S.zoom * 100) + "%";
  $("#zFit")?.classList.toggle("on", mode === "fit");
  if ($("#gridZoom table")) applyFreeze();
}

// ---------------------------------------------------------------- sheet render
function mergeIndex(sh) {
  if (sh._mi) return sh._mi;
  const mi = new Map();
  for (const m of sh.merges) for (let r = m.r1; r <= m.r2; r++) for (let c = m.c1; c <= m.c2; c++) mi.set(`${r},${c}`, m);
  sh._mi = mi;
  sh._hr = new Set(sh.hiddenRows);
  sh._hc = new Set(sh.hiddenCols);
  return mi;
}
function anchor(r, c) {
  const m = mergeIndex(sheet()).get(`${r},${c}`);
  return m ? { r: m.r1, c: m.c1, m } : { r, c, m: null };
}
function cellText(sh, r, c) {
  const e = S.edits[sh.name]?.[`${r},${c}`];
  if (e !== undefined) return e;
  return sh.cells[`${r},${c}`]?.v ?? "";
}
function editText(sh, r, c) {
  const e = S.edits[sh.name]?.[`${r},${c}`];
  if (e !== undefined) return e;
  const cell = sh.cells[`${r},${c}`];
  return cell ? cell.f ?? cell.e ?? "" : "";
}

function cellInner(sh, r, c, imgs) {
  const key = `${r},${c}`;
  const cell = sh.cells[key] || {};
  const edited = S.edits[sh.name]?.[key];
  let content = edited !== undefined ? esc(edited) : cell.h ?? esc(cell.v ?? "");
  const rot = cell.rot;
  if (rot && content) {
    if (rot === 90) content = `<span class="rot r90">${content}</span>`;
    else if (rot === 180) content = `<span class="rot r180">${content}</span>`;
    else if (rot === 255) content = `<span class="rot stack">${content}</span>`;
    else { const deg = rot <= 90 ? -rot : rot - 90; content = `<span class="rot" style="transform:rotate(${deg}deg)">${content}</span>`; }
  }
  let html = `<div class="c">${content}</div>`;
  if (sh.validations[key] && !readOnly()) html += `<span class="dd" data-dd="1">${I.chevDown}</span>`;
  if (imgs) html += imgs;
  return html;
}

function imageMap(sh) {
  const map = {};
  const mi = mergeIndex(sh);
  const sumW = (a, b) => { let s = 0; for (let c = a; c < b; c++) s += sh._hc.has(c) ? 0 : sh.colWidths[c] || 64; return s; };
  const sumH = (a, b) => { let s = 0; for (let r = a; r < b; r++) s += sh._hr.has(r) ? 0 : sh.rowHeights[r] || 20; return s; };
  for (const img of sh.images) {
    let { r, c } = img;
    let dx = img.dx, dy = img.dy;
    const m = mi.get(`${r},${c}`);
    if (m) { dx += sumW(m.c1, c); dy += sumH(m.r1, r); r = m.r1; c = m.c1; }
    const w = img.to ? sumW(img.c, img.to.c) + img.to.dx - img.dx : img.w;
    const h = img.to ? sumH(img.r, img.to.r) + img.to.dy - img.dy : img.h;
    const k = `${r},${c}`;
    map[k] = (map[k] || "") + `<img class="ximg" alt="" src="${img.src}" style="left:${dx - 3}px;top:${dy}px;width:${Math.max(1, w)}px;height:${Math.max(1, h)}px">`;
  }
  return map;
}

function renderSheet() {
  const sh = sheet();
  const mi = mergeIndex(sh);
  const zoomEl = $("#gridZoom");
  let style = $("#xlStyles");
  if (!style) { style = document.createElement("style"); style.id = "xlStyles"; document.head.appendChild(style); }
  style.textContent = "td.frz{background-color:#fff}\n" + sh.styles.map((s, i) => `table.xl td.s${i}{${s}}`).join("\n");

  const imgs = imageMap(sh);
  if (S.zoomMode === "fit") { S.zoom = fitZoom(); if ($("#zVal")) $("#zVal").textContent = Math.round(S.zoom * 100) + "%"; }
  const { fr, fc } = freezeFor(sh);
  const custom = new Set(sh.customHeights || []);
  const hdrW = 44, hdrH = 22;
  const leftOf = [0, hdrW];
  for (let c = 1; c <= sh.maxCol; c++) leftOf[c + 1] = leftOf[c] + (sh._hc.has(c) ? 0 : sh.colWidths[c]);

  const hlSet = S.hl && S.hl.sheet[sh.name];
  const parts = [];
  parts.push(`<table class="xl ${sh.gridLines ? "" : "nogrid"} ${readOnly() ? "readonly" : ""}" style="width:${leftOf[sh.maxCol + 1]}px"><colgroup><col style="width:${hdrW}px">`);
  for (let c = 1; c <= sh.maxCol; c++) parts.push(`<col style="width:${sh._hc.has(c) ? 0 : sh.colWidths[c]}px">`);
  parts.push(`</colgroup><thead><tr><th class="corner"></th>`);
  for (let c = 1; c <= sh.maxCol; c++) parts.push(`<th data-hc="${c}"${c <= fc ? ` class="frz-h" style="left:${leftOf[c]}px"` : ""}>${sh._hc.has(c) ? "" : colName(c)}</th>`);
  parts.push(`</tr></thead><tbody>`);
  const edits = S.edits[sh.name] || {};
  for (let r = 1; r <= sh.maxRow; r++) {
    const hidden = sh._hr.has(r);
    parts.push(`<tr data-r="${r}" class="${hidden ? "hidden" : ""}" style="height:${sh.rowHeights[r]}px"><th data-hr="${r}">${r}</th>`);
    for (let c = 1; c <= sh.maxCol; c++) {
      const key = `${r},${c}`;
      const m = mi.get(key);
      if (m && (m.r1 !== r || m.c1 !== c)) continue;
      const cell = sh.cells[key] || {};
      const cls = [];
      if (cell.s !== undefined) cls.push("s" + cell.s);
      if (cell.w) cls.push("w");
      if (edits[key] !== undefined) cls.push("dirty");
      if (cell.note) cls.push("note");
      if (hlSet && hlSet.has(key)) cls.push("hl");
      let st = "";
      if (!m && !cell.w && !cell.n && (cell.v || edits[key]) && c < sh.maxCol) {
        const nxt = sh.cells[`${r},${c + 1}`];
        if (!mi.get(`${r},${c + 1}`) && !(nxt && (nxt.v || nxt.f)) && edits[`${r},${c + 1}`] === undefined) cls.push("ov");
      }
      if (sh._hc.has(c)) st += "padding:0;font-size:0;";
      const r2 = m ? m.r2 : r, c2 = m ? m.c2 : c;
      const frzR = r2 <= fr, frzC = c2 <= fc;   // only cells entirely inside the frozen pane stick
      if (frzR || frzC) {
        cls.push("frz");
        if (frzR) cls.push("frz-r");
        if (frzC) { cls.push("frz-c"); st += `left:${leftOf[c]}px;`; }
      }
      // Rows with a fixed height in Excel clip overflowing text instead of growing
      let allCustom = true, hsum = 0;
      for (let y = r; y <= r2; y++) { if (!custom.has(y)) { allCustom = false; break; } if (!sh._hr.has(y)) hsum += sh.rowHeights[y]; }
      if (allCustom && (cell.v || cell.h || edits[key] !== undefined)) { cls.push("clip"); st += `--mh:${Math.max(0, hsum - 1)}px;`; }
      const span = m ? `${m.r2 > m.r1 ? ` rowspan="${m.r2 - m.r1 + 1}"` : ""}${m.c2 > m.c1 ? ` colspan="${m.c2 - m.c1 + 1}"` : ""}` : "";
      parts.push(`<td data-r="${r}" data-c="${c}"${span} class="${cls.join(" ")}"${st ? ` style="${st}"` : ""}>${cellInner(sh, r, c, imgs[key])}</td>`);
    }
    parts.push(`</tr>`);
  }
  parts.push(`</tbody></table>`);
  zoomEl.innerHTML = parts.join("");
  zoomEl.style.zoom = S.zoom;

  S.tdMap = new Map();
  zoomEl.querySelectorAll("td").forEach((td) => S.tdMap.set(`${td.dataset.r},${td.dataset.c}`, td));
  $$("tbody th", zoomEl).forEach((th) => (th.style.left = "0px"));
  applyFreeze();
  if (sh.truncated) toast(`Large sheet: showing the first ${sh.maxRow} rows × ${sh.maxCol} columns`, "error");
  if (S.find.q) runFind(false);
  selectCell(S.cur.r, S.cur.c, false);
}

/** Frozen rows/cols from the sheet, dropped when they would fill most of the window. */
function freezeFor(sh) {
  let fr = sh.freeze?.r || 0, fc = sh.freeze?.c || 0;
  const wrap = $("#gridWrap");
  const H = wrap?.clientHeight || 700, W = wrap?.clientWidth || 1200;
  let h = 22; for (let r = 1; r <= fr; r++) if (!sh._hr.has(r)) h += sh.rowHeights[r] || 20;
  let w = 44; for (let c = 1; c <= fc; c++) if (!sh._hc.has(c)) w += sh.colWidths[c] || 64;
  if (h * S.zoom > H * 0.45) fr = 0;
  if (w * S.zoom > W * 0.55) fc = 0;
  return { fr, fc };
}
/** Sticky offsets for frozen rows use the real (auto-grown) row heights. */
function applyFreeze() {
  const zoomEl = $("#gridZoom");
  const sh = sheet();
  const { fr } = freezeFor(sh);
  zoomEl.querySelectorAll("tbody th.frz-t").forEach((th) => { th.classList.remove("frz-t"); th.style.top = ""; });
  if (!fr) return;
  const rows = zoomEl.querySelectorAll("tbody tr");
  const tops = [];
  for (let r = 1; r <= fr; r++) tops[r] = rows[r - 1].offsetTop;
  zoomEl.querySelectorAll("td.frz-r").forEach((td) => (td.style.top = tops[+td.dataset.r] + "px"));
  $$("tbody th", zoomEl).slice(0, fr).forEach((th, i) => { th.classList.add("frz-t"); th.style.top = tops[i + 1] + "px"; });
}

function paintCell(sheetName, r, c) {
  if (sheet().name !== sheetName) return;
  const td = S.tdMap.get(`${r},${c}`);
  if (!td) return;
  const sh = sheet();
  const img = Array.from(td.querySelectorAll("img.ximg")).map((i) => i.outerHTML).join("");
  td.innerHTML = cellInner(sh, r, c, img);
  td.classList.toggle("dirty", S.edits[sh.name]?.[`${r},${c}`] !== undefined);
}

function renderTabs() {
  const el = $("#sheetTabs");
  const hlRev = S.hl ? `<span><i style="background:rgba(122,90,248,.35)"></i>Changed in Rev ${S.hl.rev}</span>` : "";
  el.innerHTML = S.doc.sheets.map((s, i) => s.state !== "visible" ? "" : `<button class="sheet-tab ${i === S.sheetIdx ? "active" : ""}" data-i="${i}">
      ${s.tabColor ? `<span class="tc" style="background:${s.tabColor}"></span>` : ""}${esc(s.name)}
      ${Object.keys(S.edits[s.name] || {}).length ? `<span class="dcount">${Object.keys(S.edits[s.name]).length}</span>` : ""}</button>`).join("") +
    `<div class="legend"><span><i style="background:rgba(253,176,34,.55)"></i>Unsaved edit</span>${hlRev}<span><i style="background:#d92d20;clip-path:polygon(0 0,100% 0,100% 100%)"></i>Note</span></div>`;
  el.querySelectorAll(".sheet-tab").forEach((b) => b.addEventListener("click", () => switchSheet(+b.dataset.i)));
}
function switchSheet(i, r = 1, c = 1) {
  if (i === S.sheetIdx && r === S.cur.r && c === S.cur.c) return;
  finishEdit(true);
  const changed = i !== S.sheetIdx;
  S.sheetIdx = i;
  S.cur = { r, c };
  if (changed) { S.find.hits = []; renderSheet(); renderTabs(); if (!r || r === 1) $("#gridWrap").scrollTo(0, 0); }
  else selectCell(r, c);
}

// ---------------------------------------------------------------- selection
function selectCell(r, c, scroll = true) {
  const sh = sheet();
  r = Math.max(1, Math.min(sh.maxRow, r));
  c = Math.max(1, Math.min(sh.maxCol, c));
  const a = anchor(r, c);
  S.cur = { r: a.r, c: a.c };
  $$("td.sel", $("#gridZoom")).forEach((td) => td.classList.remove("sel"));
  $$("th.hsel", $("#gridZoom")).forEach((th) => th.classList.remove("hsel"));
  const td = S.tdMap.get(`${a.r},${a.c}`);
  if (!td) return;
  td.classList.add("sel");
  const r2 = a.m ? a.m.r2 : a.r, c2 = a.m ? a.m.c2 : a.c;
  for (let x = a.c; x <= c2; x++) $(`th[data-hc="${x}"]`)?.classList.add("hsel");
  for (let y = a.r; y <= r2; y++) $(`th[data-hr="${y}"]`)?.classList.add("hsel");
  $("#nameBox").value = colName(a.c) + a.r + (a.m ? `:${colName(c2)}${r2}` : "");
  const fx = $("#fxInput");
  if (document.activeElement !== fx) fx.value = editText(sh, a.r, a.c);
  if (scroll) scrollIntoView(td);
}
function scrollIntoView(td) {
  const wrap = $("#gridWrap");
  const wr = wrap.getBoundingClientRect();
  const rc = td.getBoundingClientRect();
  if (td.classList.contains("frz-r") && td.classList.contains("frz-c")) return;
  // visible area = scroll box minus sticky headers and frozen panes (real screen pixels, any zoom)
  let top = $("#gridZoom thead").getBoundingClientRect().bottom;
  let left = $("#gridZoom tbody th")?.getBoundingClientRect().right ?? wr.left;
  if (!td.classList.contains("frz-r")) {
    const frozen = $$("#gridZoom td.frz-r");
    if (frozen.length) top = Math.max(top, ...frozen.slice(-40).map((x) => x.getBoundingClientRect().bottom));
  }
  if (!td.classList.contains("frz-c")) {
    const fh = $$("#gridZoom thead th.frz-h");
    if (fh.length) left = Math.max(left, fh[fh.length - 1].getBoundingClientRect().right);
  }
  const bottom = wr.top + wrap.clientHeight, right = wr.left + wrap.clientWidth;
  if (!td.classList.contains("frz-r")) {
    if (rc.top < top) wrap.scrollTop -= top - rc.top + 2;
    else if (rc.bottom > bottom) wrap.scrollTop += Math.min(rc.bottom - bottom + 6, rc.top - top);
  }
  if (!td.classList.contains("frz-c")) {
    if (rc.left < left) wrap.scrollLeft -= left - rc.left + 2;
    else if (rc.right > right) wrap.scrollLeft += Math.min(rc.right - right + 6, rc.left - left);
  }
}
function move(dr, dc) {
  const sh = sheet();
  const a = anchor(S.cur.r, S.cur.c);
  const r2 = a.m ? a.m.r2 : a.r, c2 = a.m ? a.m.c2 : a.c;
  let r = dr > 0 ? r2 + 1 : dr < 0 ? a.r - 1 : a.r;
  let c = dc > 0 ? c2 + 1 : dc < 0 ? a.c - 1 : a.c;
  while (sh._hr.has(r) && r > 0 && r <= sh.maxRow) r += dr || 1;
  while (sh._hc.has(c) && c > 0 && c <= sh.maxCol) c += dc || 1;
  if (r < 1 || c < 1 || r > sh.maxRow || c > sh.maxCol) return;
  selectCell(r, c);
}

// ---------------------------------------------------------------- editing
let editing = null;

function setValue(r, c, text, record = true) {
  const sh = sheet();
  const key = `${r},${c}`;
  const cell = sh.cells[key];
  const original = cell ? cell.f ?? cell.e ?? "" : "";
  const before = S.edits[sh.name]?.[key];
  const current = before !== undefined ? before : original;
  if (text === current) return false;
  S.edits[sh.name] = S.edits[sh.name] || {};
  if (text === original) delete S.edits[sh.name][key];
  else S.edits[sh.name][key] = text;
  if (record) { S.undo.push({ sheet: sh.name, key, before, after: S.edits[sh.name][key] }); S.redo = []; }
  paintCell(sh.name, r, c);
  editsChanged();
  return true;
}
function editsChanged() {
  const n = pendingCount();
  const btn = $("#edSave");
  if (btn) { btn.disabled = !n; const b = $("#saveCount"); b.hidden = !n; b.textContent = n; }
  renderTabs();
  saveDraft();
}
function applyHistory(entry, dir) {
  const i = S.doc.sheets.findIndex((s) => s.name === entry.sheet);
  const [r, c] = entry.key.split(",").map(Number);
  if (i !== S.sheetIdx) switchSheet(i, r, c);
  const val = dir === "undo" ? entry.before : entry.after;
  S.edits[entry.sheet] = S.edits[entry.sheet] || {};
  if (val === undefined) delete S.edits[entry.sheet][entry.key]; else S.edits[entry.sheet][entry.key] = val;
  paintCell(entry.sheet, r, c);
  selectCell(r, c);
  editsChanged();
}
function undo() { if (readOnly()) return; finishEdit(true); const e = S.undo.pop(); if (e) { S.redo.push(e); applyHistory(e, "undo"); } }
function redo() { if (readOnly()) return; finishEdit(true); const e = S.redo.pop(); if (e) { S.undo.push(e); applyHistory(e, "redo"); } }

function startEdit(initial) {
  if (readOnly() || editing) return;
  const sh = sheet();
  const { r, c } = S.cur;
  const td = S.tdMap.get(`${r},${c}`);
  if (!td) return;
  const ta = document.createElement("textarea");
  ta.className = "cell-input";
  ta.value = initial !== undefined ? initial : editText(sh, r, c);
  const cs = getComputedStyle(td);
  ta.style.font = cs.font;
  ta.style.fontWeight = cs.fontWeight;
  ta.style.minWidth = Math.max(td.offsetWidth + 2, 120) + "px";
  td.appendChild(ta);
  const grow = () => { ta.style.height = "auto"; ta.style.height = Math.max(td.offsetHeight + 2, ta.scrollHeight + 4) + "px"; };
  grow();
  ta.addEventListener("input", () => { grow(); $("#fxInput").value = ta.value; });
  ta.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.altKey && !e.shiftKey) { e.preventDefault(); finishEdit(true); move(1, 0); focusGrid(); }
    else if (e.key === "Enter" && (e.altKey || e.shiftKey)) {
      e.preventDefault();
      const s = ta.selectionStart;
      ta.value = ta.value.slice(0, s) + "\n" + ta.value.slice(ta.selectionEnd);
      ta.selectionStart = ta.selectionEnd = s + 1; grow();
    } else if (e.key === "Tab") { e.preventDefault(); finishEdit(true); move(0, e.shiftKey ? -1 : 1); focusGrid(); }
    else if (e.key === "Escape") { e.preventDefault(); finishEdit(false); focusGrid(); }
    e.stopPropagation();
  });
  ta.addEventListener("blur", () => setTimeout(() => { if (editing && editing.ta === ta) finishEdit(true); }, 0));
  editing = { ta, r, c, sheet: sh.name };
  ta.focus();
  ta.selectionStart = ta.selectionEnd = ta.value.length;
}
function finishEdit(commit) {
  if (!editing) return;
  const { ta, r, c, sheet: sn } = editing;
  editing = null;
  const val = ta.value;
  ta.remove();
  if (commit && sheet().name === sn) setValue(r, c, val);
  if (sheet().name === sn) $("#fxInput").value = editText(sheet(), r, c);
}
function focusGrid() { $("#gridWrap")?.focus({ preventScroll: true }); }

function bindFx() {
  const fx = $("#fxInput");
  fx.addEventListener("keydown", (e) => {
    if (e.key === "Enter") { e.preventDefault(); setValue(S.cur.r, S.cur.c, fx.value); move(1, 0); focusGrid(); }
    if (e.key === "Escape") { fx.value = editText(sheet(), S.cur.r, S.cur.c); focusGrid(); }
    if (e.key === "Tab") { e.preventDefault(); setValue(S.cur.r, S.cur.c, fx.value); move(0, e.shiftKey ? -1 : 1); focusGrid(); }
  });
  fx.addEventListener("blur", () => { if (!readOnly() && fx.value !== editText(sheet(), S.cur.r, S.cur.c)) setValue(S.cur.r, S.cur.c, fx.value); });
  const nb = $("#nameBox");
  nb.addEventListener("focus", () => nb.select());
  nb.addEventListener("keydown", (e) => {
    if (e.key !== "Enter") return;
    const m = /^([A-Za-z]{1,3})(\d+)$/.exec(nb.value.trim().split(":")[0]);
    if (!m) { toast("Type a cell reference such as D12", "error"); return; }
    let c = 0; for (const ch of m[1].toUpperCase()) c = c * 26 + ch.charCodeAt(0) - 64;
    selectCell(+m[2], c); focusGrid();
  });
}

// ---------------------------------------------------------------- dropdown fields
let ddMenu = null;
function closeFloating() { ddMenu?.remove(); ddMenu = null; $$(".tooltip").forEach((t) => t.remove()); $$(".dd-menu").forEach((t) => t.remove()); }
function openDropdown(r, c) {
  closeFloating();
  const sh = sheet();
  const opts = sh.validations[`${r},${c}`];
  const td = S.tdMap.get(`${r},${c}`);
  if (!opts || !td || readOnly()) return;
  const cur = cellText(sh, r, c);
  const rect = td.getBoundingClientRect();
  ddMenu = document.createElement("div");
  ddMenu.className = "dd-menu";
  ddMenu.innerHTML = opts.map((o, i) => `<div data-i="${i}" class="${o === cur ? "on" : ""}">${esc(o)}</div>`).join("") + `<div data-i="-1" style="color:var(--muted)">Clear</div>`;
  ddMenu.style.left = rect.left + "px";
  ddMenu.style.top = rect.bottom + 4 + "px";
  ddMenu.style.minWidth = Math.max(160, rect.width) + "px";
  document.body.appendChild(ddMenu);
  ddMenu.addEventListener("mousedown", (e) => {
    const el = e.target.closest("[data-i]");
    if (!el) return;
    e.preventDefault();
    setValue(r, c, +el.dataset.i < 0 ? "" : opts[+el.dataset.i]);
    closeFloating(); focusGrid();
  });
}

// ---------------------------------------------------------------- grid events
function bindGrid() {
  const wrap = $("#gridWrap");
  wrap.addEventListener("mousedown", (e) => {
    if (e.target.closest(".cell-input")) return;
    const dd = e.target.closest(".dd");
    const td = e.target.closest("td");
    if (!td) return;
    if (editing) finishEdit(true);
    closeFloating();
    selectCell(+td.dataset.r, +td.dataset.c, false);
    if (dd) { e.preventDefault(); focusGrid(); openDropdown(+td.dataset.r, +td.dataset.c); }
  });
  wrap.addEventListener("dblclick", (e) => {
    const td = e.target.closest("td");
    if (!td || e.target.closest(".cell-input")) return;
    if (sheet().validations[`${S.cur.r},${S.cur.c}`]) openDropdown(S.cur.r, S.cur.c);
    else startEdit();
  });
  wrap.addEventListener("mouseover", (e) => {
    const td = e.target.closest("td.note");
    $$(".tooltip").forEach((t) => t.remove());
    if (!td) return;
    const cell = sheet().cells[`${td.dataset.r},${td.dataset.c}`];
    if (!cell?.note) return;
    const tip = document.createElement("div");
    tip.className = "tooltip";
    tip.textContent = cell.note;
    const rc = td.getBoundingClientRect();
    tip.style.left = rc.right + 6 + "px";
    tip.style.top = rc.top + "px";
    document.body.appendChild(tip);
  });
  wrap.addEventListener("mouseleave", () => $$(".tooltip").forEach((t) => t.remove()));
  wrap.addEventListener("scroll", () => { if (ddMenu) closeFloating(); }, { passive: true });
  wrap.addEventListener("keydown", (e) => {
    if (editing) return;
    const k = e.key;
    const mod = e.ctrlKey || e.metaKey;
    if (k === "ArrowDown" && e.altKey) { e.preventDefault(); openDropdown(S.cur.r, S.cur.c); return; }
    if (k === "ArrowUp") { e.preventDefault(); move(-1, 0); }
    else if (k === "ArrowDown") { e.preventDefault(); move(1, 0); }
    else if (k === "ArrowLeft") { e.preventDefault(); move(0, -1); }
    else if (k === "ArrowRight") { e.preventDefault(); move(0, 1); }
    else if (k === "Tab") { e.preventDefault(); move(0, e.shiftKey ? -1 : 1); }
    else if (k === "Enter") { e.preventDefault(); move(e.shiftKey ? -1 : 1, 0); }
    else if (k === "F2") { e.preventDefault(); startEdit(); }
    else if ((k === "Delete" || k === "Backspace") && !readOnly()) { e.preventDefault(); setValue(S.cur.r, S.cur.c, ""); $("#fxInput").value = ""; }
    else if (mod && k.toLowerCase() === "z") { e.preventDefault(); undo(); }
    else if (mod && k.toLowerCase() === "y") { e.preventDefault(); redo(); }
    else if (mod && k.toLowerCase() === "c") { e.preventDefault(); navigator.clipboard?.writeText(editText(sheet(), S.cur.r, S.cur.c)); toast("Copied"); }
    else if (k === "Home") { e.preventDefault(); selectCell(S.cur.r, 1); }
    else if (!mod && !e.altKey && k.length === 1 && !readOnly()) { e.preventDefault(); startEdit(k); }
  });
  wrap.addEventListener("paste", (e) => {
    if (editing || readOnly()) return;
    const text = e.clipboardData?.getData("text/plain");
    if (text == null) return;
    e.preventDefault();
    pasteGrid(text);
  });
}
function pasteGrid(text) {
  const rows = text.replace(/\r\n?/g, "\n").replace(/\n$/, "").split("\n").map((line) => line.split("\t"));
  const sh = sheet();
  const { r: r0, c: c0 } = S.cur;
  let n = 0;
  rows.forEach((cols, dy) => cols.forEach((val, dx) => {
    const r = r0 + dy, c = c0 + dx;
    if (r > sh.maxRow || c > sh.maxCol) return;
    const a = anchor(r, c);
    if (a.r !== r || a.c !== c) return;
    if (setValue(r, c, val.replace(/^"([\s\S]*)"$/, "$1").replace(/""/g, '"'))) n++;
  }));
  if (n) toast(`Pasted ${plural(n, "cell")}`);
}

// ---------------------------------------------------------------- find
function bindFind() {
  const inp = $("#findInput");
  inp.addEventListener("input", () => { S.find.q = inp.value; runFind(true); });
  inp.addEventListener("keydown", (e) => {
    if (e.key === "Enter") { e.preventDefault(); stepFind(e.shiftKey ? -1 : 1); }
    if (e.key === "Escape") { inp.value = ""; S.find.q = ""; runFind(false); focusGrid(); }
  });
  $("#findNext").addEventListener("click", () => stepFind(1));
  $("#findPrev").addEventListener("click", () => stepFind(-1));
}
function runFind(jump) {
  $$("td.found", $("#gridZoom")).forEach((td) => td.classList.remove("found", "cur"));
  const q = S.find.q.trim().toLowerCase();
  const sh = sheet();
  S.find.hits = [];
  if (q) {
    for (const [key, td] of S.tdMap) {
      const [r, c] = key.split(",").map(Number);
      if (String(cellText(sh, r, c)).toLowerCase().includes(q)) { S.find.hits.push([r, c]); td.classList.add("found"); }
    }
    S.find.hits.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  }
  S.find.i = -1;
  $("#findCount").textContent = q ? `${S.find.hits.length} found` : "";
  if (jump && S.find.hits.length) stepFind(1);
}
function stepFind(dir) {
  const hits = S.find.hits;
  if (!hits.length) return;
  S.find.i = (S.find.i + dir + hits.length) % hits.length;
  $$("td.found.cur", $("#gridZoom")).forEach((td) => td.classList.remove("cur"));
  const [r, c] = hits[S.find.i];
  S.tdMap.get(`${r},${c}`)?.classList.add("cur");
  selectCell(r, c);
  $("#findCount").textContent = `${S.find.i + 1} / ${hits.length}`;
}

// ---------------------------------------------------------------- save / export
function pendingList() {
  const out = [];
  for (const [sn, cells] of Object.entries(S.edits)) {
    const sh = S.doc.sheets.find((s) => s.name === sn);
    for (const [key, val] of Object.entries(cells)) {
      const [r, c] = key.split(",").map(Number);
      const cell = sh?.cells[key];
      out.push({ sheet: sn, r, c, cell: colName(c) + r, old: cell ? cell.f ?? cell.e ?? "" : "", new: val, label: rowLabel(sh, r, c) });
    }
  }
  return out.sort((a, b) => a.sheet.localeCompare(b.sheet) || a.r - b.r || a.c - b.c);
}
function rowLabel(sh, r, c) {
  // best-effort human label: the first text cell on the row, left of the edited cell
  if (!sh) return "";
  for (let x = 1; x < c; x++) {
    const m = sh._mi?.get(`${r},${x}`);
    const cell = sh.cells[m ? `${m.r1},${m.c1}` : `${r},${x}`];
    if (cell?.v && !cell.n && cell.v.length > 2 && !cell.rot) return cell.v;
  }
  return "";
}
function changesTable(list, limit = 60) {
  const rows = list.slice(0, limit).map((ch) => `<tr>
    <td class="ref" data-sheet="${esc(ch.sheet)}" data-r="${ch.r}" data-c="${ch.c}" title="${esc(ch.sheet)}">${esc(ch.cell)}</td>
    <td>${ch.label ? `<div style="color:var(--muted);font-size:11.5px;margin-bottom:2px">${esc(ch.label)}</div>` : ""}
      ${ch.old !== "" ? `<span class="old">${esc(ch.old)}</span> → ` : '<span style="color:var(--faint)">(empty)</span> → '}
      ${ch.new !== "" ? `<span class="new">${esc(ch.new)}</span>` : '<span style="color:var(--faint)">(cleared)</span>'}</td></tr>`).join("");
  return `<div class="changes"><table><thead><tr><th style="width:62px">Cell</th><th>Change</th></tr></thead><tbody>${rows}</tbody></table>
    ${list.length > limit ? `<div class="more">+ ${list.length - limit} more</div>` : ""}</div>`;
}
function bindRefs(root) {
  root.querySelectorAll("td.ref").forEach((el) => el.addEventListener("click", () => gotoCell(el.dataset.sheet, +el.dataset.r, +el.dataset.c)));
}
function gotoCell(sheetName, r, c) {
  const i = S.doc.sheets.findIndex((s) => s.name === sheetName);
  if (i < 0) return;
  if (i !== S.sheetIdx) { S.sheetIdx = i; S.cur = { r, c }; renderSheet(); renderTabs(); }
  selectCell(r, c);
  const td = S.tdMap.get(`${S.cur.r},${S.cur.c}`);
  if (td) { td.animate([{ outline: "3px solid #7a5af8" }, { outline: "3px solid transparent" }], { duration: 1200 }); }
}

async function saveDialog() {
  finishEdit(true);
  if (!pendingCount()) return;
  if (!S.user) await askUser();
  const list = pendingList();
  const res = await modal({
    title: `Save ${plural(list.length, "change")}`,
    text: `This creates <b>Rev ${S.doc.rev + 1}</b>. The Excel file on the server is updated and the previous version is kept in history.`,
    icon: I.save,
    wide: true,
    body: `<div class="field"><label>What changed and why? <span style="font-weight:400;color:var(--muted)">(recommended)</span></label>
      <textarea id="saveNote" placeholder="e.g. Updated kerb weight after supplier input, per review on 27-Sep"></textarea></div>
      ${changesTable(list)}`,
    actions: [{ label: "Keep editing" }, {
      label: `${I.save}Save revision`, primary: true, handler: async (w) => {
        try {
          return await postJSON("/api/save", { path: S.doc.path, baseRev: S.doc.rev, user: S.user, note: $("#saveNote", w).value, edits: S.edits });
        } catch (err) {
          if (err.status === 409) return { conflict: err };
          throw err;
        }
      },
    }],
    onOpen: (w) => bindRefs(w),
  });
  if (!res) return;
  if (res.conflict) {
    const again = await modal({
      title: "Someone else saved first",
      text: esc(res.conflict.message),
      icon: I.alert, iconStyle: "background:#fffaeb;color:#dc6803;box-shadow:0 0 0 7px #fffcf5",
      actions: [{ label: "Cancel" }, { label: "Load latest & keep my edits", primary: true }],
    });
    if (again) { await reloadDoc(true); toast("Latest version loaded — your edits are re-applied on top. Review and save."); }
    return;
  }
  S.edits = {}; S.undo = []; S.redo = [];
  try { localStorage.removeItem(draftKey(S.doc.path)); } catch (_) { /* ignore */ }
  toast(res.saved ? `Saved as Rev ${res.rev} — ${plural(res.changes.length, "cell")} updated` : "Nothing changed");
  S.hl = null; S.openRev = null;
  await reloadDoc(false);
}
async function reloadDoc(keepEdits) {
  const edits = keepEdits ? S.edits : {};
  const scroll = [$("#gridWrap")?.scrollTop, $("#gridWrap")?.scrollLeft];
  const sheetName = sheet().name;
  const doc = await getJSON(`/api/document?path=${enc(S.doc.path)}`);
  S.doc = doc;
  S.edits = edits;
  const i = doc.sheets.findIndex((s) => s.name === sheetName);
  S.sheetIdx = i >= 0 ? i : 0;
  await loadTree();
  renderSidebar(doc.path);
  renderEditor();
  if (S.drawer) loadHistory();
  const wrap = $("#gridWrap");
  if (wrap && scroll[0] != null) { wrap.scrollTop = scroll[0]; wrap.scrollLeft = scroll[1]; }
}

function popMenu(anchorEl, items) {
  closeFloating();
  const r = anchorEl.getBoundingClientRect();
  ddMenu = document.createElement("div");
  ddMenu.className = "dd-menu";
  ddMenu.innerHTML = items.map((it, i) => it ? `<div data-i="${i}" style="display:flex;gap:10px;align-items:flex-start;padding:9px 12px">
      <span style="width:17px;height:17px;color:var(--muted);margin-top:1px">${it.icon}</span><span><b style="font-weight:600;display:block">${it.label}</b>${it.sub ? `<small style="color:var(--muted)">${it.sub}</small>` : ""}</span></div>`
    : `<hr style="border:0;border-top:1px solid var(--line);margin:4px 0">`).join("");
  document.body.appendChild(ddMenu);
  ddMenu.style.minWidth = "300px";
  ddMenu.style.top = r.bottom + 6 + "px";
  ddMenu.style.left = Math.max(8, r.right - ddMenu.offsetWidth) + "px";
  ddMenu.addEventListener("mousedown", (e) => {
    const el = e.target.closest("[data-i]");
    if (!el) return;
    e.preventDefault();
    closeFloating();
    items[+el.dataset.i].run();
  });
  setTimeout(() => document.addEventListener("mousedown", function h(e) { if (ddMenu && !ddMenu.contains(e.target)) closeFloating(); document.removeEventListener("mousedown", h); }), 0);
}
function exportMenu(btn) {
  const d = S.doc;
  const fname = d.file;
  const items = [];
  if (readOnly()) {
    items.push({ icon: I.download, label: `Download Rev ${d.viewingRev}`, sub: "Exact file as it was at this revision", run: () => download(`/api/export?path=${enc(d.path)}&rev=${d.viewingRev}`, null, fname) });
  } else {
    if (pendingCount()) items.push({ icon: I.edit, label: "Download with my unsaved edits", sub: `Current Rev ${d.rev} + ${plural(pendingCount(), "pending edit")}`, run: () => download("/api/export", { path: d.path, edits: S.edits }, fname).catch((e) => toast(e.message, "error")) });
    items.push({ icon: I.download, label: `Download saved version (Rev ${d.rev})`, sub: "Original Excel file with all formatting", run: () => download(`/api/export?path=${enc(d.path)}`, null, fname).catch((e) => toast(e.message, "error")) });
  }
  popMenu(btn, items);
}
function moreMenu(btn) {
  popMenu(btn, [
    { icon: I.copy, label: "Copy to another variant…", sub: "Start a new variant from this sheet", run: copyDialog },
    { icon: I.grid, label: "Toggle gridlines", sub: "Show / hide cell gridlines", run: () => { const t = $("table.xl"); t.classList.toggle("nogrid"); } },
    null,
    { icon: I.users, label: `Signed in as ${esc(S.user || "—")}`, sub: "Change name", run: () => askUser(true) },
  ]);
}

// ---------------------------------------------------------------- history
function toggleDrawer() {
  S.drawer = !S.drawer;
  const body = $(".ed-body");
  const btn = $("#edHistory");
  btn.classList.toggle("tb-toggle", S.drawer);
  btn.classList.toggle("on", S.drawer);
  if (S.drawer) {
    const d = document.createElement("aside");
    d.className = "drawer"; d.id = "drawer";
    body.appendChild(d);
    renderDrawer();
  } else {
    $("#drawer")?.remove();
    if (S.hl) { S.hl = null; renderSheet(); renderTabs(); }
  }
}
async function loadHistory() {
  S.history = await getJSON(`/api/history?path=${enc(S.doc.path)}`);
  paintDrawer();
}
function renderDrawer() {
  const d = $("#drawer");
  d.innerHTML = `<div class="drawer-head"><div><h3>Revision history</h3><small>Every save is kept — nothing is ever lost</small></div>
    <button class="btn sm icon ghost" id="drClose">${I.x}</button></div><div class="drawer-body" id="drBody"><div class="loading" style="min-height:160px"><div class="spinner"></div></div></div>`;
  $("#drClose").addEventListener("click", toggleDrawer);
  loadHistory();
}
const KIND = {
  edit: { icon: I.edit, label: "Edited in DocHub" },
  external: { icon: I.alert, label: "Changed outside DocHub" },
  restore: { icon: I.restore, label: "Restored" },
  import: { icon: I.upload, label: "Imported" },
};
function paintDrawer() {
  const body = $("#drBody");
  if (!body) return;
  const cur = S.doc.rev;
  body.innerHTML = `<ul class="tl">${S.history.map((h) => {
    const k = KIND[h.kind] || KIND.edit;
    const open = S.openRev === h.rev;
    const withLabels = (h.changes || []).map((ch) => ({ ...ch, label: rowLabel(S.doc.sheets.find((s) => s.name === ch.sheet), ch.r, ch.c) }));
    return `<li class="k-${h.kind} ${open ? "open" : ""}" data-rev="${h.rev}" style="${open ? "padding-right:10px" : ""}">
      <span class="dot">${k.icon}</span>
      <div class="rv-top"><b>Rev ${h.rev}</b>${h.rev === cur ? '<span class="pill st-approved nodot">Current</span>' : ""}<span class="when" title="${esc(fullTime(h.time))}">${timeAgo(h.time)}</span></div>
      <div class="rv-sub" style="margin-top:3px"><span class="avatar sm" style="width:20px;height:20px;font-size:9px">${esc(initials(h.user))}</span><b style="color:var(--ink-2)">${esc(h.user)}</b><span>· ${k.label}</span></div>
      ${h.note ? `<div class="rv-note">${esc(h.note)}</div>` : ""}
      <div class="rv-sub" style="margin-top:6px">
        ${h.changes?.length ? `<button data-act="toggle">${open ? "Hide" : "Show"} ${plural(h.changes.length, "change")}</button>` : `<span>${h.kind === "import" ? "Initial version" : "No cell changes"}</span>`}
        ${h.rev !== cur ? `<button data-act="view">View</button>` : ""}
        <button data-act="dl">Download</button>
        ${h.rev !== cur && !readOnly() ? `<button data-act="restore">Restore</button>` : ""}
      </div>
      ${open && h.changes?.length ? changesTable(withLabels, 200) : ""}
    </li>`;
  }).join("")}</ul>`;
  bindRefs(body);
  body.querySelectorAll("li").forEach((li) => {
    const rev = +li.dataset.rev;
    const h = S.history.find((x) => x.rev === rev);
    li.querySelectorAll("[data-act]").forEach((b) => b.addEventListener("click", () => {
      const act = b.dataset.act;
      if (act === "toggle") {
        S.openRev = S.openRev === rev ? null : rev;
        S.hl = S.openRev === rev ? highlightFrom(h) : null;
        paintDrawer(); renderSheet(); renderTabs();
        if (S.hl && h.changes.length) gotoCell(h.changes[0].sheet, h.changes[0].r, h.changes[0].c);
      } else if (act === "view") openDoc(S.doc.path, rev);
      else if (act === "dl") download(`/api/export?path=${enc(S.doc.path)}&rev=${rev}`, null, S.doc.file);
      else if (act === "restore") restoreRev(rev);
    }));
  });
}
function highlightFrom(h) {
  const sheetMap = {};
  for (const ch of h.changes || []) (sheetMap[ch.sheet] = sheetMap[ch.sheet] || new Set()).add(`${ch.r},${ch.c}`);
  return { rev: h.rev, sheet: sheetMap };
}
async function restoreRev(rev) {
  const ok = await modal({
    title: `Restore revision ${rev}?`,
    text: `The document will be put back exactly as it was in Rev ${rev}. This is saved as a <b>new revision</b>, so the current version stays in history and can be restored again.`,
    icon: I.restore, iconStyle: "background:#f4f3ff;color:#7a5af8;box-shadow:0 0 0 7px #f9f8ff",
    actions: [{ label: "Cancel" }, { label: `Restore Rev ${rev}`, primary: true, handler: () => postJSON("/api/restore", { path: S.doc.path, rev, user: S.user }) }],
  });
  if (!ok) return;
  toast(`Restored — saved as Rev ${ok.rev}`);
  S.edits = {};
  if (readOnly()) { S.doc = null; openDoc(ok.path || parseHash().path); return; }
  await reloadDoc(false);
}

// ---------------------------------------------------------------- global keys
document.addEventListener("keydown", (e) => {
  if (!S.doc || !$("#gridWrap")) return;
  const mod = e.ctrlKey || e.metaKey;
  if (mod && e.key.toLowerCase() === "s") { e.preventDefault(); if (!readOnly()) saveDialog(); }
  if (mod && e.key.toLowerCase() === "f") { e.preventDefault(); $("#findInput").focus(); $("#findInput").select(); }
});
let resizeT;
window.addEventListener("resize", () => {
  clearTimeout(resizeT);
  resizeT = setTimeout(() => { if (S.doc && $("#gridZoom table")) { if (S.zoomMode === "fit") setZoom(fitZoom(), "fit"); else applyFreeze(); } }, 150);
});
window.addEventListener("beforeunload", (e) => {
  if (S.doc && pendingCount()) { saveDraft(); e.preventDefault(); e.returnValue = ""; }
});
document.addEventListener("mousedown", (e) => {
  if (ddMenu && !ddMenu.contains(e.target) && !e.target.closest(".dd")) closeFloating();
});

// ---------------------------------------------------------------- boot
(async function boot() {
  paintUser();
  $("#userBtn").addEventListener("click", () => askUser(true));
  try { const w = localStorage.getItem("dochub:sidebar"); if (w) document.documentElement.style.setProperty("--sidebar", w); } catch (_) { /* ignore */ }
  bindSearch();
  try { await loadTree(); } catch (err) {
    $("#main").innerHTML = `<div class="page"><div class="empty-state"><div class="big">${I.alert}</div><h3>Cannot reach the DocHub server</h3><p>${esc(err.message)}</p></div></div>`;
    return;
  }
  window.addEventListener("hashchange", route);
  await route();
  if (!S.user) askUser();
})();
