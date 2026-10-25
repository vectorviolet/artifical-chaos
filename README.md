# Artificial Chaos

![Coverage](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/vectorviolet/artifical-chaos/main/.github/badges/coverage.json)

Artificial Chaos is a 2D top-down game prototype built with [pygame](https://www.pygame.org/). You control the last human still in control of their own mind, freeing mind-controlled soldiers into a following squad while fighting off autonomous combat drones — see [GDD.md](GDD.md) for the full story/design doc.

![Gameplay](docs/preview.gif)

> **⚠️ Status: unfinished prototype**, not in active development. Core combat, a first pass of effects, and flag-capture win/lose now work (see Gameplay below); most of the effects/projectiles sheets, 2 of 6 soldier classes, and 1 of 5 drone types (Centipede) are still unimplemented. It has been migrated onto my shared [`pygamine`](https://github.com/vectorviolet/pygamine) engine (vendored as a git submodule, like [chokepoint](https://github.com/vectorviolet/chokepoint)): the game loop now extends `pygamine.Application`, entities are `GameObject`s with `Transform`/`SpriteRenderer2D`/`Animator` components rendered through `pygamine.Camera`, and asset/spritesheet handling uses `pygamine` instead of project-local copies.

## Gameplay

Move the squad leader around the map. When you get close to a soldier, they join your army and start following you while spreading out to avoid crowding each other. Hold the left mouse button to fire your sidearm at the nearest drone in range — ranged attacks flash a muzzle, a tracer flies to the target, and a spark/blood-spatter hits home; drones burst into an explosion on death. Recruited soldiers auto-fight nearby drones too. Drones aggro onto the player or squad within range and melee or fire back. Every objective flag spawns with a drone guarding it — clear it, then stand at the flag (with the player or a recruited soldier) to capture it; a drone back in range halts or reverses progress. Capture every flag on the map to win; the Squad Leader dying ends the run. Your own HP is always shown overhead; soldiers and drones show theirs too, once they've taken a hit. Walking leaves a trail of fading footprints, and your rank insignia is shown next to the player.

### Entities

| Entity                | Sprite                                                             | Behaviour                                                                 |
|-----------------------|----------------------------------------------------------------------|---------------------------------------------------------------------------|
| Squad Leader (player) | `SquadLeader.png`  | WASD/arrow movement with friction; leaves footprints; recruits nearby soldiers; rank insignia shown above; fires a sidearm at the nearest drone in range while the left mouse button is held |
| Soldier               | `Assault-Class.png`, `Sniper-Class.png`, `MachineGunner-Class.png`, `AntiTank-Class.png` | Recruited when the player comes within range (shown with a green ring underneath), then follows/avoids crowding, and auto-fires at the nearest drone in range instead of following once one's close enough — fully autonomous, no player-directed targeting |
| Drone                 | `Scarab.png`, `Spider.png`, `Hornet.png`, `Wasp.png` | Aggros onto the player/squad within range, chases, then melees or fires depending on distance (Hornet/Wasp are ranged-only, no melee); Scarab/Spider hold a destroyed pose before being removed, Hornet/Wasp are removed immediately (no destroyed frame in their sheets) |
| Objective flag        | `objective-flag.png`, `objective-pulse.png` | Spawns with a drone guarding it; a green circle fills in behind it while held by the player/a recruited soldier and uncontested by a nearby drone, stops pulsing once captured |

### Controls

| Action               | Input                  |
|----------------------|------------------------|
| Move                 | `W` `A` `S` `D` / Arrow keys |
| Toggle debug overlay | `F1`                   |
| Toggle fullscreen    | `F11`                  |
| Quit                 | `Esc`                  |

## Requirements

- Python 3.10+
- [pygame](https://www.pygame.org/), [pytmx](https://github.com/bitcraft/pytmx)

## Running

```bash
git clone --recurse-submodules https://github.com/vectorviolet/artifical-chaos.git
cd artifical-chaos
pip install pygame pytmx
python __main__.py
```

If you forgot `--recurse-submodules`: `git submodule update --init` (pulls in the `pygamine` engine).

## Project layout

```
__main__.py               Entry point — injects src/ + src/pygamine/ onto sys.path, runs Game()
src/app/game.py           Game (extends pygamine.Application) — update/draw orchestration
src/gameplay/map.py       Tiled map loader + Obstacle (collision walls)
src/gameplay/camera.py    FollowCamera — pygamine.Camera plus a follow() helper
src/gameplay/collision.py AABB Collide resolution against the wall list
src/gameplay/animation.py Builds Animator clips from pygamine.SpriteSheet frames
src/gameplay/combat.py    Shared hitscan combat primitives (find_nearest/ready_to_attack/apply_damage)
src/gameplay/effects.py   Cosmetic combat VFX (muzzle flash, hit spark/spatter, explosion, bullet tracer)
src/gameplay/ui.py        Overhead progress/HP bars + radial fills (draw_bar, draw_radial_progress, draw_health_bar)
src/gameplay/player.py    Player (squad leader) + Footprint; fights with a sidearm
src/gameplay/soldier.py   Recruitable soldiers that follow + auto-fight nearby drones
src/gameplay/robots.py    Drone base class + Scarab/Spider/Hornet/Wasp subclasses (aggro/chase/attack AI)
src/gameplay/flag.py      Objective flags -- capturable while held and uncontested by a drone
src/util/constants.py     Constants (FPS, render size, sprite sizes, durations, ranks, combat tuning)
src/pygamine/             Shared engine (git submodule)
assets/                   Images (soldiers, robots, UI), tileset + Tiled map
```

## Credits

Art from [mattwalkden](https://mattwalkden.itch.io/) — released into the public domain under [CC0](https://creativecommons.org/publicdomain/zero/1.0/). A written credit is not required but appreciated. See [CREDITS.md](CREDITS.md) for every asset pack and library with its license; it also ships with the game.

## Asset sources

Every file under `assets/` is listed in `assets/SOURCES.yaml` with its source:

- **A pack**, given by its slug (for example `kenney-ui-pack`). The entry also gives the file's
  path inside that pack as `original`. Images built from several pack files list them under
  `composited_from` instead. Edited pack files say what changed under `modified`.
- **`own`**, for files made for this game.
- **`ai-generated`**, for files made with an AI image tool. Each needs a `note` naming the tool and
  who generated it; the credits list them under "AI-generated content".
- **`unknown`**, for files whose origin or license isn't confirmed yet. Each needs a `todo` that
  says what to do; the credits list them as "not yet verified".

The `packs` section names each pack, its author, URL, license and what the game uses it for.
Each pack's own license text is in `licenses/assets/<slug>.txt`, and every build ships it.

When you add, replace or remove an asset:

1. Update `assets/SOURCES.yaml`, and add `licenses/assets/<slug>.txt` for any new pack.
2. Run `uv run python scripts/gen_credits.py` to regenerate CREDITS.md's asset section. Don't
   edit that section by hand.
3. Run the tests. `tests/test_sources.py` fails if a file is missing from `SOURCES.yaml`, if a
   listed file doesn't exist, if a pack has no license text, or if CREDITS.md is out of date.

Only ship assets whose license allows bundling them in a distributed game; resolve every
`unknown` entry before the next release.

## Contributing

1. Fork this repository.
2. Clone your fork: `git clone https://github.com/<you>/artifical-chaos.git`
3. Create a branch: `git checkout -b feature/<your-feature>`
4. Commit + push: `git commit -am "<message>" && git push origin feature/<your-feature>`
5. Open a pull request.

## Author

Umutcan Ekinci — [umutcannekinci@gmail.com](mailto:umutcannekinci@gmail.com)

## License

See [LICENSE](LICENSE) (MIT).
