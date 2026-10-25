# White Rabbit page

A fan page about White Rabbit candy in English, German and Chinese, published with GitHub Pages from the root of `main` at https://dsaad68.github.io/whiterabbit/.

- `index.html` is the whole site. Don't hand-edit the generated blocks; edit the sources and rebuild.
- The words live in `content.py`. After editing them, run `python3 build_content.py content.py index.html`, which replaces the block between `CONTENT:BEGIN` and `CONTENT:END`.
- The rabbit lives in `rabbit.json`: three poses (`leap` for the logo, prints and icons; `gather` and `stretch`, which the History rabbit morphs between) with one shared path structure. After editing it, run `python3 build_rabbit.py rabbit.json index.html`, which rewrites the `<symbol id="rabbit-sym">` and the `RABBIT:BEGIN` … `RABBIT:END` block. Line weights per size are the `--rw` / `--rwl` CSS variables.
- Running both builds on an unchanged checkout reproduces `index.html` byte for byte; use that as a check.
- The page was also published as a claude.ai artifact (https://claude.ai/artifact/7L7hmS6wdV5o7KeXacgbT3). To refresh it, republish with the Artifact tool using `file_path: index.html` (single file, no capabilities).
