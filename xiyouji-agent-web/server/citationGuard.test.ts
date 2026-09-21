// citationGuard.test.ts — W599 判定逻辑单测（node:test·经 tsx 运行）
// 运行：cd xiyouji-agent-web && node --import tsx --test server/citationGuard.test.ts
import { test } from "node:test";
import assert from "node:assert";
import path from "path";
import { fileURLToPath } from "url";
import { applyCitationGuard } from "./citationGuard.js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..", ".."); // 仓库根

test("真实路径转 GitHub blob 链接", () => {
  const r = applyCitationGuard("详见 docs/00-导读/术语表.md。", ROOT);
  assert.match(r.text, /\[docs\/00-导读\/术语表\.md\]\(https:\/\/github\.com\/1273984347\/xiyouji\/blob\/main\/docs\/00-导读\/术语表\.md\)/);
  assert.equal(r.unverified.length, 0);
  assert.equal(r.linked, 1);
});

test("伪造路径不删原文但文末警示", () => {
  const r = applyCitationGuard("依据 docs/00-导读/不存在的文件-xyz.md。", ROOT);
  assert.ok(r.text.includes("docs/00-导读/不存在的文件-xyz.md"), "原文保留");
  assert.ok(r.text.includes("⚠️ 未能核实的引用路径"));
  assert.equal(r.unverified.length, 1);
});

test("无路径文本零改动", () => {
  const t = "孙悟空被称为心猿，与六耳猕猴真假难辨。";
  const r = applyCitationGuard(t, ROOT);
  assert.equal(r.text, t);
  assert.equal(r.linked, 0);
  assert.equal(r.unverified.length, 0);
});

test("同一路径只链接一次（去重）", () => {
  const r = applyCitationGuard(
    "见 docs/00-导读/术语表.md 与 docs/00-导读/术语表.md 的关系。",
    ROOT
  );
  assert.equal(r.linked, 1);
  assert.equal((r.text.match(/blob\/main\//g) || []).length, 1);
});

test("空文本安全", () => {
  const r = applyCitationGuard("", ROOT);
  assert.equal(r.text, "");
});
