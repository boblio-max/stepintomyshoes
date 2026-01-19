"""
Step Into My Shoes - Engineer World
Solve puzzles by placing components correctly under time pressure.
Teaches: Spatial reasoning, problem-solving, systematic thinking.
"""

import pygame
import random
from engine.colors import (
    BACKGROUND, WHITE, BLACK, ENGINEER_PRIMARY, ENGINEER_SECONDARY,
    ENGINEER_ACCENT, SUCCESS, DANGER, WARNING, TEXT_SECONDARY, CARD_BG,
    ACCENT, TEXT_MUTED, PRIMARY
)
from engine.ui import (
    draw_text, draw_text_left, draw_wrapped_text, ModernButton, ParticleSystem, ScreenFlash,
    ProgressBar
)
from engine.backstory_ai import get_performance_feedback, get_career_lesson

pygame.init()

WIDTH, HEIGHT = 900, 600

# Circuit component definitions
COMPONENTS = {
    "resistor": {"symbol": "R", "color": (200, 100, 50), "name": "Resistor"},
    "capacitor": {"symbol": "C", "color": (50, 150, 200), "name": "Capacitor"},
    "inductor": {"symbol": "L", "color": (100, 200, 100), "name": "Inductor"},
    "diode": {"symbol": "D", "color": (200, 50, 150), "name": "Diode"},
    "transistor": {"symbol": "T", "color": (150, 100, 200), "name": "Transistor"},
    "led": {"symbol": "★", "color": (255, 200, 50), "name": "LED"},
}

# Puzzle definitions
PUZZLES = [
    {
        "name": "Power Supply Filter",
        "description": "Place components to filter the power supply",
        "grid_size": (4, 3),
        "targets": [(0, 1), (2, 0), (3, 2)],
        "components": ["capacitor", "resistor", "diode"],
        "time_limit": 20
    },
    {
        "name": "LED Driver Circuit",
        "description": "Build a circuit to control the LED brightness",
        "grid_size": (4, 3),
        "targets": [(1, 0), (2, 1), (3, 2)],
        "components": ["resistor", "transistor", "led"],
        "time_limit": 25
    },
    {
        "name": "Signal Amplifier",
        "description": "Amplify the input signal with this configuration",
        "grid_size": (5, 3),
        "targets": [(0, 1), (2, 0), (2, 2), (4, 1)],
        "components": ["resistor", "capacitor", "transistor", "resistor"],
        "time_limit": 30
    },
    {
        "name": "Oscillator Circuit",
        "description": "Create a frequency generator",
        "grid_size": (4, 4),
        "targets": [(0, 0), (1, 2), (2, 1), (3, 3)],
        "components": ["inductor", "capacitor", "resistor", "transistor"],
        "time_limit": 30
    },
    {
        "name": "Voltage Regulator",
        "description": "Stabilize the output voltage",
        "grid_size": (5, 3),
        "targets": [(0, 0), (1, 1), (3, 1), (4, 2)],
        "components": ["diode", "capacitor", "transistor", "resistor"],
        "time_limit": 25
    },
    {
        "name": "Logic Gate",
        "description": "Build a basic AND gate circuit",
        "grid_size": (4, 4),
        "targets": [(0, 1), (1, 0), (1, 2), (2, 1), (3, 1)],
        "components": ["diode", "diode", "resistor", "resistor", "led"],
        "time_limit": 35
    }
]


class GridCell:
    """A single cell in the circuit grid."""
    
    def __init__(self, row, col, cell_size, offset_x, offset_y):
        self.row = row
        self.col = col
        self.cell_size = cell_size
        self.x = offset_x + col * cell_size
        self.y = offset_y + row * cell_size
        self.component = None
        self.is_target = False
        self.is_correct = False
        self.expected_component = None
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
    
    def draw(self, screen, selected=False):
        rect = self.get_rect()
        
        # Background
        if self.is_target:
            if self.is_correct:
                bg_color = (40, 80, 40)
            else:
                bg_color = (60, 50, 40)
        else:
            bg_color = CARD_BG
        
        pygame.draw.rect(screen, bg_color, rect, border_radius=4)
        
        # Border
        border_color = ENGINEER_ACCENT if selected else TEXT_MUTED
        pygame.draw.rect(screen, border_color, rect, 2, border_radius=4)
        
        # Target indicator
        if self.is_target and not self.component:
            pygame.draw.circle(screen, ENGINEER_ACCENT, rect.center, 8, 2)
        
        # Component
        if self.component:
            comp_data = COMPONENTS.get(self.component, {})
            symbol = comp_data.get("symbol", "?")
            color = comp_data.get("color", WHITE)
            
            font = pygame.font.SysFont("arial", 24, bold=True)
            text = font.render(symbol, True, color)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)


