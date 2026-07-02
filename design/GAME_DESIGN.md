# RTS Game Design Document

## Overview

An offline hero/unit designer tool for an RTS (Real-Time Strategy) game. The tool manages hero data through a web interface backed by Excel workbooks, with support for custom fields, categories, images, and versioned design documents.

---

## Core Hierarchy

```
Kingdom → Age → Hero → Stats/Properties
```

- **Kingdom**: Race-based faction (e.g., Humans, Dwarves, Elves)
- **Age**: Technological/civilizational era (e.g., Stone Age, Medieval Age)
- **Hero**: Individual unit with stats, abilities, and images
- **Stats**: Dynamic properties grouped by category

---

## The Seven Kingdoms

| # | Kingdom | Dominant Races | Description |
|---|---------|---------------|-------------|
| 1 | **Humans** | Human | The baseline kingdom, versatile and balanced |
| 2 | **Kingdom of Ores** | Dwarves | Mountain-dwelling master craftsmen and heavy infantry |
| 3 | **Kingdom of Magic** | Elves, Wizards, Gnomes | Arcane-focused, ranged and spellcasting superiority |
| 4 | **Kingdom of Evil** | Necromancers, Witches, Goblins | Dark magic, undead, swarms, debuffs |
| 5 | **Kingdom of the Ancients** | Silurian, Dinosaurs | Primitive but powerful, riding dinosaurs |
| 6 | **Kingdom of the Beasts** | Minotaurs, Trolls, Balrogs, Dragons, Serpents | Monstrous creatures, brute strength, terrors |
| 7 | **Kingdom of the Divines** | Gods, Angels, Demigods, Oracles, Archangels | Divine beings, holy powers, extremely powerful but costly |

Each kingdom progresses through all Ages, but their units reflect the kingdom's thematic identity within each era.

---

## Ages (Technological Progression)

All kingdoms share the same timeline:

1. **Classical Age** — Basic civilization, early warfare
2. **Medieval Age** — Knights, castles, organized religion
3. **Mythic Age** — Divine intervention, legendary heroes, magic peaks

*Note: Future ages may include Stone Age, Bronze Age, Iron Age, etc.*

---

## Hero System

### Properties

Heroes have the following default properties, all editable and extensible:

| Category | Fields |
|----------|--------|
| **Identity** | Hero Name, Kingdom, Age, Temple, God, Role, Unit Type |
| **Combat Stats** | Health, Mobility, Melee ATK, Ranged ATK, Magic ATK, Dodge, Parry |
| **Defense** | Melee DEF, Ranged DEF, Magic DEF |
| **Abilities** | Passive, Abilities, Ultimate Skill |
| **Resource** | Cost, Population |
| **Notes** | Free text notes, strengths/weaknesses |

*All property fields are dynamically configurable — add, rename, delete, or recategorize any field.*

### Roles

Example roles by kingdom:

| Kingdom | Common Roles |
|---------|-------------|
| Humans | Knight, Archer, Pikeman, General |
| Kingdom of Ores | Ironbreaker, Runesmith, Slayer, Engineer |
| Kingdom of Magic | Arcanist, Ranger, Enchanter, Druid |
| Kingdom of Evil | Necromancer, Warlock, Goblin Shaman, Witch |
| Kingdom of the Ancients | Dino-Rider, Beastmaster, Shaman, Chieftain |
| Kingdom of the Beasts | Minotaur Berserker, Dragon, Troll Brute, Balrog |
| Kingdom of the Divines | Paladin, Oracle, Archangel, Demigod |

### Sample Heroes

**Paladin** (Kingdom of the Divines, Mythic Age)
- Role: Heavy Tank
- Health: Extremely High
- Melee ATK: Very High
- Passive: Divine Retribution (counterattack every hit)
- Ultimate: Bulwark of Athenia
- Strong vs: Archers | Weak vs: Mages

**Sword Master** (Kingdom of Magic, Mythic Age)
- Role: Duelist
- Health: Moderate
- Mobility: High
- Melee ATK: Extremely High
- Passive: Battle Focus
- Ultimate: Barathor's Wrath

---

## Game Mechanics

### Rage System
- Heroes build Rage through combat
- Required to cast Ultimate Skills
- Example: Paladin needs 1000 Rage, Sword Master needs 800

### Counter System
- Heavy Tanks strong vs Archers
- Duelists strong vs other melee
- Mages strong vs Tanks (low magic defense)
- Archers strong vs flying/magic users

---

## Tool Features

| Feature | Description |
|---------|-------------|
| **Hero Editor** | Visual form-based editor with portrait upload |
| **Age Management** | Create/rename/delete ages, move heroes between them |
| **Kingdom Filter** | Select a kingdom to view all its heroes across ages |
| **Compare Mode** | Side-by-side comparison of 2+ heroes with diff highlighting |
| **Schema Manager** | Add/edit/delete fields, categories, roles, gods, kingdoms |
| **Image Support** | Portrait + up to 5 extra images per hero |
| **Excel Export** | Per-kingdom sheets (e.g., `K_Humans`, `K_Kingdom_of_Ores`) |
| **Auto-save** | Changes saved every 500ms and every 10 minutes |
| **Search** | Filter heroes by name, god, temple, role, or ability text |

---

## Storage Format

The tool generates an Excel workbook with the following sheets:

| Sheet | Content |
|-------|---------|
| `Kingdoms` | List of all kingdoms |
| `Ages` | List of all ages |
| `Fields` | Schema definition (name, category, type) |
| `Categories` | Field category groups |
| `Roles` | List of unit roles |
| `Gods` | List of gods/temples |
| `K_<Kingdom>` | Heroes per kingdom (one sheet each) |
| `Heroes` | Unified backup of all heroes |
| `Legacy_Export` | Flat table for external tools |

Images are stored in `data/images/` as PNG/JPG files referenced by filename.

---

## Versioning

Design documents in the `design/` folder are versioned via Git. Every save creates a commit with a descriptive message, allowing:
- Viewing change history
- Diffing between versions
- Reverting to previous designs
- Collaborative editing through GitHub

---

## Future Extensions

- [ ] Unit trees / upgrade paths per kingdom
- [ ] Resource costs and build times
- [ ] Technology trees per age
- [ ] Terrain and weather modifiers
- [ ] Campaign/story integration
- [ ] Multiplayer balance metrics
