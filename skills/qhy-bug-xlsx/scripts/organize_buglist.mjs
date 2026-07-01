import fs from "node:fs/promises";
import path from "node:path";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const artifactToolPath = require.resolve("@oai/artifact-tool", {
  paths: [
    process.env.ARTIFACT_TOOL_NODE_MODULES || process.cwd(),
    process.cwd(),
  ],
});
const { FileBlob, SpreadsheetFile, Workbook } = await import(artifactToolPath);

const [inputPath, outDirArg, outputNameArg] = process.argv.slice(2);

if (!inputPath || !outDirArg) {
  console.error("Usage: node organize_buglist.mjs <input.xlsx> <output-dir> [output-name.xlsx]");
  process.exit(2);
}

const outDir = path.resolve(outDirArg);
const outputName = outputNameArg || `${path.basename(inputPath, path.extname(inputPath))}_整理版.xlsx`;
const outputPath = path.join(outDir, outputName);

function excelSerialToDate(value) {
  if (typeof value !== "number") return null;
  return new Date(Math.round((value - 25569) * 86400 * 1000));
}

function cleanText(value) {
  return String(value ?? "").replace(/\s+/g, " ").trim();
}

function severityNo(value) {
  const m = cleanText(value).match(/^(\d+)/);
  return m ? Number(m[1]) : null;
}

