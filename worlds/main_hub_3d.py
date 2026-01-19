"""
Main 3D Hub - walkable lobby to choose careers

The hub shows doors for each career world. Approach a door and press
`E` to enter that career's 3D world. This file wires the runner and
the individual world classes together.
"""
from engine.ursina_framework import GameWorld, GameRunner
try:
    from ursina import Entity, color, Vec3, Text, distance, held_keys
    from ursina.prefabs.first_person_controller import FirstPersonController
except Exception:
    raise ImportError('Ursina is required (pip install ursina)')

from worlds.doctor_ursina_3d import Doctor3DWorld
from worlds.lawyer_ursina_3d import Lawyer3DWorld
from worlds.influencer_ursina_3d import Influencer3DWorld
from worlds.politician_ursina_3d import Politician3DWorld
from worlds.engineer_ursina_3d import Engineer3DWorld


class HubWorld(GameWorld):
    def on_start(self):
        self.player = FirstPersonController()
        self.player.height = 2

        self.spawn(Entity(model='plane', scale=Vec3(28,1,28), color=color.rgb(30,30,40)))

        # doors (simple colored cubes representing each career)
        self.doors = {
            'Doctor': (self.spawn(Entity(model='cube', scale=Vec3(2,4,0.3), position=Vec3(-8,2,6), color=color.azure)), Doctor3DWorld),
            'Lawyer': (self.spawn(Entity(model='cube', scale=Vec3(2,4,0.3), position=Vec3(-2,2,6), color=color.brown)), Lawyer3DWorld),
            'Influencer': (self.spawn(Entity(model='cube', scale=Vec3(2,4,0.3), position=Vec3(4,2,6), color=color.azure)), Influencer3DWorld),
            'Politician': (self.spawn(Entity(model='cube', scale=Vec3(2,4,0.3), position=Vec3(10,2,6), color=color.gold)), Politician3DWorld),
            'Engineer': (self.spawn(Entity(model='cube', scale=Vec3(2,4,0.3), position=Vec3(16,2,6), color=color.light_gray)), Engineer3DWorld),
        }

        self.hint = self.spawn(Text(text='Walk to a door and press E to enter a career world', position=(-0.7,0.45)))
        self.prompt = self.spawn(Text(text='', position=(0,-0.45)))

    def on_update(self, dt):
        # check proximity to doors
        from ursina import distance
        player_pos = self.player.position
        near = None
        for name, (door_entity, world_cls) in self.doors.items():
            if (door_entity.position - player_pos).length() < 3.0:
                near = (name, world_cls)
                break

        if near:
            name, world_cls = near
            self.prompt.text = f'Press E to enter: {name}'
            from ursina import held_keys
            if held_keys['e']:
                # change world via runner
                self.runner.change_world(world_cls)
        else:
            self.prompt.text = ''


def main():
    runner = GameRunner(start_world=HubWorld)
    runner.run()


if __name__ == '__main__':
    main()
