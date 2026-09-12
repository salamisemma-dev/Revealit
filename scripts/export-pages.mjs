import { cp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";

const origin = process.env.PAGES_SOURCE_ORIGIN ?? "http://127.0.0.1:8787";
const basePath = (process.env.PAGES_BASE_PATH ?? "").replace(/\/$/, "");
const routes = ["/", "/reveal-fit", "/foundation", "/foundation/anbi", "/contact", "/privacy"];
const outDir = "pages-dist";
const alreadyBased = basePath ? `${basePath.slice(1)}/` : "";

function pagePath(route) {
  return route === "/" ? join(outDir, "index.html") : join(outDir, route.slice(1), "index.html");
}

function withPagesBase(html) {
  if (!basePath) return html;
  return html
    .replace(new RegExp(`(href|src|poster)="/(?!(?:/|${alreadyBased}))`, "g"), `$1="${basePath}/`)
    .replace(new RegExp(`url\\((["']?)/(?!(?:/|${alreadyBased}))(images|media|_next|favicon\\.svg)`, "g"), `url($1${basePath}/$2`)
    .replace(new RegExp(`(["'\`])/(?!(?:/|${alreadyBased}))(images|media|_next|favicon\\.svg)`, "g"), `$1${basePath}/$2`);
}

async function fetchHtml(route) {
  const response = await fetch(new URL(route, origin));
  if (!response.ok) {
    throw new Error(`Could not export ${route}: ${response.status} ${response.statusText}`);
  }
  return withPagesBase(await response.text());
}

async function rewriteTextAssets(dir) {
  const { readdir, stat } = await import("node:fs/promises");
  for (const entry of await readdir(dir)) {
    const path = join(dir, entry);
    const info = await stat(path);
    if (info.isDirectory()) {
      await rewriteTextAssets(path);
      continue;
    }
    if (!/\.(css|js|json)$/.test(path)) continue;
    const current = await readFile(path, "utf8");
    const next = withPagesBase(current);
    if (next !== current) await writeFile(path, next);
  }
}

await rm(outDir, { recursive: true, force: true });
await mkdir(outDir, { recursive: true });
await cp("dist/client", outDir, { recursive: true });
await cp("public", join(outDir, "public"), { recursive: true });

for (const route of routes) {
  const target = pagePath(route);
  await mkdir(dirname(target), { recursive: true });
  await writeFile(target, await fetchHtml(route), "utf8");
}

await writeFile(join(outDir, "404.html"), await readFile(join(outDir, "index.html"), "utf8"));
await rewriteTextAssets(outDir);
