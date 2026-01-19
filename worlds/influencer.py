"""
Step Into My Shoes - Influencer World
Hit timing bars perfectly to create viral content.
Teaches: Timing, rhythm, performance under pressure, consistency.
"""

import pygame
import random
import math
from engine.colors import (
    BACKGROUND, WHITE, BLACK, INFLUENCER_PRIMARY, INFLUENCER_SECONDARY,
    INFLUENCER_ACCENT, SUCCESS, DANGER, WARNING, TEXT_SECONDARY, CARD_BG,
    ACCENT, TEXT_MUTED, PRIMARY
)
from engine.ui import (
    draw_text, draw_text_left, draw_wrapped_text, ModernButton, ParticleSystem, ScreenFlash,
    ProgressBar
)
from engine.backstory_ai import get_performance_feedback, get_career_lesson

pygame.init()

WIDTH, HEIGHT = 900, 600

# Content types with different timing patterns
CONTENT_TYPES = [
    {
        "name": "Unboxing Video",
        "description": "Open products with perfect timing for reactions",
        "beat_count": 8,
        "speed": 1.0,
        "icon": "📦"
    },
    {
        "name": "Dance Challenge",
        "description": "Hit the moves at exactly the right moment",
        "beat_count": 12,
        "speed": 1.3,
        "icon": "💃"
    },
    {
        "name": "Comedy Sketch",
        "description": "Deliver punchlines with perfect comedic timing",
        "beat_count": 6,
        "speed": 0.9,
        "icon": "😂"
    },
    {
        "name": "Product Review",
        "description": "Highlight features at key moments",
        "beat_count": 8,
        "speed": 1.0,
        "icon": "⭐"
    },
    {
        "name": "Tutorial Video",
        "description": "Demonstrate steps clearly and on time",
        "beat_count": 10,
        "speed": 0.85,
        "icon": "📚"
    },
    {
        "name": "Live Stream Moment",
        "description": "React to events in real-time",
        "beat_count": 10,
        "speed": 1.4,
        "icon": "🎬"
    }
]


class TimingBeat:
    """A single timing target to hit."""
    
    def __init__(self, target_time, lane=0):
        self.target_time = target_time
        self.lane = lane  # 0 = left, 1 = center, 2 = right
        self.hit = False
        self.missed = False
        self.hit_quality = None  # "perfect", "good", "ok", None
    
    def get_x_position(self, bar_x, bar_width):
        """Get x position based on lane."""
        segment = bar_width // 3
        return bar_x + segment // 2 + self.lane * segment


