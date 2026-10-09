---
name: xiaohongshu-publish
description: "Publisher for a finished Xiaohongshu note. Use when the user wants to publish an image-text note (小红书图文) or a video note (小红书视频) with a title, body, and local media."
metadata:
  version: 1.0.0
---

# Xiaohongshu publisher

Publish one finished 图文 or 视频 note. The **发布单** is the note the user has been shown. The creator site opens on a later message that publishes that 发布单.

## Steps

### 1. Classify

Choose **publish** only when all three hold:

1. This conversation already showed a 发布单.
2. The message authorizes that 发布单 with 发布, 发出去, or publish.
3. The message leaves kind, title, body, media, and tags unchanged, and it names no directory other than that 发布单's 目录.

Every other message is a **slip** turn.

**Done when:** publish is chosen only if all three hold; otherwise the turn is a slip.

### 2. Slip

Follow [`note-format.md`](note-format.md). Show the 发布单 and end the turn.

**Done when:** the 发布单 from note-format.md is on screen and its 校验 matches the note file, or the note was refused with the failing field and no publish directory was created. The creator site stays closed.

### 3. Publish

Open [`publish-flow.md`](publish-flow.md) only after step 1 chose publish, and run it.

**Done when:** the outcome required by publish-flow.md is on screen.

## Boundaries

When the user wants the wording written, ask for the finished title, body, and local media.
