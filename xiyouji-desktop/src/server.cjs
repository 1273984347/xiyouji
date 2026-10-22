'use strict';

// 本地静态内容服务：纯 Node stdlib http，只监听 127.0.0.1 的随机端口。
// 安全边界：只接受 GET/HEAD；路径 decode + path.resolve 后必须仍位于 rootDir 内（防目录穿越）；
// 响应统一带 X-Content-Type-Options: nosniff；HTML 不缓存，静态资源缓存一天。

const fs = require('node:fs');
const fsp = require('node:fs/promises');
const http = require('node:http');
const path = require('node:path');
const { pipeline } = require('node:stream/promises');

const HOST = '127.0.0.1';

const MIME_TYPES = Object.freeze({
  '.html': 'text/html; charset=utf-8',
  '.htm': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.map': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.gif': 'image/gif',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.otf': 'font/otf',
  '.txt': 'text/plain; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8',
  '.md': 'text/markdown; charset=utf-8',
  '.webmanifest': 'application/manifest+json; charset=utf-8',
  '.wasm': 'application/wasm',
});

const HTML_CACHE_CONTROL = 'no-cache';
const STATIC_CACHE_CONTROL = 'public, max-age=86400';

/**
 * 判断 candidate 是否仍在 rootDir 内（含 rootDir 本身）。
 * @param {string} rootDir 已 path.resolve 的根目录
 * @param {string} candidate 已 path.resolve 的目标路径
 */
function isInsideRoot(rootDir, candidate) {
  if (candidate === rootDir) {
    return true;
  }
  const prefix = rootDir.endsWith(path.sep) ? rootDir : rootDir + path.sep;
  return candidate.startsWith(prefix);
}

function contentTypeFor(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return MIME_TYPES[ext] || 'application/octet-stream';
}

function cacheControlFor(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return ext === '.html' || ext === '.htm' ? HTML_CACHE_CONTROL : STATIC_CACHE_CONTROL;
}

function writeTextResponse(res, statusCode, body, { method = 'GET', contentType = 'text/plain; charset=utf-8', cacheControl = 'no-cache', extraHeaders = {} } = {}) {
  const payload = Buffer.from(body, 'utf8');
  const headers = {
    'Content-Type': contentType,
    'Content-Length': payload.length,
    'Cache-Control': cacheControl,
    'X-Content-Type-Options': 'nosniff',
    ...extraHeaders,
  };
  res.writeHead(statusCode, headers);
  if (method === 'HEAD') {
    res.end();
    return;
  }
  res.end(payload);
}

async function sendNotFound(res, method, rootDir) {
  const customPage = path.join(rootDir, '404.html');
  try {
    const stat = await fsp.stat(customPage);
    if (stat.isFile()) {
      const headers = {
        'Content-Type': 'text/html; charset=utf-8',
        'Content-Length': stat.size,
        'Cache-Control': 'no-cache',
        'X-Content-Type-Options': 'nosniff',
      };
      res.writeHead(404, headers);
      if (method === 'HEAD') {
        res.end();
        return;
      }
      await pipeline(fs.createReadStream(customPage), res).catch(() => {});
      return;
    }
  } catch {
    // 没有自定义 404 页面时回退到纯文本。
  }
  writeTextResponse(res, 404, '404 Not Found\n', { method });
}

