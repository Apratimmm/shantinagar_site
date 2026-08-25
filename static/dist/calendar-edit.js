// Calendar editor: rendering, event editing, and saving.
// Server-provided data is injected inline (SERVER_DATA) and the Django URL
// for POST is passed via window.UPDATE_URL — this file itself is cached.

const SERVER_DATA = JSON.parse(
  document.getElementById("server-data")?.textContent || '{"hasData":false}'
);
const UPDATE_URL = window.UPDATE_URL || "/calendar/update/";

const MONTH_NAMES = [
  "Baishakh", "Jestha", "Ashadh", "Shrawan",
  "Bhadra", "Ashwin", "Kartik", "Mangsir",
  "Poush", "Magh", "Falgun", "Chaitra",
];

const WEEKDAYS = ["S", "M", "T", "W", "T", "F", "S"];

// ---- Storage for user-added events (per rendered month) ----
const EXTRA_STORE = "schoolCalendarExtras";
const EXTRA = loadExtras();

function loadExtras() {
  try {
    const raw = localStorage.getItem(EXTRA_STORE);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

function saveExtras() {
  try {
    localStorage.setItem(EXTRA_STORE, JSON.stringify(EXTRA));
  } catch {
    /* storage unavailable — keep working in-session */
  }
}

// Stable identity for the month currently being rendered, so extras persist
// per month even across different month names / custom inputs.
function monthId(monthIndex, monthName) {
  return monthIndex !== -1
    ? "i:" + monthIndex
    : "n:" + (monthName || "").toLowerCase();
}

function monthIndexFromName(name) {
  const norm = (name || "").trim().toLowerCase();
  return MONTH_NAMES.findIndex((m) => m.toLowerCase() === norm);
}

// Read current form values in one place — avoids repeated DOM queries.
function readFormValues() {
  return {
    name: document.getElementById("month-name").value.trim() || "Mangsir",
    days: parseInt(document.getElementById("day-count").value, 10) || 31,
    start: parseInt(document.getElementById("start-day").value, 10) || 0,
  };
}

// Merge server events + user extras for the given month name.
function mergeEvents(name) {
  const serverEvents =
    SERVER_DATA.hasData && name === SERVER_DATA.monthName
      ? SERVER_DATA.events || {}
      : {};
  return Object.assign({}, serverEvents, EXTRA[currentMonthId] || {});
}

// Render a single month card. `extraByDay` maps day -> { label, type }.
// Server events and user-added events are both passed in via this object;
// user extras take precedence over server events for the same day.
function renderMonth(monthName, daysInMonth, firstDay, extraByDay) {
  const extra = extraByDay || {};

  // Pre-compute the set of weekend days once; both cell styling and the
  // event list reuse this set instead of recalculating weekday per day twice.
  const weekendDays = new Set();
  for (let d = 1; d <= daysInMonth; d++) {
    const weekday = (firstDay + d - 1) % 7;
    if (weekday === 0 || weekday === 6) weekendDays.add(d);
  }

  // Every Saturday and Sunday is a weekend holiday. All other events
  // are added by users.
  const regularFor = (day) =>
    weekendDays.has(day)
      ? { label: "Weekend", type: "holiday" }
      : null;

  // User-added events take precedence so the cell reflects what you set.
  const eventFor = (day) => {
    const ex = extra[day];
    return ex ? ex : regularFor(day);
  };

  const cells = [];
  for (let i = 0; i < firstDay; i++)
    cells.push('<div class="aspect-square"></div>');

  for (let d = 1; d <= daysInMonth; d++) {
    const ev = eventFor(d);
    const tone = ev
      ? ev.type === "holiday"
        ? "bg-red-500/15 text-red-600 font-semibold text-destructive"
        : "bg-primary/15 font-semibold text-primary"
      : "text-foreground/70";

    const title = ev ? ev.label : "Click to add an event";

    cells.push(
      `<div data-day="${d}"
            title="${title}"
            class="day-cell flex aspect-square cursor-pointer items-center justify-center rounded-lg text-sm ${tone} transition-colors hover:bg-secondary">`
      + d +
      `</div>`
    );
  }

  // Combine weekend holidays + user-added events, sorted by day.
  const combined = [];
  for (const d of weekendDays.keys()) {
    combined.push({ day: d, label: "Weekend", type: "holiday" });
  }
  // User-added events replace auto weekends for their day
  Object.entries(extra).forEach(([dayStr, ev]) => {
    const day = Number(dayStr);
    const idx = combined.findIndex((e) => e.day === day);
    if (idx !== -1) combined.splice(idx, 1);
    combined.push({ day, label: ev.label, type: ev.type });
  });
  combined.sort((a, b) => a.day - b.day);

  // Weekends are visible on the grid (as holiday cells) but omitted
  // from the legend list to keep it focused on actual events.
  const legendEvents = combined.filter((e) => e.label !== "Weekend");

  let list = "";
  if (legendEvents.length) {
    list = `<ul class="mt-5 space-y-2 border-t border-border pt-4 text-sm">
      ${legendEvents
        .map(
          (e) => `
        <li class="flex items-start gap-3">
          <span class="mt-1.5 h-2 w-2 shrink-0 rounded-full ${
            e.type === "holiday" ? "bg-destructive" : "bg-primary"
          }"></span>
          <span>
            <span class="font-mono text-xs uppercase tracking-widest text-muted-foreground">
              ${e.day}
            </span>
            <br />${e.label}
          </span>
        </li>`
        )
        .join("")}
    </ul>`;
  }

  return `
    <div class="rounded-2xl border border-border bg-card p-6 shadow">
      <h3 class="font-display text-lg font-bold tracking-tight">
        ${monthName}
      </h3>
      <div class="mt-4 grid grid-cols-7 gap-1 text-center font-mono text-xs uppercase tracking-widest text-muted-foreground">
        ${WEEKDAYS.map((d) => `<div class="py-1">${d}</div>`).join("")}
      </div>
      <div class="mt-1 grid grid-cols-7 gap-1">${cells.join("")}</div>
      ${list}
    </div>`;
}

// ---- Host wiring ----
const form = document.getElementById("month-form");
const out = document.getElementById("month");
const legend = document.getElementById("legend");
const editor = document.getElementById("editor");
const editorForm = document.getElementById("editor-form");
const editorDay = document.getElementById("editor-day");
const editorLabel = document.getElementById("editor-label");
const editorType = document.getElementById("editor-type");
const editorRemove = document.getElementById("editor-remove");
const editorCancel = document.getElementById("editor-cancel");

const createBtn = document.getElementById("create-calender");
const createBtnText = document.getElementById("create-calender-text");
const createBtnSpinner = document.getElementById("create-calender-spinner");
const saveMessage = document.getElementById("save-message");

let currentMonthId = null;
let currentEditDay = null;

function renderFromInputs() {
  const { name, days, start } = readFormValues();

  const monthIndex = monthIndexFromName(name);
  currentMonthId = monthId(monthIndex, name);

  const extra = mergeEvents(name);

  out.innerHTML = renderMonth(name, days, start, extra);
  legend.classList.remove("hidden");
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function showSaveMessage(text, isError) {
  saveMessage.textContent = text;
  saveMessage.className = "pt-2 text-center text-sm " + (isError
    ? "text-destructive"
    : "text-green-600");
  saveMessage.classList.remove("hidden");
}

function hideSaveMessage() {
  saveMessage.classList.add("hidden");
}

async function update_month() {
  const { name, days, start } = readFormValues();

  createBtn.disabled = true;
  createBtnText.textContent = "Saving…";
  hideSaveMessage();

  const allEvents = mergeEvents(name);

  const eventsList = Object.entries(allEvents).map(([day, ev]) => ({
    event_date: Number(day),
    event_name: ev.label,
    event_type: ev.type,
  }));

  try {
    const response = await fetch(UPDATE_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        monthName: name,
        daysInMonth: days,
        startDay: start,
        events: eventsList,
      }),
    });
    const data = await response.json();

    // Reset loading state
    createBtn.disabled = false;
    createBtnText.textContent = "Create calendar";
    createBtnSpinner.classList.add("hidden");

    if (data.success) {
      showSaveMessage(data.message, false);
      setTimeout(() => location.reload(), 1500);
    } else {
      showSaveMessage("Error: " + data.message, true);
    }
  } catch (err) {
    console.error("Failed to save calendar:", err);
    createBtn.disabled = false;
    createBtnText.textContent = "Create calendar";
    createBtnSpinner.classList.add("hidden");
    showSaveMessage("Failed to save calendar.", true);
  }
}

