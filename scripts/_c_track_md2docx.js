/**
 * _c_track_md2docx.js — C 轨论文（可验证性基础设施）Markdown → Word 投稿稿转换器（一次性·可重复执行）
 *
 * 用法：DOCX_NM=<docx模块路径> node scripts/_c_track_md2docx.js <input.md> <output.docx>
 * 依赖：npm 包 docx（复用 tmpe/w607_docxgen，经 DOCX_NM 环境变量引入）
 *
 * 与 _w607_md2docx.js（B 轨专用）的差异：
 * - [^n] 行内引用 → 真 Word 脚注（FootnoteReferenceRun），「## 注释」节的 [^n]: 定义 → 文档脚注表
 * - 图为「文内图注」形态：命中 **图 C-N　…** 行时于该处插入图片+图注（B 轨为按节注入）
 * - 「## 关联文档」仓库内部节整体剔除
 * - 生成后须以 _c_track_docx_footnote_fix.py 补 settings.xml 脚注编号（①②③·每页重排）
 */
const fs = require("fs");
const path = require("path");
const docx = require(process.env.DOCX_NM || "docx");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Header, Footer, PageNumber,
  AlignmentType, HeadingLevel, FootnoteReferenceRun,
} = docx;

const [, , inputMd, outputDocx] = process.argv;
if (!inputMd || !outputDocx) {
  console.error("usage: node _c_track_md2docx.js <input.md> <output.docx>");
  process.exit(1);
}

const ROOT = "D:/xiyouji";
const FIGDIR = ROOT + "/docs/S4-学术投稿/07-图表";
const C_FIGS = {
  1: FIGDIR + "/C-图1-三层体系.png",
  2: FIGDIR + "/C-图2-锚点查询实测.png",
  3: FIGDIR + "/C-图3-校验输出实测.png",
  4: FIGDIR + "/C-图4-门禁运行实测.png",
};
const FIG_W = { 1: 500, 2: 540, 3: 540, 4: 540 };

// ---------- 字体/版式（与 B 轨同基调·纯黑正文） ----------
const F_BODY = { ascii: "Times New Roman", eastAsia: "SimSun" };
const F_HEAD = { ascii: "Times New Roman", eastAsia: "SimHei" };
const LINE = 360;

function pngSize(buf) {
  return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
}

// ---------- 行内解析：[^n] 脚注引用 + **粗体** / *斜体* / 反引号剥除 ----------
// Word 要求脚注引用与脚注 1:1：同一 [^n] 的第 2+ 次出现自动生成「同注 N」新脚注（id 从 100 起）
const footnotes = {};
const seenRefs = new Set();
let tongzhuId = 100;

