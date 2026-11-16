import { JSDOM } from 'jsdom';

const dom = new JSDOM('<!doctype html><html><body><div id="raiz"></div></body></html>', {
  url: 'http://localhost:5174/',
  pretendToBeVisual: true,
});

const { window } = dom;
globalThis.window = window;
globalThis.document = window.document;
globalThis.localStorage = window.localStorage;
globalThis.matchMedia = window.matchMedia || (() => ({
  matches: false,
  media: '',
  addListener() {},
  removeListener() {},
  addEventListener() {},
  removeEventListener() {},
  dispatchEvent() { return false; },
}));

try {
  await import('./src/main.jsx');
  console.log('IMPORT_OK');
} catch (err) {
  console.error('IMPORT_ERROR');
  console.error(err && err.stack ? err.stack : String(err));
  process.exitCode = 1;
}
