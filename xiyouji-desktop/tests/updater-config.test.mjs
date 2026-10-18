// 配置 lint 式断言（不联网、不依赖 electron）：锁定发布契约中的关键字段，
// 防止版本号 / 更新源 / 产物名被误改导致 CI 或 releases 直链失效。

import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { describe, it } from 'node:test';

const DESKTOP_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

function readText(fileName) {
  return fs.readFileSync(path.join(DESKTOP_ROOT, fileName), 'utf8');
}

const packageJson = JSON.parse(readText('package.json'));
const builderYml = readText('electron-builder.yml');
const gitignore = readText('.gitignore');

describe('package.json 契约', () => {
  it('基础字段', () => {
    assert.equal(packageJson.name, 'xiyouji-desktop');
    assert.equal(packageJson.version, '2.3.0');
    assert.equal(packageJson.private, true);
    assert.equal(packageJson.main, 'src/main.cjs');
    assert.equal(packageJson.engines.node, '>=22');
    assert.equal(packageJson.license, 'MIT');
    assert.equal(packageJson.author, '详解西游记项目');
    assert.equal(packageJson.type, undefined, '不应设置 type（主进程使用 CommonJS .cjs）');
  });

  it('依赖版本精确锁定，且不引入其它运行时依赖', () => {
    assert.deepEqual(packageJson.dependencies, { 'electron-updater': '6.8.9' });
    assert.equal(packageJson.devDependencies.electron, '44.9.0');
    assert.equal(packageJson.devDependencies['electron-builder'], '26.15.3');
    assert.equal(Object.keys(packageJson.dependencies).length, 1);
  });

  it('npm scripts 名称与命令符合 CI 契约', () => {
    assert.deepEqual(packageJson.scripts, {
      start: 'electron .',
      test: 'node --test',
      'prepare:content': 'node scripts/prepare-content.mjs',
      'pack:dir': 'npm run prepare:content && electron-builder --dir',
      'dist:win': 'npm run prepare:content && electron-builder --win --x64 --publish never',
      'dist:mac': 'npm run prepare:content && electron-builder --mac --universal --publish never',
      'dist:linux': 'npm run prepare:content && electron-builder --linux --x64 --publish never',
    });
  });
});

describe('electron-builder.yml 契约', () => {
  it('appId / productName / 目录配置', () => {
    assert.match(builderYml, /^appId: com\.xiyouji\.desktop$/m);
    assert.match(builderYml, /^productName: 详解西游记$/m);
    assert.match(builderYml, /^directories:\s*$/m);
    assert.match(builderYml, /buildResources: assets/);
    assert.match(builderYml, /output: dist/);
  });

  it('app 内容与 extraResources 指向仓库根 site/', () => {
    assert.match(builderYml, /files:\s*\n\s*- "src\/\*\*"\s*\n\s*- "package\.json"/);
    assert.match(builderYml, /from: "\.\.\/site"/);
    assert.match(builderYml, /to: "site"/);
    assert.match(builderYml, /from: "generated\/content-version\.json"/);
    assert.match(builderYml, /to: "content-version\.json"/);
  });

  it('publish 指向 GitHub Releases（electron-updater 的 app-update.yml 来源）', () => {
    assert.match(builderYml, /provider: github/);
    assert.match(builderYml, /owner: "1273984347"/);
    assert.match(builderYml, /repo: "xiyouji"/);
    assert.match(builderYml, /releaseType: release/);
  });

  it('三平台产物名为固定字面量且不含中文', () => {
    const artifactNames = builderYml
      .split(/\r?\n/)
      .filter((line) => line.trim().startsWith('artifactName:'))
      .map((line) => line.split('artifactName:')[1].trim());
    assert.deepEqual(artifactNames, [
      '"xiyouji-desktop-win-x64.${ext}"',
      '"xiyouji-desktop-mac-universal.${ext}"',
      '"xiyouji-desktop-linux-x86_64.${ext}"',
    ]);
    for (const name of artifactNames) {
      assert.doesNotMatch(name, /[\u4e00-\u9fff]/, `产物名不应含中文：${name}`);
    }
  });

  it('NSIS / mac / linux 关键配置', () => {
    assert.match(builderYml, /target: nsis/);
    assert.match(builderYml, /oneClick: false/);
    assert.match(builderYml, /perMachine: false/);
    assert.match(builderYml, /allowToChangeInstallationDirectory: true/);
    assert.match(builderYml, /createDesktopShortcut: true/);
    assert.match(builderYml, /shortcutName: 详解西游记/);
    assert.match(builderYml, /deleteAppDataOnUninstall: false/);
    assert.match(builderYml, /target:\s*\n\s*- dmg\s*\n\s*- zip/);
    assert.match(builderYml, /category: public\.app-category\.education/);
    assert.match(builderYml, /identity: null/);
    assert.match(builderYml, /- AppImage/);
    assert.match(builderYml, /category: Education/);
  });
});

describe('.gitignore 契约', () => {
  it('忽略 node_modules / dist / generated / 日志', () => {
    const lines = gitignore.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
    for (const expected of ['node_modules/', 'dist/', 'generated/', '*.log']) {
      assert.ok(lines.includes(expected), `缺少忽略项：${expected}`);
    }
  });
});
