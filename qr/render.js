// node qr/render.js — renders card.html and the bare QR to PNG with the pre-installed Chromium
const { chromium } = require("playwright");
const path = require("path");
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });
  await p.goto("file://" + path.join(__dirname, "card.html"));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(500);
  await p.locator(".card").screenshot({ path: path.join(__dirname, "whiterabbit-qr-card.png") });
  await p.goto("file://" + path.join(__dirname, "whiterabbit-qr.svg"));
  await p.setViewportSize({ width: 656, height: 656 });
  await p.screenshot({ path: path.join(__dirname, "whiterabbit-qr.png"), clip: { x: 0, y: 0, width: 656, height: 656 } });
  await b.close();
})();
