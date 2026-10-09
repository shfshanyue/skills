# Note format

The publish directory holds one `note.md`. Media stays at the absolute paths recorded in the note. The active directory is the 目录 on the latest 发布单, or the directory the user names this turn. Leave each publish directory in place.

## Directory

A user-named directory is the publish directory. Create that leaf when its parent exists. When the parent is missing, name the missing parent and stop.

Otherwise create a new directory in the process temporary directory, with a unique name starting with `xiaohongshu-publish-`. When the canonical note bytes equal the latest 发布单's `note.md`, reuse that directory and show the 发布单 for those bytes.

Write `note.md` only after the note passes the rules below. A refusal names the failing field and creates no directory.

## note.md

UTF-8, LF, no BOM. Header lines, then a line that is exactly `---`, then the body. The file ends with one newline. Split each header line on the first `: `.

Order: `kind`, `title`, then each `image` or `video` and optional `cover`, then each `tag`. No blank header lines. One space after the colon.

```
kind: image-text
title: 周末爬山
image: /Users/wangx/Pictures/1.jpg
image: /Users/wangx/Pictures/2.jpg
tag: 爬山
tag: 周末
---
今天去了香山，风很大。
```

```
kind: video
title: 周末爬山
video: /Users/wangx/Movies/hike.mp4
cover: /Users/wangx/Pictures/hike-cover.jpg
tag: 爬山
---
今天去了香山，风很大。
```

Omit `tag` when there are no topics. Omit `cover` when the video has no cover.

| Field | Rule |
|-------|------|
| `kind` | `image-text` or `video` |
| `title` | One non-empty trimmed line |
| body | The user's text after `---`, non-empty, preserved |
| `image` | Absolute path of an existing regular file. One or more, in carousel order, and only on `image-text` |
| `video` | One absolute path of an existing regular file, only on `video` |
| `cover` | At most one absolute path of an existing regular file, only on `video` |
| `tag` | Trimmed topic with no leading `#`. Drop empties and exact duplicates. Keep the remaining order |

Resolve a relative path against the current working directory at write time. Both media kinds in one request: ask which kind, and write nothing. A named existing `note.md` with no new fields is slipped as-is when it already matches these rules; otherwise rewrite it in place to this canonical form.

## Digest

The digest is the lowercase hex SHA-256 of the exact `note.md` bytes.

## 发布单

Field labels stay as written here. `image-text` displays as 图文, `video` as 视频. Number images from 1. Prefix each topic with `#` on this sheet only. Omit 话题 when there are no tags, and omit 封面 when there is no cover.

```
发布单（说「发布」才会打开创作者中心）
目录：<absolute directory>
文件：<absolute note.md>
校验：<digest>
形态：图文
标题：<title>
图片：
1. <absolute path>
话题：#爬山 #周末
正文：
<stored body>
```

A video sheet uses `视频：<absolute path>` in place of the numbered 图片 list, and adds `封面：<absolute path>` when the note has a cover.
