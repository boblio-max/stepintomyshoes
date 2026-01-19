"""
Step Into My Shoes - Lawyer World
Detect contradictions and logical inconsistencies in witness statements.
Teaches: Logic, critical thinking, attention to detail.
"""

import pygame
import random
from engine.colors import (
    BACKGROUND, WHITE, BLACK, LAWYER_PRIMARY, LAWYER_SECONDARY,
    LAWYER_ACCENT, SUCCESS, DANGER, WARNING, TEXT_SECONDARY, CARD_BG,
    ACCENT, TEXT_MUTED
)
from engine.ui import (
    draw_text, draw_text_left, draw_wrapped_text, ModernButton, ParticleSystem, ScreenFlash
)
from engine.backstory_ai import get_performance_feedback, get_career_lesson

pygame.init()

WIDTH, HEIGHT = 900, 600

# Case scenarios with statements and contradictions
CASE_SCENARIOS = [
    {
        "case_title": "The Missing Artifact",
        "context": "A valuable artifact was stolen from a museum at 10 PM.",
        "statements": [
            {"witness": "Guard", "text": "I was at my post the entire night. No one passed by."},
            {"witness": "Curator", "text": "I left at 9 PM and the artifact was secure."},
            {"witness": "Suspect", "text": "I was at the movies until midnight. The guard can confirm he saw me leave at 11 PM."}
        ],
        "contradiction": 2,
        "explanation": "The suspect claims the guard saw them leave at 11 PM, but the guard said no one passed by all night."
    },
    {
        "case_title": "The Broken Window",
        "context": "A store window was broken during a thunderstorm last night.",
        "statements": [
            {"witness": "Owner", "text": "I heard the crash during the heavy rain around 8 PM."},
            {"witness": "Neighbor", "text": "I was walking my dog when it happened. The sky was clear."},
            {"witness": "Passerby", "text": "I saw someone running away but couldn't see their face due to the rain."}
        ],
        "contradiction": 1,
        "explanation": "The neighbor claims the sky was clear, but both the owner and passerby mention rain."
    },
    {
        "case_title": "The Alibi Problem",
        "context": "A robbery occurred at 3 PM on Tuesday.",
        "statements": [
            {"witness": "Defendant", "text": "I was at the gym with my trainer from 2-4 PM."},
            {"witness": "Trainer", "text": "We had a session that day, starting at 2 PM for about 90 minutes."},
            {"witness": "Gym Staff", "text": "The defendant checked in at 3:30 PM according to our records."}
        ],
        "contradiction": 2,
        "explanation": "The gym records show check-in at 3:30 PM, contradicting claims of being there since 2 PM."
    },
    {
        "case_title": "The Witness Statement",
        "context": "A hit-and-run occurred at the intersection at night.",
        "statements": [
            {"witness": "Driver", "text": "The traffic light was green when I crossed the intersection."},
            {"witness": "Pedestrian", "text": "I saw the car run a red light at high speed."},
            {"witness": "Officer", "text": "The traffic camera was malfunctioning that night."}
        ],
        "contradiction": 0,
        "explanation": "The driver claims the light was green, but the pedestrian clearly saw a red light."
    },
    {
        "case_title": "The Office Incident",
        "context": "Confidential documents went missing from the office.",
        "statements": [
            {"witness": "Manager", "text": "Only Sarah and Tom had access to the filing cabinet."},
            {"witness": "Sarah", "text": "I haven't been to the office in two weeks due to vacation."},
            {"witness": "Tom", "text": "Sarah and I were both working late last Thursday when I last saw the files."}
        ],
        "contradiction": 2,
        "explanation": "Tom claims Sarah was working late last Thursday, but Sarah says she was on vacation for two weeks."
    },
    {
        "case_title": "The Car Accident",
        "context": "Two cars collided at an intersection yesterday morning.",
        "statements": [
            {"witness": "Driver A", "text": "I was driving the speed limit of 35 mph when they ran the stop sign."},
            {"witness": "Driver B", "text": "I came to a complete stop. They were going at least 50 mph."},
            {"witness": "Bystander", "text": "Both cars seemed to be going about the same speed."}
        ],
        "contradiction": 0,
        "explanation": "Driver A claims 35 mph, Driver B claims 50+ mph - a direct contradiction about speed."
    },
    {
        "case_title": "The Inheritance Dispute",
        "context": "A wealthy relative's will is being contested.",
        "statements": [
            {"witness": "Nephew", "text": "Aunt Martha told me I would inherit the house just last month."},
            {"witness": "Lawyer", "text": "The will was written three years ago and hasn't been modified."},
            {"witness": "Niece", "text": "Aunt Martha mentioned changing her will recently."}
        ],
        "contradiction": 1,
        "explanation": "The lawyer states the will wasn't modified, but both relatives claim recent promises of changes."
    },
    {
        "case_title": "The Restaurant Incident",
        "context": "A customer claims they were food poisoned at a restaurant.",
        "statements": [
            {"witness": "Customer", "text": "I got sick immediately after eating the seafood dish."},
            {"witness": "Chef", "text": "All our seafood is fresh and properly stored. No other complaints."},
            {"witness": "Waiter", "text": "The customer mentioned they also ate at another restaurant earlier."}
        ],
        "contradiction": 0,
        "explanation": "Customer claims immediate sickness from this restaurant, but the waiter reveals they ate elsewhere too."
    }
]