async function handleRequest(req, res, rootDir) {
  const method = req.method || 'GET';
  if (method !== 'GET' && method !== 'HEAD') {
    writeTextResponse(res, 405, '405 Method Not Allowed\n', {
      method,
      extraHeaders: { Allow: 'GET, HEAD' },
    });
    return;
  }

  let pathname;
  try {
    const url = new URL(req.url || '/', `http://${HOST}`);
    pathname = decodeURIComponent(url.pathname);
  } catch {
    writeTextResponse(res, 400, '400 Bad Request\n', { method });
    return;
  }

  if (pathname.includes('\0')) {
    writeTextResponse(res, 400, '400 Bad Request\n', { method });
    return;
  }

  const relativePath = pathname.replace(/^\/+/, '');
  let candidate = path.resolve(rootDir, relativePath);
  if (!isInsideRoot(rootDir, candidate)) {
    await sendNotFound(res, method, rootDir);
    return;
  }

  let stat;
  try {
    stat = await fsp.stat(candidate);
  } catch (error) {
    if (error && (error.code === 'ENOENT' || error.code === 'ENOTDIR')) {
      await sendNotFound(res, method, rootDir);
      return;
    }
    throw error;
  }

  // 目录请求：无尾斜杠时先 301 补斜杠（保证相对链接正确），再回退到 index.html。
  if (stat.isDirectory()) {
    if (!pathname.endsWith('/')) {
      const location = encodeURI(pathname) + '/';
      const headers = {
        Location: location,
        'Content-Length': 0,
        'Cache-Control': 'no-cache',
        'X-Content-Type-Options': 'nosniff',
      };
      res.writeHead(301, headers);
      res.end();
      return;
    }
    candidate = path.join(candidate, 'index.html');
    try {
      stat = await fsp.stat(candidate);
    } catch (error) {
      if (error && (error.code === 'ENOENT' || error.code === 'ENOTDIR')) {
        await sendNotFound(res, method, rootDir);
        return;
      }
      throw error;
    }
  }

  if (!stat.isFile() || !isInsideRoot(rootDir, candidate)) {
    await sendNotFound(res, method, rootDir);
    return;
  }

  const headers = {
    'Content-Type': contentTypeFor(candidate),
    'Content-Length': stat.size,
    'Cache-Control': cacheControlFor(candidate),
    'X-Content-Type-Options': 'nosniff',
  };
  res.writeHead(200, headers);
  if (method === 'HEAD') {
    res.end();
    return;
  }
  await pipeline(fs.createReadStream(candidate), res).catch(() => {
    // 客户端提前断开时 pipeline 会抛错；连接已不可用，忽略即可。
  });
}

/**
 * 启动本地内容服务。
 * @param {{ rootDir: string, host?: string, port?: number }} options
 * @returns {Promise<{ url: string, port: number, server: import('node:http').Server, close: () => Promise<void> }>}
 */
function createContentServer({ rootDir, host = HOST, port = 0 } = {}) {
  if (!rootDir || typeof rootDir !== 'string') {
    return Promise.reject(new Error('createContentServer 需要 rootDir 参数'));
  }
  const resolvedRoot = path.resolve(rootDir);
  const server = http.createServer((req, res) => {
    handleRequest(req, res, resolvedRoot).catch((error) => {
      if (!res.headersSent) {
        writeTextResponse(res, 500, '500 Internal Server Error\n', { method: req.method || 'GET' });
      } else {
        res.destroy();
      }
      // 该错误只影响单个请求，避免静默；主进程日志由调用方按需接管。
      console.error('[server] 处理请求失败:', error && error.message ? error.message : error);
    });
  });

  return new Promise((resolve, reject) => {
    const onError = (error) => {
      reject(error);
    };
    server.once('error', onError);
    server.listen(port, host, () => {
      server.removeListener('error', onError);
      const address = server.address();
      const actualPort = address && typeof address === 'object' ? address.port : port;
      let closed = false;
      const close = () => {
        if (closed) {
          return Promise.resolve();
        }
        closed = true;
        return new Promise((resolveClose) => {
          if (!server.listening) {
            resolveClose();
            return;
          }
          if (typeof server.closeAllConnections === 'function') {
            server.closeAllConnections();
          }
          server.close(() => {
            resolveClose();
          });
        });
      };
      resolve({
        url: `http://${host}:${actualPort}/`,
        port: actualPort,
        server,
        rootDir: resolvedRoot,
        close,
      });
    });
  });
}

module.exports = {
  createContentServer,
  MIME_TYPES,
  HOST,
};