class EngineerWorld:
    """
    Engineer Career Mini-Game
    Players place components in the correct positions to complete circuits.
    """
    
    def __init__(self, story_package=None):
        self.story = story_package or {
            "intro": "Welcome to the Engineering Lab!\n\nYou must complete circuit designs by placing components in the correct positions.\n\nSelect components from your inventory and place them on target cells.\nWork quickly but accurately!"
        }
        self.state = "intro"
        self.score = 0
        self.total_puzzles = 4
        self.current_puzzle_index = 0
        self.puzzles = []
        self.current_puzzle = None
        
        # Grid state
        self.grid = []
        self.grid_offset_x = 200
        self.grid_offset_y = 150
        self.cell_size = 80
        
        # Inventory
        self.inventory = []
        self.selected_component = None
        self.selected_cell = None
        
        # Timer
        self.time_remaining = 0
        
        # Stats
        self.perfect_solves = 0
        self.total_placed = 0
        self.errors = 0
        
        # Visual effects
        self.particles = ParticleSystem()
        self.flash = ScreenFlash()
        self.feedback_text = ""
        self.feedback_timer = 0
        
        # UI elements
        self.start_btn = ModernButton(350, 480, 200, 55, "Start Project",
                                       ENGINEER_PRIMARY, ENGINEER_SECONDARY)
        self.submit_btn = ModernButton(700, 400, 150, 50, "Submit",
                                        ENGINEER_PRIMARY, ENGINEER_SECONDARY)
        self.next_btn = ModernButton(350, 500, 200, 55, "Next Puzzle",
                                      ENGINEER_PRIMARY, ENGINEER_SECONDARY)
        self.finish_btn = ModernButton(350, 500, 200, 55, "View Report",
                                        ENGINEER_PRIMARY, ENGINEER_SECONDARY)
        self.back_btn = ModernButton(350, 500, 200, 55, "Return to Hub",
                                      CARD_BG, ENGINEER_PRIMARY)
        
        self.inventory_buttons = []
        self.generate_puzzles()
        
        self.clock = pygame.time.Clock()
        self.scene_manager = None
    
    def generate_puzzles(self):
        """Generate random puzzles."""
        puzzles = random.sample(PUZZLES, min(self.total_puzzles, len(PUZZLES)))
        self.puzzles = puzzles
        if self.puzzles:
            self.load_puzzle(0)
    
    def load_puzzle(self, index):
        """Load a puzzle and set up the grid."""
        if index < len(self.puzzles):
            self.current_puzzle = self.puzzles[index]
            self.current_puzzle_index = index
            self.time_remaining = self.current_puzzle["time_limit"]
            self.selected_component = None
            self.selected_cell = None
            
            # Create grid
            cols, rows = self.current_puzzle["grid_size"]
            self.grid = []
            
            # Center the grid
            total_width = cols * self.cell_size
            total_height = rows * self.cell_size
            self.grid_offset_x = (WIDTH - total_width) // 2
            self.grid_offset_y = 160
            
            for row in range(rows):
                grid_row = []
                for col in range(cols):
                    cell = GridCell(row, col, self.cell_size, 
                                   self.grid_offset_x, self.grid_offset_y)
                    grid_row.append(cell)
                self.grid.append(grid_row)
            
            # Set targets and expected components
            targets = self.current_puzzle["targets"]
            components = self.current_puzzle["components"]
            
            for i, (col, row) in enumerate(targets):
                if row < len(self.grid) and col < len(self.grid[0]):
                    self.grid[row][col].is_target = True
                    if i < len(components):
                        self.grid[row][col].expected_component = components[i]
            
            # Set up inventory
            self.inventory = list(components)
            random.shuffle(self.inventory)
            
            # Create inventory buttons
            self.inventory_buttons = []
            inv_x = 50
            inv_y = 400
            for i, comp in enumerate(self.inventory):
                btn_y = inv_y + i * 45
                self.inventory_buttons.append({
                    "component": comp,
                    "rect": pygame.Rect(inv_x, btn_y, 120, 40),
                    "used": False
                })
    
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
        mx, my = event.pos
        
        if self.state == "intro":
            if self.start_btn.is_clicked(event):
                self.state = "gameplay"
        
        elif self.state == "gameplay":
            # Check inventory clicks
            for inv_btn in self.inventory_buttons:
                if inv_btn["rect"].collidepoint(mx, my) and not inv_btn["used"]:
                    self.selected_component = inv_btn["component"]
                    self.selected_cell = None
                    break
            
            # Check grid clicks
            for row in self.grid:
                for cell in row:
                    if cell.get_rect().collidepoint(mx, my):
                        if self.selected_component and cell.is_target and not cell.component:
                            # Place component
                            cell.component = self.selected_component
                            self.total_placed += 1
                            
                            # Mark inventory as used
                            for inv_btn in self.inventory_buttons:
                                if inv_btn["component"] == self.selected_component and not inv_btn["used"]:
                                    inv_btn["used"] = True
                                    break
                            
                            self.selected_component = None
                            
                            # Check if correct
                            if cell.component == cell.expected_component:
                                cell.is_correct = True
                                self.particles.emit(cell.x + self.cell_size // 2,
                                                   cell.y + self.cell_size // 2,
                                                   SUCCESS, 10)
                            
                            # Check if puzzle is complete
                            if self.check_puzzle_complete():
                                self.complete_puzzle()
                        elif cell.component:
                            # Remove component
                            removed = cell.component
                            cell.component = None
                            cell.is_correct = False
                            
                            # Return to inventory
                            for inv_btn in self.inventory_buttons:
                                if inv_btn["component"] == removed and inv_btn["used"]:
                                    inv_btn["used"] = False
                                    break
                        break
            
            # Check submit button
            if self.submit_btn.is_clicked(event):
                self.complete_puzzle()
        
        elif self.state == "puzzle_complete":
            if self.next_btn.is_clicked(event) or self.finish_btn.is_clicked(event):
                if self.current_puzzle_index < len(self.puzzles) - 1:
                    self.load_puzzle(self.current_puzzle_index + 1)
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
            if event.key == pygame.K_ESCAPE:
                self.selected_component = None
            elif event.key == pygame.K_RETURN:
                self.complete_puzzle()
    
    def check_puzzle_complete(self):
        """Check if all targets have correct components."""
        for row in self.grid:
            for cell in row:
                if cell.is_target:
                    if not cell.component or cell.component != cell.expected_component:
                        return False
        return True
    
    def complete_puzzle(self):
        """Complete the current puzzle and calculate score."""
        correct = 0
        total = 0
        
        for row in self.grid:
            for cell in row:
                if cell.is_target:
                    total += 1
                    if cell.component == cell.expected_component:
                        correct += 1
                    elif cell.component:
                        self.errors += 1
        
        # Calculate score
        time_bonus = int(self.time_remaining * 5)
        accuracy = correct / total if total > 0 else 0
        base_score = int(accuracy * 200)
        
        puzzle_score = base_score + time_bonus
        self.score += puzzle_score
        
        if accuracy == 1.0:
            self.perfect_solves += 1
            self.feedback_text = f"Perfect! +{puzzle_score} pts"
            self.flash.flash(SUCCESS, 80)
            self.particles.emit(WIDTH // 2, HEIGHT // 2, SUCCESS, 40)
        elif accuracy >= 0.5:
            self.feedback_text = f"Good! +{puzzle_score} pts"
            self.flash.flash(ACCENT, 50)
        else:
            self.feedback_text = f"Needs work! +{puzzle_score} pts"
        
        self.feedback_timer = 2.0
        self.state = "puzzle_complete"
    
    def update(self, dt):
        """Update game state."""
        self.particles.update(dt)
        self.flash.update()
        
        if self.feedback_timer > 0:
            self.feedback_timer -= dt
        
        if self.state == "gameplay":
            self.time_remaining -= dt
            if self.time_remaining <= 0:
                self.time_remaining = 0
                self.complete_puzzle()
    
    def draw(self, screen):
        """Draw current state."""
        screen.fill(BACKGROUND)
        
        if self.state == "intro":
            self.draw_intro(screen)
        elif self.state == "gameplay":
            self.draw_gameplay(screen)
        elif self.state == "puzzle_complete":
            self.draw_puzzle_complete(screen)
        elif self.state == "results":
            self.draw_results(screen)
        
        self.particles.draw(screen)
        self.flash.draw(screen)
    
    def draw_intro(self, screen):
        """Draw intro screen."""
        # Header
        header_rect = pygame.Rect(0, 0, WIDTH, 100)
        pygame.draw.rect(screen, ENGINEER_PRIMARY, header_rect)
        draw_text(screen, "Engineer World", 42, WIDTH // 2, 35, WHITE, bold=True)
        draw_text(screen, "Circuit Design Lab", 18, WIDTH // 2, 72, TEXT_SECONDARY)
        
        # Intro text
        draw_wrapped_text(self.story["intro"], screen, 100, 140, 22, WHITE, 700)
        
        # Instructions
        draw_text(screen, "How to Play:", 24, WIDTH // 2, 310, ENGINEER_ACCENT, bold=True)
        instructions = [
            "Click a component from your inventory to select it",
            "Click on a target cell (marked with circles) to place it",
            "Match each component to its correct position",
            "Complete the circuit before time runs out!"
        ]
        for i, instruction in enumerate(instructions):
            draw_text_left(screen, f"• {instruction}", 18, 180, 345 + i * 28, TEXT_SECONDARY)
        
        self.start_btn.draw(screen)
    
    def draw_gameplay(self, screen):
        """Draw gameplay screen."""
        # Header
        header_rect = pygame.Rect(0, 0, WIDTH, 60)
        pygame.draw.rect(screen, ENGINEER_PRIMARY, header_rect)
        
        if self.current_puzzle:
            draw_text(screen, f"Project: {self.current_puzzle['name']}", 
                     24, WIDTH // 2, 20, WHITE, bold=True)
            draw_text(screen, self.current_puzzle['description'], 
                     14, WIDTH // 2, 45, TEXT_SECONDARY)
        
        # Timer
        timer_color = DANGER if self.time_remaining < 5 else (
            WARNING if self.time_remaining < 10 else SUCCESS
        )
        draw_text(screen, f"Time: {int(self.time_remaining)}s", 
                 20, WIDTH - 80, 85, timer_color, bold=True)
        
        # Score
        draw_text(screen, f"Score: {self.score}", 18, 80, 85, WHITE)
        
        # Progress
        draw_text(screen, f"Puzzle {self.current_puzzle_index + 1}/{len(self.puzzles)}", 
                 16, WIDTH // 2, 85, TEXT_SECONDARY)
        
        # Puzzle description
        draw_text(screen, "Place components on target cells:", 16, WIDTH // 2, 120, ENGINEER_ACCENT)
        
        # Draw grid
        for row in self.grid:
            for cell in row:
                is_selected = (self.selected_cell == cell)
                cell.draw(screen, selected=is_selected)
        
        # Inventory panel
        inv_panel = pygame.Rect(30, 380, 160, 200)
        pygame.draw.rect(screen, CARD_BG, inv_panel, border_radius=10)
        draw_text(screen, "Components", 16, 110, 395, WHITE, bold=True)
        
        for inv_btn in self.inventory_buttons:
            comp = inv_btn["component"]
            rect = inv_btn["rect"]
            
            if inv_btn["used"]:
                color = TEXT_MUTED
                bg = BACKGROUND
            elif comp == self.selected_component:
                color = WHITE
                bg = ENGINEER_ACCENT
            else:
                color = WHITE
                bg = CARD_BG
            
            pygame.draw.rect(screen, bg, rect, border_radius=6)
            pygame.draw.rect(screen, ENGINEER_ACCENT if comp == self.selected_component else TEXT_MUTED, 
                           rect, 2, border_radius=6)
            
            comp_data = COMPONENTS.get(comp, {})
            name = comp_data.get("name", comp)
            symbol = comp_data.get("symbol", "?")
            
            draw_text(screen, f"{symbol} {name}", 14, rect.centerx, rect.centery, color)
        
        # Instructions
        if self.selected_component:
            draw_text(screen, f"Selected: {COMPONENTS.get(self.selected_component, {}).get('name', '?')}", 
                     16, WIDTH // 2, HEIGHT - 50, ENGINEER_ACCENT)
            draw_text(screen, "Click a target cell to place, or click again to remove", 
                     14, WIDTH // 2, HEIGHT - 25, TEXT_MUTED)
        else:
            draw_text(screen, "Click a component from inventory to select", 
                     14, WIDTH // 2, HEIGHT - 25, TEXT_MUTED)
        
        # Submit button
        self.submit_btn.draw(screen)
    
    def draw_puzzle_complete(self, screen):
        """Draw puzzle completion screen."""
        # Keep gameplay visible
        self.draw_gameplay(screen)
        
        # Overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))
        
        # Results box
        box_rect = pygame.Rect(200, 180, 500, 240)
        pygame.draw.rect(screen, CARD_BG, box_rect, border_radius=16)
        
        is_perfect = all(
            cell.is_correct for row in self.grid for cell in row if cell.is_target
        )
        border_color = SUCCESS if is_perfect else ENGINEER_ACCENT
        pygame.draw.rect(screen, border_color, box_rect, 3, border_radius=16)
        
        if is_perfect:
            draw_text(screen, "Circuit Complete!", 32, WIDTH // 2, 220, SUCCESS, bold=True)
        else:
            draw_text(screen, "Project Submitted", 32, WIDTH // 2, 220, ENGINEER_ACCENT, bold=True)
        
        draw_text(screen, self.feedback_text, 22, WIDTH // 2, 270, WHITE)
        
        # Stats for this puzzle
        correct = sum(1 for row in self.grid for cell in row 
                     if cell.is_target and cell.is_correct)
        total = sum(1 for row in self.grid for cell in row if cell.is_target)
        
        draw_text(screen, f"Accuracy: {correct}/{total} components", 
                 18, WIDTH // 2, 320, TEXT_SECONDARY)
        
        if self.current_puzzle_index < len(self.puzzles) - 1:
            self.next_btn.draw(screen)
        else:
            self.finish_btn.draw(screen)
    
    def draw_results(self, screen):
        """Draw final results screen."""
        # Header
        header_rect = pygame.Rect(0, 0, WIDTH, 100)
        pygame.draw.rect(screen, ENGINEER_PRIMARY, header_rect)
        draw_text(screen, "Project Complete!", 42, WIDTH // 2, 35, WHITE, bold=True)
        draw_text(screen, "Engineering Performance Review", 18, WIDTH // 2, 72, TEXT_SECONDARY)
        
        # Stats
        stats_y = 130
        draw_text(screen, f"Total Score: {self.score}", 
                 32, WIDTH // 2, stats_y, WHITE, bold=True)
        draw_text(screen, f"Perfect Circuits: {self.perfect_solves}/{len(self.puzzles)}", 
                 24, WIDTH // 2, stats_y + 45, ENGINEER_ACCENT)
        draw_text(screen, f"Components Placed: {self.total_placed}", 
                 20, WIDTH // 2, stats_y + 85, TEXT_SECONDARY)
        
        # Grade
        perfect_pct = (self.perfect_solves / len(self.puzzles)) * 100 if self.puzzles else 0
        
        if perfect_pct >= 75:
            grade = "Master Engineer"
            grade_color = SUCCESS
        elif perfect_pct >= 50:
            grade = "Senior Engineer"
            grade_color = ACCENT
        elif perfect_pct >= 25:
            grade = "Junior Engineer"
            grade_color = WARNING
        else:
            grade = "Engineering Intern"
            grade_color = DANGER
        
        draw_text(screen, grade, 36, WIDTH // 2, stats_y + 145, grade_color, bold=True)
        
        # Feedback
        feedback = get_performance_feedback("Engineer", self.perfect_solves, len(self.puzzles))
        draw_wrapped_text(feedback, screen, 100, stats_y + 200, 18, TEXT_SECONDARY, 700)
        
        # Real-world lesson
        lesson = get_career_lesson("Engineer")
        draw_text(screen, "What Real Engineers Do:", 20, WIDTH // 2, stats_y + 280, 
                 ENGINEER_ACCENT, bold=True)
        draw_wrapped_text(lesson, screen, 100, stats_y + 310, 16, TEXT_MUTED, 700)
        
        self.back_btn.draw(screen)
