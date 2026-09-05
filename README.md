# Furious Lardinus

A first-person raycaster shooter written in Python, built to run on a Casio fx-9860G-family
graphing calculator (mono, 128×64) through [PythonExtra](https://github.com/TheRainbowPhoenix/PythonExtra).

Game logic lives on top of a small platform-agnostic engine, `gamekit` (`game/src/gamekit`),
which abstracts vectors, rects, rendering and input behind a common API — the game code itself
never talks to `gint` directly.

## Table of contents

- [Project layout](#project-layout)
- [Requirements](#requirements)
- [Installing on a calculator](#installing-on-a-calculator)
- [Controls](#controls)
- [Building assets from source](#building-assets-from-source)
- [Links](#links)

## Project layout

```
game/
  src/
    gamekit/       platform-agnostic engine: Vector2/Rect2, Input, Renderer, Clock abstractions
    game/          game logic (levels, objects, weapons, rendering) — engine-only, no gint
    systems/       platform backends: gint_renderer.py, gint_input.py, gint_clock.py
    actions/       device-agnostic action/binding system (Actions.MOVE_FORWARD, ...)
    assets/        sprites (pre-baked as gint.image Python modules) and fonts
    main.py        calculator entry point
tools/
  Fx-SDK-2.11.0/       vendored fx-SDK (fxconv asset converter, used offline to bake sprites)
  PythonExtra-*/       vendored PythonExtra release (examples, prebuilt .g1a/.g3a)
  build_gint_textures.py   PNG → gint.image converter, run offline before shipping assets
.github/workflows/release.yml   CI: publishes PythonExtra.g1a + the packaged game/ folder
```

## Requirements

- A Casio fx-9860G-family calculator (mono screen, 128×64) with **PythonExtra** installed.
- To rebuild sprite assets from source PNGs: Python 3 with `Pillow` (only needed for
  `tools/build_gint_textures.py`, not for running the game).

## Installing on a calculator

1. Grab the latest [release](../../releases) — it contains `PythonEx.g1a` and a
   `game-<version>.zip`.
2. If PythonExtra isn't installed yet: connect the calculator via USB in storage mode and copy
   `PythonEx.g1a` to its root — the calculator installs it as an add-in.
3. Extract `game-<version>.zip` and copy the resulting `game` folder onto the
   calculator's storage (same USB connection).
4. Open PythonExtra on the calculator, browse to `game/src/main.py` and run it.

## Controls

| Action        | Key |
| ------------- | --- |
| Move          | 8 / 4 / 2 / 6 |
| Turn          | ◄ / ► |
| Fire          | ▲ |
| Switch weapon | F1 / F2 / F3 |
| Pause         | AC |
| Quit          | EXIT |

## Building assets from source

Sprites are shipped as pre-baked `gint.image(...)` Python modules (see `game/src/assets/sprites`),
not raw PNGs — PythonExtra has no image codec, so conversion happens offline:

```
pip install Pillow
python tools/build_gint_textures.py
```

This reuses fx-SDK's real `fxconv` conversion code (PNG quantization to the 4-shade
`gray_alpha` palette + bitplane packing) and writes a `.py` sibling next to every
`game/src/assets/sprites/**/*.png`.

## Links

- [lephe/Fx-SDK](https://github.com/lephe/Fx-SDK) — the fx-9860G/fx-CG toolchain and `fxconv`
  asset converter this project's asset pipeline is built on.
- [TheRainbowPhoenix/PythonExtra](https://github.com/TheRainbowPhoenix/PythonExtra) — the
  MicroPython/`gint` fork this game runs on.
- [PythonExtra documentation](https://therainbowphoenix.github.io/PythonExtra/index.html)
