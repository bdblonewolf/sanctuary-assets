# Sanctuary design notes (engineering backlog)

## 2026-11-01 - Diablo 1/2 study ideas (approved by Brian via the art bot)
Source: /workspace/sanctuary_art/research/sanctuary_and_diablo_study.md (sections 4-5).
Implement where it fits and blends with the game. Rule: do NOT change any existing environment without asking Brian first.

- Loot colours in D2 tier order, toned down, plus a distinct drop sound for each tier.
- Several death and hit-react animations for each monster family.
- Elite packs marked by dark-hinted auras and physical tells, never skin recolours. Magic takes its element's colour with a dark hint.
- A tight light radius in dungeons; the town is the only warm-lit place (fits the existing town ambient rule).
- Modular, worn player armour with a scraped heraldry slot. Each NPC's keepsake visible on their model.
- A Tristram-style mood theme for Martsirt (music).

Gaps in the docs to define: a loot-colour table, set items, runewords, crafting, whether maps are randomly generated, audio direction.
Waiting on Brian: Quill's voice, whether the Act III coast zones start at level 3, names for the Act V town and the desert city.

## 2026-11-01 - Engineering queue
- Stage 12B sent (rect rings, ocean, isle 96x80, angel). Waiting on Brian's report.
- Border/coast kit stage: use the 12G baseline (/workspace/v5work/backup_pre12H/) unless Brian okays 12H.
- Outdoor ground and plants stage (v5_ground).
- Mission: port all 2D into 3D (audit at /workspace/sanctuary/port_audit_2d_to_3d.md, in progress).
- Audio glitch/static fix. Monster/NPC pathing wiggle fix with a subtle, unnoticeable collision bounce.
