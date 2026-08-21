# Roadmap reference

Use this file when building or updating the learning **roadmap** in Phase 2 and after every scoring event in Phase 4.

## Build rules

1. Break the topic into 4–7 **nodes**, ordered foundational → advanced
2. Render a Mermaid flowchart showing all nodes with status and unlock dependencies
3. Re-render the roadmap every time a node's status changes (after scoring)
4. Each session focuses on **one node at a time**
5. Use the **mermaid tool** to render all roadmap diagrams as actual diagrams

## Node statuses

| Status                 | Icon  | Mermaid Style             |
| ---------------------- | ----- | ------------------------- |
| Mastered (≥80)         | ✅ 🟢  | `fill:#059669,color:#fff` |
| Current                | 📖 🔵 | `fill:#0284C7,color:#fff` |
| Extra Practice (60–79) | 🟠    | `fill:#EA580C,color:#fff` |
| Needs Rework (<60)     | ⚠️ 🔴 | `fill:#DC2626,color:#fff` |
| Locked                 | 🔒 ⬜  | `fill:#52525B,color:#fff` |

## Mermaid format

```
flowchart TD
    A["🟢 Node1\nTopic Name\n✅ 92pts"] --> B["🔵 Node2\nTopic Name\n📖 In Progress"]
    B --> C["⬜ Node3\nTopic Name\n🔒 Locked"]
    ...
    style A fill:#059669,color:#fff
    style B fill:#0284C7,color:#fff
    style C fill:#52525B,color:#fff
```

Present the roadmap to the learner and confirm before starting the first node.

## Text progress tracker

Display after every scoring event, synchronized with the Mermaid roadmap:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 Topic: [Topic Name]
Overall Progress: [completed] / [total] nodes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ [Node 1]           Score: [XX]/100  Attempts: [N]
  🟠 [Node 2]           Score: [XX]/100  Extra practice (weakness: [brief])
  🔓 [Node 3] (current) Score: In progress...
  🔒 [Node 4]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⭐ Best score: [Node] ([XX] pts)
🎯 Total questions: [N] | Accuracy: [XX]%
⚠️  Recurring pattern: [if same error type appears across nodes, flag it]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Cross-node weakness tracking

If the same type of error appears in multiple nodes, proactively tell the learner: "I'm noticing a pattern — this might be a systematic gap worth addressing."
