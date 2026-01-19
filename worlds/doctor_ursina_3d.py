"""
Doctor 3D Prototype (Ursina)

Minimal, self-contained 3D playable prototype using the Ursina engine.
Features:
- Move around a simple ER room (WASD + mouse) with a first-person controller
- Approach a patient entity, read symptoms, choose one of four diagnoses
- Timer per patient, scoring, simple particle feedback on results

Notes:
- Requires `ursina` (pip install ursina). If not present, the script prints
  installation instructions and exits gracefully.
- This prototype is intentionally lightweight and asset-free so it runs
  without external files. It is intended as a starting point for a fuller
  3D conversion.
"""

"""
Doctor 3D World (refactored to use engine.ursina_framework.GameWorld)

This version uses the shared `GameRunner` / `GameWorld` from
`engine.ursina_framework` so it can be switched cleanly inside a single
Ursina app and co-exist with other 3D worlds.
"""

from engine.ursina_framework import GameRunner, GameWorld
import random
try:
    from ursina import Entity, color, Vec3, Text, Button, invoke, camera, Audio
    from ursina.prefabs.first_person_controller import FirstPersonController
except Exception:
    raise ImportError('Ursina is required to run 3D worlds (pip install ursina)')


# Small local patient dataset (kept standalone)
PATIENT_CASES = [
    {"symptoms": ["High fever", "Persistent cough", "Body aches"], "diagnosis": "Influenza", "hint": "Common viral infection"},
    {"symptoms": ["Severe headache", "Stiff neck", "Light sensitivity"], "diagnosis": "Meningitis", "hint": "Brain membrane inflammation"},
    {"symptoms": ["Fatigue", "Pale skin", "Shortness of breath"], "diagnosis": "Anemia", "hint": "Low red blood cells"},
    {"symptoms": ["Chest pain", "Left arm numbness", "Cold sweats"], "diagnosis": "Heart Attack", "hint": "Cardiac emergency"},
    {"symptoms": ["Sore throat", "Swollen tonsils", "White patches"], "diagnosis": "Strep Throat", "hint": "Bacterial throat infection"}
]


class Patient3D:
    def __init__(self, position, case):
        self.case = case
        self.entity = Entity(model='cube', color=color.azure, scale=Vec3(1.0, 1.8, 1.0), position=position)
        self.label = Text(text='Patient', position=(0, .9, 0), parent=self.entity, origin=(0,0))
        self.treated = False

    def disable(self):
        try:
            self.entity.disable()
        except Exception:
            pass
        try:
            self.label.disable()
        except Exception:
            pass


