"""
Lawyer 3D World (polished)

Interactive courtroom prototype adapted from the Doctor 3D pattern.
Approach the witness, enable choices (which statement contradicts the evidence),
use time and combo scoring, and receive particle feedback and optional sounds.
"""
from engine.ursina_framework import GameWorld
import random
try:
    from ursina import Entity, color, Vec3, Text, Button, invoke, camera, Audio
    from ursina.prefabs.first_person_controller import FirstPersonController
except Exception:
    raise ImportError('Ursina is required (pip install ursina)')


CASE_DATA = [
    {"prompt": ["Witness says saw the defendant at 9pm", "Camera timestamp shows 8pm", "Alibi: at home"], "correct": "Camera timestamp shows 8pm"},
    {"prompt": ["Witness: I heard shouting", "No noise on record", "No neighbors reported noise"], "correct": "No noise on record"},
    {"prompt": ["Witness: victim left alone", "CCTV shows visitor", "Phone records show calls"], "correct": "CCTV shows visitor"},
    {"prompt": ["Witness: I saw a red car", "Forensics: paint not from red cars", "Traffic cams show blue car"], "correct": "Traffic cams show blue car"},
]


class Lawyer3DWorld(GameWorld):
    def on_start(self):
        self.player = FirstPersonController()
        self.player.height = 2

        # scene
        self.spawn(Entity(model='plane', scale=Vec3(22,1,22), color=color.rgb(30,30,40)))
        self.spawn(Entity(model='cube', scale=Vec3(20,4,0.2), position=Vec3(0,2,-10), color=color.light_gray))

        # witness entity
        self.witness = self.spawn(Entity(model='cube', scale=Vec3(0.8,1.8,0.8), position=Vec3(0,0,4), color=color.azure))

        # UI panel
        panel = Entity(parent=camera.ui, model='quad', scale=Vec3(0.78,0.36,1), color=color.rgba(10,10,10,140), position=Vec3(0,-0.3,0))
        self.prompt_text = self.spawn(Text(parent=camera.ui, text='', position=(-0.68,-0.23), origin=(0,0), scale=1.0))
        self.timer_text = self.spawn(Text(parent=camera.ui, text='', position=(0.62,-0.18), origin=(0,0)))
        self.score_text = self.spawn(Text(parent=camera.ui, text='Score: 0', position=(0.62,-0.24), origin=(0,0)))
        self.message_text = self.spawn(Text(parent=camera.ui, text='', position=(0,-0.38), origin=(0,0)))

        # option buttons
        self.option_buttons = []
        for i in range(3):
            b = Button(parent=camera.ui, text=f'Option {i+1}', scale=(0.34,0.08), position=(-0.5 + i*0.5, -0.5))
            b.on_click = lambda i=i: self.on_option_selected(i)
            b.disable()
            self.option_buttons.append(self.spawn(b))

        # audio placeholders
        try:
            self.snd_correct = Audio('', autoplay=False)
            self.snd_wrong = Audio('', autoplay=False)
        except Exception:
            self.snd_correct = None
            self.snd_wrong = None

        # state
        self.cases = random.sample(CASE_DATA, min(4, len(CASE_DATA)))
        self.current_index = -1
        self.current_case = None
        self.time_per_case = 25.0
        self.time_remaining = self.time_per_case
        self.score = 0
        self.combo = 0

        self.next_case()

    def next_case(self):
        self.current_index += 1
        if self.current_index >= len(self.cases):
            self.end_session()
            return

        self.current_case = self.cases[self.current_index]
        choices = list(self.current_case['prompt'])
        random.shuffle(choices)
        self.prompt_text.text = '\n'.join(self.current_case['prompt'])
        for i, b in enumerate(self.option_buttons):
            b.text = choices[i]

        self.time_remaining = self.time_per_case
        self.message_text.text = 'Approach the witness and choose the contradictory statement.'
        self.option_enabled = False

    def on_option_selected(self, idx):
        if not self.current_case:
            return
        # require approach
        dist = (self.player.position - self.witness.position).length()
        if dist > 3.0 and not self.option_enabled:
            self.message_text.text = 'Get closer to the witness to interact.'
            return

        if dist <= 3.0 and not self.option_enabled:
            self.option_enabled = True
            self.message_text.text = 'You may now select.'
            for b in self.option_buttons:
                try:
                    b.enable()
                except Exception:
                    pass
            try:
                self.witness.color = color.cyan
            except Exception:
                self.witness.color = color.azure

        selected = self.option_buttons[idx].text
        correct = self.current_case['correct']
        if selected == correct:
            self.combo += 1
            combo_bonus = self.combo * 8
            time_bonus = int((self.time_remaining / self.time_per_case) * 40)
            points = 80 + combo_bonus + time_bonus
            self.score += points
            self.message_text.text = f'Correct! +{points} pts (combo x{self.combo})'
            self.witness.color = color.green
            if self.snd_correct:
                try:
                    self.snd_correct.play()
                except Exception:
                    pass
            self.spawn_feedback(self.witness.position, color.green)
        else:
            self.combo = 0
            self.message_text.text = f'Wrong — correct: {correct}'
            self.witness.color = color.red
            if self.snd_wrong:
                try:
                    self.snd_wrong.play()
                except Exception:
                    pass
            self.spawn_feedback(self.witness.position, color.red)

        self.score_text.text = f'Score: {self.score}'
        for b in self.option_buttons:
            try:
                b.disable()
            except Exception:
                pass
        self.option_enabled = False
        invoke(self.clear_and_next, delay=1.0)

    def spawn_feedback(self, position, col):
        probes = []
        for i in range(12):
            p = Entity(model='sphere', scale=Vec3(0.05,0.05,0.05), color=col, position=position + Vec3(random.uniform(-0.3,0.3), random.uniform(0,0.6), random.uniform(-0.3,0.3)))
            probes.append(p)
            try:
                p.animate_scale(0.6, duration=0.45)
                p.animate_position(p.position + Vec3(random.uniform(-0.6,0.6), random.uniform(0.6,1.2), random.uniform(-0.6,0.6)), duration=0.45)
            except Exception:
                pass
        invoke(lambda: [setattr(x, 'enabled', False) for x in probes], delay=0.6)

    def clear_and_next(self):
        self.message_text.text = ''
        self.next_case()

    def end_session(self):
        self.prompt_text.text = ''
        self.message_text.text = f'Session complete! Final score: {self.score}'
        for b in self.option_buttons:
            try:
                b.disable()
            except Exception:
                pass

    def on_update(self, dt):
        if self.current_case:
            self.time_remaining -= dt
            if self.time_remaining <= 0:
                self.message_text.text = 'Time up! Moving on.'
                invoke(self.clear_and_next, delay=1.0)
            self.timer_text.text = f'Time: {int(self.time_remaining)}s'
