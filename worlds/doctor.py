"""
Step Into My Shoes - Doctor World
Triage patients by matching symptoms to diagnoses under time pressure.
Teaches: Speed, decision-making, attention under pressure.
"""

import pygame
import random
from engine.colors import (
    BACKGROUND, WHITE, BLACK, GREY, DOCTOR_PRIMARY, DOCTOR_SECONDARY,
    DOCTOR_ACCENT, SUCCESS, DANGER, WARNING, TEXT_SECONDARY, CARD_BG,
    ACCENT, TEXT_MUTED
)
from engine.ui import (
    draw_text, draw_text_left, draw_wrapped_text, ModernButton,
    ParticleSystem, ScreenFlash, draw_lives
)
from engine.backstory_ai import get_performance_feedback, get_career_lesson

pygame.init()

WIDTH, HEIGHT = 900, 600

# Patient data with symptoms and correct diagnoses
PATIENT_CASES = [
    {
        "symptoms": ["High fever", "Persistent cough", "Body aches"],
        "diagnosis": "Influenza",
        "severity": "moderate",
        "hint": "Common viral infection"
    },
    {
        "symptoms": ["Severe headache", "Stiff neck", "Light sensitivity"],
        "diagnosis": "Meningitis",
        "severity": "critical",
        "hint": "Brain membrane inflammation"
    },
    {
        "symptoms": ["Fatigue", "Pale skin", "Shortness of breath"],
        "diagnosis": "Anemia",
        "severity": "moderate",
        "hint": "Low red blood cells"
    },
    {
        "symptoms": ["Excessive thirst", "Frequent urination", "Blurred vision"],
        "diagnosis": "Diabetes",
        "severity": "moderate",
        "hint": "Blood sugar disorder"
    },
    {
        "symptoms": ["Chest pain", "Left arm numbness", "Cold sweats"],
        "diagnosis": "Heart Attack",
        "severity": "critical",
        "hint": "Cardiac emergency"
    },
    {
        "symptoms": ["Rash", "Joint pain", "Fever after tick bite"],
        "diagnosis": "Lyme Disease",
        "severity": "moderate",
        "hint": "Tick-borne infection"
    },
    {
        "symptoms": ["Wheezing", "Difficulty breathing", "Chest tightness"],
        "diagnosis": "Asthma Attack",
        "severity": "urgent",
        "hint": "Airway constriction"
    },
    {
        "symptoms": ["Sudden confusion", "Slurred speech", "Face drooping"],
        "diagnosis": "Stroke",
        "severity": "critical",
        "hint": "Brain blood flow issue"
    },
    {
        "symptoms": ["Abdominal pain", "Nausea", "Right side tenderness"],
        "diagnosis": "Appendicitis",
        "severity": "urgent",
        "hint": "Inflamed appendix"
    },
    {
        "symptoms": ["Sore throat", "Swollen tonsils", "White patches"],
        "diagnosis": "Strep Throat",
        "severity": "mild",
        "hint": "Bacterial throat infection"
    }
]

ALL_DIAGNOSES = [case["diagnosis"] for case in PATIENT_CASES]


class Patient:
    """Represents a patient case."""
    
    def __init__(self, case_data):
        self.symptoms = case_data["symptoms"]
        self.correct_diagnosis = case_data["diagnosis"]
        self.severity = case_data["severity"]
        self.hint = case_data["hint"]
        self.treated = False
        self.result = None
    
    def get_severity_color(self):
        if self.severity == "critical":
            return DANGER
        elif self.severity == "urgent":
            return WARNING
        elif self.severity == "moderate":
            return DOCTOR_PRIMARY
        return ACCENT


