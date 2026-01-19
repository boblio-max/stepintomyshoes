"""
Engineer 3D World (polished)

Panel/puzzle challenge: approach a control panel and select the correct
sequence/tool to repair a circuit. Time and correctness affect score.
"""
from engine.ursina_framework import GameWorld
import random
try:
    from ursina import Entity, color, Vec3, Text, Button, invoke, camera, Audio
    from ursina.prefabs.first_person_controller import FirstPersonController
except Exception:
    raise ImportError('Ursina is required (pip install ursina)')


PUZZLES = [
    {"desc": ["Fuse blown", "Loose wire", "Broken resistor"], "correct": "Loose wire"},
    {"desc": ["Overheated motor", "Corroded contact", "Bad capacitor"], "correct": "Corroded contact"},
    {"desc": ["Short circuit", "Open circuit", "Low voltage"], "correct": "Open circuit"},
]


class Engineer3DWorld(GameWorld):
    def on_start(self):
        self.player = FirstPersonController()
        self.player.height = 2

        self.spawn(Entity(model='plane', scale=Vec3(22,1,22), color=color.gray))
        self.panel_entity = self.spawn(Entity(model='cube', scale=Vec3(4,0.6,2), position=Vec3(0,0.3,4), color=color.rgba(180,180,180,255)))

        panel = Entity(parent=camera.ui, model='quad', scale=Vec3(0.78,0.36,1), color=color.rgba(10,10,10,140), position=Vec3(0,-0.3,0))
        self.desc_text = self.spawn(Text(parent=camera.ui, text='Engineer: Approach panel to inspect problem', position=(-0.68,-0.23)))
        self.timer_text = self.spawn(Text(parent=camera.ui, text='', position=(0.62,-0.18)))
        self.score_text = self.spawn(Text(parent=camera.ui, text='Score: 0', position=(0.62,-0.24)))
        self.message_text = self.spawn(Text(parent=camera.ui, text='', position=(0,-0.38)))

        self.option_buttons = []
        for i in range(3):
            b = Button(parent=camera.ui, text=f'Option {i+1}', scale=(0.32,0.07), position=(-0.52 + i*0.4, -0.5))
            b.on_click = lambda i=i: self.on_option_selected(i)
            b.disable()
            self.option_buttons.append(self.spawn(b))

        try:
            self.snd = Audio('', autoplay=False)
        except Exception:
            self.snd = None

        self.puzzles = random.sample(PUZZLES, min(3, len(PUZZLES)))
        self.current_index = -1
        self.time_per_puzzle = 22.0
        self.time_remaining = self.time_per_puzzle
        self.score = 0
        self.combo = 0

        self.next_puzzle()

    def next_puzzle(self):
        self.current_index += 1
        if self.current_index >= len(self.puzzles):
            self.end_session()
            return

        self.current = self.puzzles[self.current_index]
        choices = list(self.current['desc'])
        random.shuffle(choices)
        self.desc_text.text = '\n'.join(self.current['desc'])
        for i, b in enumerate(self.option_buttons):
            b.text = choices[i]

        self.time_remaining = self.time_per_puzzle
        self.message_text.text = 'Approach the panel and choose the fix.'
        self.option_enabled = False

    def on_option_selected(self, idx):
        if not self.current:
            return
        dist = (self.player.position - self.panel_entity.position).length()
        if dist > 3.0 and not self.option_enabled:
            self.message_text.text = 'Move closer to the panel to interact.'
            return

        if dist <= 3.0 and not self.option_enabled:
            self.option_enabled = True
            self.message_text.text = 'You may now select a fix.'
            for b in self.option_buttons:
                try:
                    b.enable()
                except Exception:
                    pass
            try:
                self.panel_entity.color = color.azure
            except Exception:
                self.panel_entity.color = color.rgba(180,180,180,255)

        selected = self.option_buttons[idx].text
        correct = self.current['correct']
        if selected == correct:
            self.combo += 1
            combo_bonus = self.combo * 10
            time_bonus = int((self.time_remaining / self.time_per_puzzle) * 50)
            points = 120 + combo_bonus + time_bonus
            self.score += points
            self.message_text.text = f'Fixed! +{points} pts (combo x{self.combo})'
            self.panel_entity.color = color.green
            if self.snd:
                try:
                    self.snd.play()
                except Exception:
                    pass
            self.spawn_sparks(self.panel_entity.position, color.yellow)
        else:
            self.combo = 0
            self.message_text.text = f'Incorrect — correct: {correct}'
            self.panel_entity.color = color.red
            if self.snd:
                try:
                    self.snd.play()
                except Exception:
                    pass
            self.spawn_sparks(self.panel_entity.position, color.red)

        self.score_text.text = f'Score: {self.score}'
        for b in self.option_buttons:
            try:
                b.disable()
            except Exception:
                pass
        self.option_enabled = False
        invoke(self.clear_and_next, delay=1.0)

    def spawn_sparks(self, position, col):
        probes = []
        for i in range(14):
            p = Entity(model='sphere', scale=Vec3(0.04,0.04,0.04), color=col, position=position + Vec3(random.uniform(-0.3,0.3), random.uniform(0,0.6), random.uniform(-0.3,0.3)))
            probes.append(p)
            try:
                p.animate_position(p.position + Vec3(random.uniform(-0.6,0.6), random.uniform(0.8,1.4), random.uniform(-0.6,0.6)), duration=0.5)
                p.animate_scale(0.01, duration=0.5)
            except Exception:
                pass
        invoke(lambda: [setattr(x, 'enabled', False) for x in probes], delay=0.7)

    def clear_and_next(self):
        self.message_text.text = ''
        self.next_puzzle()

    def end_session(self):
        self.desc_text.text = ''
        self.message_text.text = f'All systems checked! Final score: {self.score}'
        for b in self.option_buttons:
            try:
                b.disable()
            except Exception:
                pass

    def on_update(self, dt):
        if self.current:
            self.time_remaining -= dt
            if self.time_remaining <= 0:
                self.message_text.text = 'Timeout — moving to next problem.'
                invoke(self.clear_and_next, delay=1.0)
            self.timer_text.text = f'Time: {int(self.time_remaining)}s'