class Doctor3DWorld(GameWorld):
    def on_start(self):
        # Player controller
        self.player = FirstPersonController()
        # use integer height to match controller expectations
        self.player.height = 2

        # Room
        self.spawn(Entity(model='plane', scale=Vec3(20,1,20), color=color.gray))
        self.spawn(Entity(model='cube', scale=Vec3(20,4,0.2), position=Vec3(0,2,-10), color=color.light_gray))
        self.spawn(Entity(model='cube', scale=Vec3(20,4,0.2), position=Vec3(0,2,10), color=color.light_gray))
        self.spawn(Entity(model='cube', scale=Vec3(0.2,4,20), position=Vec3(-10,2,0), color=color.light_gray))
        self.spawn(Entity(model='cube', scale=Vec3(0.2,4,20), position=Vec3(10,2,0), color=color.light_gray))

        # UI (screen-space via camera.ui)
        # panel background
        panel = Entity(parent=camera.ui, model='quad', scale=Vec3(0.78, 0.36, 1), color=color.rgba(10,10,10,140), position=Vec3(0, -0.3, 0))

        self.symptoms_text = self.spawn(Text(parent=camera.ui, text='', position=(-0.68, -0.23), origin=(0,0), scale=1.1))
        self.timer_text = self.spawn(Text(parent=camera.ui, text='', position=(0.62, -0.18), origin=(0,0), scale=1.0))
        self.score_text = self.spawn(Text(parent=camera.ui, text='Score: 0', position=(0.62, -0.24), origin=(0,0), scale=0.95))
        self.message_text = self.spawn(Text(parent=camera.ui, text='', position=(0, -0.38), origin=(0,0), scale=1.0))

        # Buttons (screen-space) - disabled until player approaches
        self.option_buttons = []
        for i in range(4):
            b = Button(parent=camera.ui, text=f'Option {i+1}', scale=(0.25,0.07), position=(-0.6 + i*0.4, -0.5))
            b.on_click = lambda i=i: self.on_option_selected(i)
            b.disable()
            self.option_buttons.append(self.spawn(b))

        # sound effects (optional)
        try:
            self.snd_correct = Audio('', autoplay=False)
            self.snd_wrong = Audio('', autoplay=False)
        except Exception:
            self.snd_correct = None
            self.snd_wrong = None

        # combo
        self.combo = 0

        # State
        self.patients = []
        self.current_index = -1
        self.current_patient = None
        self.time_per_patient = 20.0
        self.time_remaining = self.time_per_patient
        self.score = 0

        self.prepare_patients()
        self.next_patient()

    def prepare_patients(self):
        positions = [Vec3(-6,0, -4), Vec3(-2,0,-5), Vec3(2,0,-5), Vec3(6,0,-4), Vec3(0,0,2)]
        cases = random.sample(PATIENT_CASES, min(5, len(PATIENT_CASES)))
        self.patients = [Patient3D(positions[i], cases[i]) for i in range(len(cases))]

    def next_patient(self):
        self.current_index += 1
        if self.current_index >= len(self.patients):
            self.end_shift()
            return

        self.current_patient = self.patients[self.current_index]
        case = self.current_patient.case
        correct = case['diagnosis']
        all_diag = [c['diagnosis'] for c in PATIENT_CASES if c['diagnosis'] != correct]
        choices = [correct] + random.sample(all_diag, 3)
        random.shuffle(choices)

        self.symptoms_text.text = '\n'.join(case['symptoms'])
        for i, b in enumerate(self.option_buttons):
            b.text = choices[i]

        self.time_remaining = self.time_per_patient
        self.message_text.text = 'Approach the patient and choose the diagnosis.'
        # flag to control whether player can choose
        self.option_enabled = False

    def on_option_selected(self, idx):
        if not self.current_patient:
            return
        # require player to be near the patient
        dist = (self.player.position - self.current_patient.entity.position).length()
        if dist > 3.0 and not self.option_enabled:
            self.message_text.text = 'Get closer to interact with the patient.'
        if dist <= 3.0 and not self.option_enabled:
            # enable interaction
            self.option_enabled = True
            self.message_text.text = 'You may now select a diagnosis.'
            for b in self.option_buttons:
                try:
                    b.enable()
                except Exception:
                    pass
            # highlight patient (use brighter cyan)
            try:
                self.current_patient.entity.color = color.cyan
            except Exception:
                self.current_patient.entity.color = color.azure
        if dist > 3.0 and self.option_enabled:
            # walked away
            self.option_enabled = False
            for b in self.option_buttons:
                try:
                    b.disable()
                except Exception:
                    pass
            self.current_patient.entity.color = color.azure
        selected = self.option_buttons[idx].text
        correct = self.current_patient.case['diagnosis']
        # interaction only allowed if near
        dist = (self.player.position - self.current_patient.entity.position).length()
        if dist > 3.0:
            self.message_text.text = 'Too far to interact.'
            return

        if selected == correct:
            self.combo += 1
            combo_bonus = self.combo * 10
            time_bonus = int((self.time_remaining / self.time_per_patient) * 50)
            points = 100 + combo_bonus + time_bonus
            self.score += points
            self.message_text.text = f'Correct! +{points} pts (combo x{self.combo})'
            self.current_patient.entity.color = color.green
            if self.snd_correct:
                try:
                    self.snd_correct.play()
                except Exception:
                    pass
            # spawn particles
            self.spawn_feedback_particles(self.current_patient.entity.position, color.green)
        else:
            self.combo = 0
            self.message_text.text = f'Wrong — correct: {correct}'
            self.current_patient.entity.color = color.red
            if self.snd_wrong:
                try:
                    self.snd_wrong.play()
                except Exception:
                    pass
            self.spawn_feedback_particles(self.current_patient.entity.position, color.red)

        self.score_text.text = f'Score: {self.score}'
        # disable options immediately until next patient
        for b in self.option_buttons:
            try:
                b.disable()
            except Exception:
                pass
        self.option_enabled = False
        invoke(self.clear_message_and_next, delay=1.0)

    def spawn_feedback_particles(self, position, col):
        # simple particle effect: spawn small spheres that expand and fade
        probes = []
        for i in range(10):
            p = Entity(model='sphere', scale=Vec3(0.05,0.05,0.05), color=col, position=position + Vec3(random.uniform(-0.3,0.3), random.uniform(0,0.6), random.uniform(-0.3,0.3)))
            probes.append(p)
            # animate scale and position
            try:
                p.animate_scale(0.6, duration=0.45, curve='out_quad')
                p.animate_position(p.position + Vec3(random.uniform(-0.6,0.6), random.uniform(0.6,1.2), random.uniform(-0.6,0.6)), duration=0.45, curve='out_quad')
            except Exception:
                pass
        # disable after delay
        invoke(lambda: [setattr(x, 'enabled', False) for x in probes], delay=0.6)

    def clear_message_and_next(self):
        self.message_text.text = ''
        if self.current_patient:
            self.current_patient.treated = True
        self.next_patient()

    def end_shift(self):
        self.symptoms_text.text = ''
        self.message_text.text = f'Shift complete! Final score: {self.score}'
        for b in self.option_buttons:
            try:
                b.disable()
            except Exception:
                pass

    def on_update(self, dt):
        if self.current_patient:
            self.time_remaining -= dt
            if self.time_remaining <= 0:
                self.message_text.text = 'Time up! Moving to next patient.'
                self.current_patient.entity.color = color.yellow
                invoke(self.clear_message_and_next, delay=1.0)
            self.timer_text.text = f'Time: {int(self.time_remaining)}s'


def main():
    runner = GameRunner(start_world=Doctor3DWorld)
    runner.run()


if __name__ == '__main__':
    main()
