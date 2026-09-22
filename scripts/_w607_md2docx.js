/**
 * _w607_md2docx.js — W607 S4 论文 Markdown → Word 投稿稿转换器（一次性·可重复执行）
 *
 * 用法：DOCX_NM=<docx模块路径> node scripts/_w607_md2docx.js <input.md> <output.docx>
 * 依赖：npm 包 docx（安装于 tmpe/w607_docxgen，经 DOCX_NM 环境变量引入，不入仓库依赖）
 *
 * 解析约定（与论文 md 结构强耦合，属专用转换器非通用 md 渲染器）：
 * - 首行 `# ` 为标题；标题后至首个 `---` 的引注块（> 行）跳过
 * - 尾部最后一个「后随 > 行的 ---」之后为仓库内部页脚，跳过
 * - `## X` → 一级节标题；`**表 N　…**` 全粗行 → 表题（表格上方·keepNext）
 * - `|` 行聚合为三线表；注释（①-⑯）/参考文献（[n]）条目 → 悬挂缩进五号
 * - 图 1/2 插入 §3 末，图 3-6 插入 §5 末（图注格式：图 N　图名（来源））
 * - 行内 **粗体** 与 *斜体* 解析为对应 TextRun；反引号剥除
 */
const fs = require("fs");
const path = require("path");
const docx = require(process.env.DOCX_NM || "docx");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  ImageRun, Header, Footer, PageNumber, AlignmentType, HeadingLevel,
  WidthType, BorderStyle,
} = docx;

const [, , inputMd, outputDocx] = process.argv;
if (!inputMd || !outputDocx) {
  console.error("usage: node _w607_md2docx.js <input.md> <output.docx>");
  process.exit(1);
}

const ROOT = "D:/xiyouji";
const FIGDIR = ROOT + "/docs/S4-学术投稿/图表";
// FIG5_OVERRIDE：匿名稿用顶栏裁除变体（scripts/_w608_crop_fig5.py 产出·双盲脱敏）
const FIG5 = process.env.FIG5_OVERRIDE || FIGDIR + "/图5-取经路线图-浅.png";

// ---------- 字体/版式常量（学术场景·纯黑正文） ----------
const F_BODY = { ascii: "Times New Roman", eastAsia: "SimSun" };
const F_HEAD = { ascii: "Times New Roman", eastAsia: "SimHei" };
const LINE = 360; // 1.5x（学术场景覆盖默认 1.3x）

// ---------- 图表配置 ----------
const FIGS = {
  "1": { file: FIGDIR + "/图1-文化母题转译流程.png", w: 540,
    cap: "图 1\u3000文化母题→设计令牌转译流程（来源：作者自绘）" },
  "2": { file: FIGDIR + "/图2-令牌三层模型.png", w: 430,
    cap: "图 2\u3000令牌架构三层模型（来源：作者自绘）" },
  "3": { file: FIGDIR + "/图3-人物语义网络-浅.png", w: 540,
    cap: "图 3\u3000人物语义网络页·浅色主题（来源：项目页面截图）" },
  "4": { file: FIGDIR + "/图4-八十一难难度热力图-浅.png", w: 540,
    cap: "图 4\u3000八十一难难度热力图·浅色主题（来源：项目页面截图）" },
  "5": { file: FIG5, w: 540,
    cap: "图 5\u3000取经路线图·浅色主题（来源：项目页面截图）" },
  "6": { file: FIGDIR + "/图6-用户研究设计.png", w: 540,
    cap: "图 6\u3000用户研究设计示意（来源：作者自绘）" },
};
const SECTION_FIGS = { "3": ["1", "2"], "5": ["3", "4", "5", "6"] };

function pngSize(buf) {
  return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
}

function figureBlock(no) {
  const cfg = FIGS[no];
  const buf = fs.readFileSync(cfg.file);
  const { w, h } = pngSize(buf);
  let dw = cfg.w;
  let dh = Math.round((dw * h) / w);
  const MAXH = 800; // 版心文字高约 929px：图+图注须同页，超限等比缩窄
  if (dh > MAXH) {
    dw = Math.round((MAXH * w) / h);
    dh = MAXH;
  }
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 200, line: LINE },
      keepNext: true,
      children: [new ImageRun({ data: buf, transformation: { width: dw, height: dh }, type: "png" })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 60, after: 200, line: LINE },
      children: [new TextRun({ text: cfg.cap, size: 21, font: F_BODY, color: "000000" })],
    }),
  ];
}

