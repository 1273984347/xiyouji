import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import http from 'node:http';
import os from 'node:os';
import path from 'node:path';
import { after, before, describe, it } from 'node:test';

import serverModule from '../src/server.cjs';

const { createContentServer } = serverModule;

/**
 * 向本地服务发一个原生 HTTP 请求（可指定未规范化的 path，用于目录穿越测试）。
 * @returns {Promise<{ statusCode: number, headers: Record<string, string>, body: string }>}
 */
function request(baseUrl, { method = 'GET', requestPath = null } = {}) {
  return new Promise((resolve, reject) => {
    const target = new URL(baseUrl);
    const req = http.request(
      {
        hostname: target.hostname,
        port: target.port,
        path: requestPath === null ? `${target.pathname}${target.search}` : requestPath,
        method,
      },
      (res) => {
        const chunks = [];
        res.on('data', (chunk) => chunks.push(chunk));
        res.on('end', () => {
          resolve({
            statusCode: res.statusCode,
            headers: res.headers,
            body: Buffer.concat(chunks).toString('utf8'),
          });
        });
        res.on('error', reject);
      },
    );
    req.on('error', reject);
    req.end();
  });
}

describe('server.cjs 本地内容服务', () => {
  let tempRoot = '';
  let siteDir = '';
  let baseUrl = '';
  let contentServer = null;

  before(async () => {
    tempRoot = await fs.mkdtemp(path.join(os.tmpdir(), 'xiyouji-server-test-'));
    siteDir = path.join(tempRoot, 'site');
    await fs.mkdir(path.join(siteDir, 'sub'), { recursive: true });
    await fs.writeFile(path.join(siteDir, 'index.html'), '<!doctype html><html><body><h1>西游记</h1></body></html>', 'utf8');
    await fs.writeFile(path.join(siteDir, '404.html'), '<!doctype html><html><body>自定义 404 西游记</body></html>', 'utf8');
    await fs.writeFile(path.join(siteDir, 'sub', 'a.html'), '<!doctype html><html><body>子页面内容</body></html>', 'utf8');
    await fs.writeFile(path.join(siteDir, 'sub', 'index.html'), '<!doctype html><html><body>子目录首页</body></html>', 'utf8');
    await fs.writeFile(path.join(siteDir, 'style.css'), 'body { color: #000; }', 'utf8');
    await fs.writeFile(path.join(siteDir, 'app.js'), 'console.log("x");', 'utf8');
    await fs.writeFile(path.join(siteDir, 'data.json'), '{"ok":true}', 'utf8');
    // 站点根之外的机密文件：任何穿越请求都不允许读到它。
    await fs.writeFile(path.join(tempRoot, 'secret.txt'), 'TOP_SECRET_SHOULD_NOT_LEAK', 'utf8');
    await fs.writeFile(path.join(tempRoot, 'package.json'), '{"name":"outside-secret"}', 'utf8');

    contentServer = await createContentServer({ rootDir: siteDir });
    baseUrl = contentServer.url;
  });

  after(async () => {
    if (contentServer) {
      await contentServer.close();
    }
    await fs.rm(tempRoot, { recursive: true, force: true });
  });

  it('GET / 返回 200、text/html，且含「西游记」', async () => {
    const res = await request(baseUrl);
    assert.equal(res.statusCode, 200);
    assert.match(String(res.headers['content-type']), /^text\/html/);
    assert.match(res.body, /西游记/);
    assert.equal(res.headers['x-content-type-options'], 'nosniff');
    assert.equal(res.headers['cache-control'], 'no-cache');
  });

  it('GET /index.html 返回 200 且内容正确', async () => {
    const res = await request(baseUrl, { requestPath: '/index.html' });
    assert.equal(res.statusCode, 200);
    assert.match(res.body, /西游记/);
    assert.ok(Number(res.headers['content-length']) > 0);
  });

  it('GET /sub/a.html 返回 200', async () => {
    const res = await request(baseUrl, { requestPath: '/sub/a.html' });
    assert.equal(res.statusCode, 200);
    assert.match(res.body, /子页面内容/);
  });

  it('GET /sub/ 目录请求回退到 index.html', async () => {
    const res = await request(baseUrl, { requestPath: '/sub/' });
    assert.equal(res.statusCode, 200);
    assert.match(res.body, /子目录首页/);
  });

  it('GET /sub（无尾斜杠）返回 301 并指向 /sub/', async () => {
    const res = await request(baseUrl, { requestPath: '/sub' });
    assert.equal(res.statusCode, 301);
    assert.equal(res.headers.location, '/sub/');
  });

  it('GET /missing 返回 404 且使用自定义 404.html', async () => {
    const res = await request(baseUrl, { requestPath: '/missing' });
    assert.equal(res.statusCode, 404);
    assert.match(String(res.headers['content-type']), /^text\/html/);
    assert.match(res.body, /自定义 404 西游记/);
    assert.equal(res.headers['x-content-type-options'], 'nosniff');
  });

  it('编码目录穿越 /%2e%2e/secret.txt 不泄露站点外文件', async () => {
    const res = await request(baseUrl, { requestPath: '/%2e%2e/secret.txt' });
    assert.notEqual(res.statusCode, 200);
    assert.doesNotMatch(res.body, /TOP_SECRET_SHOULD_NOT_LEAK/);
  });

  it('编码目录穿越 /%2e%2e/package.json 不泄露站点外文件', async () => {
    const res = await request(baseUrl, { requestPath: '/%2e%2e/package.json' });
    assert.notEqual(res.statusCode, 200);
    assert.doesNotMatch(res.body, /outside-secret/);
  });

  it('原始 ../ 路径（未编码）不泄露站点外文件', async () => {
    const res = await request(baseUrl, { requestPath: '/../secret.txt' });
    assert.doesNotMatch(res.body, /TOP_SECRET_SHOULD_NOT_LEAK/);
  });

  it('反斜杠穿越 /..%5csecret.txt 不泄露站点外文件', async () => {
    const res = await request(baseUrl, { requestPath: '/..%5csecret.txt' });
    assert.doesNotMatch(res.body, /TOP_SECRET_SHOULD_NOT_LEAK/);
  });

  it('HEAD 返回 200 且无响应体', async () => {
    const res = await request(baseUrl, { method: 'HEAD', requestPath: '/index.html' });
    assert.equal(res.statusCode, 200);
    assert.equal(res.body, '');
    assert.ok(Number(res.headers['content-length']) > 0);
  });

  it('POST 返回 405 且带 Allow 头', async () => {
    const res = await request(baseUrl, { method: 'POST' });
    assert.equal(res.statusCode, 405);
    assert.equal(res.headers.allow, 'GET, HEAD');
  });

  it('PUT / DELETE 同样返回 405', async () => {
    for (const method of ['PUT', 'DELETE']) {
      const res = await request(baseUrl, { method });
      assert.equal(res.statusCode, 405);
    }
  });

  it('MIME 类型正确：css / js / json', async () => {
    const css = await request(baseUrl, { requestPath: '/style.css' });
    assert.match(String(css.headers['content-type']), /^text\/css/);
    assert.equal(css.headers['cache-control'], 'public, max-age=86400');

    const js = await request(baseUrl, { requestPath: '/app.js' });
    assert.match(String(js.headers['content-type']), /^text\/javascript/);

    const json = await request(baseUrl, { requestPath: '/data.json' });
    assert.match(String(json.headers['content-type']), /^application\/json/);
  });

  it('close() 之后端口不可再连接', async () => {
    const extra = await createContentServer({ rootDir: siteDir });
    assert.ok(extra.port > 0);
    await extra.close();
    assert.equal(extra.server.listening, false);
    await assert.rejects(
      request(extra.url),
      (error) => error && (error.code === 'ECONNREFUSED' || error.code === 'ECONNRESET'),
    );
  });
});
