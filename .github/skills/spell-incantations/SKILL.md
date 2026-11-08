---
name: spell-incantations
description: 'Research D&D spells and create repeatable, speakable homebrew incantations. Use when the user gives a spell name and asks for its incantation, verbal component, or casting phrase, including spells not listed in an existing guide.'
---

# Spell Incantations

Create a short, repeatable verbal incantation for any D&D spell. This is a homebrew flavor system, not an official D&D rule, and it never changes a spell's mechanics.

## Research the Spell First

The user may provide only a spell name. Treat that as a request to research the spell, not as a reason to ask them to supply its rules.

1. **Establish the rules version.** Use D&D 5e 2014 by default for this workspace. Follow an edition/version named by the user instead. Do not silently mix versions.
2. **Search local sourcebooks first.** Start with `assets/Player's Handbook.md`; then search other relevant local rulebooks, including `assets/Tasha's Cauldron of Everything.md`, `assets/Van Richten's Guide to Ravenloft.md`, `assets/Dungeon Master's Guide.md`, `assets/Monster Manual.md`, and any other relevant book in `assets/`. Search by the spell's exact name and plausible heading variants, then read the complete spell entry—not just a search snippet—including its header, components, range, casting time, target/area, full effect, and higher-level text.
3. **Resolve ambiguity.** If the same name has materially different versions or the user's source is unclear, identify the available candidates and ask which one they mean. If the edition is specified, use only that version. Do not combine similarly named spells.
4. **Use a careful fallback if no local entry exists.** Search an authoritative or reputable source for the requested edition and verify all the details needed below. Prefer an official source when its full rules text is accessible; otherwise use a reputable spell reference and identify the source/version in the answer. Treat web summaries as secondary evidence, not as a substitute for an accessible primary text. Do not fabricate missing details.
5. **Collect the complete working profile.** Record:
   - whether the spell has a verbal component;
   - base spell level;
   - range, targets, and area shape and dimensions, if any;
   - casting time;
   - its actual effects, including damage/healing types, conditions, movement, sensory or material themes, and important limits;
   - its "At Higher Levels" effect, if any.
6. **Set the casting level.** Use the slot level stated by the user. If none is stated, generate for the spell's base level and label that assumption; do not delay with a question. For a ritual cast without a slot, use the base level.

When the user supplies a complete spell entry or summary, use it directly unless it conflicts with the requested edition or an explicit source. If an essential detail cannot be found or verified, say what is missing and ask only for that detail. If the verified spell has no verbal component, say that it has no incantation under this system; do not invent one unless the user explicitly wants a nonverbal vocal flourish. Keep source use concise: cite the spell source and paraphrase its effect rather than reproducing the full copyrighted entry.

## Generation Rules

### 1. Set the word count

Count the spell's level for this casting: use its base level unless it is cast with a higher-level slot, in which case use the slot level. A cantrip is level 0. Ritual casting without a slot uses the base level.

| Level for this casting | Total spoken words |
|---|---:|
| Cantrip-3 | 2 |
| 4-5 | 3 |
| 6-7 | 4 |
| 8-9 | 5 |

The prefix is the first word and counts toward the total. Fill every remaining word with a meaningful effect-word; do not add filler. If upcasting changes the spell's effect, reflect that in an effect-word when possible. The word count is flavor only and never changes casting time or power.

For homebrew spells above 9th level, use `5 + ceiling((level - 9) / 2)` total words: 10th-11th level spells have 6 words, 12th-13th have 7, and so on.

### 2. Choose one prefix category

Use the spell's actual area geometry first, regardless of its range or target. A ray is not a line area unless the spell says it affects a line. If there is no area geometry, use the first applicable category below.

| Spell's form or delivery | Prefix category |
|---|---|
| Line area | Line |
| Cone area | Cone |
| Cube area | Cube |
| Sphere, radius, or emanation area | Sphere |
| Cylinder area | Cylinder |
| Wall or plane area | Wall |
| Other, compound, or irregular area | Other area |
| No area; range is Touch | Touch |
| No area; affects only the caster (Self range) | Self |
| No area; one chosen creature or object at range | Single target |
| No area; multiple chosen creatures or objects at range | Multiple targets |
| No area; creates or places an effect at a chosen point or location | Point effect |
| No area; none of the above describes the effect | Other effect |

