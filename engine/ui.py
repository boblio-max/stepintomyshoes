"""
Step Into My Shoes - UI Components
Modern, polished UI components for the career simulation game.
"""

import pygame
import math
from engine.colors import (
    WHITE, BLACK, GREY, PRIMARY, PRIMARY_LIGHT, SECONDARY,
    ACCENT, DANGER, BACKGROUND, CARD_BG, CARD_BG_HOVER,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, SUCCESS
)

pygame.font.init()

# ============================================================================
# CORE BUTTON CLASSES
# ============================================================================

class Button:
    """Basic button with hover detection."""
    
    def __init__(self, x, y, width, height, text, font_name="arial", font_size=28,
                 text_color=BLACK, bg_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = pygame.font.SysFont(font_name, font_size)
        self.text_color = text_color
        self.bg_color = bg_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)


class ModernButton:
    """Enhanced button with animations and modern styling."""
    
    def __init__(self, x, y, width, height, text,
                 primary_color=PRIMARY,
                 hover_color=PRIMARY_LIGHT,
                 text_color=WHITE,
                 font_size=22,
                 disabled=False,
                 border_radius=12,
                 selected_color=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.primary_color = primary_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font_size = font_size
        self.disabled = disabled
        self.border_radius = border_radius
        self.rect = pygame.Rect(x, y, width, height)
        
        # Animation state
        self.scale = 1.0
        self.target_scale = 1.0
        self.alpha = 255
        # Selection state (set externally without mutating colors)
        self.selected = False
        self.selected_color = selected_color or hover_color
    
    def update(self):
        """Smooth animation updates."""
        self.scale += (self.target_scale - self.scale) * 0.15

        # Avoid calling `is_hover()` here to prevent recursion with `update()`.
        if not self.disabled:
            mx, my = pygame.mouse.get_pos()
            hovering = self.rect.collidepoint(mx, my)
            self.target_scale = 1.03 if hovering else 1.0
        else:
            self.target_scale = 1.0

    def get_scaled_rect(self):
        """Return the current drawn (scaled) rect for accurate hit testing."""
        # Ensure animation state is updated so scale is current
        # (but avoid infinite recursion since is_hover calls update)
        scale = self.scale
        scaled_w = int(self.width * scale)
        scaled_h = int(self.height * scale)
        scaled_x = self.x + (self.width - scaled_w) // 2
        scaled_y = self.y + (self.height - scaled_h) // 2
        return pygame.Rect(scaled_x, scaled_y, scaled_w, scaled_h)
    
    def draw(self, surface):
        """Draw the button with effects."""
        self.update()
        
        # Calculate scaled dimensions
        scaled_w = int(self.width * self.scale)
        scaled_h = int(self.height * self.scale)
        scaled_x = self.x + (self.width - scaled_w) // 2
        scaled_y = self.y + (self.height - scaled_h) // 2
        
        # Shadow
        shadow_rect = pygame.Rect(scaled_x + 3, scaled_y + 3, scaled_w, scaled_h)
        pygame.draw.rect(surface, (0, 0, 0), shadow_rect, border_radius=self.border_radius)
        
        # Main button
        rect = pygame.Rect(scaled_x, scaled_y, scaled_w, scaled_h)
        
        if self.disabled:
            color = GREY
        elif self.is_hover():
            color = self.hover_color
        elif getattr(self, "selected", False):
            color = self.selected_color
        else:
            color = self.primary_color
        
        pygame.draw.rect(surface, color, rect, border_radius=self.border_radius)
        
        # Border for depth
        if not self.disabled and self.is_hover():
            pygame.draw.rect(surface, WHITE, rect, 2, border_radius=self.border_radius)
        
        # Text
        font = pygame.font.SysFont("arial", self.font_size, bold=True)
        text_color = TEXT_MUTED if self.disabled else self.text_color
        text_surf = font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)
    
    def is_hover(self):
        # Use the drawn (possibly scaled) rect for hover detection
        if self.disabled:
            return False
        self.update()
        mx, my = pygame.mouse.get_pos()
        return self.get_scaled_rect().collidepoint(mx, my)
    
    def is_clicked(self, event):
        """Check if button was clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Use event position for reliable click detection
            try:
                ex, ey = event.pos
            except Exception:
                ex, ey = pygame.mouse.get_pos()
            return self.get_scaled_rect().collidepoint(ex, ey) and not self.disabled
        return False


class IconButton(ModernButton):
    """Button with an icon."""
    
    def __init__(self, x, y, size, icon, **kwargs):
        super().__init__(x, y, size, size, icon, **kwargs)
        self.icon = icon
    
    def draw(self, surface):
        self.update()
        
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        color = self.hover_color if self.is_hover() else self.primary_color
        
        pygame.draw.rect(surface, color, rect, border_radius=self.border_radius)
        
        font = pygame.font.SysFont("arial", self.font_size, bold=True)
        icon_surf = font.render(self.icon, True, self.text_color)
        icon_rect = icon_surf.get_rect(center=rect.center)
        surface.blit(icon_surf, icon_rect)


# ============================================================================
# CARD COMPONENTS
# ============================================================================

class CareerCard:
    """Visual card for career selection."""
    
    def __init__(self, x, y, width, height, name, icon, color, available=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.icon = icon
        self.color = color
        self.available = available
        
        # Animation
        self.scale = 1.0
        self.target_scale = 1.0
        self.hover = False
    
    def update(self):
        self.scale += (self.target_scale - self.scale) * 0.15
        self.target_scale = 1.05 if self.is_hover() and self.available else 1.0
    
    def is_hover(self):
        mx, my = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mx, my)
        return self.hover
    
    def draw(self, surface):
        self.update()
        
        # Scaled dimensions
        scaled_w = int(self.rect.width * self.scale)
        scaled_h = int(self.rect.height * self.scale)
        scaled_x = self.rect.x + (self.rect.width - scaled_w) // 2
        scaled_y = self.rect.y + (self.rect.height - scaled_h) // 2
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_w, scaled_h)
        
        # Shadow
        shadow = pygame.Rect(scaled_x + 4, scaled_y + 4, scaled_w, scaled_h)
        pygame.draw.rect(surface, (0, 0, 0), shadow, border_radius=16)
        
        # Card background
        bg_color = CARD_BG if self.available else (40, 40, 50)
        pygame.draw.rect(surface, bg_color, scaled_rect, border_radius=16)
        
        # Hover border
        if self.hover and self.available:
            pygame.draw.rect(surface, self.color, scaled_rect, 3, border_radius=16)
        
        # Color bar at top
        bar_rect = pygame.Rect(scaled_x + 12, scaled_y + 12, scaled_w - 24, 65)
        pygame.draw.rect(surface, self.color, bar_rect, border_radius=10)
        
        # Icon
        icon_font = pygame.font.SysFont("segoeuisymbol", 40)
        icon_surf = icon_font.render(self.icon, True, WHITE)
        icon_rect = icon_surf.get_rect(center=bar_rect.center)
        surface.blit(icon_surf, icon_rect)
        
        # Career name
        name_font = pygame.font.SysFont("arial", 20, bold=True)
        name_surf = name_font.render(self.name, True, WHITE)
        name_rect = name_surf.get_rect(centerx=scaled_rect.centerx, top=scaled_y + 90)
        surface.blit(name_surf, name_rect)
        
        # Status
        if not self.available:
            status_font = pygame.font.SysFont("arial", 12)
            status_surf = status_font.render("Coming Soon", True, TEXT_MUTED)
            status_rect = status_surf.get_rect(centerx=scaled_rect.centerx, bottom=scaled_y + scaled_h - 10)
            surface.blit(status_surf, status_rect)


# ============================================================================
# PROGRESS COMPONENTS
# ============================================================================

class ProgressBar:
    """Animated progress bar."""
    
    def __init__(self, x, y, width, height, max_value=100, color=ACCENT):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_value = max_value
        self.value = 0
        self.display_value = 0
        self.color = color
        self.bg_color = CARD_BG
        self.border_radius = height // 2
    
    def set_value(self, value):
        self.value = max(0, min(value, self.max_value))
    
    def update(self):
        self.display_value += (self.value - self.display_value) * 0.1
    
    def draw(self, surface, label=None):
        self.update()
        
        # Background
        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.bg_color, bg_rect, border_radius=self.border_radius)
        
        # Fill
        fill_width = int((self.display_value / self.max_value) * self.width)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.x, self.y, fill_width, self.height)
            pygame.draw.rect(surface, self.color, fill_rect, border_radius=self.border_radius)
        
        # Label
        if label:
            font = pygame.font.SysFont("arial", self.height - 4, bold=True)
            text_surf = font.render(label, True, WHITE)
            text_rect = text_surf.get_rect(center=bg_rect.center)
            surface.blit(text_surf, text_rect)


class Timer:
    """Visual countdown timer."""
    
    def __init__(self, x, y, radius, duration, color=ACCENT):
        self.x = x
        self.y = y
        self.radius = radius
        self.duration = duration
        self.remaining = duration
        self.color = color
        self.warning_color = DANGER
        self.running = False
    
    def start(self):
        self.running = True
        self.remaining = self.duration
    
    def stop(self):
        self.running = False
    
    def reset(self):
        self.remaining = self.duration
        self.running = False
    
    def update(self, dt):
        if self.running and self.remaining > 0:
            self.remaining -= dt
            if self.remaining < 0:
                self.remaining = 0
    
    def is_finished(self):
        return self.remaining <= 0
    
    def draw(self, surface):
        # Background circle
        pygame.draw.circle(surface, CARD_BG, (self.x, self.y), self.radius)
        
        # Progress arc
        progress = self.remaining / self.duration
        color = self.warning_color if progress < 0.25 else self.color
        
        if progress > 0:
            start_angle = -math.pi / 2
            end_angle = start_angle + (2 * math.pi * progress)
            
            # Draw arc as filled polygon
            points = [(self.x, self.y)]
            for i in range(int(progress * 36) + 1):
                angle = start_angle + (i / 36) * 2 * math.pi * progress
                px = self.x + self.radius * math.cos(angle)
                py = self.y + self.radius * math.sin(angle)
                points.append((px, py))
            
            if len(points) > 2:
                pygame.draw.polygon(surface, color, points)
        
        # Inner circle
        pygame.draw.circle(surface, BACKGROUND, (self.x, self.y), self.radius - 8)
        
        # Time text
        seconds = max(0, int(self.remaining))
        font = pygame.font.SysFont("arial", self.radius // 2, bold=True)
        time_surf = font.render(str(seconds), True, WHITE)
        time_rect = time_surf.get_rect(center=(self.x, self.y))
        surface.blit(time_surf, time_rect)


# ============================================================================
# TEXT UTILITIES
# ============================================================================

def draw_text(screen, text, size, x, y, color=BLACK, font_name="arial", bold=False):
    """Draw centered text."""
    font = pygame.font.SysFont(font_name, size, bold=bold)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    screen.blit(text_surf, text_rect)


def draw_text_left(screen, text, size, x, y, color=BLACK, font_name="arial", bold=False):
    """Draw left-aligned text."""
    font = pygame.font.SysFont(font_name, size, bold=bold)
    text_surf = font.render(text, True, color)
    screen.blit(text_surf, (x, y))


def draw_multiline_text(text, screen, x, y, size, color=BLACK, font_name="arial", line_spacing=5):
    """Draw multiple lines of text."""
    font = pygame.font.SysFont(font_name, size)
    lines = text.split("\n")
    for i, line in enumerate(lines):
        line_surf = font.render(line, True, color)
        screen.blit(line_surf, (x, y + i * (size + line_spacing)))


def draw_wrapped_text(text, screen, x, y, size, color, max_width, font_name="arial", line_spacing=8):
    """Draw text with word wrapping."""
    font = pygame.font.SysFont(font_name, size)
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        if font.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    for i, line in enumerate(lines):
        line_surf = font.render(line, True, color)
        screen.blit(line_surf, (x, y + i * (size + line_spacing)))
    
    return len(lines) * (size + line_spacing)


def draw_lives(screen, lives, max_lives, x, y, heart_size=20, spacing=8, full_color=DANGER, empty_color=TEXT_MUTED):
    """Draw a simple hearts-based lives HUD using a heart character.

    - `x,y` is the starting position (leftmost heart).
    - Uses a bold font heart character for portability.
    """
    try:
        heart_font = pygame.font.SysFont("segoeuisymbol", heart_size, bold=True)
    except Exception:
        heart_font = pygame.font.SysFont("arial", heart_size, bold=True)

    for i in range(max_lives):
        color = full_color if i < lives else empty_color
        heart_surf = heart_font.render("♥", True, color)
        screen.blit(heart_surf, (x + i * (heart_size + spacing), y))


# ============================================================================
# VISUAL EFFECTS
# ============================================================================

class Particle:
    """Simple particle for visual effects."""
    
    def __init__(self, x, y, color, velocity=None, life=1.0, size=4):
        self.x = x
        self.y = y
        self.color = color
        self.vx = velocity[0] if velocity else (pygame.time.get_ticks() % 100 - 50) / 15
        self.vy = velocity[1] if velocity else -2 - (pygame.time.get_ticks() % 50) / 25
        self.life = life
        self.max_life = life
        self.size = size
    
    def update(self, dt):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.15  # Gravity
        self.life -= dt * 2
    
    def draw(self, surface):
        if self.life > 0:
            alpha = self.life / self.max_life
            size = int(self.size * alpha)
            if size > 0:
                pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), size)
    
    def is_alive(self):
        return self.life > 0


class ParticleSystem:
    """Manages multiple particles."""
    
    def __init__(self):
        self.particles = []
    
    def emit(self, x, y, color, count=10):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
    
    def update(self, dt):
        for p in self.particles[:]:
            p.update(dt)
            if not p.is_alive():
                self.particles.remove(p)
    
    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)


class ScreenFlash:
    """Flash effect for feedback."""
    
    def __init__(self):
        self.alpha = 0
        self.color = WHITE
    
    def flash(self, color=WHITE, intensity=100):
        self.color = color
        self.alpha = intensity
    
    def update(self):
        if self.alpha > 0:
            self.alpha -= 8
    
    def draw(self, surface):
        if self.alpha > 0:
            overlay = pygame.Surface(surface.get_size())
            overlay.fill(self.color)
            overlay.set_alpha(self.alpha)
            surface.blit(overlay, (0, 0))


# ============================================================================
# NOTIFICATION SYSTEM
# ============================================================================

class Toast:
    """Pop-up notification."""
    
    def __init__(self, text, duration=2.0, color=ACCENT):
        self.text = text
        self.duration = duration
        self.remaining = duration
        self.color = color
        self.y_offset = 0
        self.target_y = 0
    
    def update(self, dt):
        self.remaining -= dt
        self.y_offset += (self.target_y - self.y_offset) * 0.2
    
    def draw(self, surface, x, y):
        if self.remaining > 0:
            alpha = min(1.0, self.remaining / 0.5)  # Fade out
            
            font = pygame.font.SysFont("arial", 20, bold=True)
            text_surf = font.render(self.text, True, WHITE)
            
            padding = 20
            width = text_surf.get_width() + padding * 2
            height = text_surf.get_height() + padding
            
            rect = pygame.Rect(x - width // 2, y + self.y_offset, width, height)
            pygame.draw.rect(surface, self.color, rect, border_radius=8)
            
            text_rect = text_surf.get_rect(center=rect.center)
            surface.blit(text_surf, text_rect)
    
    def is_alive(self):
        return self.remaining > 0
