# Prompt

My notion is backed up to a file at `/app/notion_backup.json`.

I need you to explore the Notion schema from this file and come up with a way to split the single file into a folder structure like below:

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

## Rules (Do not break)

- Only use `jq '...keys' notion_backup.json` to explore just the keys, going a little deeper into each object as required.
- Do NOT read the whole notion_backup.json, it's a 2.29MB JSON file that instantly exhausts your context window.