function normalizeSolution(raw) {
  let s = cleanText(raw).replace(/（/g, "(").replace(/）/g, ")");
  s = s.replace(/\(#fixed\)/gi, "")
    .replace(/\(#external\)/gi, "")
    .replace(/\(#postponed\)/gi, "")
    .replace(/\(#notrepro\)/gi, "")
    .replace(/\(#bydesign\)/gi, "")
    .replace(/\(#willnotfix\)/gi, "")
    .replace(/\(#duplicate\)/gi, "");
  return s.trim();
}

function statusCategory(solution) {
  const raw = cleanText(solution);
  const s = normalizeSolution(solution);
  if (/已解决|#fixed/i.test(raw)) return "已解决";
  if (/重复Bug|#duplicate/i.test(raw)) return "重复Bug";
  if (/不予解决|#willnotfix/i.test(raw)) return "不予解决";
  if (/外部原因|#external/i.test(raw)) return "外部原因";
  if (/设计如此|#bydesign/i.test(raw)) return "设计如此";
  if (/无法重现|未复现|#notrepro/i.test(raw)) return "无法重现";
  if (/延期|可延期|转任务|7月处理|下次处理|#postponed/i.test(raw)) return "延期/转任务";
  if (/需处理|未处理|可处理|观察/.test(s)) return "待处理";
  return s || "未分类";
}

function actionSuggestion(solution) {
  const status = statusCategory(solution);
  const s = normalizeSolution(solution);
  if (status === "待处理") return /观察/.test(s) ? "观察后确认" : "待开发处理";
  if (status === "延期/转任务") return /7月/.test(s) ? "7月排期跟进" : "排期跟进";
  if (["无法重现", "设计如此", "不予解决", "重复Bug"].includes(status)) return "关闭前确认";
  if (status === "外部原因") return "外部原因确认";
  if (status === "已解决") return "回归验证";
  return "待确认";
}

function planHint(solution) {
  const s = normalizeSolution(solution);
  if (/7月/.test(s)) return "7月处理";
  if (/下次/.test(s)) return "下次处理";
  if (/延期|可延期/.test(s)) return "延期";
  if (/不影响本次发布/.test(s)) return "不影响本次发布";
  if (/观察/.test(s)) return "观察处理";
  return "";
}

function moduleOf(title) {
  const t = cleanText(title);
  const pairs = [
    ["指挥调度", /指挥调度|调度会议/],
    ["融合会议", /融合会议/],
    ["简易会议", /简易会议|快速会议|多人会议/],
    ["共享/协作", /共享|协作|屏幕共享/],
    ["地图/定位", /地图|定位|位置上报|标会|标绘/],
    ["图像资源", /图像资源|预置位/],
    ["日程/预定会议", /日程|预定会议|最近会议/],
    ["IM/通话", /IM|语音通话|微信视频电话/],
    ["转写/AI", /转写|字幕|华智ai|华智AI|会议纪要/],
    ["设备/登录", /登录|设备|上线|下线|内网|外网/],
    ["性能/后台", /CPU|cpu|发烫|挂机|息屏|后台|多任务|卡顿|未响应/],
    ["音视频", /视频|音频|麦克风|摄像头|蓝牙|耳机|声音|黑屏|图像/],
  ];
  for (const [name, regex] of pairs) {
    if (regex.test(t)) return name;
  }
  return "其他";
}

function noteOf(value) {
  if (typeof value === "number") return "";
  return cleanText(value);
}

function overviewOf(title) {
  let text = cleanText(title)
    .replace(/^\s*[（(]T0[）)]\s*/i, "")
    .replace(/^\s*[（(]华平会议[）)]\s*/i, "")
    .replace(/^华平会议[）)]?/, "")
    .replace(/，?如图。?$/g, "")
    .replace(/，?如视频。?$/g, "")
    .trim();
  return text.length > 42 ? `${text.slice(0, 42)}...` : text;
}

const sourceWorkbook = await SpreadsheetFile.importXlsx(await FileBlob.load(inputPath));
const allRows = [];

for (let i = 0; i < sourceWorkbook.worksheets.items.length; i++) {
  const sheet = sourceWorkbook.worksheets.getItemAt(i);
  const used = sheet.getUsedRange();
  if (!used) continue;
  const values = used.values;
  if (!values || values.length < 2) continue;
  const header = values[0].map(cleanText);
  const bugIdIx = header.findIndex((h) => /bug编号|bug id|缺陷编号|编号/i.test(h));
  const titleIx = header.findIndex((h) => /bug标题|标题|问题|描述/i.test(h));
  const severityIx = header.findIndex((h) => /严重程度|严重级别|优先级|级别/i.test(h));
  const solutionIx = header.findIndex((h) => /解决方案|处理|状态|结论/i.test(h));
  const dateIx = header.findIndex((h) => /解决日期|关闭日期|日期/i.test(h));
  if (bugIdIx < 0 || titleIx < 0) continue;

  for (const row of values.slice(1)) {
    if (!cleanText(row[bugIdIx]) && !cleanText(row[titleIx])) continue;
    const solutionRaw = solutionIx >= 0 ? row[solutionIx] : "";
    const dateRaw = dateIx >= 0 ? row[dateIx] : "";
    allRows.push({
      source: sheet.name,
      bugId: cleanText(row[bugIdIx]),
      title: cleanText(row[titleIx]),
      severity: severityIx >= 0 ? cleanText(row[severityIx]) : "",
      severityNo: severityIx >= 0 ? severityNo(row[severityIx]) : null,
      status: statusCategory(solutionRaw),
      solution: normalizeSolution(solutionRaw),
      action: actionSuggestion(solutionRaw),
      plan: planHint(solutionRaw),
      module: moduleOf(row[titleIx]),
      resolvedDate: excelSerialToDate(dateRaw),
      note: noteOf(dateRaw),
    });
  }
}

if (allRows.length === 0) {
  throw new Error("No bug rows found. Expected columns like Bug编号 and Bug标题.");
}

const priorityOrder = new Map([
  ["待处理", 1],
  ["延期/转任务", 2],
  ["无法重现", 3],
  ["外部原因", 4],
  ["已解决", 5],
  ["设计如此", 6],
  ["不予解决", 7],
  ["重复Bug", 8],
]);

allRows.sort((a, b) => {
  const pa = priorityOrder.get(a.status) ?? 99;
  const pb = priorityOrder.get(b.status) ?? 99;
  if (pa !== pb) return pa - pb;
  if ((a.severityNo ?? 9) !== (b.severityNo ?? 9)) return (a.severityNo ?? 9) - (b.severityNo ?? 9);
  return Number(b.bugId) - Number(a.bugId);
});

const wb = Workbook.create();
const summary = wb.worksheets.add("总览");
const detail = wb.worksheets.add("全部明细");
const t0Detail = wb.worksheets.add("T0明细");

const headers = ["来源", "Bug编号", "严重级别", "级别数", "状态归类", "模块", "处理建议", "计划/提示", "解决日期", "Bug标题", "原解决方案", "备注"];
const rowToArray = (r) => [r.source, r.bugId, r.severity, r.severityNo, r.status, r.module, r.action, r.plan, r.resolvedDate, r.title, r.solution, r.note];

function applySheetBase(sheet) {
  sheet.showGridLines = false;
}

function styleTitle(sheet, title, subtitle = "") {
  sheet.getRange("A1:L1").merge();
  sheet.getRange("A1").values = [[title]];
  sheet.getRange("A1").format.font = { bold: true, fontSize: 18, color: "#111827" };
  sheet.getRange("A1").format.fill = { color: "#EAF2FF" };
  sheet.getRange("A1").format.rowHeight = 28;
  if (subtitle) {
    sheet.getRange("A2:L2").merge();
    sheet.getRange("A2").values = [[subtitle]];
    sheet.getRange("A2").format.font = { fontSize: 10, color: "#4B5563" };
    sheet.getRange("A2").format.fill = { color: "#F8FAFC" };
    sheet.getRange("A2").format.rowHeight = 24;
  }
}

function writeTable(sheet, title, rows, tableName) {
  applySheetBase(sheet);
  styleTitle(sheet, title, `共 ${rows.length} 条。已做状态归类、模块归类、日期/备注拆分，标题保留原文。`);
  const data = [headers, ...rows.map(rowToArray)];
  const range = sheet.getRangeByIndexes(3, 0, data.length, headers.length);
  range.values = data;
  range.format.wrapText = true;
  range.format.font = { fontSize: 10, color: "#111827" };
  const headerRange = sheet.getRangeByIndexes(3, 0, 1, headers.length);
  headerRange.format.fill = { color: "#E5E7EB" };
  headerRange.format.font = { bold: true, color: "#111827" };
  headerRange.format.horizontalAlignment = "center";
  headerRange.format.rowHeight = 24;
  const bodyRows = Math.max(rows.length, 1);
  const bodyRange = sheet.getRangeByIndexes(4, 0, bodyRows, headers.length);
  bodyRange.format.rowHeight = 40;
  sheet.getRangeByIndexes(4, 8, bodyRows, 1).setNumberFormat("yyyy-mm-dd");
  sheet.getRange("A:D").format.horizontalAlignment = "center";
  sheet.getRange("E:I").format.horizontalAlignment = "center";
  sheet.getRange("J:L").format.horizontalAlignment = "left";
  sheet.getRange("A:A").format.columnWidth = 12;
  sheet.getRange("B:B").format.columnWidth = 11;
  sheet.getRange("C:D").format.columnWidth = 10;
  sheet.getRange("E:E").format.columnWidth = 14;
  sheet.getRange("F:F").format.columnWidth = 14;
  sheet.getRange("G:H").format.columnWidth = 14;
  sheet.getRange("I:I").format.columnWidth = 13;
  sheet.getRange("J:J").format.columnWidth = 78;
  sheet.getRange("K:K").format.columnWidth = 30;
  sheet.getRange("L:L").format.columnWidth = 28;
  sheet.freezePanes.freezeRows(4);
  if (rows.length > 0) {
    const table = sheet.tables.add(`A4:L${rows.length + 4}`, true, tableName);
    table.style = "TableStyleLight1";
    table.showFilterButton = true;
  }
}

function countBy(rows, field) {
  return Array.from(new Set(rows.map((r) => r[field])))
    .map((value) => [value, rows.filter((r) => r[field] === value).length]);
}

function writeSummary(sheet, rows) {
  applySheetBase(sheet);
  styleTitle(sheet, "总览", "按状态、模块和优先级聚合，明细见后续工作表。");
  const pendingRows = rows.filter((r) => ["待处理", "延期/转任务"].includes(r.status));
  const metrics = [
    ["总 Bug 数", rows.length],
    ["T0 Bug 数", rows.filter((r) => /^t0$/i.test(r.source)).length],
    ["待处理/延期", pendingRows.length],
    ["P1 严重问题", rows.filter((r) => r.severityNo === 1).length],
    ["已解决", rows.filter((r) => r.status === "已解决").length],
  ];
  sheet.getRange("A4:B8").values = metrics;
  sheet.getRange("A4:A8").format.fill = { color: "#F3F4F6" };
  sheet.getRange("A4:A8").format.font = { bold: true, color: "#374151" };
  sheet.getRange("B4:B8").format.font = { bold: true, color: "#111827", fontSize: 14 };
  sheet.getRange("A4:B8").format.rowHeight = 24;

  const statusRows = countBy(rows, "status")
    .sort((a, b) => (priorityOrder.get(a[0]) ?? 99) - (priorityOrder.get(b[0]) ?? 99));
  sheet.getRange("D4:E4").values = [["状态归类", "数量"]];
  sheet.getRange(`D5:E${statusRows.length + 4}`).values = statusRows;
  sheet.getRange("D4:E4").format.fill = { color: "#E5E7EB" };
  sheet.getRange("D4:E4").format.font = { bold: true, color: "#111827" };
  sheet.getRange(`D4:E${statusRows.length + 4}`).format.rowHeight = 24;

  const moduleRows = countBy(rows, "module").sort((a, b) => b[1] - a[1]);
  sheet.getRange("G4:H4").values = [["模块归类", "数量"]];
  sheet.getRange(`G5:H${moduleRows.length + 4}`).values = moduleRows;
  sheet.getRange("G4:H4").format.fill = { color: "#E5E7EB" };
  sheet.getRange("G4:H4").format.font = { bold: true, color: "#111827" };
  sheet.getRange(`G4:H${moduleRows.length + 4}`).format.rowHeight = 24;

  const focusRows = rows
    .filter((r) => r.severityNo === 1 || ["待处理", "延期/转任务"].includes(r.status))
    .slice(0, 20)
    .map((r) => [r.bugId, r.source, r.status, r.action, overviewOf(r.title)]);
  sheet.getRange("A12:E12").values = [["重点问题", "来源", "状态", "处理建议", "问题概览"]];
  if (focusRows.length) sheet.getRange(`A13:E${focusRows.length + 12}`).values = focusRows;
  sheet.getRange("A12:E12").format.fill = { color: "#E5E7EB" };
  sheet.getRange("A12:E12").format.font = { bold: true, color: "#111827" };
  sheet.getRange(`A12:E${focusRows.length + 12}`).format.rowHeight = 30;
  sheet.getRange("A:A").format.columnWidth = 14;
  sheet.getRange("B:B").format.columnWidth = 12;
  sheet.getRange("C:D").format.columnWidth = 14;
  sheet.getRange("E:E").format.columnWidth = 60;
  sheet.getRange("D:D").format.columnWidth = 16;
  sheet.getRange("G:G").format.columnWidth = 18;
  sheet.getRange("H:H").format.columnWidth = 10;
  sheet.getUsedRange().format.wrapText = true;
  sheet.getUsedRange().format.verticalAlignment = "top";
  sheet.freezePanes.freezeRows(3);
}

writeSummary(summary, allRows);
writeTable(detail, "全部明细", allRows, "AllBugsTable");
writeTable(t0Detail, "T0明细", allRows.filter((r) => /^t0$/i.test(r.source)), "T0BugsTable");

for (const sheet of wb.worksheets.items) {
  sheet.getUsedRange().format.verticalAlignment = "top";
}

await fs.mkdir(outDir, { recursive: true });

const errorScan = await wb.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "formula error scan",
});
console.log(errorScan.ndjson);

for (const sheetName of ["总览", "T0明细", "全部明细"]) {
  const preview = await wb.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
  await fs.writeFile(path.join(outDir, `preview_${sheetName}.png`), new Uint8Array(await preview.arrayBuffer()));
}

const output = await SpreadsheetFile.exportXlsx(wb);
await output.save(outputPath);
console.log(outputPath);
