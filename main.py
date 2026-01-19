"""
Step Into My Shoes - Career Exploration Game
FBLA Computer Game & Simulation Competition Entry

A polished, educational career simulation game where players explore
different careers through interactive mini-worlds.

Features:
- 5 unique career worlds with distinct gameplay mechanics
- Dynamic AI-driven backstory generation
- Modern, responsive UI with animations
- Educational content about real-world careers
"""

import pygame
import sys
import math
from typing import Optional, Dict, List

from engine.core import SceneManager
from engine.ui import (
    Button, ModernButton, CareerCard, draw_text, draw_wrapped_text,
    ParticleSystem, ScreenFlash
)
from engine.colors import (
    WHITE, BLACK, GREY, BACKGROUND, CARD_BG, TEXT_SECONDARY, TEXT_MUTED,
    PRIMARY, ACCENT, DANGER, SUCCESS, WARNING,
    DOCTOR_PRIMARY, LAWYER_PRIMARY, INFLUENCER_PRIMARY,
    POLITICIAN_PRIMARY, ENGINEER_PRIMARY
)
from engine.backstory_ai import generate_backstory

# Import all worlds
from worlds.doctor import DoctorWorld
from worlds.lawyer import LawyerWorld
from worlds.influencer import InfluencerWorld
from worlds.politician import PoliticianWorld
from worlds.engineer import EngineerWorld


# ============================================================================
# GAME CONFIGURATION
# ============================================================================

class Config:
    """Centralized game configuration."""
    WIDTH = 900
    HEIGHT = 600
    FPS = 60
    TITLE = "Step Into My Shoes"
    SUBTITLE = "Career Exploration Game"
    VERSION = "1.0.0"


# ============================================================================
# CAREER DATA
# ============================================================================

CAREERS = {
    "Doctor": {
        "name": "Doctor",
        "icon": "⚕",
        "tagline": "Save lives under pressure",
        "color": DOCTOR_PRIMARY,
        "world_class": DoctorWorld,
        "available": True
    },
    "Lawyer": {
        "name": "Lawyer",
        "icon": "⚖",
        "tagline": "Find truth in testimony",
        "color": LAWYER_PRIMARY,
        "world_class": LawyerWorld,
        "available": True
    },
    "Influencer": {
        "name": "Influencer",
        "icon": "★",
        "tagline": "Create viral content",
        "color": INFLUENCER_PRIMARY,
        "world_class": InfluencerWorld,
        "available": True
    },
    "Politician": {
        "name": "Politician",
        "icon": "⬢",
        "tagline": "Lead with wisdom",
        "color": POLITICIAN_PRIMARY,
        "world_class": PoliticianWorld,
        "available": True
    },
    "Engineer": {
        "name": "Engineer",
        "icon": "⚙",
        "tagline": "Build the future",
        "color": ENGINEER_PRIMARY,
        "world_class": EngineerWorld,
        "available": True
    }
}


# ============================================================================
# SCREEN REFERENCE (set during initialization)
# ============================================================================

SCREEN: pygame.Surface = None  # type: ignore


# ============================================================================
# VISUAL EFFECTS
# ============================================================================

class BackgroundEffect:
    """Animated background with floating particles."""
    
    def __init__(self):
        self.particles = []
        self.time = 0
        
        # Create initial particles
        for _ in range(15):
            self.add_particle()
    
    def add_particle(self):
        import random
        self.particles.append({
            "x": random.randint(0, Config.WIDTH),
            "y": random.randint(0, Config.HEIGHT),
            "size": random.randint(2, 5),
            "speed": random.uniform(0.2, 0.8),
            "alpha": random.randint(30, 80)
        })
    
    def update(self, dt):
        self.time += dt
        
        for p in self.particles:
            p["y"] -= p["speed"]
            p["x"] += math.sin(self.time + p["y"] * 0.01) * 0.3
            
            if p["y"] < -10:
                p["y"] = Config.HEIGHT + 10
                p["x"] = pygame.time.get_ticks() % Config.WIDTH
    
    def draw(self, surface):
        for p in self.particles:
            color = (100, 120, 150)
            pygame.draw.circle(surface, color, (int(p["x"]), int(p["y"])), p["size"])


# ============================================================================
# MAIN MENU SCENE
# ============================================================================

