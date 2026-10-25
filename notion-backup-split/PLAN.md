# Notion Backup Split Plan

## Goal

Split the single-file Notion backup at `/app/notion_backup.json` (2.29 MB) into a
folder structure of per-database and per-page folders, each containing a
`content.json`, with subpages as nested folders.

## Output location

`/app/notion_backup/`

## Schema findings

**Top level:** `{ databases: {...}, pages: {...} }` — both objects keyed by UUID.

**`.databases[id]`** → `{ schema, rows }`

- `schema` = database metadata object (title, `properties` = column defs
  `{name, type, description, ...}`, `parent: {type: "workspace"}`, `is_inline`, ...)
- `rows` = object keyed by row UUID → each row is a page-like object
  (`properties` keyed by column name, `parent: {type: "database_id"}`, `blocks`, ...)

**`.pages[id]`** → standard Notion page object; title at
`properties.title.title[].plain_text`; content in `blocks` array.

**Subpages:** a subpage is a `child_page` block —
`{ id, type: "child_page", child_page: { title }, children: [content blocks...],
parent: { page_id } }`. Its `children` array is the subpage's content; blocks
recurse via `children`. In this export, all `child_page` blocks sit directly
in a page's `blocks` array (no subpage-within-subpage), and databases/rows
contain zero `child_page` blocks.

## Target structure

```plaintext
databases/
|- database1_title/
|  `- content.json
|  |- subpage1_title/ (if any)
|  |  `- content.json
|  |- subpage2_title/ (if any)
|  |- ...
|  `- subpageN_title/ (if any)
|- database2_title/
|- ...
`- databaseN_title/
pages/
|- page1_title/
|  |- content.json
|  |- subpage1_title/ (if any)
|  |  `- content.json
|  |- subpage2_title/ (if any)
|  |- ...
|  `- subpageN_title/ (if any)
|- page2_title/
|- ...
`- pageN_title/
```

## content.json semantics

- **Database folders:** the full `.databases[id]` entry (`schema` + `rows`)
  written verbatim.
- **Page folders:** the page object with each `child_page` block replaced by a
  stub `{"type": "child_page", "title": "...", "folder": "<subfolder name>"}` —
  subpage data lives only in its own folder (no duplication).
- **Subpage folders:** the original `child_page` block verbatim (its `children`
  array is the subpage's content).

## Implementation approach

A small Python script (stdlib only) that loads the JSON once, writes everything,
and never prints file contents into the conversation:

1. Sanitize every title for the filesystem (`/\:*?"<>|`, control chars, trim;
   empty → `Untitled`).
2. Dedupe same-parent folder-name collisions by appending the first 8 chars of
   the block/page ID.
3. Recurse into subpage `children` so nested `child_page` blocks (none in this
   export, but future-proof) also become nested folders.
4. Print the resulting tree.
