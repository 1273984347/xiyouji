import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { after, before, describe, it } from 'node:test';

import {
  computeContentVersion,
  extractContentBatch,
  readStatValue,
  writeContentVersionFile,
} from '../scripts/prepare-content.mjs';

const STATS_ENTITY = {
  a1_a6_docs: { domain: 'docs/01-06', value: 615 },
  html_total: { domain: 'site/**/*.html', value: 857 },
  visualization_pages: { domain: 'site/data', value: 87 },
};

async function writeFile(target, content) {
  await fs.mkdir(path.dirname(target), { recursive: true });
  await fs.writeFile(target, content, 'utf8');
}

/** 造一个假仓库：package.json / CHANGELOG.md / site/index.html / scripts/output/stats.json */
async function createFakeRepo({ changelog, withSite = true } = {}) {
  const repoRoot = await fs.mkdtemp(path.join(os.tmpdir(), 'xiyouji-prepare-'));
  await writeFile(path.join(repoRoot, 'package.json'), JSON.stringify({ name: 'xiyouji-desktop', version: '9.9.9' }));
  await writeFile(
    path.join(repoRoot, 'CHANGELOG.md'),
    changelog ??
      [
        '# 更新日志',
        '',
        '## [Unreleased]',
        '',
        '### W902（2030-01-02）：假批次段',
        '',
        '### W901（2030-01-01）：更旧的假批次段',
        '',
      ].join('\n'),
  );
  if (withSite) {
    await writeFile(path.join(repoRoot, 'site', 'index.html'), '<!doctype html><html><body>西游记</body></html>');
  }
  await writeFile(path.join(repoRoot, 'scripts', 'output', 'stats.json'), JSON.stringify(STATS_ENTITY, null, 2));
  return repoRoot;
}

describe('scripts/prepare-content.mjs 内容批次提取', () => {
  it('识别新形态「### W###（YYYY-MM-DD）」并取文档顺序首个', () => {
    // CHANGELOG 新段在上：文档顺序第一个 W 段即最新批次。
    const changelog = [
      '### W803（2026-10-19）：最新',
      '### W802（2026-10-18）：较旧',
    ].join('\n');
    assert.deepEqual(extractContentBatch(changelog), { contentBatch: 'W803', contentDate: '2026-10-19' });
  });

  it('识别历史形态「### vX.Y.Z（date）：W###」', () => {
    const changelog = '### v2.3.304（2026-10-11）：W710 收口批\n### v2.3.303（2026-10-10）：W709 分层批';
    assert.deepEqual(extractContentBatch(changelog), { contentBatch: 'W710', contentDate: '2026-10-11' });
  });

  it('新形态与历史形态混排时取位置最靠前者', () => {
    const changelog = [
      '### W803（2026-10-19）：新形态最新',
      '### v2.3.304（2026-10-11）：W710 历史形态',
    ].join('\n');
    assert.deepEqual(extractContentBatch(changelog), { contentBatch: 'W803', contentDate: '2026-10-19' });
  });

  it('无批次段时抛错', () => {
    assert.throws(() => extractContentBatch('# 更新日志\n\n没有批次段'), /未找到内容批次段/);
  });

  it('stats.json 同时支持实体 {value} 与裸数字', () => {
    assert.equal(readStatValue({ a1_a6_docs: { value: 615 } }, 'a1_a6_docs'), 615);
    assert.equal(readStatValue({ a1_a6_docs: 615 }, 'a1_a6_docs'), 615);
    assert.throws(() => readStatValue({}, 'a1_a6_docs'), /缺少有效数字字段/);
  });
});

describe('scripts/prepare-content.mjs computeContentVersion', () => {
  let repoRoot = '';

  before(async () => {
    repoRoot = await createFakeRepo();
  });

  after(async () => {
    await fs.rm(repoRoot, { recursive: true, force: true });
  });

  it('从假仓库提取批次、日期与三个计数', async () => {
    const version = await computeContentVersion({ repoRoot, desktopRoot: repoRoot });
    assert.equal(version.appVersion, '9.9.9');
    assert.equal(version.contentBatch, 'W902');
    assert.equal(version.contentDate, '2030-01-02');
    assert.equal(version.docCount, 615);
    assert.equal(version.pageCount, 857);
    assert.equal(version.vizCount, 87);
    assert.ok(!Number.isNaN(Date.parse(version.builtAt)), 'builtAt 应为可解析的 ISO 时间');
  });

  it('缺 site/index.html 时抛出明确错误', async () => {
    const noSiteRepo = await createFakeRepo({ withSite: false });
    try {
      assert.throws(
        () => computeContentVersion({ repoRoot: noSiteRepo, desktopRoot: noSiteRepo }),
        /缺少站点入口文件/,
      );
    } finally {
      await fs.rm(noSiteRepo, { recursive: true, force: true });
    }
  });

  it('缺 stats.json 时抛出明确错误', async () => {
    const noStatsRepo = await createFakeRepo();
    await fs.rm(path.join(noStatsRepo, 'scripts'), { recursive: true, force: true });
    try {
      assert.throws(
        () => computeContentVersion({ repoRoot: noStatsRepo, desktopRoot: noStatsRepo }),
        /读取 .*stats\.json 失败/,
      );
    } finally {
      await fs.rm(noStatsRepo, { recursive: true, force: true });
    }
  });

  it('writeContentVersionFile 写入 generated/content-version.json', async () => {
    const targetRepo = await createFakeRepo();
    try {
      const version = await computeContentVersion({ repoRoot: targetRepo, desktopRoot: targetRepo });
      const written = writeContentVersionFile({ desktopRoot: targetRepo, version });
      assert.equal(written, path.join(targetRepo, 'generated', 'content-version.json'));
      const parsed = JSON.parse(await fs.readFile(written, 'utf8'));
      assert.equal(parsed.contentBatch, version.contentBatch);
      assert.equal(parsed.docCount, 615);
    } finally {
      await fs.rm(targetRepo, { recursive: true, force: true });
    }
  });
});