For unusual spells, prioritize explicit area geometry over range, then use the no-area categories. "Other area" and "Other effect" are deliberate fallbacks: select the one that best fits the spell rather than forcing it into a misleading shape. A touch spell affecting an area uses its area category, not Touch.

### 3. Form the prefix

For the original six categories, use the matching prefix for the level band. These spellings reproduce the [Reddit post's](https://www.reddit.com/r/DnD/comments/jcoglp/incantation_guide_for_verbal_spell_component_by/) fan-made examples; they are not official rules or a universal D&D language.

| Level band | Touch | Line | Cone | Cube | Sphere | Cylinder |
|---|---|---|---|---|---|---|
| Cantrip-1 | Rah | Su | Zhen | As | Hoc | By |
| 2-3 | Rahja | Sutur | Zhensa | Astrei | Hocla | Byres |
| 4-5 | Rahjahim | Suturine | Zhensashin | Astreimole | Hoclaros | Byreskaal |
| 6-7 | Rahjahimhel | Suturinegen | Zhensashinron | Astreimoleux | Hoclaroskhon | Byreskaalaerr |
| 8-9 | Rahjahimhelvuh | Suturinegenzee | Zhensashinronlong | Astreimoleuxelle | Hoclaroskhonsone | Byreskaalaer |

For the additional categories, use these roots and extend them by level: Cantrip-1 uses the root; 2-3 appends `ja`; 4-5 appends `ja-him`; 6-7 appends `ja-him-hel`; 8-9 appends `ja-him-hel-vuh`. Remove hyphens when speaking.

| Category | Root |
|---|---|
| Self | Esh |
| Single target | Vel |
| Multiple targets | Mira |
| Point effect | Tor |
| Wall | Keth |
| Other area | Oru |
| Other effect | Nym |

For example, a level 4-5 wall spell uses `Kethjahim`. Do not change the established prefixes above to fit the extension pattern.

For spells above 9th level, start with the category's 8-9 prefix and append `sha` once per level above 9. This applies to both the six established prefixes and the additional roots.

### 4. Build the effect-words

After the prefix, choose as many short, pronounceable words as needed to reach the required count. Treat them as evocative magical vocabulary, not literal translations. Prefer distinct sounds and a clear relationship to the spell's supplied information.

Choose words in this order, skipping anything that does not apply:

1. The primary action or result (such as bind, reveal, mend, veil, or summon).
2. Its defining substance, energy, sense, movement, or target.
3. A distinctive secondary effect or condition.
4. An important limit or additional effect that makes the spell recognizable.

At low levels, combine related effects into one compact word rather than breaking the word-count rule. At higher levels, use the extra words to distinguish secondary effects or important upcast changes. Keep the phrase easy to say aloud; an invented or familiar-language word is fine, but use one style consistently within the phrase. Do not copy a published incantation from another source unless the user supplied it and asked to use it.

## Casting-Time Performance

Speak the words in a deliberate, audible cadence. For a casting time of about 10 seconds or less, say the phrase once. For a longer casting time, repeat it continuously at a steady cadence until the casting is complete, as a flavor convention inspired by the Reddit guide. This does not alter the spell's actual casting time, interruptions, components, or other rules.

## Output and Checks

Give the incantation first, then briefly show how it was generated:

- **Spell and casting level**
- **Incantation**
- **Pronunciation**, only if a word's reading is unclear
- **Construction:** selected category and prefix, plus a short gloss of the effect-words
- **Delivery:** once or repeated, based on casting time
- **Spell source:** book and spell heading, or fallback reference and version, when research was needed

Before presenting it, check that:

- the spell has a verbal component;
- its rules version and spell identity are established;
- the component, level, target/area, casting time, and effects were checked in the complete entry or a reliable complete summary;
- the prefix matches the area/delivery rules and level band;
- the total word count is exact, including the prefix;
- every effect-word is supported by the provided spell information;
- the result is speakable and does not imply a new mechanical effect.

If the user asks only for the spoken text, omit the construction notes. Keep the answer concise and label the system homebrew when that context is not already clear.
