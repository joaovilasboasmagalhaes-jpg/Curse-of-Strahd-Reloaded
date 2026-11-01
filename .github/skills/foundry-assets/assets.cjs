const fs = require("node:fs");
const path = require("node:path");
const os = require("node:os");
const crypto = require("node:crypto");

const DEFAULT_DATA = path.join(process.env.LOCALAPPDATA || "", "FoundryVTT", "Data");
const DEFAULT_APP = "C:\\Program Files\\Foundry Virtual Tabletop\\resources\\app";
const DEFAULT_CATALOG = path.join(__dirname, "catalog.json");
const WORLD = "curse-of-strahd";

function readJSON(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function saveJSON(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const temporary = `${file}.${crypto.randomUUID()}.tmp`;
  try {
    fs.writeFileSync(temporary, JSON.stringify(value, null, 2) + "\n", { encoding: "utf8", flag: "wx" });
    fs.renameSync(temporary, file);
  } finally {
    if (fs.existsSync(temporary)) fs.unlinkSync(temporary);
  }
}

function level(ownership, user, parent = 0) {
  const value = ownership?.[user._id] ?? ownership?.default ?? 0;
  if (![-1, 0, 1, 2, 3].includes(value)) throw new Error(`Unknown ownership level: ${value}`);
  return value === -1 ? parent : value;
}

function access(entry, page, users) {
  return users.filter(user => user.role > 0 && user.role < 3).map(user => {
    const journalLevel = level(entry.ownership, user);
    const pageLevel = page
      ? level(page.ownership ?? { default: -1 }, user, journalLevel) : journalLevel;
    return {
      userId: user._id,
      userName: user.name,
      journalLevel,
      pageLevel,
      journalInSidebar: journalLevel >= 2,
      pageReadable: pageLevel >= 2,
      access: ["none", "limited", "observer", "owner"][pageLevel],
    };
  });
}

function localFile(data, source) {
  if (/^[a-z][a-z0-9+.-]*:|^[/\\]{2}/i.test(source)) return null;
  const relative = decodeURIComponent(source.split(/[?#]/)[0]).replace(/[/\\]/g, path.sep);
  const file = path.resolve(data, relative);
  const inside = path.relative(path.resolve(data), file);
  if (inside.startsWith("..") || path.isAbsolute(inside)) throw new Error(`Asset outside Data: ${source}`);
  return file;
}

function fingerprint(data, source) {
  const file = localFile(data, source);
  if (!file) return { state: "external", sha256: null };
  try {
    const stat = fs.statSync(file);
    if (!stat.isFile()) throw new Error(`Not an asset file: ${file}`);
    return {
      state: "present", bytes: stat.size,
      sha256: crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex"),
    };
  } catch (error) {
    if (error.code === "ENOENT") return { state: "missing", sha256: null };
    throw error;
  }
}

function cachedText(previous, sha256) {
  if (!previous) return { status: "pending", text: "", source: null, sha256: null };
  return {
    ...previous,
    status: previous.sha256 && previous.sha256 === sha256 ? previous.status : previous.text ? "stale" : "pending",
  };
}

function plainText(html) {
  return html.replace(/<(script|style)\b[^>]*>[\s\S]*?<\/\1>/gi, "")
    .replace(/<br\s*\/?>|<\/(?:p|div|h[1-6]|li|tr)>/gi, "\n")
    .replace(/<[^>]*>/g, "")
    .replace(/&#(x[0-9a-f]+|\d+);/gi, (_, value) => String.fromCodePoint(
      value[0].toLowerCase() === "x" ? parseInt(value.slice(1), 16) : Number(value)))
    .replace(/&(amp|lt|gt|quot|apos|nbsp);/g, (_, entity) => ({
      amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " ",
    })[entity]).trim();
}

function buildCatalog({ data, folderName, folders, entries, pages, users, previous, now }) {
  const roots = folders.filter(folder => folder.type === "JournalEntry" && folder.name === folderName);
  if (roots.length !== 1) throw new Error(`Expected one JournalEntry folder "${folderName}", found ${roots.length}`);
  const selected = new Set([roots[0]._id]);
  let size;
  do {
    size = selected.size;
    for (const folder of folders) if (selected.has(folder.folder)) selected.add(folder._id);
  } while (size !== selected.size);
  const assets = new Map();
  function add(source, reference) {
    if (!source) return;
    const normalized = /^[a-z][a-z0-9+.-]*:|^[/\\]{2}/i.test(source)
      ? source : decodeURIComponent(source.split(/[?#]/)[0]).replace(/%/g, "%25").replace(/\\/g, "/");
    if (!assets.has(normalized)) {
      const file = fingerprint(data, normalized);
      const old = previous?.assets.find(asset => asset.id === normalized);
      const sameImage = file.sha256 && previous?.assets.find(asset =>
        asset.sha256 === file.sha256 && asset.transcription?.status === "verified");
      assets.set(normalized, {
        id: normalized, name: path.posix.basename(normalized), ...file,
        notes: old?.notes || "", tags: old?.tags || [],
        transcription: cachedText(
          old?.transcription?.status === "verified" ? old.transcription : sameImage?.transcription || old?.transcription,
          file.sha256,
        ), references: [],
      });
    }
    if (reference && !assets.get(normalized).references.some(existing =>
      existing.journalId === reference.journalId && existing.pageId === reference.pageId)) {
      assets.get(normalized).references.push(reference);
    }
  }
  const root = path.join(data, "worlds", WORLD, "assets", "handouts");
  function scan(dir) {
    for (const item of fs.readdirSync(dir, { withFileTypes: true })) {
      const file = path.join(dir, item.name);
      if (item.name.startsWith(".")) continue;
      if (item.isDirectory()) scan(file);
      else if (item.isFile()) add(path.relative(data, file));
    }
  }
  scan(root);
  const journals = [];
  for (const entry of entries.filter(entry => selected.has(entry.folder))) {
    const embedded = pages.filter(page => page.parentId === entry._id);
    const entryPages = embedded.length ? embedded : (entry.pages || []);
    const journal = {
      id: entry._id, name: entry.name, folderId: entry.folder,
      ownership: entry.ownership || {}, players: access(entry, null, users), pages: [],
    };
    if (entry.img) add(entry.img, {
      journalId: entry._id, journalName: entry.name, pageId: null, pageName: null,
      players: access(entry, null, users),
    });
    for (const page of entryPages) {
      const players = access(entry, page, users);
      const html = page.text?.content || "";
      const sources = new Set(page.src ? [page.src] : []);
      for (const match of html.matchAll(/<(?:img|source)\b[^>]*\bsrc\s*=\s*["']([^"']+)["']/gi)) {
        sources.add(match[1].replace(/&amp;/g, "&"));
      }
      const reference = {
        journalId: entry._id, journalName: entry.name, pageId: page._id,
        pageName: page.name, pageType: page.type, players,
      };
      for (const source of sources) add(source, reference);
      journal.pages.push({
        id: page._id, name: page.name, type: page.type, ownership: page.ownership ?? { default: -1 },
        players, sources: [...sources], text: html ? plainText(html) : page.text?.markdown || "",
        html, markdown: page.text?.markdown || "",
      });
    }
    journals.push(journal);
  }
  // Keep removed assets and their transcriptions, but never retain obsolete permission claims.
  for (const old of previous?.assets || []) {
    if (!assets.has(old.id)) assets.set(old.id, {
      ...old, state: "unreferenced", references: [],
      transcription: cachedText(old.transcription, null),
    });
  }
  return {
    schemaVersion: 1, checkedAt: now, world: WORLD, folder: folderName,
    source: "local-database-copy",
    caveats: [
      "Best-effort disk snapshot; live unsaved changes and modules may differ. Refresh after permission changes.",
      "Access is not proof of viewing. Temporary Show to Players events are not tracked.",
      "Limited (1) is not observer (2); sidebar visibility requires journal level >= 2. Page access is reported separately.",
      "Unreferenced files have unknown sharing outside the selected journal folder, not confirmed private.",
    ],
    journals: journals.sort((a, b) => a.name.localeCompare(b.name)),
    assets: [...assets.values()].sort((a, b) => a.id.localeCompare(b.id)),
  };
}

async function readDatabase(ClassicLevel, source, destination, prefixes) {
  fs.cpSync(source, destination, { recursive: true, filter: file => path.basename(file) !== "LOCK" });
  const db = new ClassicLevel(destination, { keyEncoding: "utf8", valueEncoding: "utf8" });
  try {
    await db.open();
    const rows = [];
    for await (const [key, value] of db.iterator()) {
      if (prefixes.some(prefix => key.startsWith(prefix))) rows.push({ key, doc: JSON.parse(value) });
    }
    return rows;
  } finally {
    await db.close();
  }
}

async function refresh(options) {
  const { ClassicLevel } = require(path.join(options.app, "node_modules", "classic-level"));
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "foundry-handouts-"));
  try {
    const source = path.join(options.data, "worlds", WORLD, "data");
    const rows = {};
    for (const [name, prefixes] of Object.entries({
      folders: ["!folders!"], journal: ["!journal!", "!journal.pages!"], users: ["!users!"],
    })) {
      rows[name] = await readDatabase(ClassicLevel, path.join(source, name), path.join(temporary, name), prefixes);
    }
    const previous = fs.existsSync(options.catalog) ? readJSON(options.catalog) : null;
    const catalog = buildCatalog({
      data: options.data, folderName: options.folder, now: new Date().toISOString(), previous,
      folders: rows.folders.map(row => row.doc),
      entries: rows.journal.filter(row => row.key.startsWith("!journal!")).map(row => row.doc),
      pages: rows.journal.filter(row => row.key.startsWith("!journal.pages!")).map(row => ({
        ...row.doc, parentId: row.key.split("!")[2].split(".")[0],
      })),
      users: rows.users.map(row => ({ _id: row.doc._id, name: row.doc.name, role: row.doc.role })),
    });
    saveJSON(options.catalog, catalog);
    console.log(`Updated ${catalog.assets.length} assets and ${catalog.journals.length} journals at ${catalog.checkedAt}`);
    console.log(`Catalog: ${options.catalog}`);
  } finally {
    fs.rmSync(temporary, { recursive: true });
  }
}

function parseArgs(args) {
  const command = args.shift();
  const options = { data: DEFAULT_DATA, app: DEFAULT_APP, catalog: DEFAULT_CATALOG, folder: "Player Handouts" };
  const known = new Set(["data", "app", "catalog", "folder", "id", "file", "source", "journal", "page"]);
  const terms = [];
  while (args.length) {
    const arg = args.shift();
    if (!arg.startsWith("--")) terms.push(arg);
    else {
      const key = arg.slice(2);
      if (!known.has(key) || !args.length || args[0].startsWith("--")) throw new Error(`Invalid option: ${arg}`);
      options[key] = args.shift();
    }
  }
  return { command, options, terms };
}

function searchCatalog(catalog, terms) {
  const matches = text => terms.every(term => text.toLowerCase().includes(term.toLowerCase()));
  const excerpt = text => text.replace(/\s+/g, " ").slice(0, 240);
  return {
    assets: catalog.assets.filter(asset => matches([
      asset.id, asset.name, asset.notes, ...asset.tags, asset.transcription.text,
      ...asset.references.flatMap(reference => [reference.journalName, reference.pageName]),
    ].join(" "))).map(asset => ({
      id: asset.id, state: asset.state, textStatus: asset.transcription.status,
      excerpt: excerpt(asset.transcription.text), notes: asset.notes, tags: asset.tags,
      references: asset.references.map(reference => ({
        journalId: reference.journalId, journalName: reference.journalName,
        pageId: reference.pageId, pageName: reference.pageName,
        observerPlayers: reference.players.filter(player => player.pageReadable).length,
        limitedPlayers: reference.players.filter(player => player.access === "limited").length,
        totalPlayers: reference.players.length,
      })),
    })),
    pages: catalog.journals.flatMap(journal => journal.pages.filter(page =>
      matches([journal.name, page.name, page.text, ...page.sources].join(" "))).map(page => ({
      journalId: journal.id, journalName: journal.name, pageId: page.id, pageName: page.name,
      type: page.type, excerpt: excerpt(page.text), sources: page.sources,
    }))),
  };
}

async function main(args) {
  const { command, options, terms } = parseArgs([...args]);
  if (command === "refresh") return refresh(options);
  if (!["search", "show", "set-text"].includes(command)) {
    throw new Error("Usage: assets.ps1 refresh | search <words> | show --id <path> | set-text --id <path> --file <utf8.txt> --source <provenance>");
  }
  const catalog = readJSON(options.catalog);
  if (command === "set-text") {
    if (!options.id || !options.file || !options.source) throw new Error("set-text requires --id, --file and --source");
    const asset = catalog.assets.find(asset => asset.id === options.id);
    if (!asset || asset.state !== "present" || !asset.sha256) throw new Error("Transcription needs a present local asset");
    const current = fingerprint(options.data, asset.id);
    if (current.sha256 !== asset.sha256) throw new Error("Image changed since inventory; refresh before transcribing");
    const text = fs.readFileSync(options.file, "utf8").replace(/^\uFEFF/, "");
    if (!text.trim()) throw new Error("Transcription must not be empty; describe a deliberately text-free image explicitly");
    const transcription = {
      status: "verified", text, source: options.source, sha256: asset.sha256, checkedAt: new Date().toISOString(),
    };
    for (const candidate of catalog.assets) {
      if (candidate.sha256 === asset.sha256) candidate.transcription = { ...transcription };
    }
    saveJSON(options.catalog, catalog);
    console.log(`Saved text for ${asset.id}`);
    return;
  }
  let result;
  if (command === "search") result = searchCatalog(catalog, terms);
  else if (options.journal) {
    const journal = catalog.journals.find(journal => journal.id === options.journal);
    if (!journal) throw new Error(`Unknown journal: ${options.journal}`);
    const pages = options.page ? journal.pages.filter(page => page.id === options.page) : journal.pages;
    if (options.page && !pages.length) throw new Error(`Unknown page: ${options.page}`);
    result = { journal: { ...journal, pages } };
  } else {
    const asset = catalog.assets.find(asset => asset.id === options.id);
    if (!asset) throw new Error(`Unknown asset: ${options.id}`);
    result = { asset };
  }
  console.log(JSON.stringify({
    checkedAt: catalog.checkedAt, source: catalog.source, caveats: catalog.caveats, ...result,
  }, null, 2));
}

module.exports = { access, buildCatalog, cachedText, fingerprint, localFile, main, plainText, searchCatalog };
if (require.main === module) main(process.argv.slice(2)).catch(error => {
  console.error(`Asset catalog failed: ${error.message}. The previous catalog, if any, has not been refreshed.`);
  process.exitCode = 1;
});
