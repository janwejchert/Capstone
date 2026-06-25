import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import katex from "katex";
import puppeteer from "puppeteer-core";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const A = (p) => path.join(HERE, p);
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

const eqOpts = { displayMode: true, throwOnError: true, output: "html", strict: false, trust: true };
const EQ = {
  return_law: String.raw`r_{t+1} = \varphi\, r_t + \mu D_t + \sigma\, \varepsilon_{t+1}`,
  price_update: String.raw`p_{t+1} = p_t + \mu D_t + \sigma\, \varepsilon_{t+1}`,
  demand: String.raw`z_{i,t} = \frac{\hat{r}_{i,t+1}}{a\,\sigma^{2}}`,
  decomposition: String.raw`r_{t+1} = \textcolor{#1B6FC4}{\mu D_t} + \textcolor{#C62828}{x_{t+1}}`,
};

function renderEquations() {
  const out = {};
  for (const [k, tex] of Object.entries(EQ)) out[k] = katex.renderToString(tex, eqOpts);
  return out;
}

function inlineSvg(name) {
  return fs.readFileSync(A(`assets/${name}.svg`), "utf8");
}

function assemble() {
  let html = fs.readFileSync(A("poster.template.html"), "utf8");
  const vals = JSON.parse(fs.readFileSync(A("assets/figure_values.json"), "utf8"));
  const eqs = renderEquations();
  const figs = {
    dual_channel: inlineSvg("fig_dual_channel"),
    saturation: inlineSvg("fig_saturation"),
    threshold_r2: inlineSvg("fig_threshold_r2"),
    threshold_phi: inlineSvg("fig_threshold_phi"),
    schematic: inlineSvg("schematic"),
  };
  const logo = `<img class="logo" src="assets/ielogo.jpeg" alt="IE">`;
  html = html.replace(/\{\{logo\}\}/g, logo);
  html = html.replace(/\{\{val:([a-z0-9_]+)\}\}/g, (_, k) => String(vals[k] ?? `?${k}?`));
  html = html.replace(/\{\{eq:([a-z_]+)\}\}/g, (_, k) => eqs[k] ?? `?eq:${k}?`);
  html = html.replace(/\{\{fig:([a-z0-9_]+)\}\}/g, (_, k) => figs[k] ?? `?fig:${k}?`);
  fs.writeFileSync(A("poster.html"), html);
  return html;
}

async function toPdf() {
  const outDir = path.join(HERE, "..", "results", "poster");
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: true,
    args: ["--no-sandbox", "--font-render-hinting=none"],
  });
  const page = await browser.newPage();
  await page.goto("file://" + A("poster.html"), { waitUntil: "networkidle0" });
  await page.pdf({
    path: path.join(outDir, "poster.pdf"),
    width: "841mm", height: "1189mm",
    printBackground: true, preferCSSPageSize: false,
    margin: { top: "0", right: "0", bottom: "0", left: "0" },
  });
  await browser.close();
}

assemble();
await toPdf();
console.log("wrote results/poster/poster.pdf");
