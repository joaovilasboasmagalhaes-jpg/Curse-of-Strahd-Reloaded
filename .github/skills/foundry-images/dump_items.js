// Run by build_item_icons.py via Foundry's Electron binary (ELECTRON_RUN_AS_NODE=1).
// Reads copies of LevelDB packs (SRC_DIRS, ';'-separated) and writes [{src, type, name, img}] to OUT_FILE.
const { ClassicLevel } = require(process.env.CLASSIC_LEVEL);
const fs = require("fs");
const path = require("path");

(async () => {
  const rows = [];
  for (const dir of process.env.SRC_DIRS.split(";")) {
    const db = new ClassicLevel(dir, { keyEncoding: "utf8", valueEncoding: "utf8" });
    try {
      await db.open();
      for await (const [key, value] of db.iterator()) {
        if (!(key.startsWith("!actors.items!") || key.startsWith("!items!"))) continue;
        let doc;
        try { doc = JSON.parse(value); } catch { continue; }
        rows.push({ src: path.basename(dir), type: doc.type, name: doc.name, img: doc.img });
      }
    } catch (e) {
      console.error("FAIL", dir, e.message);
    } finally {
      await db.close().catch(() => {});
    }
  }
  fs.writeFileSync(process.env.OUT_FILE, JSON.stringify(rows));
  console.log("rows", rows.length);
})();
