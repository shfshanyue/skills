# Publish flow

Run this file only after SKILL.md step 1 chose publish. Drive the browser with the ego-browser skill: one TaskSpace for this publish, resume that same space after `handOff`, and take controls from the current snapshot. Use that skill's file-upload, `handOff`, and `finish` APIs.

**Pre-click stop.** Report the reason and finish an open TaskSpace with no kept pages. 发布 stays unclicked.

**Digest gate.** Recompute the `note.md` digest defined in [`note-format.md`](note-format.md). On a mismatch, take a pre-click stop whose reason is that the note changed, then run SKILL.md step 2 on the current `note.md`. That slip or refusal ends the flow.

## 1. Match the 发布单

Apply the digest gate.

**Done when:** the digest equals 校验, or the digest gate has ended the flow with a new 发布单.

## 2. Open the publish page

Open `https://creator.xiaohongshu.com/publish/publish`, record the space id, and snapshot. When that URL is not the publish surface, report the page and take the pre-click stop.

When the snapshot is a login, 实名, or captcha wall, `handOff` and say what the user needs to finish. After they return, rerun step 1 in the same space, then snapshot and continue from the step that was waiting.

**Done when:** the space id is recorded and the snapshot shows the publish page, or the user holds the space.

## 3. Enter the matching upload entry

Land on 上传图文 for 图文, or 上传视频 for 视频. When the snapshot shows another entry, switch to the matching one and snapshot again.

**Done when:** the snapshot shows the entry that matches 形态.

## 4. Upload

Upload with the ego-browser file APIs.

图文: upload the image paths in note order. Wait until those images are visible in that order, at most 60 seconds.

视频: upload the one video. Wait until the page shows the video can be published, at most 3 minutes. Upload a cover only when the note has one; otherwise leave the page's cover.

A visible upload failure, or a wait that runs out, is a pre-click stop.

**Done when:** the page shows the note's media, or a pre-click stop is done.

## 5. Fill

Fill the title and the body, then read them back. The title equals the note title, and the body contains the note body. Add each tag as a topic until each tag is visible. Topic markers that the page inserts into the description still pass the body check.

A page limit, a rejected tag, or another visible content error is a pre-click stop. A login, 实名, or captcha wall uses the hand-off in step 2.

Leave schedule, location, visibility, and every switch outside steps 4 and 5 as the page opened them.

**Done when:** title, body, and every tag check out, or a pre-click stop is done.

## 6. Click 发布

Apply the digest gate. When it matches, click 发布 once.

**Done when:** 发布 was clicked once after the digest matched, or the digest gate ended the flow with a new 发布单.

## 7. Report

The note is published when the page shows success wording, or a note link that is not still the publish editor URL. Report 形态, 标题, 目录, that wording, and the link when the page shows one. Then finish the TaskSpace with no kept pages.

When the outcome is unclear, keep the publish page, describe the visible state, and leave the one click in step 6 as the only click.

**Done when:** the chat has a published result, or an unclear page that was kept.
