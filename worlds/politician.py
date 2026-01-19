"""
Step Into My Shoes - Politician World
Manage public approval by responding to issues and crises.
Teaches: Strategic thinking, communication, public relations.
"""

import pygame
import random
from engine.colors import (
    BACKGROUND, WHITE, BLACK, POLITICIAN_PRIMARY, POLITICIAN_SECONDARY,
    POLITICIAN_ACCENT, SUCCESS, DANGER, WARNING, TEXT_SECONDARY, CARD_BG,
    ACCENT, TEXT_MUTED
)
from engine.ui import (
    draw_text, draw_text_left, draw_wrapped_text, ModernButton, ParticleSystem, ScreenFlash,
    ProgressBar
)
from engine.backstory_ai import get_performance_feedback, get_career_lesson

pygame.init()

WIDTH, HEIGHT = 900, 600

# Political issues with response options
POLITICAL_ISSUES = [
    {
        "headline": "Budget Crisis: City Funds Running Low",
        "context": "The city treasury reports a significant deficit. Citizens are worried.",
        "responses": [
            {"text": "Propose spending cuts to essential services", "approval": -15, "outcome": "Citizens protest cuts to public services."},
            {"text": "Announce a comprehensive budget review", "approval": 10, "outcome": "Your measured approach reassures the public."},
            {"text": "Blame the previous administration", "approval": -5, "outcome": "Some see this as deflection, others agree."},
            {"text": "Propose new business incentives to boost revenue", "approval": 15, "outcome": "Your proactive solution impresses voters."}
        ]
    },
    {
        "headline": "Traffic Gridlock: Commuters Demand Action",
        "context": "Rush hour traffic has become unbearable. Commuters are frustrated.",
        "responses": [
            {"text": "Promise to study the issue further", "approval": -10, "outcome": "Citizens want action, not more studies."},
            {"text": "Announce immediate road improvement projects", "approval": 15, "outcome": "Your quick action wins public support."},
            {"text": "Encourage remote work and flexible hours", "approval": 5, "outcome": "A practical short-term solution."},
            {"text": "Propose a new public transit expansion", "approval": 20, "outcome": "Your vision for the future inspires hope."}
        ]
    },
    {
        "headline": "School Overcrowding Reaches Critical Levels",
        "context": "Parents are concerned about class sizes and teacher shortages.",
        "responses": [
            {"text": "Redirect funds from other projects to education", "approval": 10, "outcome": "Parents appreciate your priorities."},
            {"text": "Announce a new school construction plan", "approval": 20, "outcome": "Your investment in education wins hearts."},
            {"text": "Suggest private school alternatives", "approval": -20, "outcome": "This appears out of touch with working families."},
            {"text": "Form a task force with teachers and parents", "approval": 5, "outcome": "Collaboration is seen as a positive step."}
        ]
    },
    {
        "headline": "Local Business Owner Accuses You of Favoritism",
        "context": "A prominent business owner claims you gave contracts to friends.",
        "responses": [
            {"text": "Deny all accusations aggressively", "approval": -10, "outcome": "Your defensive stance raises suspicions."},
            {"text": "Release all contract documentation publicly", "approval": 15, "outcome": "Transparency wins public trust."},
            {"text": "Threaten legal action against the accuser", "approval": -15, "outcome": "This looks like intimidation to voters."},
            {"text": "Invite an independent audit of all contracts", "approval": 20, "outcome": "Your openness impresses citizens."}
        ]
    },
    {
        "headline": "Environmental Protest Blocks City Hall",
        "context": "Climate activists demand immediate action on pollution.",
        "responses": [
            {"text": "Have police clear the protesters", "approval": -20, "outcome": "Images of the crackdown go viral."},
            {"text": "Meet with protest leaders personally", "approval": 15, "outcome": "Your willingness to listen wins respect."},
            {"text": "Announce a green initiative task force", "approval": 10, "outcome": "A step forward, but activists want more."},
            {"text": "Propose a comprehensive sustainability plan", "approval": 20, "outcome": "Your bold vision gains wide support."}
        ]
    },
    {
        "headline": "Healthcare Costs Rising, Hospitals Overwhelmed",
        "context": "Local hospitals report record wait times and staff shortages.",
        "responses": [
            {"text": "Blame federal policies for the crisis", "approval": -5, "outcome": "Passing blame frustrates some voters."},
            {"text": "Announce emergency funding for hospitals", "approval": 15, "outcome": "Immediate action shows leadership."},
            {"text": "Propose a regional healthcare partnership", "approval": 20, "outcome": "Your collaborative approach impresses experts."},
            {"text": "Suggest people use urgent care instead", "approval": -15, "outcome": "This seems dismissive of the real problem."}
        ]
    },
    {
        "headline": "Crime Rate Spikes in Downtown Area",
        "context": "Residents and businesses are concerned about safety.",
        "responses": [
            {"text": "Call for more aggressive policing", "approval": 5, "outcome": "Some support this, others worry about overreach."},
            {"text": "Announce community safety programs", "approval": 15, "outcome": "A balanced approach wins approval."},
            {"text": "Downplay the statistics publicly", "approval": -15, "outcome": "This seems out of touch with real fears."},
            {"text": "Propose youth job programs to address root causes", "approval": 20, "outcome": "Your thoughtful approach impresses many."}
        ]
    },
    {
        "headline": "Rival Politician Releases Attack Ad Against You",
        "context": "The ad questions your integrity and leadership.",
        "responses": [
            {"text": "Launch an attack ad in response", "approval": -10, "outcome": "Negative campaigning turns off voters."},
            {"text": "Ignore it and focus on your achievements", "approval": 10, "outcome": "Taking the high road earns respect."},
            {"text": "Hold a press conference addressing the claims", "approval": 15, "outcome": "Direct communication shows strength."},
            {"text": "Release endorsements from community leaders", "approval": 20, "outcome": "Third-party support validates your leadership."}
        ]
    },
    {
        "headline": "Major Employer Threatens to Leave the City",
        "context": "A large company says taxes are too high and may relocate.",
        "responses": [
            {"text": "Offer massive tax breaks immediately", "approval": -5, "outcome": "Some see this as giving in to corporate pressure."},
            {"text": "Negotiate a balanced incentive package", "approval": 15, "outcome": "Your skilled negotiation impresses voters."},
            {"text": "Let them leave; we don't negotiate", "approval": -15, "outcome": "This seems reckless with jobs at stake."},
            {"text": "Highlight other businesses ready to invest", "approval": 10, "outcome": "Showing alternatives projects confidence."}
        ]
    },
    {
        "headline": "Water Quality Tests Show Concerning Results",
        "context": "Lab tests reveal elevated levels of contaminants.",
        "responses": [
            {"text": "Downplay the findings to avoid panic", "approval": -20, "outcome": "A cover-up attempt destroys trust."},
            {"text": "Immediately inform the public with solutions", "approval": 20, "outcome": "Transparency and action earn praise."},
            {"text": "Order more tests before commenting", "approval": 5, "outcome": "Caution is understood but delays concern people."},
            {"text": "Blame the testing methodology", "approval": -15, "outcome": "Denial looks like irresponsibility."}
        ]
    }
]


