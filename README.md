# Step Into My Shoes

## Career Exploration Game

**FBLA Computer Game & Simulation Competition Entry**

---

## Overview

Step Into My Shoes is an educational career exploration game where players experience different careers through interactive mini-worlds. Each career features unique gameplay mechanics that simulate real job tasks, teaching valuable skills and giving players a taste of what each profession is really like.

## Features

###  Five Unique Career Worlds

1. **Doctor World** - Diagnose patients under time pressure
   - Triage incoming patients with various symptoms
   - Match symptoms to correct diagnoses
   - Build combos for bonus points
   - *Skills taught: Quick decision-making, pattern recognition, working under pressure*

2. **Lawyer World** - Find contradictions in witness statements
   - Analyze multiple witness testimonies
   - Identify logical inconsistencies
   - Build your case by finding the truth
   - *Skills taught: Critical thinking, logical reasoning, attention to detail*

3. **Influencer World** - Master timing to create viral content
   - Hit timing bars perfectly to record content
   - Maintain energy while creating videos
   - Build combos for maximum engagement
   - *Skills taught: Timing, rhythm, consistency, performance under pressure*

4. **Politician World** - Manage public approval through decisions
   - Respond to political issues and crises
   - Balance competing interests
   - Maintain public trust
   - *Skills taught: Strategic thinking, communication, decision-making*

5. **Engineer World** - Solve circuit puzzles with spatial reasoning
   - Place components in correct positions
   - Complete circuits under time pressure
   - Think systematically to solve problems
   - *Skills taught: Spatial reasoning, problem-solving, systematic thinking*

### Dynamic AI Backstory System

Every playthrough features a unique, procedurally-generated backstory that immerses players in their chosen career. The system uses:
- Randomized character names and personalities
- Career-specific scenarios and challenges
- Varied mentors and workplace settings
- Dynamic difficulty modifiers

###  Modern UI/UX

- Smooth animations and transitions
- Particle effects for visual feedback
- Consistent color theming per career
- Responsive button hover states
- Clear progress indicators

## Requirements

- Python 3.8 or higher
- Pygame 2.0 or higher

## Installation

1. Ensure Python is installed on your system
2. Install Pygame:
   ```
   pip install pygame
   ```
3. Run the game:
   ```
   python main.py
   ```

## Controls

### General
- **Mouse** - Navigate menus, select options
- **ESC** - Return to previous screen

### In Mini-Games
- **↑/↓ Arrows** - Navigate options
- **Enter** - Confirm selection
- **1-4 Number Keys** - Quick select options
- **Space** - Action key (varies by game)

## Technical Architecture

```
step_into_my_shoes/
├── main.py                 # Main menu, career selector, scene manager
├── engine/
│   ├── __init__.py
│   ├── core.py             # Scene manager
│   ├── ui.py               # UI components (buttons, cards, progress bars)
│   ├── colors.py           # Global color definitions
│   ├── backstory_ai.py     # Dynamic story generator
│   ├── world.py            # Base world class
│   └── player.py           # Player object
└── worlds/
    ├── __init__.py
    ├── doctor.py           # Doctor mini-game
    ├── lawyer.py           # Lawyer mini-game
    ├── influencer.py       # Influencer mini-game
    ├── politician.py       # Politician mini-game
    └── engineer.py         # Engineer mini-game
```

## Educational Value

Step Into My Shoes teaches players about:
- **Soft Skills** - Communication, decision-making, time management
- **Job Requirements** - What each career actually involves day-to-day
- **Pressure Management** - Working effectively under deadlines
- **Critical Thinking** - Analyzing information and making decisions
- **Career Exploration** - Exposure to diverse career paths

## Competition Compliance

This game meets all FBLA Computer Game & Simulation requirements:
- ✅ Runs on Windows (tested on Windows 10/11)
- ✅ Secure (no networking, no external API calls)
- ✅ No game-breaking bugs
- ✅ Clean, modular architecture
- ✅ Educational content related to careers
- ✅ Original creative work

## Credits

Created for the FBLA Computer Game & Simulation Competition

---

*"Step into the shoes of professionals and discover your future career!"*
