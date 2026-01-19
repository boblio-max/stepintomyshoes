"""
Politician 3D World (polished)

Speech-and-policy choice challenge. Approach podium, choose a policy stance,
manage approval score with combo/time bonuses and particle feedback.
"""
from engine.ursina_framework import GameWorld
import random
try:
    from ursina import Entity, color, Vec3, Text, Button, invoke, camera, Audio
    from ursina.prefabs.first_person_controller import FirstPersonController
except Exception:
    raise ImportError('Ursina is required (pip install ursina)')


POLICY_CHOICES = [
    ("Invest in Healthcare", 0.75),
    ("Cut Taxes", 0.6),
    ("Increase Defense", 0.55),
    ("Green Initiative", 0.8),
]


class Politician3DWorld(GameWorld):
    def on_start(self):
        self.player = FirstPersonController()
        self.player.height = 2

        self.spawn(Entity(model='plane', scale=Vec3(22,1,22), color=color.gray))
        self.podium = self.spawn(Entity(model='cube', scale=Vec3(2,0.6,1), position=Vec3(0,0.3,4), color=color.gold))

        panel = Entity(parent=camera.ui, model='quad', scale=Vec3(0.78,0.36,1), color=color.rgba(10,10,10,140), position=Vec3(0,-0.3,0))
        self.info_text = self.spawn(Text(parent=camera.ui, text='Politician: Approach podium and choose a policy', position=(-0.68,-0.23)))
        self.timer_text = self.spawn(Text(parent=camera.ui, text='', position=(0.62,-0.18)))
        self.approval_text = self.spawn(Text(parent=camera.ui, text='Approval: 50', position=(0.62,-0.24)))
        self.message_text = self.spawn(Text(parent=camera.ui, text='', position=(0,-0.38)))

        self.option_buttons = []
        for i in range(4):
            b = Button(parent=camera.ui, text=POLICY_CHOICES[i][0], scale=(0.24,0.07), position=(-0.66 + i*0.33, -0.5))
            b.on_click = lambda i=i: self.on_option_selected(i)
            b.disable()
            self.option_buttons.append(self.spawn(b))

        try:
            self.snd = Audio('', autoplay=False)
        except Exception:
            self.snd = None

        self.time_per_choice = 20.0
        self.time_remaining = self.time_per_choice
        self.approval = 50
        self.combo = 0

    def on_option_selected(self, idx):
        dist = (self.player.position - self.podium.position).length()
        if dist > 3.0:
            self.message_text.text = 'Get to the podium to present policy.'
            return

        choice, base = POLICY_CHOICES[idx]
        self.combo += 1
        combo_bonus = self.combo * 2
        time_bonus = int((self.time_remaining / self.time_per_choice) * 20)
        approval_change = int(base * 30 + combo_bonus + time_bonus + random.randint(-5,5))
        self.approval = max(0, min(100, self.approval + approval_change))
        self.message_text.text = f'Chose "{choice}" — Approval +{approval_change}'
        if self.snd:
            try:
                self.snd.play()
            except Exception:
                pass
        col = color.gold if approval_change > 0 else color.red
        self.spawn_feedback(self.podium.position, col)
        for b in self.option_buttons:
            try:
                b.disable()
            except Exception:
                pass
        invoke(self.reset_round, delay=1.0)

    def spawn_feedback(self, position, col):
        probes = []
        for i in range(10):
            p = Entity(model='cube', scale=Vec3(0.06,0.06,0.06), color=col, position=position + Vec3(random.uniform(-0.4,0.4), random.uniform(0,0.6), random.uniform(-0.4,0.4)))
            probes.append(p)
            try:
                p.animate_position(p.position + Vec3(random.uniform(-0.6,0.6), random.uniform(0.8,1.4), random.uniform(-0.6,0.6)), duration=0.6)
                p.animate_scale(0.01, duration=0.6)
            except Exception:
                pass
        invoke(lambda: [setattr(x, 'enabled', False) for x in probes], delay=0.8)

    def reset_round(self):
        self.message_text.text = 'Choose another policy at the podium.'
        for b in self.option_buttons:
            try:
                b.enable()
            except Exception:
                pass
        self.time_remaining = self.time_per_choice

    def on_update(self, dt):
        dist = (self.player.position - self.podium.position).length()
        if dist <= 3.0:
            for b in self.option_buttons:
                try:
                    b.enable()
                except Exception:
                    pass
            self.info_text.text = 'At podium — select a policy.'
        else:
            for b in self.option_buttons:
                try:
                    b.disable()
                except Exception:
                    pass
            self.info_text.text = 'Approach the podium to present.'

        self.time_remaining -= dt
        if self.time_remaining <= 0:
            self.combo = 0
            self.message_text.text = 'Time expired — opposition moved quickly.'
            self.time_remaining = self.time_per_choice
        self.timer_text.text = f'Time: {int(self.time_remaining)}s'
        self.approval_text.text = f'Approval: {self.approval}'
