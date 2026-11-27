(() => {
  "use strict";

  const API = (window.MOLE_API || "").replace(/\/$/, "");
  const FREE_LIMIT = 5;
  const PAID_LIMIT = 500;
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

  // ---------------------------------------------------------------- utils

  const esc = (v) =>
    String(v ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  const num = (v, d = 1) => (v === null || v === undefined || v === "" || isNaN(+v) ? "—" : (+v).toFixed(d));

  function tone(text) {
    const t = String(text || "").toLowerCase();
    if (t.includes("not") || t.includes("low") || t.includes("inactive") || t.includes("error")) return "bad";
    if (t.includes("medium") || t.includes("moderate")) return "warn";
    if (t.includes("high") || t.includes("drug-like") || t.includes("active")) return "good";
    return "neutral";
  }
  const badge = (text, t) => `<span class="badge b-${t || tone(text)}">${esc(text)}</span>`;

  const stats = (items) =>
    `<div class="stats">${items
      .map(([l, v, u]) => `<div class="stat"><div class="stat-l">${esc(l)}</div><div class="stat-v">${esc(v)}${u ? `<small>${esc(u)}</small>` : ""}</div></div>`)
      .join("")}</div>`;

  const bar = (v, max = 100) => `<div class="bar-t"><div class="bar-f" style="width:${Math.max(0, Math.min(100, (+v / max) * 100)) || 0}%"></div></div>`;

  const scoreBars = (items) =>
    `<div class="bars">${items
      .map(([l, v]) => `<div><div class="bar-h"><span>${esc(l)}</span><b>${num(v)}</b></div>${bar(v)}</div>`)
      .join("")}</div>`;

  const cellBar = (v, max = 100, d = 1) => `<div class="cell-bar">${bar(v, max)}<b>${num(v, d)}</b></div>`;

  function table(columns, rows) {
    const head = columns.map((c) => `<th class="${c.cls || ""}">${esc(c.label)}</th>`).join("");
    const body = rows
      .map((r) => `<tr>${columns.map((c) => `<td class="${c.cls || ""}">${c.render ? c.render(r[c.key], r) : esc(r[c.key] ?? "—")}</td>`).join("")}</tr>`)
      .join("");
    return `<div class="table-wrap"><table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div>`;
  }

  const kvTable = (obj) =>
    table(
      [
        { key: "k", label: "Property", cls: "k" },
        { key: "v", label: "Value", cls: "num" },
      ],
      Object.entries(obj || {}).map(([k, v]) => ({ k, v: typeof v === "number" ? +v.toFixed(3) : v })),
    );

  function hchart(counts) {
    const entries = Object.entries(counts).sort((a, b) => b[1] - a[1]);
    const max = Math.max(1, ...entries.map((e) => e[1]));
    return `<div class="hchart">${entries
      .map(([k, v]) => `<div class="hrow"><span title="${esc(k)}">${esc(k)}</span>${bar(v, max)}<b>${v}</b></div>`)
      .join("")}</div>`;
  }

  function tabs(id, names) {
    return `<div class="tabs" role="tablist">${names
      .map((n, i) => `<button type="button" role="tab" data-tabs="${id}" data-tab="${i}" aria-selected="${i === 0}">${esc(n)}</button>`)
      .join("")}</div>`;
  }
  const panel = (id, i, html) => `<div class="panel" data-panel="${id}-${i}" ${i ? "hidden" : ""}>${html}</div>`;

  document.addEventListener("click", (e) => {
    const t = e.target.closest("[data-tabs]");
    if (!t) return;
    const id = t.dataset.tabs;
    $$(`[data-tabs="${id}"]`).forEach((b) => b.setAttribute("aria-selected", b === t));
    $$(`[data-panel^="${id}-"]`).forEach((p) => (p.hidden = p.dataset.panel !== `${id}-${t.dataset.tab}`));
  });

  function download(name, content, type) {
    const blob = content instanceof Blob ? content : new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = Object.assign(document.createElement("a"), { href: url, download: name });
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function toCSV(rows, columns) {
    const cols = columns || Object.keys(rows[0] || {});
    const cell = (v) => {
      const s = v === null || v === undefined ? "" : String(v);
      return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
    };
    return [cols.join(","), ...rows.map((r) => cols.map((c) => cell(r[c])).join(","))].join("\n");
  }

  // ---------------------------------------------------------------- api

  async function request(path, options = {}, expect = "json") {
    let res;
    try {
      res = await fetch(API + path, options);
    } catch {
      throw new Error("Could not reach the MOLE-AI server. Check your connection and try again.");
    }
    if (!res.ok) {
      let msg = `Request failed (${res.status}).`;
      try {
        const body = await res.json();
        if (body.detail) msg = typeof body.detail === "string" ? body.detail : "Please check your input.";
      } catch { /* not json */ }
      throw new Error(msg);
    }
    return expect === "blob" ? res.blob() : res.json();
  }

  function busy(statusEl, label) {
    statusEl.innerHTML = `<div class="status"><span class="spinner"></span><span>${esc(label)}</span><span class="hint"></span></div>`;
    const timer = setTimeout(() => {
      const h = $(".hint", statusEl);
      if (h) h.textContent = "The server may be waking up. The first request can take up to a minute.";
    }, 5000);
    return () => {
      clearTimeout(timer);
      statusEl.innerHTML = "";
    };
  }
  const showError = (el, err) => (el.innerHTML = `<div class="alert">${esc(err.message || err)}</div>`);

  async function withButton(btn, fn) {
    btn.classList.add("busy");
    try {
      return await fn();
    } finally {
      btn.classList.remove("busy");
    }
  }

  // ---------------------------------------------------------------- routing

  const views = ["overview", "single", "batch", "similarity"];
  function route() {
    const v = views.includes(location.hash.slice(1)) ? location.hash.slice(1) : "overview";
    views.forEach((name) => ($(`#view-${name}`).hidden = name !== v));
    $$(".nav a").forEach((a) => (a.dataset.view === v ? a.setAttribute("aria-current", "page") : a.removeAttribute("aria-current")));
    window.scrollTo(0, 0);
  }
  window.addEventListener("hashchange", route);
  route();

  // Wake the API early so the first real request is faster.
  fetch(API + "/health").catch(() => {});

  // ---------------------------------------------------------------- file drops

  function dropZone(zoneId, inputId, nameId, onFile) {
    const zone = $(zoneId), input = $(inputId), name = $(nameId);
    const set = (file) => {
      if (!file) return;
      zone.classList.add("has");
      name.textContent = `${file.name} · ${(file.size / 1024).toFixed(1)} KB`;
      onFile(file);
    };
    input.addEventListener("change", () => set(input.files[0]));
    ["dragenter", "dragover"].forEach((ev) => zone.addEventListener(ev, (e) => { e.preventDefault(); zone.classList.add("over"); }));
    ["dragleave", "drop"].forEach((ev) => zone.addEventListener(ev, (e) => { e.preventDefault(); zone.classList.remove("over"); }));
    zone.addEventListener("drop", (e) => set(e.dataTransfer.files[0]));
  }

  async function countRows(file) {
    const text = await file.text();
    const lines = text.split(/\r?\n/).filter((l) => l.trim());
    const header = (lines[0] || "").split(",").map((h) => h.trim().toLowerCase().replace(/^"|"$/g, ""));
    return { count: Math.max(0, lines.length - 1), hasSmiles: header.includes("smiles") };
  }

  // ================================================================ single

  const singleForm = $("#single-form");
  const singleInput = $("#single-smiles");
  const singleStatus = $("#single-status");
  const singleResult = $("#single-result");
  let lastSingle = null;

  $$("[data-example]").forEach((b) =>
    b.addEventListener("click", () => {
      singleInput.value = b.dataset.example;
      singleForm.requestSubmit();
    }),
  );

  singleForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const smiles = singleInput.value.trim();
    if (!smiles) return showError(singleStatus, "Enter a SMILES string first.");
    const btn = $("button[type=submit]", singleForm);
    const done = busy(singleStatus, "Analysing molecule…");
    try {
      const data = await withButton(btn, () =>
        request("/analyze", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ smiles }) }),
      );
      done();
      lastSingle = data;
      renderSingle(data);
    } catch (err) {
      done();
      showError(singleStatus, err);
    }
  });

  // SVG markup produced by RDKit on our own API; only accept real <svg> roots.
  const svg = (markup) => (typeof markup === "string" && markup.trim().startsWith("<svg") ? markup : "");

  function renderSingle({ smiles, result, explanation, structure, analogue_structures: thumbs = {} }) {
    const r = result.ranking, q = result.qsar, a = result.admet;
    const ex = explanation || {};
    const scoreItems = [["Activity", r.activity_score], ["ADMET", r.admet_score]];
    if (ex.molecular_properties && ex.molecular_properties.score != null) scoreItems.push(["Molecular properties", ex.molecular_properties.score]);
    scoreItems.push(["Overall", r.overall_score]);

    const interp = [
      ["Activity", ex.activity && ex.activity.interpretation],
      ["ADMET", ex.admet && ex.admet.interpretation],
      ["Ranking", ex.ranking && ex.ranking.interpretation],
    ].filter((x) => x[1]);

    // optimisation
    const opt = result.optimization || {};
    let optHtml = `<p class="small">No optimisation analysis is available for this molecule.</p>`;
    if (Object.keys(opt).length) {
      const level = opt.optimization_priority || "Not available";
      const t = { High: "bad", Medium: "warn" }[level] || "good";
      const sugg = (opt.suggestions || []).map((s) => `<li>${esc(s)}</li>`).join("");
      optHtml = `
        <div class="mol">Optimisation need ${badge(level, t)}</div>
        <div class="two">
          <div><h3 class="sub-t">Suggestions</h3>${sugg ? `<ol class="list">${sugg}</ol>` : `<p class="small">No changes suggested.</p>`}</div>
          <div>${opt.properties && Object.keys(opt.properties).length ? `<h3 class="sub-t">Properties considered</h3>${kvTable(opt.properties)}` : ""}</div>
        </div>`;
    }

    // analogues
    const evald = (result.generated_candidate_evaluation || []).slice().sort((x, y) => (y.overall_score ?? 0) - (x.overall_score ?? 0));
    let anaHtml = `<p class="small">No analogues could be generated for this molecule.</p>`;
    if (evald.length) {
      const best = evald[0];
      anaHtml = `
        ${stats([["Analogues", evald.length], ["Best overall score", num(best.overall_score), "/ 100"], ["Top analogue", best.candidate_id || "—"]])}
        ${table(
          [
            { key: "candidate_id", label: "Structure", cls: "thumb", render: (v) => svg(thumbs[v]) || "—" },
            { key: "candidate_id", label: "ID" },
            { key: "smiles", label: "SMILES", cls: "smiles", render: (v) => `<span title="${esc(v)}">${esc(v)}</span>` },
            { key: "strategy", label: "Strategy" },
            { key: "similarity", label: "Similarity", render: (v) => cellBar(v, 1, 2) },
            { key: "predicted_pIC50", label: "pIC50", cls: "num", render: (v) => num(v, 2) },
            { key: "admet_score", label: "ADMET", cls: "num", render: (v) => num(v) },
            { key: "overall_score", label: "Overall", render: (v) => cellBar(v) },
            { key: "priority", label: "Priority", render: (v) => (v ? badge(v) : "—") },
          ],
          evald,
        )}
        <div class="actions"><button type="button" class="btn" id="dl-analogues">Download analogues (CSV)</button></div>
        <p class="small">Analogues are rule-based structural variants with predicted scores. They are hypotheses, not validated compounds.</p>`;
    } else if ((result.generation || []).length) {
      anaHtml = table(
        [
          { key: "candidate_id", label: "ID" },
          { key: "smiles", label: "SMILES", cls: "smiles" },
          { key: "strategy", label: "Strategy" },
          { key: "similarity", label: "Similarity", render: (v) => cellBar(v, 1, 2) },
        ],
        result.generation,
      );
    }

    const activity = String(q.activity_class || "—").replace(/ Activity$/, "");
    const desc = (result.chemistry && result.chemistry.descriptors) || {};
    const formula = desc.molecular_formula || desc.formula || desc["Molecular Formula"] || desc.MolecularFormula || "";

    singleResult.innerHTML = `
      <div class="results">
        <div class="mol"><span class="mol-s">${esc(smiles)}</span>${badge(r.priority)}</div>
        <div class="lead">
          ${svg(structure) ? `<figure class="struct" style="margin:0">${svg(structure)}<figcaption class="struct-c"><span>2D structure</span><span>${esc(formula)}</span></figcaption></figure>` : ""}
          <div>
            ${stats([
              ["Overall score", num(r.overall_score), "/ 100"],
              ["Predicted pIC50", num(q.predicted_pIC50, 2)],
              ["ADMET score", num(a.admet_score), "/ 100"],
              ["Activity", activity],
            ])}
            ${ex.recommendation ? `<div class="note"><div class="note-t">Recommendation</div>${esc(ex.recommendation)}</div>` : ""}
          </div>
        </div>
        ${tabs("s", ["Summary", "Properties", "Optimisation", "Analogues", "Export"])}
        ${panel("s", 0, `
          <div class="two">
            <div><h3 class="sub-t">Score profile</h3>${scoreBars(scoreItems)}</div>
            <div><h3 class="sub-t">Interpretation</h3>
              <div class="dl">${interp.map(([k, v]) => `<div class="dl-r"><div class="dl-k">${esc(k)}</div><div class="dl-v">${esc(v)}</div></div>`).join("")}</div>
              ${ex.summary ? `<details class="more"><summary>Full scientific summary</summary><div>${esc(ex.summary)}</div></details>` : ""}
            </div>
          </div>`)}
        ${panel("s", 1, `
          <div class="two even">
            <div><h3 class="sub-t">Molecular descriptors</h3>${kvTable(result.chemistry && result.chemistry.descriptors)}</div>
            <div><h3 class="sub-t">ADMET</h3>
              <div class="mol">Drug-likeness ${badge(a.drug_likeness || "—")}</div>
              ${a.properties ? kvTable(a.properties) : ""}
              <p class="small">QSAR model: ${esc(q.model || "—")}</p>
            </div>
          </div>`)}
        ${panel("s", 2, optHtml)}
        ${panel("s", 3, anaHtml)}
        ${panel("s", 4, `
          <h3 class="sub-t">Downloads</h3>
          <div class="actions">
            <button type="button" class="btn primary" id="dl-single-pdf">PDF report</button>
            <button type="button" class="btn" id="dl-single-json">Raw data (JSON)</button>
          </div>
          <details class="more"><summary>View raw analysis</summary><div><pre>${esc(JSON.stringify(result, null, 2))}</pre></div></details>`)}
      </div>`;

    const dlA = $("#dl-analogues");
    if (dlA) dlA.addEventListener("click", () => download("MOLE_AI_evaluated_generated_candidates.csv", toCSV(evald), "text/csv"));
    $("#dl-single-json").addEventListener("click", () =>
      download("MOLE_AI_analysis.json", JSON.stringify(result, null, 2), "application/json"),
    );
    $("#dl-single-pdf").addEventListener("click", (e) =>
      withButton(e.currentTarget, async () => {
        try {
          const blob = await request(
            "/analyze/report",
            { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ smiles: lastSingle.smiles }) },
            "blob",
          );
          download("MOLE_AI_single_molecule_report.pdf", blob);
        } catch (err) {
          alert(err.message);
        }
      }),
    );
  }

  // ================================================================ batch

  let batchFile = null;
  let batchRows = null;
  let batchColumns = null;
  const batchRun = $("#batch-run");
  const batchInfo = $("#batch-info");
  const accessField = $("#access-field");
  const batchStatus = $("#batch-status");
  const batchResult = $("#batch-result");

  $("#template-btn").addEventListener("click", () =>
    download(
      "MOLE_AI_molecular_library_template.csv",
      "compound_id,smiles\nCompound_001,CCO\nCompound_002,CCN\nCompound_003,c1ccccc1\nCompound_004,CC(=O)Oc1ccccc1C(=O)O\n",
      "text/csv",
    ),
  );

  dropZone("#batch-drop", "#batch-file", "#batch-file-name", async (file) => {
    batchFile = file;
    batchResult.innerHTML = "";
    batchStatus.innerHTML = "";
    const { count, hasSmiles } = await countRows(file);
    const paid = count > FREE_LIMIT;
    $("#plan-free").classList.toggle("on", !paid);
    $("#plan-paid").classList.toggle("on", paid);
    accessField.hidden = !paid || count > PAID_LIMIT;
    batchRun.disabled = !hasSmiles || count === 0 || count > PAID_LIMIT;
    if (!hasSmiles) batchInfo.innerHTML = `<div class="alert">No <code>smiles</code> column found in this file.</div>`;
    else if (count > PAID_LIMIT) batchInfo.innerHTML = `<div class="alert">This file has ${count} molecules; the limit is ${PAID_LIMIT}. Contact MOLE-AI for larger libraries.</div>`;
    else batchInfo.innerHTML = `<p style="margin:-4px 0 14px">${count} molecule${count === 1 ? "" : "s"} detected${paid ? " — a paid batch (€49) is required." : " — free tier."}</p>`;
  });

  function batchForm() {
    const fd = new FormData();
    fd.append("file", batchFile);
    const code = $("#access-code").value.trim();
    if (code) fd.append("access_code", code);
    return fd;
  }

  batchRun.addEventListener("click", async () => {
    if (!batchFile) return;
    const done = busy(batchStatus, "Screening library…");
    try {
      const data = await withButton(batchRun, () => request("/batch", { method: "POST", body: batchForm() }));
      done();
      batchRows = data.rows;
      batchColumns = data.columns;
      renderBatch();
    } catch (err) {
      done();
      showError(batchStatus, err);
    }
  });

  function renderBatch() {
    const ok = batchRows.filter((r) => r.Status === "Success").sort((a, b) => (b["Overall Score"] ?? 0) - (a["Overall Score"] ?? 0));
    const failed = batchRows.filter((r) => r.Status !== "Success");
    const scores = ok.map((r) => +r["Overall Score"]).filter((v) => !isNaN(v));
    const top = scores.length ? Math.max(...scores) : 0;
    const mean = scores.length ? scores.reduce((a, b) => a + b, 0) / scores.length : 0;

    const count = (key) => ok.reduce((acc, r) => ((acc[r[key] ?? "—"] = (acc[r[key] ?? "—"] || 0) + 1), acc), {});
    const byCompound = Object.fromEntries(ok.map((r) => [r["Compound ID"] || r.SMILES, +num(r["Overall Score"])]));

    const names = ["Ranking", "Distribution"];
    if (failed.length) names.push(`Errors (${failed.length})`);

    batchResult.innerHTML = `
      <div class="results">
        ${stats([
          ["Screened", batchRows.length],
          ["Successful", ok.length, `of ${batchRows.length}`],
          ["Top score", num(top), "/ 100"],
          ["Mean score", num(mean), "/ 100"],
        ])}
        <div class="actions">
          <button type="button" class="btn primary" id="dl-batch-csv">Download results (CSV)</button>
          <button type="button" class="btn" id="dl-batch-pdf">PDF report</button>
        </div>
        ${tabs("b", names)}
        ${panel("b", 0, ok.length ? table(
          [
            { key: "Rank", label: "#", cls: "num" },
            { key: "Compound ID", label: "Compound" },
            { key: "SMILES", label: "SMILES", cls: "smiles", render: (v) => `<span title="${esc(v)}">${esc(v)}</span>` },
            { key: "Molecular Formula", label: "Formula" },
            { key: "Predicted pIC50", label: "pIC50", cls: "num", render: (v) => num(v, 2) },
            { key: "Activity", label: "Activity", render: (v) => esc(String(v || "—").replace(/ Activity$/, "")) },
            { key: "ADMET Score", label: "ADMET", cls: "num", render: (v) => num(v) },
            { key: "Overall Score", label: "Overall", render: (v) => cellBar(v) },
            { key: "Priority", label: "Priority", render: (v) => (v ? badge(v) : "—") },
          ],
          ok,
        ) : `<p class="small">No molecules were screened successfully.</p>`)}
        ${panel("b", 1, ok.length ? `
          <div class="two even">
            <div><h3 class="sub-t">Activity</h3>${hchart(count("Activity"))}</div>
            <div><h3 class="sub-t">Priority</h3>${hchart(count("Priority"))}</div>
          </div>
          <h3 class="sub-t" style="margin-top:32px">Overall score by compound</h3>
          <div class="hchart">${Object.entries(byCompound)
            .map(([k, v]) => `<div class="hrow"><span title="${esc(k)}">${esc(k)}</span>${bar(v)}<b>${num(v)}</b></div>`)
            .join("")}</div>` : `<p class="small">No successful predictions to chart.</p>`)}
        ${failed.length ? panel("b", 2, table(
          [
            { key: "Compound ID", label: "Compound" },
            { key: "SMILES", label: "SMILES", cls: "smiles" },
            { key: "Status", label: "Reason" },
          ],
          failed,
        )) : ""}
      </div>`;

    $("#dl-batch-csv").addEventListener("click", () =>
      download("MOLE_AI_ranked_screening_results.csv", toCSV(batchRows, batchColumns), "text/csv"),
    );
    $("#dl-batch-pdf").addEventListener("click", (e) =>
      withButton(e.currentTarget, async () => {
        try {
          const blob = await request("/batch/report", { method: "POST", body: batchForm() }, "blob");
          download("MOLE_AI_batch_screening_report.pdf", blob);
        } catch (err) {
          alert(err.message);
        }
      }),
    );
  }

  // ================================================================ similarity

  let simFile = null;
  const simForm = $("#sim-form");
  const simStatus = $("#sim-status");
  const simResult = $("#sim-result");

  dropZone("#sim-drop", "#sim-file", "#sim-file-name", (file) => {
    simFile = file;
    simResult.innerHTML = "";
  });

  simForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = $("#sim-query").value.trim();
    if (!query) return showError(simStatus, "Enter a query SMILES first.");
    if (!simFile) return showError(simStatus, "Choose a library CSV first.");
    const fd = new FormData();
    fd.append("file", simFile);
    fd.append("query", query);
    fd.append("top_k", $("#sim-k").value || "10");
    const btn = $("button[type=submit]", simForm);
    const done = busy(simStatus, "Comparing fingerprints…");
    try {
      const data = await withButton(btn, () => request("/similarity", { method: "POST", body: fd }));
      done();
      renderSimilarity(data);
    } catch (err) {
      done();
      showError(simStatus, err);
    }
  });

  function renderSimilarity({ matches, library_size, query_structure }) {
    if (!matches.length) {
      simResult.innerHTML = `<div class="results"><p class="small">No valid molecules were found in the library.</p></div>`;
      return;
    }
    simResult.innerHTML = `
      <div class="results">
        <div class="lead">
          ${svg(query_structure) ? `<figure class="struct" style="margin:0">${svg(query_structure)}<figcaption class="struct-c"><span>Query</span><span>${esc($("#sim-query").value.trim())}</span></figcaption></figure>` : ""}
          <div>
            ${stats([
              ["Library", library_size],
              ["Shown", matches.length],
              ["Best match", matches[0].compound_id || "—"],
              ["Tanimoto", num(matches[0].similarity, 3)],
            ])}
          </div>
        </div>
        ${table(
          [
            { key: "structure", label: "Structure", cls: "thumb", render: (v) => svg(v) || "—" },
            { key: "compound_id", label: "Compound" },
            { key: "smiles", label: "SMILES", cls: "smiles", render: (v) => `<span title="${esc(v)}">${esc(v)}</span>` },
            { key: "similarity", label: "Tanimoto similarity", render: (v) => cellBar(v, 1, 3) },
          ],
          matches,
        )}
        <div class="actions"><button type="button" class="btn" id="dl-sim">Download results (CSV)</button></div>
      </div>`;
    $("#dl-sim").addEventListener("click", () =>
      download("MOLE_AI_similarity_results.csv", toCSV(matches, ["compound_id", "smiles", "similarity"]), "text/csv"),
    );
  }
})();