class DoctorWorld:
    """
    Doctor Career Mini-Game
    Players diagnose patients by matching symptoms to conditions.
    """
    
    def __init__(self, story_package=None):
        self.story = story_package or {
            "intro": "Welcome to the Emergency Room!\n\nPatients are arriving with various symptoms.\nYour job is to correctly diagnose each one.\n\nRead the symptoms carefully and select the right diagnosis.\nSpeed and accuracy both matter!"
        }
        self.state = "intro"
        self.score = 0
        self.total_patients = 5
        self.current_patient_index = 0
        self.patients = []
        self.current_patient = None
        self.options = []
        self.selected_option = None
        self.time_per_patient = 15.0
        self.time_remaining = self.time_per_patient
        self.combo = 0
        self.max_combo = 0
        # Lives / failure state
        self.lives = 3
        self.failed = False
        
        # Visual effects
        self.particles = ParticleSystem()
        self.flash = ScreenFlash()
        # Optional audio hooks (set to Audio(...) elsewhere if available)
        self.snd_wrong = None
        self.feedback_text = ""
        self.feedback_timer = 0
        self.feedback_color = WHITE
        
        # UI elements
        self.start_btn = ModernButton(350, 480, 200, 55, "Start Shift",
                                       DOCTOR_PRIMARY, DOCTOR_SECONDARY)
        self.next_btn = ModernButton(350, 500, 200, 55, "Next Patient",
                                      DOCTOR_PRIMARY, DOCTOR_SECONDARY)
        self.finish_btn = ModernButton(350, 500, 200, 55, "View Results",
                                        DOCTOR_PRIMARY, DOCTOR_SECONDARY)
        self.back_btn = ModernButton(350, 500, 200, 55, "Return to Hub",
                                      CARD_BG, DOCTOR_PRIMARY)
        
        self.option_buttons = []
        self.generate_patients()
        
        self.clock = pygame.time.Clock()
        self.scene_manager = None
    
    def generate_patients(self):
        """Generate random patient cases."""
        cases = random.sample(PATIENT_CASES, min(self.total_patients, len(PATIENT_CASES)))
        self.patients = [Patient(case) for case in cases]
        if self.patients:
            self.load_patient(0)
    
    def load_patient(self, index):
        """Load a patient case and generate options."""
        if index < len(self.patients):
            self.current_patient = self.patients[index]
            self.current_patient_index = index
            self.time_remaining = self.time_per_patient
            self.selected_option = None
            
            # Generate answer options (1 correct + 3 wrong)
            correct = self.current_patient.correct_diagnosis
            wrong_options = [d for d in ALL_DIAGNOSES if d != correct]
            random.shuffle(wrong_options)
            
            self.options = [correct] + wrong_options[:3]
            random.shuffle(self.options)
            
            # Create option buttons
            self.option_buttons = []
            for i, option in enumerate(self.options):
                btn = ModernButton(
                    150, 280 + i * 65, 600, 55, option,
                    CARD_BG, DOCTOR_ACCENT
                )
                self.option_buttons.append(btn)
    
    def run(self, scene_manager):
        """Main game loop."""
        self.scene_manager = scene_manager
        screen = pygame.display.get_surface()
        running = True

        while running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event)

                if event.type == pygame.KEYDOWN:
                    self.handle_key(event)

            self.update(dt)
            self.draw(screen)
            pygame.display.update()
    
    def handle_click(self, event):
        """Handle mouse clicks."""
        if self.state == "intro":
            if self.start_btn.is_clicked(event):
                self.state = "gameplay"

        elif self.state == "gameplay":
            # Use the event position for robust click detection
            for i, btn in enumerate(self.option_buttons):
                if btn.is_clicked(event):
                    self.submit_answer(i)
                    break

        elif self.state == "feedback":
            if self.next_btn.is_clicked(event) or self.finish_btn.is_clicked(event):
                if self.current_patient_index < len(self.patients) - 1:
                    self.load_patient(self.current_patient_index + 1)
                    self.state = "gameplay"
                else:
                    self.state = "results"

        elif self.state == "results":
            if self.back_btn.is_clicked(event):
                # Try robust scene change back to hub/menu
                try:
                    from main import enhanced_career_selection
                    if self.scene_manager is not None:
                        self.scene_manager.change_scene(enhanced_career_selection)
                except Exception:
                    if self.scene_manager is not None:
                        try:
                            self.scene_manager.change_scene("hub")
                        except Exception:
                            pass
                return
    
    def handle_key(self, event):
        """Handle keyboard input."""
        if self.state == "gameplay":
            # Ensure options exist to avoid ZeroDivision / IndexErrors
            if not self.options:
                return
            n = len(self.options)
            if event.key == pygame.K_UP:
                if self.selected_option is None:
                    self.selected_option = n - 1
                else:
                    self.selected_option = (self.selected_option - 1) % n
            elif event.key == pygame.K_DOWN:
                if self.selected_option is None:
                    self.selected_option = 0
                else:
                    self.selected_option = (self.selected_option + 1) % n
            elif event.key == pygame.K_RETURN:
                # Validate index before submitting
                if self.selected_option is not None and 0 <= self.selected_option < n:
                    self.submit_answer(self.selected_option)
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                idx = event.key - pygame.K_1
                if 0 <= idx < n:
                    self.submit_answer(idx)
    
    def submit_answer(self, selected_index):
        """Check the selected answer."""
        if self.current_patient is None:
            return
        # Safety: ensure selected_index is valid
        if not (0 <= selected_index < len(self.options)):
            return

        selected = self.options[selected_index]
        correct = self.current_patient.correct_diagnosis
        
        if selected == correct:
            # Correct answer
            time_bonus = int((self.time_remaining / self.time_per_patient) * 50)
            self.combo += 1
            combo_bonus = self.combo * 10
            points = 100 + time_bonus + combo_bonus
            self.score += points
            self.max_combo = max(self.max_combo, self.combo)
            
            self.current_patient.treated = True
            self.current_patient.result = "correct"
            
            self.feedback_text = f"+{points} pts"
            self.feedback_color = SUCCESS
            self.flash.flash(SUCCESS, 50)
            self.particles.emit(WIDTH // 2, HEIGHT // 2, SUCCESS, 25)
        else:
            # Wrong answer
            self.combo = 0
            self.current_patient.result = "wrong"
            # Apply small penalty and feedback
            penalty = 25
            self.score = max(0, self.score - penalty)
            self.time_remaining = max(0.0, self.time_remaining - 3.0)
            self.feedback_text = f"Wrong — correct: {correct} (-{penalty} pts)"
            self.feedback_color = DANGER
            self.flash.flash(DANGER, 60)
            # negative particles and optional sound
            try:
                self.particles.emit(WIDTH // 2, HEIGHT // 2, DANGER, 18)
            except Exception:
                pass
            if self.snd_wrong:
                try:
                    self.snd_wrong.play()
                except Exception:
                    pass
        
        # decrease life on wrong answer
        if selected != correct:
            try:
                self.lives -= 1
            except Exception:
                pass
            if self.lives <= 0:
                self.failed = True
                self.state = "results"
            else:
                self.feedback_timer = 1.5
                self.state = "feedback"
        else:
            self.feedback_timer = 1.5
            self.state = "feedback"
    
    def update(self, dt):
        """Update game state."""
        self.particles.update(dt)
        self.flash.update()
        
        if self.feedback_timer > 0:
            self.feedback_timer -= dt
        
        if self.state == "gameplay":
            self.time_remaining -= dt
            if self.time_remaining <= 0:
                # Time's up - auto submit wrong
                self.combo = 0
                if self.current_patient is not None:
                    self.current_patient.result = "timeout"
                self.feedback_text = "Time's Up!"
                self.feedback_color = DANGER
                self.feedback_timer = 1.5
                self.state = "feedback"
    
    def draw(self, screen):
        """Draw current state."""
        screen.fill(BACKGROUND)
        
        if self.state == "intro":
            self.draw_intro(screen)
        elif self.state == "gameplay":
            self.draw_gameplay(screen)
        elif self.state == "feedback":
            self.draw_feedback(screen)
        elif self.state == "results":
            self.draw_results(screen)
        
        self.particles.draw(screen)
        self.flash.draw(screen)
    
    def draw_intro(self, screen):
        """Draw intro screen."""
        # Header
        header_rect = pygame.Rect(0, 0, WIDTH, 100)
        pygame.draw.rect(screen, DOCTOR_PRIMARY, header_rect)
        draw_text(screen, "Doctor World", 42, WIDTH // 2, 35, WHITE, bold=True)
        draw_text(screen, "Emergency Room Triage", 18, WIDTH // 2, 72, TEXT_SECONDARY)
        
        # Intro text
        draw_wrapped_text(self.story["intro"], screen, 100, 150, 22, WHITE, 700)
        
        # Instructions
        draw_text(screen, "How to Play:", 24, WIDTH // 2, 350, DOCTOR_ACCENT, bold=True)
        instructions = [
            "Read the patient's symptoms carefully",
            "Select the correct diagnosis",
            "Faster answers = more points",
            "Build combos for bonus points!",
            "Avoid running out of time!"
        ]
        for i, instruction in enumerate(instructions):
            draw_text_left(screen, f"• {instruction}", 18, 180, 385 + i * 28, TEXT_SECONDARY)
        
        self.start_btn.draw(screen)
    
    def draw_gameplay(self, screen):
        """Draw gameplay screen."""
        # Header with progress
        header_rect = pygame.Rect(0, 0, WIDTH, 80)
        pygame.draw.rect(screen, DOCTOR_PRIMARY, header_rect)
        
        draw_text(screen, f"Patient {self.current_patient_index + 1}/{len(self.patients)}", 
                 28, WIDTH // 2, 25, WHITE, bold=True)
        draw_text(screen, f"Score: {self.score}  |  Combo: x{self.combo}", 
                 16, WIDTH // 2, 55, TEXT_SECONDARY)
        # Lives HUD
        try:
            draw_lives(screen, self.lives, 3, WIDTH - 160, 22, heart_size=20, spacing=6)
        except Exception:
            pass
        
        # Timer bar (clamped width to avoid negative sizes)
        time_frac = max(0.0, min(self.time_remaining, self.time_per_patient)) / max(1.0, self.time_per_patient)
        timer_width = int(time_frac * (WIDTH - 40))
        timer_color = DANGER if self.time_remaining < 5 else (
            WARNING if self.time_remaining < 10 else SUCCESS
        )
        timer_rect = pygame.Rect(20, 85, timer_width, 8)
        pygame.draw.rect(screen, timer_color, timer_rect, border_radius=4)
        
        # Patient card
        if self.current_patient:
            card_rect = pygame.Rect(100, 110, 700, 140)
            pygame.draw.rect(screen, CARD_BG, card_rect, border_radius=12)
            
            # Severity indicator
            severity_color = self.current_patient.get_severity_color()
            severity_rect = pygame.Rect(100, 110, 8, 140)
            pygame.draw.rect(screen, severity_color, severity_rect, 
                           border_top_left_radius=12, border_bottom_left_radius=12)
            
            draw_text_left(screen, "Patient Symptoms:", 20, 140, 130, TEXT_SECONDARY)

            for i, symptom in enumerate(self.current_patient.symptoms):
                draw_text_left(screen, f"• {symptom}", 22, 140, 165 + i * 32, WHITE)

            # Hint
            draw_text_left(screen, f"Hint: {self.current_patient.hint}", 
                     16, 140, 235, TEXT_MUTED)
        
        # Answer options
        draw_text(screen, "Select Diagnosis:", 20, WIDTH // 2, 265, TEXT_SECONDARY)
        
        for i, btn in enumerate(self.option_buttons):
            # Mark the selected button (do not mutate button color properties)
            btn.selected = (self.selected_option is not None and i == self.selected_option)
            btn.draw(screen)
        
        # Keyboard hints
        draw_text(screen, "Use ↑↓ arrows or 1-4 keys, Enter to confirm", 
                 14, WIDTH // 2, HEIGHT - 25, TEXT_MUTED)
    
    def draw_feedback(self, screen):
        """Draw feedback after answering."""
        self.draw_gameplay(screen)
        
        # Overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(150)
        screen.blit(overlay, (0, 0))
        
        # Feedback box
        box_rect = pygame.Rect(200, 200, 500, 200)
        pygame.draw.rect(screen, CARD_BG, box_rect, border_radius=16)
        pygame.draw.rect(screen, self.feedback_color, box_rect, 3, border_radius=16)
        
        result = getattr(self.current_patient, "result", None)
        if result == "correct":
            draw_text(screen, "Correct Diagnosis!", 32, WIDTH // 2, 250, SUCCESS, bold=True)
        else:
            draw_text(screen, "Incorrect!", 32, WIDTH // 2, 250, DANGER, bold=True)
        
        draw_text(screen, self.feedback_text, 24, WIDTH // 2, 300, self.feedback_color)
        
        if self.current_patient_index < len(self.patients) - 1:
            self.next_btn.draw(screen)
        else:
            self.finish_btn.draw(screen)
    
    def draw_results(self, screen):
        """Draw results screen."""
        # Header
        header_rect = pygame.Rect(0, 0, WIDTH, 100)
        pygame.draw.rect(screen, DOCTOR_PRIMARY, header_rect)
        draw_text(screen, "Shift Complete!", 42, WIDTH // 2, 35, WHITE, bold=True)
        draw_text(screen, "Emergency Room Results", 18, WIDTH // 2, 72, TEXT_SECONDARY)
        
        # Stats
        correct_count = sum(1 for p in self.patients if p.result == "correct")
        
        stats_y = 140
        draw_text(screen, f"Patients Treated: {correct_count}/{len(self.patients)}", 
                 28, WIDTH // 2, stats_y, WHITE, bold=True)
        draw_text(screen, f"Total Score: {self.score}", 
                 24, WIDTH // 2, stats_y + 45, DOCTOR_ACCENT)
        draw_text(screen, f"Best Combo: x{self.max_combo}", 
                 20, WIDTH // 2, stats_y + 85, TEXT_SECONDARY)
        
        # Grade
        percentage = (correct_count / len(self.patients)) * 100
        if percentage >= 80:
            grade = "A"
            grade_color = SUCCESS
        elif percentage >= 60:
            grade = "B"
            grade_color = ACCENT
        elif percentage >= 40:
            grade = "C"
            grade_color = WARNING
        else:
            grade = "D"
            grade_color = DANGER
        
        draw_text(screen, f"Grade: {grade}", 48, WIDTH // 2, stats_y + 140, grade_color, bold=True)
        
        # Feedback message
        feedback = get_performance_feedback("Doctor", correct_count, len(self.patients))
        draw_wrapped_text(feedback, screen, 100, stats_y + 200, 18, TEXT_SECONDARY, 700)
        
        # Real-world lesson
        lesson = get_career_lesson("Doctor")
        draw_text(screen, "What Real Doctors Do:", 20, WIDTH // 2, stats_y + 280, DOCTOR_ACCENT, bold=True)
        draw_wrapped_text(lesson, screen, 100, stats_y + 310, 16, TEXT_MUTED, 700)
        
        self.back_btn.draw(screen)