class LegalCase:
    """Represents a legal case with statements to analyze."""
    
    def __init__(self, case_data):
        self.title = case_data["case_title"]
        self.context = case_data["context"]
        self.statements = case_data["statements"]
        self.contradiction_index = case_data["contradiction"]
        self.explanation = case_data["explanation"]
        self.solved = False
        self.result = None


class LawyerWorld:
    """
    Lawyer Career Mini-Game
    Players analyze witness statements to find contradictions.
    """
    
    def __init__(self, story_package=None):
        self.story = story_package or {
            "intro": "Welcome to the Courtroom!\n\nAs a trial lawyer, you must analyze witness statements to find contradictions.\n\nRead each statement carefully and identify which witness is lying or mistaken."
        }
        self.state = "intro"
        self.score = 0
        self.total_cases = 5
        self.current_case_index = 0
        self.cases = []
        self.current_case = None
        self.selected_statement = None
        self.time_per_case = 30.0
        self.time_remaining = self.time_per_case
        self.streak = 0
        
        # Visual effects
        self.particles = ParticleSystem()
        self.flash = ScreenFlash()
        self.feedback_text = ""
        self.feedback_timer = 0
        
        # UI elements
        self.start_btn = ModernButton(350, 480, 200, 55, "Enter Court",
                                       LAWYER_PRIMARY, LAWYER_SECONDARY)
        self.next_btn = ModernButton(350, 500, 200, 55, "Next Case",
                                      LAWYER_PRIMARY, LAWYER_SECONDARY)
        self.finish_btn = ModernButton(350, 500, 200, 55, "View Verdict",
                                        LAWYER_PRIMARY, LAWYER_SECONDARY)
        self.back_btn = ModernButton(350, 500, 200, 55, "Return to Hub",
                                      CARD_BG, LAWYER_PRIMARY)
        
        self.statement_buttons = []
        self.generate_cases()
        
        self.clock = pygame.time.Clock()
        self.scene_manager = None
    
    def generate_cases(self):
        """Generate random legal cases."""
        cases = random.sample(CASE_SCENARIOS, min(self.total_cases, len(CASE_SCENARIOS)))
        self.cases = [LegalCase(case) for case in cases]
        if self.cases:
            self.load_case(0)
    
    def load_case(self, index):
        """Load a case and prepare UI."""
        if index < len(self.cases):
            self.current_case = self.cases[index]
            self.current_case_index = index
            self.time_remaining = self.time_per_case
            self.selected_statement = None
            
            # Create statement buttons
            self.statement_buttons = []
            for i, stmt in enumerate(self.current_case.statements):
                btn = ModernButton(
                    80, 230 + i * 100, 740, 85, "",
                    CARD_BG, LAWYER_ACCENT
                )
                self.statement_buttons.append(btn)
    
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
            for i, btn in enumerate(self.statement_buttons):
                if btn.is_clicked(event):
                    self.submit_answer(i)
                    break
        
        elif self.state == "feedback":
            if self.next_btn.is_clicked(event) or self.finish_btn.is_clicked(event):
                if self.current_case_index < len(self.cases) - 1:
                    self.load_case(self.current_case_index + 1)
                    self.state = "gameplay"
                else:
                    self.state = "results"
        
        elif self.state == "results":
            if self.back_btn.is_clicked(event):
                from main import enhanced_career_selection
                self.scene_manager.change_scene(enhanced_career_selection)
                return
    
    def handle_key(self, event):
        """Handle keyboard input."""
        if self.state == "gameplay":
            n = len(self.current_case.statements)
            if event.key == pygame.K_UP:
                if self.selected_statement is None:
                    self.selected_statement = n - 1
                else:
                    self.selected_statement = (self.selected_statement - 1) % n
            elif event.key == pygame.K_DOWN:
                if self.selected_statement is None:
                    self.selected_statement = 0
                else:
                    self.selected_statement = (self.selected_statement + 1) % n
            elif event.key == pygame.K_RETURN:
                if self.selected_statement is not None:
                    self.submit_answer(self.selected_statement)
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                idx = event.key - pygame.K_1
                if idx < len(self.current_case.statements):
                    self.submit_answer(idx)
    
    def submit_answer(self, selected_index):
        """Check the selected answer."""
        if self.current_case is None:
            return
        
        correct = self.current_case.contradiction_index
        
        if selected_index == correct:
            # Correct!
            time_bonus = int((self.time_remaining / self.time_per_case) * 50)
            self.streak += 1
            streak_bonus = self.streak * 15
            points = 100 + time_bonus + streak_bonus
            self.score += points
            
            self.current_case.solved = True
            self.current_case.result = "correct"
            
            self.feedback_text = f"+{points} pts - Contradiction Found!"
            self.flash.flash(SUCCESS, 50)
            self.particles.emit(WIDTH // 2, HEIGHT // 2, SUCCESS, 25)
        else:
            # Wrong
            self.streak = 0
            self.current_case.result = "wrong"
            # Apply penalty and feedback
            penalty = 30
            try:
                self.score = max(0, self.score - penalty)
            except Exception:
                pass
            self.time_remaining = max(0.0, self.time_remaining - 5.0) if hasattr(self, 'time_remaining') else None
            self.feedback_text = "Incorrect Analysis"
            self.flash.flash(DANGER, 60)
            try:
                self.particles.emit(WIDTH // 2, HEIGHT // 2, DANGER, 18)
            except Exception:
                pass
            if getattr(self, 'snd_wrong', None):
                try:
                    self.snd_wrong.play()
                except Exception:
                    pass
        
        self.feedback_timer = 2.0
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
                self.streak = 0
                self.current_case.result = "timeout"
                self.feedback_text = "Time's Up! The judge is impatient."
                self.feedback_timer = 2.0
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
        pygame.draw.rect(screen, LAWYER_PRIMARY, header_rect)
        draw_text(screen, "Lawyer World", 42, WIDTH // 2, 35, WHITE, bold=True)
        draw_text(screen, "Courtroom Analysis", 18, WIDTH // 2, 72, TEXT_SECONDARY)
        
        # Intro text
        draw_wrapped_text(self.story["intro"], screen, 100, 150, 22, WHITE, 700)
        
        # Instructions
        draw_text(screen, "How to Play:", 24, WIDTH // 2, 330, LAWYER_ACCENT, bold=True)
        instructions = [
            "Read the case context carefully",
            "Analyze each witness statement",
            "Find the statement with a logical contradiction",
            "Click to select the contradicting statement"
        ]
        for i, instruction in enumerate(instructions):
            draw_text(screen, f"• {instruction}", 18, WIDTH // 2, 365 + i * 28, TEXT_SECONDARY)
        
        self.start_btn.draw(screen)
    
    def draw_gameplay(self, screen):
        """Draw gameplay screen."""
        # Header
        header_rect = pygame.Rect(0, 0, WIDTH, 70)
        pygame.draw.rect(screen, LAWYER_PRIMARY, header_rect)
        
        draw_text(screen, f"Case {self.current_case_index + 1}/{len(self.cases)}: {self.current_case.title}", 
                 24, WIDTH // 2, 22, WHITE, bold=True)
        draw_text(screen, f"Score: {self.score}  |  Streak: {self.streak}", 
                 14, WIDTH // 2, 50, TEXT_SECONDARY)
        
        # Timer bar
        timer_width = int((self.time_remaining / self.time_per_case) * (WIDTH - 40))
        timer_color = DANGER if self.time_remaining < 10 else (
            WARNING if self.time_remaining < 20 else SUCCESS
        )
        timer_rect = pygame.Rect(20, 75, timer_width, 6)
        pygame.draw.rect(screen, timer_color, timer_rect, border_radius=3)
        
        # Case context
        context_rect = pygame.Rect(60, 95, 780, 50)
        pygame.draw.rect(screen, CARD_BG, context_rect, border_radius=8)
        draw_text(screen, self.current_case.context, 16, WIDTH // 2, 120, TEXT_SECONDARY)
        
        # Instructions
        draw_text(screen, "Find the contradicting statement:", 18, WIDTH // 2, 170, LAWYER_ACCENT)
        
        # Statement cards
        for i, btn in enumerate(self.statement_buttons):
            stmt = self.current_case.statements[i]

            # Use non-destructive selected flag instead of mutating colors
            btn.selected = (self.selected_statement is not None and i == self.selected_statement)
            btn.draw(screen)

            # Draw statement content (left-aligned)
            y_pos = 230 + i * 100
            draw_text_left(screen, f"Witness: {stmt['witness']}", 16, 120, y_pos + 10, LAWYER_ACCENT, bold=True)
            draw_wrapped_text(f'"{stmt["text"]}"', screen, 140, y_pos + 36, 16, WHITE, 620)
        
        # Key hints
        draw_text(screen, "Use ↑↓ arrows or 1-3 keys, Enter to confirm", 
                 14, WIDTH // 2, HEIGHT - 20, TEXT_MUTED)
    
    def draw_feedback(self, screen):
        """Draw feedback after answering."""
        self.draw_gameplay(screen)
        
        # Overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))
        
        # Feedback box
        box_rect = pygame.Rect(100, 150, 700, 300)
        pygame.draw.rect(screen, CARD_BG, box_rect, border_radius=16)
        
        correct = self.current_case.result == "correct"
        border_color = SUCCESS if correct else DANGER
        pygame.draw.rect(screen, border_color, box_rect, 3, border_radius=16)
        
        if correct:
            draw_text(screen, "Objection Sustained!", 32, WIDTH // 2, 200, SUCCESS, bold=True)
            draw_text(screen, self.feedback_text, 20, WIDTH // 2, 245, SUCCESS)
        else:
            draw_text(screen, "Objection Overruled!", 32, WIDTH // 2, 200, DANGER, bold=True)
            draw_text(screen, self.feedback_text, 20, WIDTH // 2, 245, DANGER)
        
        # Explanation
        draw_text(screen, "Explanation:", 18, WIDTH // 2, 290, LAWYER_ACCENT, bold=True)
        draw_wrapped_text(self.current_case.explanation, screen, 130, 320, 16, TEXT_SECONDARY, 640)
        
        if self.current_case_index < len(self.cases) - 1:
            self.next_btn.draw(screen)
        else:
            self.finish_btn.draw(screen)
    
    def draw_results(self, screen):
        """Draw results screen."""
        # Header
        header_rect = pygame.Rect(0, 0, WIDTH, 100)
        pygame.draw.rect(screen, LAWYER_PRIMARY, header_rect)
        draw_text(screen, "Court Adjourned!", 42, WIDTH // 2, 35, WHITE, bold=True)
        draw_text(screen, "Trial Results", 18, WIDTH // 2, 72, TEXT_SECONDARY)
        
        # Stats
        solved_count = sum(1 for c in self.cases if c.result == "correct")
        
        stats_y = 140
        draw_text(screen, f"Cases Won: {solved_count}/{len(self.cases)}", 
                 28, WIDTH // 2, stats_y, WHITE, bold=True)
        draw_text(screen, f"Total Points: {self.score}", 
                 24, WIDTH // 2, stats_y + 45, LAWYER_ACCENT)
        draw_text(screen, f"Best Streak: {self.streak}", 
                 20, WIDTH // 2, stats_y + 85, TEXT_SECONDARY)
        
        # Grade
        percentage = (solved_count / len(self.cases)) * 100
        if percentage >= 80:
            grade, grade_color = "A", SUCCESS
        elif percentage >= 60:
            grade, grade_color = "B", ACCENT
        elif percentage >= 40:
            grade, grade_color = "C", WARNING
        else:
            grade, grade_color = "D", DANGER
        
        draw_text(screen, f"Grade: {grade}", 48, WIDTH // 2, stats_y + 140, grade_color, bold=True)
        
        # Feedback
        feedback = get_performance_feedback("Lawyer", solved_count, len(self.cases))
        draw_wrapped_text(feedback, screen, 100, stats_y + 200, 18, TEXT_SECONDARY, 700)
        
        # Real-world lesson
        lesson = get_career_lesson("Lawyer")
        draw_text(screen, "What Real Lawyers Do:", 20, WIDTH // 2, stats_y + 280, LAWYER_ACCENT, bold=True)
        draw_wrapped_text(lesson, screen, 100, stats_y + 310, 16, TEXT_MUTED, 700)
        
        self.back_btn.draw(screen)