class InfluencerWorld:
    """
    Influencer Career Mini-Game
    Players hit timing bars to create perfect content.
    """
    
    def __init__(self, story_package=None):
        self.story = story_package or {
            "intro": "Welcome to the Content Studio!\n\nAs a content creator, timing is everything.\nHit the markers at exactly the right moment to create viral content.\n\nWatch the moving indicator and press SPACE when it aligns with each target!"
        }
        self.state = "intro"
        self.score = 0
        self.total_videos = 4
        self.current_video_index = 0
        self.current_content = None
        
        # Timing game state
        self.beats = []
        self.current_beat_index = 0
        self.game_time = 0
        self.beat_window = 0.15  # seconds for "perfect"
        self.good_window = 0.25  # seconds for "good"
        self.ok_window = 0.4    # seconds for "ok"
        
        # Visual state
        self.indicator_pos = 0
        self.bar_x = 100
        self.bar_width = 700
        self.bar_y = 350
        
        # Stats
        self.perfect_hits = 0
        self.good_hits = 0
        self.ok_hits = 0
        self.misses = 0
        self.energy = 100
        self.combo = 0
        self.max_combo = 0
        
        # Visual effects
        self.particles = ParticleSystem()
        self.flash = ScreenFlash()
        self.feedback_text = ""
        self.feedback_timer = 0
        self.feedback_color = WHITE
        self.hit_effects = []  # [(x, y, timer, color), ...]
        
        # UI elements
        self.start_btn = ModernButton(350, 480, 200, 55, "Start Recording",
                                       INFLUENCER_PRIMARY, INFLUENCER_SECONDARY)
        self.next_btn = ModernButton(350, 500, 200, 55, "Next Video",
                                      INFLUENCER_PRIMARY, INFLUENCER_SECONDARY)
        self.finish_btn = ModernButton(350, 500, 200, 55, "View Analytics",
                                        INFLUENCER_PRIMARY, INFLUENCER_SECONDARY)
        self.back_btn = ModernButton(350, 500, 200, 55, "Return to Hub",
                                      CARD_BG, INFLUENCER_PRIMARY)
        
        self.clock = pygame.time.Clock()
        self.scene_manager = None
        self.generate_content()
    
    def generate_content(self):
        """Generate content for all videos."""
        self.content_list = random.sample(CONTENT_TYPES, 
                                          min(self.total_videos, len(CONTENT_TYPES)))
        if self.content_list:
            self.load_video(0)
    
    def load_video(self, index):
        """Load a video and generate beats."""
        if index < len(self.content_list):
            self.current_content = self.content_list[index]
            self.current_video_index = index
            self.game_time = 0
            self.current_beat_index = 0
            self.combo = 0
            self.energy = 100
            
            # Generate beats with timing
            beat_count = self.current_content["beat_count"]
            speed = self.current_content["speed"]
            
            self.beats = []
            base_interval = 1.2 / speed
            
            for i in range(beat_count):
                # Slight variation in timing
                time_offset = (i + 1) * base_interval + random.uniform(-0.1, 0.1)
                lane = random.randint(0, 2)  # Random lane
                self.beats.append(TimingBeat(time_offset, lane))
            
            self.indicator_pos = 0
            self.hit_effects = []
    
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
        
        elif self.state == "video_complete":
            if self.next_btn.is_clicked(event) or self.finish_btn.is_clicked(event):
                if self.current_video_index < len(self.content_list) - 1:
                    self.load_video(self.current_video_index + 1)
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
            if event.key == pygame.K_SPACE:
                self.try_hit()
            elif event.key == pygame.K_LEFT:
                self.try_hit(lane=0)
            elif event.key == pygame.K_DOWN:
                self.try_hit(lane=1)
            elif event.key == pygame.K_RIGHT:
                self.try_hit(lane=2)
    
    def try_hit(self, lane=None):
        """Attempt to hit the current beat."""
        if not self.beats or self.current_beat_index >= len(self.beats):
            return
        
        current_beat = self.beats[self.current_beat_index]
        
        # Check if we're targeting the right lane (if lane specified)
        if lane is not None and current_beat.lane != lane:
            # Check if there's a beat in this lane we should hit
            for i, beat in enumerate(self.beats[self.current_beat_index:], self.current_beat_index):
                if beat.lane == lane and not beat.hit and not beat.missed:
                    time_diff = abs(self.game_time - beat.target_time)
                    if time_diff <= self.ok_window:
                        self.process_hit(i, time_diff)
                        return
            return
        
        time_diff = abs(self.game_time - current_beat.target_time)
        
        if time_diff <= self.ok_window:
            self.process_hit(self.current_beat_index, time_diff)
    
    def process_hit(self, beat_index, time_diff):
        """Process a successful hit."""
        beat = self.beats[beat_index]
        beat.hit = True
        
        x = beat.get_x_position(self.bar_x, self.bar_width)
        y = self.bar_y
        
        if time_diff <= self.beat_window:
            beat.hit_quality = "perfect"
            self.perfect_hits += 1
            self.combo += 1
            points = 100 + self.combo * 10
            self.score += points
            self.energy = min(100, self.energy + 5)
            
            self.feedback_text = "PERFECT!"
            self.feedback_color = SUCCESS
            self.particles.emit(x, y, SUCCESS, 20)
            self.hit_effects.append((x, y, 0.5, SUCCESS))
            
        elif time_diff <= self.good_window:
            beat.hit_quality = "good"
            self.good_hits += 1
            self.combo += 1
            points = 50 + self.combo * 5
            self.score += points
            self.energy = min(100, self.energy + 2)
            
            self.feedback_text = "GOOD!"
            self.feedback_color = ACCENT
            self.particles.emit(x, y, ACCENT, 12)
            self.hit_effects.append((x, y, 0.4, ACCENT))
            
        else:
            beat.hit_quality = "ok"
            self.ok_hits += 1
            self.combo = max(0, self.combo - 1)
            points = 25
            self.score += points
            
            self.feedback_text = "OK"
            self.feedback_color = WARNING
            self.hit_effects.append((x, y, 0.3, WARNING))
        
        self.max_combo = max(self.max_combo, self.combo)
        self.feedback_timer = 0.5
        
        # Move to next unhit beat
        while self.current_beat_index < len(self.beats) and self.beats[self.current_beat_index].hit:
            self.current_beat_index += 1
    
    def update(self, dt):
        """Update game state."""
        self.particles.update(dt)
        self.flash.update()
        
        if self.feedback_timer > 0:
            self.feedback_timer -= dt
        
        # Update hit effects
        self.hit_effects = [(x, y, t - dt, c) for x, y, t, c in self.hit_effects if t > 0]
        
        if self.state == "gameplay":
            self.game_time += dt
            
            # Update indicator position (oscillates)
            speed = self.current_content["speed"] if self.current_content else 1.0
            self.indicator_pos = (self.game_time * speed * 200) % self.bar_width
            
            # Check for missed beats
            for beat in self.beats:
                if not beat.hit and not beat.missed:
                    if self.game_time > beat.target_time + self.ok_window:
                        beat.missed = True
                        self.misses += 1
                        self.combo = 0
                        self.energy = max(0, self.energy - 10)
                        
                        x = beat.get_x_position(self.bar_x, self.bar_width)
                        self.hit_effects.append((x, self.bar_y, 0.3, DANGER))
            
            # Drain energy slowly
            self.energy = max(0, self.energy - dt * 2)
            
            # Check if video is complete
            all_processed = all(b.hit or b.missed for b in self.beats)
            if all_processed or self.energy <= 0:
                self.state = "video_complete"
    
    def draw(self, screen):
        """Draw current state."""
        screen.fill(BACKGROUND)
        
        if self.state == "intro":
            self.draw_intro(screen)
        elif self.state == "gameplay":
            self.draw_gameplay(screen)
        elif self.state == "video_complete":
            self.draw_video_complete(screen)
        elif self.state == "results":
            self.draw_results(screen)
        
        self.particles.draw(screen)
        self.flash.draw(screen)
    
    def draw_intro(self, screen):
        """Draw intro screen."""
        # Header
        header_rect = pygame.Rect(0, 0, WIDTH, 100)
        pygame.draw.rect(screen, INFLUENCER_PRIMARY, header_rect)
        draw_text(screen, "Influencer World", 42, WIDTH // 2, 35, WHITE, bold=True)
        draw_text(screen, "Content Creation Studio", 18, WIDTH // 2, 72, TEXT_SECONDARY)
        
        # Intro text
        draw_wrapped_text(self.story["intro"], screen, 100, 140, 22, WHITE, 700)
        
        # Instructions
        draw_text(screen, "How to Play:", 24, WIDTH // 2, 320, INFLUENCER_ACCENT, bold=True)
        instructions = [
            "Watch the moving indicator on the timing bar",
            "Press SPACE or arrow keys when it aligns with targets",
            "Perfect timing = more points and energy",
            "Build combos for bonus multipliers!"
        ]
        for i, instruction in enumerate(instructions):
            draw_text_left(screen, f"• {instruction}", 18, 140, 355 + i * 28, TEXT_SECONDARY)
        
        self.start_btn.draw(screen)
    
    def draw_gameplay(self, screen):
        """Draw gameplay screen."""
        # Header
        header_rect = pygame.Rect(0, 0, WIDTH, 60)
        pygame.draw.rect(screen, INFLUENCER_PRIMARY, header_rect)
        
        if self.current_content:
            draw_text(screen, f"{self.current_content['icon']} {self.current_content['name']}", 
                     24, WIDTH // 2, 20, WHITE, bold=True)
            draw_text(screen, self.current_content['description'], 
                     14, WIDTH // 2, 45, TEXT_SECONDARY)
        
        # Stats bar
        draw_text(screen, f"Score: {self.score}", 18, 100, 80, WHITE, bold=True)
        draw_text(screen, f"Combo: x{self.combo}", 18, 250, 80, INFLUENCER_ACCENT)
        draw_text(screen, f"Video {self.current_video_index + 1}/{len(self.content_list)}", 
                 18, WIDTH - 100, 80, TEXT_SECONDARY)
        
        # Energy bar
        energy_bar_x = 400
        energy_bar_width = 200
        energy_bar_rect = pygame.Rect(energy_bar_x, 75, energy_bar_width, 16)
        pygame.draw.rect(screen, CARD_BG, energy_bar_rect, border_radius=8)
        
        energy_fill = int((self.energy / 100) * energy_bar_width)
        if energy_fill > 0:
            energy_color = SUCCESS if self.energy > 50 else (WARNING if self.energy > 25 else DANGER)
            energy_fill_rect = pygame.Rect(energy_bar_x, 75, energy_fill, 16)
            pygame.draw.rect(screen, energy_color, energy_fill_rect, border_radius=8)
        
        draw_text(screen, "Energy", 12, energy_bar_x - 35, 82, TEXT_MUTED)
        
        # Feedback text
        if self.feedback_timer > 0:
            alpha = min(255, int(self.feedback_timer * 500))
            draw_text(screen, self.feedback_text, 36, WIDTH // 2, 150, self.feedback_color, bold=True)
        
        # Timing bar background
        bar_rect = pygame.Rect(self.bar_x, self.bar_y - 30, self.bar_width, 60)
        pygame.draw.rect(screen, CARD_BG, bar_rect, border_radius=10)
        
        # Lane dividers
        segment = self.bar_width // 3
        for i in range(1, 3):
            x = self.bar_x + i * segment
            pygame.draw.line(screen, TEXT_MUTED, (x, self.bar_y - 25), (x, self.bar_y + 25), 1)
        
        # Draw lane labels
        lane_labels = ["←", "↓", "→"]
        for i, label in enumerate(lane_labels):
            x = self.bar_x + segment // 2 + i * segment
            draw_text(screen, label, 14, x, self.bar_y + 50, TEXT_MUTED)
        
        # Draw beat targets
        for beat in self.beats:
            if beat.hit or beat.missed:
                continue
            
            x = beat.get_x_position(self.bar_x, self.bar_width)
            
            # Pulsing effect for upcoming beats
            time_until = beat.target_time - self.game_time
            if 0 < time_until < 1.0:
                pulse = 1 + 0.2 * math.sin(self.game_time * 10)
                size = int(20 * pulse)
            else:
                size = 20
            
            pygame.draw.circle(screen, INFLUENCER_ACCENT, (int(x), self.bar_y), size)
            pygame.draw.circle(screen, WHITE, (int(x), self.bar_y), size - 4)
        
        # Draw hit effects
        for x, y, timer, color in self.hit_effects:
            radius = int(30 * (1 - timer * 2))
            if radius > 0:
                pygame.draw.circle(screen, color, (int(x), int(y)), radius, 3)
        
        # Draw indicator (sweeping line)
        indicator_x = self.bar_x + int(self.indicator_pos)
        pygame.draw.line(screen, WHITE, (indicator_x, self.bar_y - 35), 
                        (indicator_x, self.bar_y + 35), 3)
        
        # Progress indicator
        beats_done = sum(1 for b in self.beats if b.hit or b.missed)
        progress = beats_done / len(self.beats) if self.beats else 0
        
        progress_rect = pygame.Rect(100, HEIGHT - 40, 700, 10)
        pygame.draw.rect(screen, CARD_BG, progress_rect, border_radius=5)
        
        progress_fill = pygame.Rect(100, HEIGHT - 40, int(700 * progress), 10)
        pygame.draw.rect(screen, INFLUENCER_ACCENT, progress_fill, border_radius=5)
        
        # Instructions
        draw_text(screen, "Press SPACE or ← ↓ → when the line hits a target!", 
                 16, WIDTH // 2, HEIGHT - 60, TEXT_SECONDARY)
    
    def draw_video_complete(self, screen):
        """Draw video completion screen."""
        # Overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))
        
        # Results box
        box_rect = pygame.Rect(150, 120, 600, 360)
        pygame.draw.rect(screen, CARD_BG, box_rect, border_radius=16)
        pygame.draw.rect(screen, INFLUENCER_ACCENT, box_rect, 3, border_radius=16)
        
        if self.current_content:
            draw_text(screen, f"{self.current_content['icon']} Video Complete!", 
                     32, WIDTH // 2, 160, WHITE, bold=True)
        
        # Stats
        perfect_pct = (self.perfect_hits / len(self.beats) * 100) if self.beats else 0
        
        draw_text(screen, f"Perfect Hits: {self.perfect_hits}", 22, WIDTH // 2, 220, SUCCESS)
        draw_text(screen, f"Good Hits: {self.good_hits}", 22, WIDTH // 2, 255, ACCENT)
        draw_text(screen, f"OK Hits: {self.ok_hits}", 22, WIDTH // 2, 290, WARNING)
        draw_text(screen, f"Misses: {self.misses}", 22, WIDTH // 2, 325, DANGER)
        
        draw_text(screen, f"Max Combo: x{self.max_combo}", 20, WIDTH // 2, 370, INFLUENCER_ACCENT)
        draw_text(screen, f"Total Score: {self.score}", 24, WIDTH // 2, 410, WHITE, bold=True)
        
        if self.current_video_index < len(self.content_list) - 1:
            self.next_btn.draw(screen)
        else:
            self.finish_btn.draw(screen)
    
    def draw_results(self, screen):
        """Draw final results screen."""
        # Header
        header_rect = pygame.Rect(0, 0, WIDTH, 100)
        pygame.draw.rect(screen, INFLUENCER_PRIMARY, header_rect)
        draw_text(screen, "Content Analytics!", 42, WIDTH // 2, 35, WHITE, bold=True)
        draw_text(screen, "Channel Performance Review", 18, WIDTH // 2, 72, TEXT_SECONDARY)
        
        # Stats
        total_beats = sum(c["beat_count"] for c in self.content_list)
        hit_rate = ((self.perfect_hits + self.good_hits + self.ok_hits) / total_beats * 100) if total_beats else 0
        
        stats_y = 130
        draw_text(screen, f"Videos Created: {len(self.content_list)}", 
                 26, WIDTH // 2, stats_y, WHITE, bold=True)
        draw_text(screen, f"Total Score: {self.score}", 
                 24, WIDTH // 2, stats_y + 40, INFLUENCER_ACCENT)
        draw_text(screen, f"Hit Rate: {hit_rate:.1f}%", 
                 22, WIDTH // 2, stats_y + 80, TEXT_SECONDARY)
        draw_text(screen, f"Best Combo: x{self.max_combo}", 
                 20, WIDTH // 2, stats_y + 115, TEXT_SECONDARY)
        
        # Grade
        if hit_rate >= 85:
            grade, grade_color = "Viral Star!", SUCCESS
        elif hit_rate >= 70:
            grade, grade_color = "Rising Creator", ACCENT
        elif hit_rate >= 50:
            grade, grade_color = "Aspiring Influencer", WARNING
        else:
            grade, grade_color = "Keep Practicing", DANGER
        
        draw_text(screen, grade, 36, WIDTH // 2, stats_y + 165, grade_color, bold=True)
        
        # Feedback
        feedback = get_performance_feedback("Influencer", self.perfect_hits + self.good_hits, total_beats)
        draw_wrapped_text(feedback, screen, 100, stats_y + 220, 18, TEXT_SECONDARY, 700)
        
        # Real-world lesson
        lesson = get_career_lesson("Influencer")
        draw_text(screen, "What Real Creators Do:", 20, WIDTH // 2, stats_y + 300, 
                 INFLUENCER_ACCENT, bold=True)
        draw_wrapped_text(lesson, screen, 100, stats_y + 330, 16, TEXT_MUTED, 700)
        
        self.back_btn.draw(screen)