def main_menu(scene_manager: SceneManager):
    """Main menu with animated title and modern buttons."""
    clock = pygame.time.Clock()
    particles = ParticleSystem()
    background = BackgroundEffect()
    
    # Buttons
    start_btn = ModernButton(
        Config.WIDTH // 2 - 150, 300, 300, 60,
        "Start Your Journey",
        ACCENT, SUCCESS, font_size=24
    )
    about_btn = ModernButton(
        Config.WIDTH // 2 - 150, 380, 300, 60,
        "About This Game",
        PRIMARY, (100, 160, 230), font_size=22
    )
    exit_btn = ModernButton(
        Config.WIDTH // 2 - 150, 460, 300, 60,
        "Exit",
        DANGER, (220, 90, 80), font_size=22
    )
    
    # Animation state
    title_offset = 0
    time_elapsed = 0
    
    running = True
    while running:
        dt = clock.tick(Config.FPS) / 1000.0
        time_elapsed += dt
        
        # Background
        SCREEN.fill(BACKGROUND)
        background.update(dt)
        background.draw(SCREEN)
        
        # Animated title
        title_offset = math.sin(time_elapsed * 2) * 5
        
        # Draw decorative header bar
        header_rect = pygame.Rect(0, 0, Config.WIDTH, 200)
        pygame.draw.rect(SCREEN, (35, 45, 65), header_rect)
        
        # Title with subtle animation
        title_y = 80 + title_offset
        
        # Glow effect
        glow_font = pygame.font.SysFont("arial", 52, bold=True)
        glow_surf = glow_font.render(Config.TITLE, True, ACCENT)
        glow_rect = glow_surf.get_rect(center=(Config.WIDTH // 2 + 2, title_y + 2))
        SCREEN.blit(glow_surf, glow_rect)
        
        # Main title
        title_font = pygame.font.SysFont("arial", 52, bold=True)
        title_surf = title_font.render(Config.TITLE, True, WHITE)
        title_rect = title_surf.get_rect(center=(Config.WIDTH // 2, title_y))
        SCREEN.blit(title_surf, title_rect)
        
        # Subtitle
        draw_text(SCREEN, Config.SUBTITLE, 22, Config.WIDTH // 2, 140, TEXT_SECONDARY)
        
        # Tagline
        draw_text(SCREEN, "Discover Your Future Through Interactive Career Worlds", 
                 18, Config.WIDTH // 2, 230, TEXT_MUTED)
        
        # Update and draw particles
        particles.update(dt)
        particles.draw(SCREEN)
        
        # Draw buttons
        start_btn.draw(SCREEN)
        about_btn.draw(SCREEN)
        exit_btn.draw(SCREEN)
        
        # Version info
        draw_text(SCREEN, f"v{Config.VERSION} | FBLA Computer Game & Simulation", 
                 12, Config.WIDTH // 2, Config.HEIGHT - 20, TEXT_MUTED)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                
                if start_btn.is_hover():
                    particles.emit(mx, my, ACCENT, 20)
                    scene_manager.change_scene(enhanced_career_selection)
                    return
                
                if about_btn.is_hover():
                    particles.emit(mx, my, PRIMARY, 15)
                    scene_manager.change_scene(about_screen)
                    return
                
                if exit_btn.is_hover():
                    particles.emit(mx, my, DANGER, 15)
                    pygame.time.wait(200)
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()


# ============================================================================
# ABOUT SCREEN
# ============================================================================

def about_screen(scene_manager: SceneManager):
    """About screen with game information."""
    clock = pygame.time.Clock()
    particles = ParticleSystem()
    
    back_btn = ModernButton(
        Config.WIDTH // 2 - 100, 520, 200, 50,
        "← Back to Menu",
        CARD_BG, PRIMARY, font_size=20
    )
    
    about_text = """Step Into My Shoes is an educational career exploration game 
designed to help students discover different career paths through 
interactive simulations.

Each career world features:
• Unique gameplay mechanics that simulate real job tasks
• Dynamic AI-generated backstories for immersive experiences  
• Educational content about real-world career skills
• Score-based challenges to test your abilities

Careers Available:
• Doctor - Diagnose patients under time pressure
• Lawyer - Find contradictions in witness statements
• Influencer - Master timing to create viral content
• Politician - Manage public approval through decisions
• Engineer - Solve circuit puzzles with spatial reasoning

Created for the FBLA Computer Game & Simulation Competition."""

    running = True
    while running:
        dt = clock.tick(Config.FPS) / 1000.0
        
        SCREEN.fill(BACKGROUND)
        
        # Header
        header_rect = pygame.Rect(0, 0, Config.WIDTH, 80)
        pygame.draw.rect(SCREEN, PRIMARY, header_rect)
        draw_text(SCREEN, "About Step Into My Shoes", 32, Config.WIDTH // 2, 40, WHITE, bold=True)
        
        # Content card
        card_rect = pygame.Rect(50, 100, Config.WIDTH - 100, 400)
        pygame.draw.rect(SCREEN, CARD_BG, card_rect, border_radius=16)
        
        # Draw about text
        draw_wrapped_text(about_text, SCREEN, 80, 120, 16, WHITE, Config.WIDTH - 160)
        
        particles.update(dt)
        particles.draw(SCREEN)
        
        back_btn.draw(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.is_hover():
                    scene_manager.change_scene(main_menu)
                    return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene_manager.change_scene(main_menu)
                    return
        
        pygame.display.update()


# ============================================================================
# CAREER SELECTION SCREEN
# ============================================================================

def enhanced_career_selection(scene_manager: SceneManager):
    """Modern career selection with card-based UI."""
    clock = pygame.time.Clock()
    particles = ParticleSystem()
    background = BackgroundEffect()
    
    # Create career cards
    cards = []
    card_width, card_height = 150, 170
    spacing = 25
    
    # Calculate grid positions (3 top, 2 bottom centered)
    career_list = list(CAREERS.values())
    
    # Top row (3 cards)
    top_row_width = 3 * card_width + 2 * spacing
    top_start_x = (Config.WIDTH - top_row_width) // 2
    top_y = 150
    
    for i in range(3):
        career = career_list[i]
        x = top_start_x + i * (card_width + spacing)
        card = CareerCard(x, top_y, card_width, card_height,
                         career["name"], career["icon"], career["color"], career["available"])
        cards.append((card, career))
    
    # Bottom row (2 cards centered)
    bottom_row_width = 2 * card_width + spacing
    bottom_start_x = (Config.WIDTH - bottom_row_width) // 2
    bottom_y = top_y + card_height + spacing + 20
    
    for i in range(2):
        career = career_list[3 + i]
        x = bottom_start_x + i * (card_width + spacing)
        card = CareerCard(x, bottom_y, card_width, card_height,
                         career["name"], career["icon"], career["color"], career["available"])
        cards.append((card, career))
    
    # Back button
    back_btn = ModernButton(30, 25, 100, 40, "← Back", CARD_BG, PRIMARY, font_size=18)
    
    # Selected career info
    hovered_career = None
    
    running = True
    while running:
        dt = clock.tick(Config.FPS) / 1000.0
        
        SCREEN.fill(BACKGROUND)
        background.update(dt)
        background.draw(SCREEN)
        
        # Header
        draw_text(SCREEN, "Choose Your Career Path", 36, Config.WIDTH // 2, 50, WHITE, bold=True)
        draw_text(SCREEN, "Select a career to begin your journey", 16, Config.WIDTH // 2, 90, TEXT_SECONDARY)
        
        # Update and draw cards
        hovered_career = None
        for card, career in cards:
            card.draw(SCREEN)
            if card.is_hover() and career["available"]:
                hovered_career = career
        
        # Show hovered career info
        if hovered_career:
            info_y = 480
            draw_text(SCREEN, hovered_career["tagline"], 18, Config.WIDTH // 2, info_y, 
                     hovered_career["color"], bold=True)
            draw_text(SCREEN, "Click to start!", 14, Config.WIDTH // 2, info_y + 25, TEXT_MUTED)
        else:
            draw_text(SCREEN, "Hover over a career to learn more", 16, 
                     Config.WIDTH // 2, 490, TEXT_MUTED)
        
        # Draw particles and back button
        particles.update(dt)
        particles.draw(SCREEN)
        back_btn.draw(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                
                if back_btn.is_hover():
                    particles.emit(mx, my, PRIMARY, 10)
                    scene_manager.change_scene(main_menu)
                    return
                
                for card, career in cards:
                    if card.is_hover() and career["available"]:
                        particles.emit(mx, my, career["color"], 25)
                        
                        # Generate backstory and go to backstory screen
                        backstory = generate_backstory(career["name"])
                        
                        scene_manager.change_scene(
                            lambda sm, c=career, b=backstory: backstory_screen(sm, c, b)
                        )
                        return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene_manager.change_scene(main_menu)
                    return
        
        pygame.display.update()


# ============================================================================
# BACKSTORY SCREEN
# ============================================================================

def backstory_screen(scene_manager: SceneManager, career: dict, backstory: str):
    """Display AI-generated backstory with typewriter effect."""
    clock = pygame.time.Clock()
    particles = ParticleSystem()
    flash = ScreenFlash()
    
    # Typewriter effect state
    full_text = backstory
    displayed_text = ""
    char_index = 0
    char_timer = 0
    char_delay = 0.025  # seconds per character
    text_complete = False
    
    # Buttons
    start_btn = ModernButton(
        Config.WIDTH // 2 - 180, 510, 160, 50,
        "Begin Career",
        career["color"], career["color"], font_size=20
    )
    start_btn.disabled = True
    
    skip_btn = ModernButton(
        Config.WIDTH // 2 + 20, 510, 160, 50,
        "Skip Intro",
        CARD_BG, PRIMARY, font_size=20
    )
    
    running = True
    while running:
        dt = clock.tick(Config.FPS) / 1000.0
        
        SCREEN.fill(BACKGROUND)
        
        # Header with career color
        header_rect = pygame.Rect(0, 0, Config.WIDTH, 90)
        pygame.draw.rect(SCREEN, career["color"], header_rect)
        
        draw_text(SCREEN, f"{career['icon']} {career['name']} Path", 
                 36, Config.WIDTH // 2, 35, WHITE, bold=True)
        draw_text(SCREEN, career["tagline"], 16, Config.WIDTH // 2, 70, TEXT_SECONDARY)
        
        # Typewriter effect
        if not text_complete:
            char_timer += dt
            if char_timer >= char_delay and char_index < len(full_text):
                displayed_text += full_text[char_index]
                char_index += 1
                char_timer = 0
            
            if char_index >= len(full_text):
                text_complete = True
                start_btn.disabled = False
        
        # Story card
        card_rect = pygame.Rect(50, 110, Config.WIDTH - 100, 380)
        pygame.draw.rect(SCREEN, CARD_BG, card_rect, border_radius=16)
        
        # Story text
        draw_wrapped_text(displayed_text, SCREEN, 80, 130, 20, WHITE, Config.WIDTH - 160)
        
        # Progress bar for text
        if not text_complete:
            progress = char_index / len(full_text)
            bar_width = 400
            bar_x = (Config.WIDTH - bar_width) // 2
            bar_y = 485
            
            pygame.draw.rect(SCREEN, CARD_BG, (bar_x, bar_y, bar_width, 6), border_radius=3)
            pygame.draw.rect(SCREEN, career["color"], 
                           (bar_x, bar_y, int(bar_width * progress), 6), border_radius=3)
        
        # Update effects
        particles.update(dt)
        flash.update()
        particles.draw(SCREEN)
        flash.draw(SCREEN)
        
        # Draw buttons
        start_btn.draw(SCREEN)
        skip_btn.draw(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                
                if skip_btn.is_hover():
                    displayed_text = full_text
                    text_complete = True
                    start_btn.disabled = False
                
                if start_btn.is_hover() and not start_btn.disabled:
                    particles.emit(mx, my, career["color"], 30)
                    flash.flash(career["color"], 50)
                    pygame.time.wait(200)
                    
                    # Launch the career world
                    world_class = career.get("world_class")
                    if world_class:
                        world = world_class()
                        scene_manager.change_scene(world.run)
                    return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not text_complete:
                        displayed_text = full_text
                        text_complete = True
                        start_btn.disabled = False
                    elif not start_btn.disabled:
                        world_class = career.get("world_class")
                        if world_class:
                            world = world_class()
                            scene_manager.change_scene(world.run)
                        return
                
                if event.key == pygame.K_ESCAPE:
                    scene_manager.change_scene(enhanced_career_selection)
                    return
        
        pygame.display.update()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def run_game():
    """Initialize and run the game."""
    global SCREEN
    
    pygame.init()
    pygame.font.init()
    
    SCREEN = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
    pygame.display.set_caption(Config.TITLE)
    
    # Set window icon (optional)
    try:
        icon = pygame.Surface((32, 32))
        icon.fill(ACCENT)
        pygame.display.set_icon(icon)
    except:
        pass
    
    scene_manager = SceneManager()
    scene_manager.change_scene(main_menu)
    scene_manager.run()


if __name__ == "__main__":
    run_game()
