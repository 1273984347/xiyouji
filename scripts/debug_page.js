/**
 * Debug a web page using Playwright. Capture console messages and/or page errors.
 *
 * Usage:
 *   node debug_page.js --url <url> --mode console
 *   node debug_page.js --url <url> --mode error
 *   node debug_page.js --url <url> --mode both   (default)
 *
 * Output: `<ISO-timestamp>  <TYPE>  <message>`
 *
 * Exit code: 0 if no errors captured, 1 if any error (pageerror or console error) captured.
 */
const { chromium } = require('playwright');

function usage() {
  console.log(
    [
      'Usage: node debug_page.js --url <url> [--mode console|error|both]',
      '',
      'Options:',
      '  --url <url>     URL or file:// path to debug (required)',
      '  --mode <mode>   console | error | both  (default: both)',
      '  --timeout <ms>  navigation timeout (default: 30000)',
      '  --wait <ms>     extra wait after networkidle (default: 2000)',
      '  -h, --help      show this help',
    ].join('\n')
  );
}

function parseArgs(argv) {
  const args = { mode: 'both', timeout: 30000, wait: 2000 };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '-h' || a === '--help') {
      args.help = true;
    } else if (a === '--url') {
      args.url = argv[++i];
    } else if (a === '--mode') {
      args.mode = argv[++i];
    } else if (a === '--timeout') {
      args.timeout = Number(argv[++i]);
    } else if (a === '--wait') {
      args.wait = Number(argv[++i]);
    }
  }
  return args;
}

function ts() {
  return new Date().toISOString();
}

(async () => {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    usage();
    process.exit(0);
  }

  if (!args.url) {
    console.error('Error: --url is required');
    usage();
    process.exit(2);
  }

  const mode = (args.mode || 'both').toLowerCase();
  if (!['console', 'error', 'both'].includes(mode)) {
    console.error(`Error: invalid mode "${args.mode}" (must be console|error|both)`);
    usage();
    process.exit(2);
  }

  const wantConsole = mode === 'console' || mode === 'both';
  const wantError = mode === 'error' || mode === 'both';

  let errorCount = 0;

  const browser = await chromium.launch({ headless: true });
  try {
    const context = await browser.newContext({
      viewport: { width: 1280, height: 800 },
    });
    const page = await context.newPage();

    if (wantConsole) {
      page.on('console', (msg) => {
        const type = msg.type();
        const text = msg.text();
        const loc = msg.location();
        const locStr = loc
          ? ` at ${loc.url}:${loc.lineNumber}:${loc.columnNumber || 0}`
          : '';
        console.log(`${ts()}  console:${type}  ${text}${locStr}`);
        if (type === 'error') {
          errorCount++;
        }
      });
    }

    if (wantError) {
      page.on('pageerror', (err) => {
        console.log(`${ts()}  pageerror  ${err.message}`);
        if (err.stack) {
          console.log(`${ts()}  pageerror:stack  ${err.stack}`);
        }
        errorCount++;
      });
    }

    await page.goto(args.url, {
      waitUntil: 'networkidle',
      timeout: args.timeout,
    });
    await page.waitForTimeout(args.wait);

    await context.close();
  } finally {
    await browser.close();
  }

  if (errorCount > 0) {
    console.log(`\nTotal errors captured: ${errorCount}`);
    process.exit(1);
  } else {
    console.log('\nNo errors captured.');
    process.exit(0);
  }
})().catch((err) => {
  console.error(`${ts()}  fatal  ${err.message}`);
  if (err.stack) console.error(err.stack);
  process.exit(1);
});
