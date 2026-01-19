"""
Influencer 3D World (polished)

Stage-based posting challenge. Approach the stage, choose the type of post
that will maximize engagement. Timing and approach influence score.
"""
from engine.ursina_framework import GameWorld
import random
try:
    from ursina import Entity, color, Vec3, Text, Button, invoke, camera, Audio
    from ursina.prefabs.first_person_controller import FirstPersonController
except Exception:
    raise ImportError('Ursina is required (pip install ursina)')


POST_TYPES = [
    ("Funny Skit", 0.6),
    ("Emotional Story", 0.8),
    ("Product Shoutout", 0.5),
    ("Live Q&A", 0.7),
]


class Influencer3DWorld(GameWorld):
    def on_start(self):
        self.player = FirstPersonController()
        self.player.height = 2

        self.spawn(Entity(model='plane', scale=Vec3(22,1,22), color=color.black))
        self.stage = self.spawn(Entity(model='cube', scale=Vec3(6,0.5,3), position=Vec3(0,0.25,4), color=color.azure))

        panel = Entity(parent=camera.ui, model='quad', scale=Vec3(0.78,0.36,1), color=color.rgba(10,10,10,140), position=Vec3(0,-0.3,0))
        self.info_text = self.spawn(Text(parent=camera.ui, text='Influencer: Step onto stage and pick a post type', position=(-0.68,-0.23)))
        self.timer_text = self.spawn(Text(parent=camera.ui, text='', position=(0.62,-0.18)))
        self.score_text = self.spawn(Text(parent=camera.ui, text='Score: 0', position=(0.62,-0.24)))
        self.message_text = self.spawn(Text(parent=camera.ui, text='', position=(0,-0.38)))

        self.option_buttons = []
        for i in range(4):
            b = Button(parent=camera.ui, text=POST_TYPES[i][0], scale=(0.24,0.07), position=(-0.66 + i*0.33, -0.5))
            b.on_click = lambda i=i: self.on_option_selected(i)
            b.disable()
            self.option_buttons.append(self.spawn(b))

        try:
            self.snd_correct = Audio('', autoplay=False)
        except Exception:
            self.snd_correct = None

        self.time_per_round = 18.0
        self.time_remaining = self.time_per_round
        self.score = 0
        self.combo = 0
        self.round_active = True

        self.message_text.text = 'Approach the stage to enable posting.'

    def on_option_selected(self, idx):
        # require on/near stage
        dist = (self.player.position - self.stage.position).length()
        if dist > 3.0:
            self.message_text.text = 'Get on stage to post.'
            return

        post, base = POST_TYPES[idx]
        # engagement influenced by base, combo, and remaining time
        self.combo += 1
        combo_bonus = self.combo * 5
        time_bonus = int((self.time_remaining / self.time_per_round) * 60)
        engagement = int(base * 200 + combo_bonus + time_bonus + random.randint(-10, 20))
        self.score += engagement
        self.message_text.text = f'Posted "{post}" — +{engagement} engagement (combo x{self.combo})'
        if self.snd_correct:
            try:
                self.snd_correct.play()
            except Exception:
                pass
        self.spawn_confetti(self.stage.position, color.magenta)
        for b in self.option_buttons:
            try:
                b.disable()
            except Exception:
                pass
        invoke(self.reset_round, delay=1.0)

    def spawn_confetti(self, position, col):
        probes = []
        for i in range(18):
            p = Entity(model='sphere', scale=Vec3(0.06,0.06,0.06), color=col, position=position + Vec3(random.uniform(-0.8,0.8), random.uniform(0,0.6), random.uniform(-0.8,0.8)))
            probes.append(p)
            try:
                p.animate_position(p.position + Vec3(random.uniform(-1.2,1.2), random.uniform(0.6,1.8), random.uniform(-1.2,1.2)), duration=0.8)
                p.animate_scale(0.02, duration=0.8)
            except Exception:
                pass
        invoke(lambda: [setattr(x, 'enabled', False) for x in probes], delay=1.0)

    def reset_round(self):
        self.message_text.text = 'Approach the stage to post again.'
        for b in self.option_buttons:
            try:
                b.enable()
            except Exception:
                pass
        self.time_remaining = self.time_per_round

    def on_update(self, dt):
        # enable buttons when near stage
        dist = (self.player.position - self.stage.position).length()
        if dist <= 3.0:
            for b in self.option_buttons:
                try:
                    b.enable()
                except Exception:
                    pass
            self.info_text.text = 'On stage — pick a post type.'
        else:
            for b in self.option_buttons:
                try:
                    b.disable()
                except Exception:
                    pass
            self.info_text.text = 'Approach the stage to enable posting.'

        self.time_remaining -= dt
        if self.time_remaining <= 0:
            # small penalty for timeout
            self.combo = 0
            self.message_text.text = 'Missed timing — audience distracted.'
            self.time_remaining = self.time_per_round
        self.timer_text.text = f'Time: {int(self.time_remaining)}s'
        self.score_text.text = f'Score: {self.score}'