function parseInline(text, baseSize) {
  function segRuns(seg) {
    const out = [];
    seg.split("**").forEach((s, i) => {
      const bold = i % 2 === 1;
      s.split("*").forEach((s2, j) => {
        if (!s2) return;
        out.push(new TextRun({
          text: s2.replace(/`/g, ""),
          bold: bold || undefined,
          italics: j % 2 === 1 || undefined,
          size: baseSize, font: F_BODY, color: "000000",
        }));
      });
    });
    return out;
  }
  const out = [];
  for (const part of text.split(/(\[\^\d+\])/)) {
    const fm = part.match(/^\[\^(\d+)\]$/);
    if (fm) {
      const id = parseInt(fm[1], 10);
      if (seenRefs.has(id)) {
        footnotes[tongzhuId] = {
          children: [new Paragraph({
            spacing: { line: 276 },
            children: [new TextRun({ text: "同注 " + id + "。", size: 18, font: F_BODY, color: "000000" })],
          })],
        };
        out.push(new FootnoteReferenceRun(tongzhuId));
        tongzhuId += 1;
      } else {
        seenRefs.add(id);
        out.push(new FootnoteReferenceRun(id));
      }
      continue;
    }
    out.push(...segRuns(part));
  }
  return out;
}

function bodyPara(text) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    indent: { firstLine: 480 },
    spacing: { line: LINE },
    children: parseInline(text, 24),
  });
}

function labeledPara(text) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { before: 60, line: LINE },
    children: parseInline(text, 24),
  });
}

function bulletPara(text) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    indent: { left: 360, hanging: 240 },
    spacing: { line: LINE },
    children: parseInline("• " + text, 21),
  });
}

function headingPara(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 200, line: LINE },
    children: [new TextRun({ text, bold: true, size: 28, font: F_HEAD, color: "000000" })],
  });
}

function heading2Para(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 160, line: LINE },
    children: [new TextRun({ text, bold: true, size: 26, font: F_HEAD, color: "000000" })],
  });
}

function figureBlock(no, caption) {
  const buf = fs.readFileSync(C_FIGS[no]);
  const { w, h } = pngSize(buf);
  let dw = FIG_W[no] || 540;
  let dh = Math.round((dw * h) / w);
  const MAXH = 800;
  if (dh > MAXH) { dw = Math.round((MAXH * w) / h); dh = MAXH; }
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
      children: [new TextRun({ text: caption, size: 21, font: F_BODY, color: "000000" })],
    }),
  ];
}

// ---------- 解析 md ----------
const raw = fs.readFileSync(inputMd, "utf-8");
const lines = raw.split(/\r?\n/);
const title = lines[0].replace(/^#\s+/, "");

let start = lines.findIndex((l, i) => i > 0 && l.trim() === "---");
if (start < 0) start = 0;

const children = [
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 240, line: Math.ceil(18 * 23), lineRule: "atLeast" },
    children: [new TextRun({ text: title, bold: true, size: 36, font: F_HEAD, color: "000000" })],
  }),
];

function sectionNameAt(i) {
  for (let j = i - 1; j >= 0; j--) {
    const p = lines[j].trim();
    if (p.startsWith("## ")) return p.slice(3).trim();
  }
  return "";
}

for (let i = start + 1; i < lines.length; i++) {
  const t = lines[i].trim();
  if (t === "") continue;
  const sec = sectionNameAt(i);
  if (sec === "关联文档" || t === "## 关联文档") continue; // 仓库内部节剔除（标题行自身亦命中）
  if (t === "---" || t.startsWith(">")) continue;

  // 脚注定义行（集中于「## 注释」节）→ 文档脚注表，不入正文
  const fd = t.match(/^\[\^(\d+)\]:\s*(.+)$/);
  if (fd) {
    footnotes[parseInt(fd[1], 10)] = fd[2];
    continue;
  }
  if (t === "## 注释") continue; // 脚注化后注释节不再成节

  if (t.startsWith("## ")) { children.push(headingPara(t.slice(3).trim())); continue; }
  if (t.startsWith("### ")) { children.push(heading2Para(t.slice(4).trim())); continue; }

  const figCap = t.match(/^\*\*图 C-([1-4])　([^*]+)\*\*$/);
  if (figCap) {
    children.push(...figureBlock(parseInt(figCap[1], 10), "图 C-" + figCap[1] + "　" + figCap[2]));
    continue;
  }
  if (t.startsWith("- ")) { children.push(bulletPara(t.slice(2))); continue; }
  if (/^\*\*[^*]+\*\*[：:]/.test(t)) { children.push(labeledPara(t)); continue; }
  children.push(bodyPara(t));
}

// ---------- 组装文档（脚注表随文档注入） ----------
const footnoteMap = {};
for (const [id, val] of Object.entries(footnotes)) {
  // 字符串 = md 脚注定义（解析行内标记）；对象 = 同注条目（已构建）
  footnoteMap[id] = typeof val === "string"
    ? { children: [new Paragraph({
        alignment: AlignmentType.JUSTIFIED,
        indent: { left: 240, hanging: 240 },
        spacing: { line: 276 },
        children: parseInline(val, 18),
      })] }
    : val;
}

const doc = new Document({
  creator: "",
  title,
  footnotes: footnoteMap,
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
      heading2: {
        run: { font: F_HEAD, size: 26, bold: true, color: "000000" },
        paragraph: { spacing: { before: 280, after: 160, line: LINE } },
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
  const refs = Object.keys(footnotes).length;
  console.log("written:", outputDocx, buf.length, "bytes,", children.length, "blocks, footnotes:", refs);
});
