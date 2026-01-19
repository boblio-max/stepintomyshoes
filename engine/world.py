"""
Step Into My Shoes - Base World Class
Template for all career mini-worlds.
"""

import pygame
from engine.colors import BACKGROUND, WHITE, TEXT_SECONDARY
from engine.ui import draw_text, ModernButton


class BaseWorld:
    """
    Base class for all career worlds.
    Provides common structure and utilities.
    """
    
    # Screen dimensions (should match main config)
    WIDTH = 900
    HEIGHT = 600
    
    def __init__(self, story_package=None):
        self.story = story_package or {"intro": "Your career adventure begins!"}
        self.state = "intro"  # intro -> gameplay -> results
        self.result = None
        self.score = 0
        self.max_score = 0
        
        # Career info
        self.career_name = "Career"
        self.career_color = (100, 100, 100)
        self.career_icon = "?"
        
        # Common UI elements
        self.clock = pygame.time.Clock()
        
    def run(self, scene_manager):
        """Main loop for the world. Override in child classes."""
        screen = pygame.display.get_surface()
        running = True
        
        while running:
            dt = self.clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                self.handle_event(event, scene_manager)
            
            self.update(dt)
            self.draw(screen)
            pygame.display.update()
    
    def handle_event(self, event, scene_manager):
        """Handle input events. Override in child classes."""
        pass
    
    def update(self, dt):
        """Update game logic. Override in child classes."""
        pass
    
    def draw(self, screen):
        """Draw current state. Override in child classes."""
        screen.fill(BACKGROUND)
        
        if self.state == "intro":
            self.draw_intro(screen)
        elif self.state == "gameplay":
            self.draw_gameplay(screen)
        elif self.state == "results":
            self.draw_results(screen)
    
    def draw_intro(self, screen):
        """Draw intro state. Override in child classes."""
        draw_text(screen, f"{self.career_icon} {self.career_name} World", 
                 48, self.WIDTH // 2, 80, WHITE, bold=True)
    
    def draw_gameplay(self, screen):
        """Draw gameplay state. Override in child classes."""
        draw_text(screen, "Gameplay", 36, self.WIDTH // 2, self.HEIGHT // 2, WHITE)
    
    def draw_results(self, screen):
        """Draw results state. Override in child classes."""
        draw_text(screen, "Results", 36, self.WIDTH // 2, self.HEIGHT // 2, WHITE)
    
    def draw_header(self, screen, title, subtitle=None):
        """Draw a standard header bar."""
        # Header background
        header_rect = pygame.Rect(0, 0, self.WIDTH, 80)
        pygame.draw.rect(screen, self.career_color, header_rect)
        
        # Title
        draw_text(screen, title, 32, self.WIDTH // 2, 30, WHITE, bold=True)
        
        # Subtitle
        if subtitle:
            draw_text(screen, subtitle, 16, self.WIDTH // 2, 58, TEXT_SECONDARY)
    
    def draw_score_display(self, screen, x, y):
        """Draw current score."""
        font = pygame.font.SysFont("arial", 24, bold=True)
        score_text = f"Score: {self.score}"
        score_surf = font.render(score_text, True, WHITE)
        screen.blit(score_surf, (x, y))
    
    def transition_to_results(self):
        """Transition to results screen."""
        self.state = "results"
    
    def get_performance_grade(self):
        """Calculate performance grade."""
        if self.max_score == 0:
            return "N/A"
        
        percentage = (self.score / self.max_score) * 100
        
        if percentage >= 90:
            return "A+"
        elif percentage >= 80:
            return "A"
        elif percentage >= 70:
            return "B"
        elif percentage >= 60:
            return "C"
        elif percentage >= 50:
            return "D"
        else:
            return "F"


# Legacy alias for backward compatibility
class world(BaseWorld):
    pass
