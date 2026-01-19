"""
Step Into My Shoes - Color Palette
A cohesive, modern color system for the career simulation game.
"""

# ============================================================================
# CORE PALETTE
# ============================================================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
DARK_GREY = (50, 50, 50)

# ============================================================================
# UI COLORS
# ============================================================================

BACKGROUND = (24, 28, 39)
BACKGROUND_LIGHT = (35, 41, 56)
CARD_BG = (44, 52, 71)
CARD_BG_HOVER = (55, 65, 88)

# ============================================================================
# PRIMARY COLORS
# ============================================================================

PRIMARY = (74, 144, 226)
PRIMARY_LIGHT = (100, 165, 240)
PRIMARY_DARK = (55, 115, 195)

SECONDARY = (52, 152, 219)
ACCENT = (46, 204, 113)
ACCENT_LIGHT = (75, 220, 140)

# ============================================================================
# STATUS COLORS
# ============================================================================

SUCCESS = (46, 204, 113)
SUCCESS_LIGHT = (75, 220, 140)
WARNING = (241, 196, 15)
WARNING_LIGHT = (245, 210, 55)
DANGER = (231, 76, 60)
DANGER_LIGHT = (240, 110, 95)
ERROR = (255, 100, 100)

# ============================================================================
# TEXT COLORS
# ============================================================================

TEXT_PRIMARY = WHITE
TEXT_SECONDARY = (189, 195, 199)
TEXT_MUTED = (127, 140, 152)
TEXT_MAIN = BLACK
BUTTON_TEXT = BLACK

# ============================================================================
# BUTTON COLORS
# ============================================================================

BUTTON_BG = (180, 180, 250)
BUTTON_HOVER = (120, 120, 220)
HIGHLIGHT = (100, 200, 100)

# ============================================================================
# CAREER-SPECIFIC COLORS
# ============================================================================

DOCTOR_PRIMARY = (231, 76, 60)
DOCTOR_SECONDARY = (192, 57, 43)
DOCTOR_ACCENT = (255, 107, 107)

LAWYER_PRIMARY = (52, 152, 219)
LAWYER_SECONDARY = (41, 128, 185)
LAWYER_ACCENT = (100, 180, 240)

INFLUENCER_PRIMARY = (155, 89, 182)
INFLUENCER_SECONDARY = (142, 68, 173)
INFLUENCER_ACCENT = (190, 120, 220)

POLITICIAN_PRIMARY = (46, 204, 113)
POLITICIAN_SECONDARY = (39, 174, 96)
POLITICIAN_ACCENT = (88, 214, 141)

ENGINEER_PRIMARY = (241, 196, 15)
ENGINEER_SECONDARY = (243, 156, 18)
ENGINEER_ACCENT = (247, 220, 111)

# ============================================================================
# GRADIENT HELPERS
# ============================================================================

def lerp_color(color1, color2, t):
    """Linear interpolation between two colors."""
    return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))

def darken(color, amount=0.2):
    """Darken a color by a percentage."""
    return tuple(max(0, int(c * (1 - amount))) for c in color)

def lighten(color, amount=0.2):
    """Lighten a color by a percentage."""
    return tuple(min(255, int(c + (255 - c) * amount)) for c in color)