function openEditor(day) {
  currentEditDay = day;
  editorDay.textContent = day;

  const { name } = readFormValues();
  const serverEvents = SERVER_DATA.hasData && name === SERVER_DATA.monthName ? SERVER_DATA.events || {} : {};
  const extraEvents = EXTRA[currentMonthId] || {};
  const existing = extraEvents[day] || serverEvents[day];

  editorLabel.value = existing ? existing.label : "";
  editorType.value = existing ? existing.type : "event";
  editorRemove.classList.toggle("hidden", !existing);
  editor.classList.remove("hidden");
  editor.style.display = "flex";
  editorLabel.focus();
}

function closeEditor() {
  editor.style.display = "none";
  editor.classList.add("hidden");
  currentEditDay = null;
}

function saveEditor() {
  const label = editorLabel.value.trim();
  if (!label) return;
  if (!EXTRA[currentMonthId]) EXTRA[currentMonthId] = {};
  EXTRA[currentMonthId][currentEditDay] = {
    label,
    type: editorType.value,
  };
  saveExtras();
  closeEditor();
  renderFromInputs();
}

function removeEditor() {
  if (EXTRA[currentMonthId]) {
    delete EXTRA[currentMonthId][currentEditDay];
    if (Object.keys(EXTRA[currentMonthId]).length === 0)
      delete EXTRA[currentMonthId];
  }

  const { name } = readFormValues();
  if (SERVER_DATA.hasData && name === SERVER_DATA.monthName && SERVER_DATA.events) {
    delete SERVER_DATA.events[currentEditDay];
  }

  saveExtras();
  closeEditor();
  renderFromInputs();
}

// When the server supplied month data, pre-fill the form and render the
// calendar automatically.  Otherwise the user fills the inputs and clicks
// "Render calendar".
if (SERVER_DATA.hasData) {
  document.getElementById("month-name").value = SERVER_DATA.monthName;
  document.getElementById("day-count").value = String(SERVER_DATA.daysInMonth);
  document.getElementById("start-day").value = String(SERVER_DATA.firstDay);
  // Lock the month-name select — the server already picked this month.
  document.getElementById("month-name").disabled = true;
  renderFromInputs();
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  renderFromInputs();
});

createBtn.addEventListener("click", update_month);

out.addEventListener("click", (e) => {
  const cell = e.target.closest("[data-day]");
  if (!cell) return;
  openEditor(Number(cell.getAttribute("data-day")));
});

editorForm.addEventListener("submit", (e) => {
  e.preventDefault();
  saveEditor();
});
editorRemove.addEventListener("click", removeEditor);
editorCancel.addEventListener("click", closeEditor);
editor.addEventListener("click", (e) => {
  if (e.target === editor) closeEditor();
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && !editor.classList.contains("hidden"))
    closeEditor();
});