// ---------- 行内解析：**粗体** / *斜体* / 反引号剥除 ----------
function inlineRuns(text, baseSize) {
  const runs = [];
  const boldParts = text.split("**");
  boldParts.forEach((seg, i) => {
    const bold = i % 2 === 1;
    const italParts = seg.split("*");
    italParts.forEach((seg2, j) => {
      if (!seg2) return;
      runs.push(new TextRun({
        text: seg2.replace(/`/g, ""),
        bold: bold || undefined,
        italics: j % 2 === 1 || undefined,
        size: baseSize, font: F_BODY, color: "000000",
      }));
    });
  });
  return runs;
}

function bodyPara(text) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    indent: { firstLine: 480 },
    spacing: { line: LINE },
    children: inlineRuns(text, 24),
  });
}

function labeledPara(text) {
  // 「**标签**：内容」或「**English Title**: content」——无首行缩进
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { before: 60, line: LINE },
    children: inlineRuns(text, 24),
  });
}

function notePara(text) {
  // 注释/参考文献条目：悬挂缩进·五号
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    indent: { left: 420, hanging: 420 },
    spacing: { line: LINE },
    children: inlineRuns(text, 21),
  });
}

function headingPara(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 200, line: LINE },
    children: [new TextRun({ text, bold: true, size: 28, font: F_HEAD, color: "000000" })],
  });
}

function captionPara(text) {
  // 表题：表格上方·居中·keepNext
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    keepNext: true,
    spacing: { before: 200, after: 80, line: LINE },
    children: inlineRuns(text, 21),
  });
}

function threeLineTable(rows) {
  const widths = [16, 30, 26, 28]; // 表 1 四列：文化层/令牌/值/语义角色
  const NB = { style: BorderStyle.NONE };
  const mkCell = (text, isHeader, colIdx) => new TableCell({
    borders: {
      top: NB, left: NB, right: NB,
      bottom: isHeader ? { style: BorderStyle.SINGLE, size: 2, color: "000000" } : NB,
    },
    margins: { top: 60, bottom: 60, left: 120, right: 120 },
    width: { size: widths[colIdx], type: WidthType.PERCENTAGE },
    children: [new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { line: LINE },
      children: inlineRuns(text, 21).map(r => r), // 粗体经行内解析保留
    })],
  });
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: "000000" },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: "000000" },
      left: NB, right: NB, insideHorizontal: NB, insideVertical: NB,
    },
    rows: rows.map((cells, ri) => new TableRow({
      tableHeader: ri === 0 || undefined,
      cantSplit: true,
      children: cells.map((c, ci) => {
        const cell = mkCell(c, ri === 0, ci);
        return cell;
      }),
    })),
  });
}

// ---------- 解析 md ----------
const raw = fs.readFileSync(inputMd, "utf-8");
const lines = raw.split(/\r?\n/);
const title = lines[0].replace(/^#\s+/, "");

// 跳过标题后的引注块：定位首个 --- 
let start = lines.findIndex((l, i) => i > 0 && l.trim() === "---");
// 尾部：最后一个后随 > 行的 --- 之后为内部页脚，截断
let end = lines.length;
for (let i = lines.length - 1; i > start; i--) {
  if (lines[i].trim() === "---") {
    const rest = lines.slice(i + 1).filter(l => l.trim());
    if (rest.length && rest.every(l => l.trim().startsWith(">"))) { end = i; break; }
  }
}

const children = [
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 240, line: Math.ceil(18 * 23), lineRule: "atLeast" },
    children: [new TextRun({ text: title, bold: true, size: 36, font: F_HEAD, color: "000000" })],
  }),
];

let curSection = null;
let tableBuf = [];
let firstBlockAfterTitle = true;

function flushTable() {
  if (!tableBuf.length) return;
  children.push(threeLineTable(tableBuf));
  children.push(new Paragraph({ spacing: { after: 120, line: LINE }, children: [] }));
  tableBuf = [];
}
function closeSection() {
  flushTable();
  if (curSection && SECTION_FIGS[curSection]) {
    SECTION_FIGS[curSection].forEach(no => children.push(...figureBlock(no)));
  }
}

for (let i = start + 1; i < end; i++) {
  const line = lines[i];
  const t = line.trim();
  if (t === "---" || t === "") { flushTable(); continue; }
  if (t.startsWith(">")) continue;

  if (t.startsWith("## ")) {
    closeSection();
    const h = t.slice(3).trim();
    const m = h.match(/^(\d)\s/);
    curSection = m ? m[1] : null;
    children.push(headingPara(h));
    continue;
  }

  if (t.startsWith("|")) {
    const cells = t.split("|").slice(1, -1).map(c => c.trim());
    if (cells.every(c => /^:?-{2,}:?$/.test(c))) continue; // 分隔行
    tableBuf.push(cells);
    continue;
  }

  const isNoteSection = (() => {
    // 判断当前处于注释/参考文献节：向前找最近的节标题
    for (let j = i - 1; j > start; j--) {
      const p = lines[j].trim();
      if (p.startsWith("## ")) return /注释|参考文献/.test(p);
      if (p === "---" || p === "") continue;
    }
    return false;
  })();

  if (/^\*\*表 \d/.test(t)) { children.push(captionPara(t)); continue; }
  if (/^\*\*[^*]+\*\*[：:]/.test(t) || /^\*\*(English Title|Abstract|Keywords)\*\*/.test(t)) {
    children.push(labeledPara(t)); continue;
  }
  if (/^[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯]/.test(t) || /^\[\d+\]/.test(t) || isNoteSection) {
    children.push(notePara(t)); continue;
  }
  children.push(bodyPara(t));
}
closeSection();

// ---------- 组装文档 ----------
const doc = new Document({
  creator: "",
  title: title,
  styles: {
    default: {
      document: {
        run: { font: F_BODY, size: 24, color: "000000" },
        paragraph: { spacing: { line: LINE } },
      },
      heading1: {
        run: { font: F_HEAD, size: 28, bold: true, color: "000000" },
        paragraph: { spacing: { before: 360, after: 200, line: LINE } },
      },
    },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1440, bottom: 1440, left: 1701, right: 1417, header: 850, footer: 992 },
      },
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ children: [PageNumber.CURRENT], size: 21, font: F_BODY })],
        })],
      }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(outputDocx, buf);
  console.log("written:", outputDocx, buf.length, "bytes,", children.length, "blocks");
});
