# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project aims to
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] – 2026-08-12

### Added

- Startup splash screen and a title card as a second splash slide.
- A controls tutorial overlay, with restart-on-any-key at game over.
- A dedicated spawn point, tighter tutorial key clusters, and a redesigned restart prompt.
- Wall-impact decals, a persistent squad-stance HUD, and line-of-sight gating for ranged attacks.
- Flag difficulty tiers ranked by distance from the spawn point.
- `big-fragments.png`/`small-fragments.png` VFX on drone death.
- itch.io store description.

### Changed

- Reworked Spider to melee-only and gave soldier classes distinct HP.
- Renamed the `pygame_core` submodule/dependency to `pygamine` and tracked it through several releases.

### Fixed

- Replaced an O(movers × walls) collision cost with a static `SpatialGrid`.
- Muzzle flash position now mirrors with facing instead of tracking the aim angle.
- Clamped `delta_time` to fix a post-restart teleport/tunneling bug.

## [0.1.0] – 2026-07-27

Initial release. Drone AI, hitscan combat, drone/soldier class variety, flag-capture win condition,
recruited-soldier squads, combat VFX (muzzle flash, hit spark, explosions, tracers), and a PyInstaller
release pipeline for Windows/macOS/Linux plus itch.io.
