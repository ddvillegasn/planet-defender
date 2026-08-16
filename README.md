# Planet Defender

A 2D arcade game built with Python and Pygame. You pilot a ship defending a planet from incoming
meteors, collecting power-ups and staying alive.

Built as a first-year programming project at Universidad Tecnológica de Pereira, as an exercise in
structuring a complete game loop with object-oriented design.

---

## What it exercises

A game is a useful first project because it forces things a script never does: state that survives
between frames, input that arrives asynchronously, collision detection between arbitrary pairs of
objects, and a main loop that must hold a stable frame rate while doing all of it.

This one covers:

- A **finite state flow** — menu, story screen, play, game over — where each state has its own event
  handling and its own render pass.
- **Frame-independent updates** so behaviour does not change with machine speed.
- **Collision detection** between projectiles, meteors, power-ups and the player.
- **Asset management** — sprites and audio loaded once at start, not per frame.

---

## Controls

| Key | Action |
|---|---|
| `W` `A` `S` `D` or arrow keys | Move the ship |
| `Space` | Shoot |
| `↑` `↓` | Navigate the menu |
| `Enter` | Select |

---

## Running it

Requires Python 3.8+.

```bash
pip install -r requirements.txt
python juego.py
```

Run it from the repository root — the game loads its sprites and audio by relative path
(`nave.png`, `fondo.jpg`, `sonidofondo.mp3` and others), so they must be alongside the script.

---

## Stack

`Python` · `Pygame` for rendering, input and audio · `random` and `time` from the standard library.
Pygame is the only external dependency.

## Status

Complete as a course project. Not maintained.

Known rough edges, kept honest rather than quietly fixed: the whole game lives in a single
`juego.py`, and the media files are committed at full resolution, which makes the repository heavier
than the code deserves.
