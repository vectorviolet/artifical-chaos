"""Headless boot check -- catches asset/map wiring mistakes that only
surface once the game is actually built and run (e.g. a Tiled object layer
referencing a renamed asset). Run locally with:

    SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy uv run python scripts/smoke_test.py

Requires cwd = repo root (matches how __main__.py and CI both invoke it).
"""
import sys

sys.path.insert(0, "src")
sys.path.insert(0, "src/pygamine")


def boot_game() -> None:
    from app.game import Game

    game = Game()
    print(f"  map spawned: {len(game.flags)} flags, {len(game.soldiers)} soldiers, "
          f"{len(game.robots)} robots, {len(game.walls)} walls")

    # _listen_inputs() is normally called every frame by Application.run()
    # before update() -- populates game.keys, which Player/Soldier read.
    game._listen_inputs()
    for _ in range(3):
        game.update()
        game.draw()
    print("  3 update/draw frames: OK")

    # restart() re-runs the same heavy Map/Player/Tutorial construction
    # __init__ does -- worth a real (not monkeypatched) pass here, since
    # tests/test_game_restart.py only exercises it against lightweight
    # stand-ins to avoid loading the real Tiled map on every test run.
    game.restart()
    game.update()
    game.draw()
    print("  restart(): OK")


def run_game_briefly() -> None:
    # The path the steps above never touch: the splash, any run() override
    # and the hand-off into the main loop (a crash there once shipped unseen).
    from app.game import Game
    from pygamine.devtools.smoke import run_briefly

    frames = run_briefly(Game())
    print(f"  splash + {frames} main-loop frames via the real run(): OK")


def main() -> None:
    print("Booting Game() and running a few frames...")
    boot_game()
    print("Running the real run() -- splash and main loop -- briefly...")
    run_game_briefly()
    print("Smoke test passed.")


if __name__ == "__main__":
    main()
