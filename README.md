# SmolPet

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![pygame-ce](https://img.shields.io/badge/pygame--ce-2.5-00AA00?style=for-the-badge&logo=python&logoColor=white)
![pywin32](https://img.shields.io/badge/pywin32-Win32%20API-5391FE?style=for-the-badge&logo=windows&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Status](https://img.shields.io/badge/Status-Demo%20complete-brightgreen?style=for-the-badge)

A virtual desktop pet written in Python. A character that lives on top of all
your windows: it falls with gravity, bounces off the edges, can be dragged with
the mouse, decides what to do on its own, talks through text bubbles and switches
between several characters.

A personal project, born as a programming challenge and as a gift.

## Goal

Build a desktop pet with autonomous behavior from scratch, without an existing
engine: believable physics, a simple weight-based AI, spritesheet animations
driven by a state machine, several characters with their own phrases, and Windows
integration (an always-on-top transparent window and reading the active window).
The focus was writing every system by hand.

## Stack

- Python 3.14
- pygame-ce (Community Edition)
- pywin32 (`win32api`, `win32gui`, `win32con`) for the transparent window
- pygetwindow to read the active OS window

Windows only: the window and input layer rely on the Win32 API.

## Architecture

Entity-Component pattern: an `Entity` holds a list of `Component`s and the logic
lives inside each component.

```
main.py              Game loop, Win32 transparent window, keyboard
entites_setup.py     Builds entities and components (World.entities)
characters_setup.py  Character data (spritesheet + phrases)
states_graph.py      State graph and transitions
game_consts.py       Physics, AI and action-weight constants
essentials/
  basics.py          World, Entity, Component, SpriteSheet, Animation, State...
  components.py       Concrete components (see below)
  math_custom.py      Vector2D
  window_consts.py    Screen, FPS, colors
  debug_tools.py      FPS monitor
```

Main components (`essentials/components.py`):

- **PhysicalBall:** gravity, bouncing off floor/walls, air resistance.
- **MouseDrag:** drag with the mouse via spring-like forces.
- **Animator:** plays animations from a `SpriteSheet`.
- **StatesManager:** state machine that picks the animation for the current state.
- **AIController:** autonomous decisions (move, talk, wait, sleep) by weights.
- **CharactersHandler:** switches character (spritesheet and phrases) on the fly.
- **TextBubble:** dialogue bubbles with 9-slice scaling and text wrapping.
- **ParticlesManager:** particles (sparks, hearts, smoke, popcorn).

Key techniques: fixed timestep for physics, a state machine with transition
conditions (`lambda`), weight-based random AI, spritesheets with index-based
animations, an always-on-top transparent window via color key (Win32), and
9-slice scaling for the bubbles.

## Running it

Requires Windows.

```bash
git clone https://github.com/QchuDev/SmolPet.git
cd SmolPet
python -m venv .venv && .venv\Scripts\activate
pip install pygame-ce pywin32 pygetwindow
python main.py
```

Controls: `ESC` quits; `1`-`4` emit particles (spark, popcorn, heart, smoke) at
the cursor; hold left click to drag the pet.

## Project status

Functional/complete as a demo, on hold. The core (physics, animations, states,
AI, characters, particles, bubbles) is implemented and running. Pending:

- Windows only.
- `user_activity.py` reads the active window but is not wired into the AI yet.
- The `AIController`'s `open_img` action and `images_search_testing.py` are
  partially implemented.
- `EntityEraser`, `ParticlesEmitter` and the `punch` states are marked WIP.
- Coupling between components: this motivated re-engineering the engine layer as
  a separate project (Circline).

## Related project

[Circline](https://github.com/QchuDev/Circline): a re-engineering of SmolPet's
embedded engine layer as a reusable ECS (Registry + Systems, GPU rendering). It
extracts the engine, not the whole app. SmolPet is the product; Circline is the
engineering behind its engine.
