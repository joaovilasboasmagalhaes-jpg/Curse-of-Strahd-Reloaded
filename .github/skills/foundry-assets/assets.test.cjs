const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { access, buildCatalog, cachedText, localFile, main, plainText, searchCatalog } = require("./assets.cjs");

const users = [
  { _id: "a", name: "Player A", role: 1 }, { _id: "b", name: "Player B", role: 2 },
  { _id: "assistant", role: 3 }, { _id: "gm", role: 4 }, { _id: "banned", role: 0 },
];

test("page inheritance, defaults, explicit denial and GM exclusion", () => {
  const entry = { ownership: { default: 2, b: 0 } };
  const inherited = access(entry, { ownership: { default: -1 } }, users);
  assert.deepEqual(inherited.map(row => row.pageLevel), [2, 0]);
  assert.equal(inherited[0].journalInSidebar, true);
  assert.equal(inherited[1].pageReadable, false);
  const overrides = access(entry, { ownership: { default: -1, a: 0, b: 3 } }, users);
  assert.deepEqual(overrides.map(row => row.access), ["none", "owner"]);
  assert.equal(overrides[1].journalInSidebar, false);
  assert.equal(overrides[1].pageReadable, true);
  assert.equal(access(entry, { ownership: { default: 1 } }, users)[0].pageReadable, false);
  assert.equal(access(entry, {}, users)[0].pageLevel, 2);
  assert.throws(() => access({ ownership: { default: 7 } }, null, users), /Unknown ownership/);
});

test("safe local paths and URL handling", () => {
  const root = path.resolve("fixture-data");
  assert.equal(localFile(root, "https://example.invalid/a.png"), null);
  assert.equal(localFile(root, "//example.invalid/a.png"), null);
  assert.equal(localFile(root, "worlds/A%20B.png?v=2"), path.join(root, "worlds", "A B.png"));
  assert.throws(() => localFile(root, "%2e%2e/escape.png"), /outside Data/);
  assert.throws(() => localFile(root, "%not-valid"), URIError);
});

test("native HTML text is cached without script content", () => {
  assert.equal(plainText("<p>A &amp; B</p><p>&#x43;&#68;</p><script>hidden</script>"), "A & B\nCD");
});

test("transcription invalidation retains text and hash", () => {
  const original = { status: "verified", text: "Old text", sha256: "old" };
  assert.equal(cachedText(original, "old").status, "verified");
  assert.equal(cachedText(original, "new").status, "stale");
  assert.equal(cachedText(original, null).text, "Old text");
  assert.equal(cachedText(null, "new").status, "pending");
});

function fixture(t) {
  const data = fs.mkdtempSync(path.join(os.tmpdir(), "handout-test-"));
  t.after(() => fs.rmSync(data, { recursive: true }));
  const dir = path.join(data, "worlds", "curse-of-strahd", "assets", "handouts");
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, "a b.png"), "first image");
  const source = "worlds/curse-of-strahd/assets/handouts/a b.png";
  const options = {
    data, folderName: "Player Handouts", users, now: "2026-01-01T00:00:00Z",
    folders: [
      { _id: "root", name: "Player Handouts", type: "JournalEntry" },
      { _id: "child", folder: "root", type: "JournalEntry" },
      { _id: "other", name: "Private", type: "JournalEntry" },
    ],
    entries: [
      { _id: "journal", folder: "child", name: "Clue", ownership: { default: 2 } },
      { _id: "excluded", folder: "other", name: "Excluded" },
    ],
    pages: [{
      _id: "page", parentId: "journal", name: "Letter", type: "image",
      ownership: { default: -1 }, src: source.replace(" ", "%20"),
      text: { content: `<p>Native text</p><img src="${source}">` },
    }],
  };
  return { data, source, options, dir };
}

test("inventory includes descendants, canonicalizes encoded paths and keeps native text", t => {
  const { options, source } = fixture(t);
  const catalog = buildCatalog(options);
  assert.equal(catalog.journals.length, 1);
  assert.equal(catalog.assets.length, 1);
  assert.equal(catalog.assets[0].id, source);
  assert.equal(catalog.assets[0].references[0].players[0].pageLevel, 2);
  assert.equal(catalog.assets[0].references.length, 1);
  assert.equal(catalog.journals[0].pages[0].text, "Native text");
  assert.equal(catalog.assets[0].transcription.status, "pending");
});

test("search gives bounded excerpts and page-specific native text results", t => {
  const { options } = fixture(t);
  const catalog = buildCatalog(options);
  catalog.assets[0].transcription.text = "Secret ".repeat(1000);
  const results = searchCatalog(catalog, ["secret", "clue"]);
  assert.equal(results.assets.length, 1);
  assert.ok(results.assets[0].excerpt.length <= 240);
  assert.equal(results.assets[0].references[0].observerPlayers, 2);
  assert.equal(results.pages.length, 0);
  const textResults = searchCatalog(catalog, ["native", "clue"]);
  assert.equal(textResults.pages[0].pageId, "page");
  assert.equal(textResults.pages[0].excerpt, "Native text");
});