class PoliticalCrisis:
    """Represents a political issue requiring response."""
    
    def __init__(self, issue_data):
        self.headline = issue_data["headline"]
        self.context = issue_data["context"]
        self.responses = issue_data["responses"]
        self.resolved = False
        self.chosen_response = None
        self.outcome = None


class PoliticianWorld:
    """
    Politician Career Mini-Game
    Players manage approval rating by responding to political issues.
    """
    
    def __init__(self, story_package=None):
        self.story = story_package or {
            "intro": "Welcome to City Hall!\n\nAs an elected official, you must respond to various issues and crises.\nEvery decision affects your approval rating.\n\nChoose wisely - the public is watching!"
        }
        self.state = "intro"
        self.score = 0
        self.approval = 50  # Start at 50%
        self.total_issues = 6
        self.current_issue_index = 0
        self.issues = []
        self.current_issue = None
        self.selected_response = None
        
        # Track decisions
        self.good_decisions = 0
        self.bad_decisions = 0
        self.neutral_decisions = 0
        
        # Visual effects
        self.particles = ParticleSystem()
        self.flash = ScreenFlash()
        self.feedback_text = ""
        self.feedback_timer = 0
        self.approval_change = 0
        
        # UI elements
        self.start_btn = ModernButton(350, 480, 200, 55, "Take Office",
                                       POLITICIAN_PRIMARY, POLITICIAN_SECONDARY)
        self.next_btn = ModernButton(350, 500, 200, 55, "Next Issue",
                                      POLITICIAN_PRIMARY, POLITICIAN_SECONDARY)
        self.finish_btn = ModernButton(350, 500, 200, 55, "View Legacy",
                                        POLITICIAN_PRIMARY, POLITICIAN_SECONDARY)
        self.back_btn = ModernButton(350, 500, 200, 55, "Return to Hub",
                                      CARD_BG, POLITICIAN_PRIMARY)
        
        self.response_buttons = []
        self.generate_issues()
        
        self.clock = pygame.time.Clock()
        self.scene_manager = None
    
    def generate_issues(self):
        """Generate random political issues."""
        issues = random.sample(POLITICAL_ISSUES, 
                              min(self.total_issues, len(POLITICAL_ISSUES)))
        self.issues = [PoliticalCrisis(issue) for issue in issues]
        if self.issues:
            self.load_issue(0)
    
    def load_issue(self, index):
        """Load an issue and prepare response options."""
        if index < len(self.issues):
            self.current_issue = self.issues[index]
            self.current_issue_index = index
            self.selected_response = None
            
            # Create response buttons
            self.response_buttons = []
            for i, response in enumerate(self.current_issue.responses):
                btn = ModernButton(
                    80, 250 + i * 70, 740, 60, "",
                    CARD_BG, POLITICIAN_ACCENT
                )
                self.response_buttons.append(btn)
    
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
            for i, btn in enumerate(self.response_buttons):
                if btn.is_clicked(event):
                    self.submit_response(i)
                    break
        
        elif self.state == "feedback":
            if self.next_btn.is_clicked(event) or self.finish_btn.is_clicked(event):
                if self.current_issue_index < len(self.issues) - 1:
                    self.load_issue(self.current_issue_index + 1)
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
            n = len(self.current_issue.responses)
            if event.key == pygame.K_UP:
                if self.selected_response is None:
                    self.selected_response = n - 1
                else:
                    self.selected_response = (self.selected_response - 1) % n
            elif event.key == pygame.K_DOWN:
                if self.selected_response is None:
                    self.selected_response = 0
                else:
                    self.selected_response = (self.selected_response + 1) % n
            elif event.key == pygame.K_RETURN:
                if self.selected_response is not None:
                    self.submit_response(self.selected_response)
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                idx = event.key - pygame.K_1
                if idx < len(self.current_issue.responses):
                    self.submit_response(idx)
    
    def submit_response(self, selected_index):
        """Process the selected response."""
        if self.current_issue is None:
            return
        
        response = self.current_issue.responses[selected_index]
        self.current_issue.chosen_response = response
        self.current_issue.outcome = response["outcome"]
        self.current_issue.resolved = True
        
        # Apply approval change
        change = response["approval"]
        self.approval_change = change
        self.approval = max(0, min(100, self.approval + change))
        
        # Track decision quality
        if change > 10:
            self.good_decisions += 1
            self.score += 100 + change * 2
            self.feedback_text = f"Approval +{change}%"
            self.flash.flash(SUCCESS, 50)
            self.particles.emit(WIDTH // 2, 150, SUCCESS, 20)
        elif change > 0:
            self.neutral_decisions += 1
            self.score += 50 + change
            self.feedback_text = f"Approval +{change}%"
            self.flash.flash(ACCENT, 30)
        elif change >= -5:
            self.neutral_decisions += 1
            self.score += 25
            self.feedback_text = f"Approval {change}%"
        else:
            self.bad_decisions += 1
            self.feedback_text = f"Approval {change}%"
            self.flash.flash(DANGER, 50)
            try:
                self.particles.emit(WIDTH // 2, 150, DANGER, 20)
            except Exception:
                pass
            # small score penalty for poor choices
            try:
                self.score = max(0, self.score - 25)
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
        pygame.draw.rect(screen, POLITICIAN_PRIMARY, header_rect)
        draw_text(screen, "Politician World", 42, WIDTH // 2, 35, WHITE, bold=True)
        draw_text(screen, "City Hall Leadership", 18, WIDTH // 2, 72, TEXT_SECONDARY)
        
        # Intro text
        draw_wrapped_text(self.story["intro"], screen, 100, 140, 22, WHITE, 700)
        
        # Instructions
        draw_text(screen, "How to Play:", 24, WIDTH // 2, 320, POLITICIAN_ACCENT, bold=True)
        instructions = [
            "Read each political situation carefully",
            "Consider how different responses will affect public opinion",
            "Choose the response you think is best",
            "Maintain high approval to succeed!"
        ]
        for i, instruction in enumerate(instructions):
            draw_text_left(screen, f"• {instruction}", 18, 180, 355 + i * 28, TEXT_SECONDARY)
        
        self.start_btn.draw(screen)
    
    def draw_gameplay(self, screen):
        """Draw gameplay screen."""
        # Header
        header_rect = pygame.Rect(0, 0, WIDTH, 70)
        pygame.draw.rect(screen, POLITICIAN_PRIMARY, header_rect)
        
        draw_text(screen, f"Issue {self.current_issue_index + 1}/{len(self.issues)}", 
                 24, WIDTH // 2, 22, WHITE, bold=True)
        draw_text(screen, f"Score: {self.score}", 14, WIDTH // 2, 50, TEXT_SECONDARY)
        
        # Approval meter
        approval_x = 70
        approval_width = 200
        
        meter_bg = pygame.Rect(approval_x, 85, approval_width, 20)
        pygame.draw.rect(screen, CARD_BG, meter_bg, border_radius=10)
        
        approval_fill = int((self.approval / 100) * approval_width)
        if self.approval >= 60:
            meter_color = SUCCESS
        elif self.approval >= 40:
            meter_color = WARNING
        else:
            meter_color = DANGER
        
        meter_fill = pygame.Rect(approval_x, 85, approval_fill, 20)
        pygame.draw.rect(screen, meter_color, meter_fill, border_radius=10)
        
        draw_text(screen, f"Approval: {self.approval}%", 14, 
                 approval_x + approval_width + 80, 94, WHITE, bold=True)
        
        # Issue card
        card_rect = pygame.Rect(60, 120, 780, 110)
        pygame.draw.rect(screen, CARD_BG, card_rect, border_radius=12)
        
        draw_text(screen, self.current_issue.headline, 22, WIDTH // 2, 150, WHITE, bold=True)
        draw_wrapped_text(self.current_issue.context, screen, 80, 180, 16, TEXT_SECONDARY, 720)
        
        # Response options
        draw_text(screen, "Choose your response:", 18, WIDTH // 2, 240, POLITICIAN_ACCENT)
        
        for i, btn in enumerate(self.response_buttons):
            response = self.current_issue.responses[i]
            # Use selected flag rather than mutating colors
            btn.selected = (self.selected_response is not None and i == self.selected_response)
            btn.draw(screen)

            # Response text (left-aligned)
            y_pos = 250 + i * 70
            draw_wrapped_text(response["text"], screen, 100, y_pos + 18, 16, WHITE, 700)
        
        # Key hints
        draw_text(screen, "Use ↑↓ arrows or 1-4 keys, Enter to confirm", 
                 14, WIDTH // 2, HEIGHT - 20, TEXT_MUTED)
    
    def draw_feedback(self, screen):
        """Draw feedback after responding."""
        self.draw_gameplay(screen)
        
        # Overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))
        
        # Feedback box
        box_rect = pygame.Rect(150, 150, 600, 300)
        pygame.draw.rect(screen, CARD_BG, box_rect, border_radius=16)
        
        border_color = SUCCESS if self.approval_change > 0 else (
            DANGER if self.approval_change < -5 else WARNING
        )
        pygame.draw.rect(screen, border_color, box_rect, 3, border_radius=16)
        
        # Result header
        if self.approval_change > 10:
            header = "Excellent Decision!"
        elif self.approval_change > 0:
            header = "Good Response"
        elif self.approval_change >= -5:
            header = "Neutral Outcome"
        else:
            header = "Poor Decision"
        
        draw_text(screen, header, 32, WIDTH // 2, 195, border_color, bold=True)
        draw_text(screen, self.feedback_text, 24, WIDTH // 2, 240, border_color)
        
        # Outcome
        draw_text(screen, "Public Reaction:", 18, WIDTH // 2, 290, TEXT_SECONDARY)
        draw_wrapped_text(self.current_issue.outcome, screen, 180, 320, 18, WHITE, 540)
        
        # Current approval
        draw_text(screen, f"Current Approval: {self.approval}%", 20, WIDTH // 2, 390, 
                 POLITICIAN_ACCENT, bold=True)
        
        if self.current_issue_index < len(self.issues) - 1:
            self.next_btn.draw(screen)
        else:
            self.finish_btn.draw(screen)
    
    def draw_results(self, screen):
        """Draw final results screen."""
        # Header
        header_rect = pygame.Rect(0, 0, WIDTH, 100)
        pygame.draw.rect(screen, POLITICIAN_PRIMARY, header_rect)
        draw_text(screen, "Term Complete!", 42, WIDTH // 2, 35, WHITE, bold=True)
        draw_text(screen, "Your Political Legacy", 18, WIDTH // 2, 72, TEXT_SECONDARY)
        
        # Final stats
        stats_y = 130
        draw_text(screen, f"Final Approval: {self.approval}%", 
                 32, WIDTH // 2, stats_y, WHITE, bold=True)
        draw_text(screen, f"Total Points: {self.score}", 
                 24, WIDTH // 2, stats_y + 45, POLITICIAN_ACCENT)
        
        # Decision breakdown
        draw_text(screen, f"Good Decisions: {self.good_decisions}  |  "
                         f"Neutral: {self.neutral_decisions}  |  "
                         f"Poor: {self.bad_decisions}", 
                 18, WIDTH // 2, stats_y + 90, TEXT_SECONDARY)
        
        # Legacy rating
        if self.approval >= 70:
            legacy = "Beloved Leader"
            legacy_color = SUCCESS
            desc = "The people adore you! Your name will be remembered fondly."
        elif self.approval >= 50:
            legacy = "Competent Official"
            legacy_color = ACCENT
            desc = "You did a solid job. The city is better for your service."
        elif self.approval >= 30:
            legacy = "Controversial Figure"
            legacy_color = WARNING
            desc = "Your tenure was mixed. Some support you, others don't."
        else:
            legacy = "Unpopular Politician"
            legacy_color = DANGER
            desc = "Your decisions were widely criticized. Re-election looks unlikely."
        
        draw_text(screen, legacy, 36, WIDTH // 2, stats_y + 145, legacy_color, bold=True)
        draw_wrapped_text(desc, screen, 150, stats_y + 190, 18, TEXT_SECONDARY, 600)
        
        # Real-world lesson
        lesson = get_career_lesson("Politician")
        draw_text(screen, "What Real Politicians Do:", 20, WIDTH // 2, stats_y + 270, 
                 POLITICIAN_ACCENT, bold=True)
        draw_wrapped_text(lesson, screen, 100, stats_y + 300, 16, TEXT_MUTED, 700)
        
        self.back_btn.draw(screen)
