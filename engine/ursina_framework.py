"""
Lightweight Ursina framework helpers for the 3D conversion.

Provides a GameRunner that owns the Ursina app and can switch between
GameWorld subclasses cleanly without restarting the process.

This file is intentionally dependency-friendly: it will raise a helpful
message if `ursina` is not installed.
"""
try:
    from ursina import Ursina, Entity, color, Vec3, Text, Button, window, invoke, camera, time
except Exception:
    raise ImportError("Ursina is required for the 3D framework. Install with `pip install ursina`.")

from typing import Type, Optional


class GameWorld:
    """Base class for all 3D worlds.

    Subclasses should implement `on_start(self)` to create entities/UI and
    `on_update(self, dt)` for per-frame updates. `on_end` should cleanup.
    """

    def __init__(self, runner: 'GameRunner'):
        self.runner = runner
        self.entities = []
        self.ui = []

    def spawn(self, entity):
        self.entities.append(entity)
        return entity

    def spawn_ui(self, element):
        self.ui.append(element)
        return element

    def on_start(self):
        pass

    def on_update(self, dt):
        pass

    def on_end(self):
        # disable entities and UI created by the world
        for e in self.entities:
            try:
                e.disable()
            except Exception:
                pass
        for u in self.ui:
            try:
                u.disable()
            except Exception:
                pass


class GameRunner:
    """Runs an Ursina app and manages world switching."""

    def __init__(self, start_world: Optional[Type[GameWorld]] = None):
        self.app = Ursina()
        window.title = 'Step Into My Shoes - 3D'
        window.borderless = False
        window.fullscreen = False
        self.current_world: Optional[GameWorld] = None
        self.start_world = start_world

        # Runner update called by Ursina each frame
        self.app.update = self._update

    def change_world(self, world_cls: Type[GameWorld]):
        # end previous
        if self.current_world:
            try:
                self.current_world.on_end()
            except Exception:
                pass
        # instantiate and start new
        self.current_world = world_cls(self)
        try:
            self.current_world.on_start()
        except Exception as e:
            print('Error starting world:', e)

    def _update(self):
        dt = time.dt
        if self.current_world:
            try:
                self.current_world.on_update(dt)
            except Exception as e:
                print('Error in world update:', e)

    def run(self):
        # optionally start an initial world
        if self.start_world:
            self.change_world(self.start_world)
        self.app.run()