test("refresh preserves metadata, invalidates changed text, clears removed references", t => {
  const { options, source, dir } = fixture(t);
  const first = buildCatalog(options);
  first.assets[0].notes = "DM note";
  first.assets[0].tags = ["clue"];
  first.assets[0].transcription = { status: "verified", text: "First", sha256: first.assets[0].sha256 };
  const unchanged = buildCatalog({ ...options, previous: first });
  assert.equal(unchanged.assets[0].transcription.status, "verified");
  fs.writeFileSync(path.join(dir, "a b.png"), "changed");
  const changed = buildCatalog({ ...options, previous: first });
  assert.equal(changed.assets[0].transcription.status, "stale");
  assert.equal(changed.assets[0].notes, "DM note");
  assert.deepEqual(changed.assets[0].tags, ["clue"]);
  fs.unlinkSync(path.join(dir, "a b.png"));
  assert.equal(buildCatalog({ ...options, previous: first }).assets[0].state, "missing");
  const removed = buildCatalog({ ...options, entries: [], pages: [], previous: first });
  assert.equal(removed.assets.find(asset => asset.id === source).state, "unreferenced");
  assert.deepEqual(removed.assets[0].references, []);
});

test("ambiguous or missing journal folder is an explicit error", t => {
  const { options } = fixture(t);
  assert.throws(() => buildCatalog({ ...options, folders: [] }), /found 0/);
  assert.throws(() => buildCatalog({ ...options, folders: [options.folders[0], options.folders[0]] }), /found 2/);
});

test("set-text persists and shares hash-matched text; rejects changed files and empty text", async t => {
  const { options, data, source, dir } = fixture(t);
  fs.copyFileSync(path.join(dir, "a b.png"), path.join(dir, "copy.png"));
  const catalogFile = path.join(data, "catalog.json");
  fs.writeFileSync(catalogFile, JSON.stringify(buildCatalog(options)));
  const textFile = path.join(data, "text.txt");
  fs.writeFileSync(textFile, "Verified transcription");
  const args = ["set-text", "--catalog", catalogFile, "--data", data, "--id", source,
    "--file", textFile, "--source", "Visual check"];
  await main(args);
  const saved = JSON.parse(fs.readFileSync(catalogFile, "utf8"));
  assert.equal(saved.assets.filter(asset => asset.transcription.text === "Verified transcription").length, 2);
  fs.writeFileSync(textFile, " ");
  await assert.rejects(main(args), /must not be empty/);
  fs.writeFileSync(path.join(dir, "a b.png"), "different");
  await assert.rejects(main(args), /Image changed/);
});

test("unavailable Foundry leaves last-known catalog intact", async t => {
  const { data } = fixture(t);
  const file = path.join(data, "catalog.json");
  fs.writeFileSync(file, '{"checkedAt":"old"}');
  await assert.rejects(main(["refresh", "--app", path.join(data, "missing"), "--catalog", file]));
  assert.equal(fs.readFileSync(file, "utf8"), '{"checkedAt":"old"}');
});

test("refresh reads copied LevelDB documents and never changes the source databases", async t => {
  const { options, data, source } = fixture(t);
  const app = process.env.FOUNDRY_APP || "C:\\Program Files\\Foundry Virtual Tabletop\\resources\\app";
  const { ClassicLevel } = require(path.join(app, "node_modules", "classic-level"));
  const dbRoot = path.join(data, "worlds", "curse-of-strahd", "data");
  fs.mkdirSync(dbRoot, { recursive: true });
  for (const [name, records] of Object.entries({
    folders: options.folders.map(folder => [`!folders!${folder._id}`, folder]),
    users: users.map(user => [`!users!${user._id}`, { ...user, password: "must-not-export" }]),
    journal: [
      ...options.entries.map(entry => [`!journal!${entry._id}`, entry]),
      ...options.pages.map(page => [`!journal.pages!${page.parentId}.${page._id}`, page]),
    ],
  })) {
    const db = new ClassicLevel(path.join(dbRoot, name), { valueEncoding: "json" });
    try {
      await db.open();
      await db.batch(records.map(([key, value]) => ({ type: "put", key, value })));
    } finally {
      await db.close();
    }
  }
  function snapshot(dir) {
    return fs.readdirSync(dir, { recursive: true, withFileTypes: true })
      .filter(item => item.isFile()).map(item => {
        const file = path.join(item.parentPath, item.name);
        return [path.relative(dir, file), fs.readFileSync(file).toString("base64")];
      }).sort((a, b) => a[0].localeCompare(b[0]));
  }
  const before = snapshot(dbRoot);
  const catalogFile = path.join(data, "catalog.json");
  await main(["refresh", "--data", data, "--app", app, "--catalog", catalogFile]);
  const saved = fs.readFileSync(catalogFile, "utf8");
  assert.ok(!saved.includes("must-not-export"));
  const catalog = JSON.parse(saved);
  assert.equal(catalog.assets[0].id, source);
  assert.equal(catalog.assets[0].references[0].pageId, "page");
  assert.equal(catalog.journals[0].pages.length, 1);
  assert.deepEqual(snapshot(dbRoot), before);
  await assert.rejects(main([
    "refresh", "--data", data, "--app", app, "--catalog", catalogFile, "--folder", "No such folder",
  ]), /found 0/);
  assert.equal(fs.readFileSync(catalogFile, "utf8"), saved);
});
