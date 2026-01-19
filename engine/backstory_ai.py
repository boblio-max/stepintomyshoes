"""
Step Into My Shoes - Dynamic AI Story Generator
Generates unique, engaging backstories for each career world.
"""

import random

# ============================================================================
# CHARACTER NAME GENERATORS
# ============================================================================

FIRST_NAMES = [
    "Alex", "Jordan", "Morgan", "Taylor", "Casey", "Riley", "Avery", "Quinn",
    "Skyler", "Parker", "Drew", "Cameron", "Reese", "Dakota", "Finley", "Sage",
    "Emery", "Rowan", "Phoenix", "Blake", "Jamie", "Kendall", "River", "Hayden"
]

LAST_NAMES = [
    "Chen", "Ramirez", "Patel", "Johnson", "Williams", "Garcia", "Martinez",
    "Thompson", "Anderson", "Rodriguez", "Lee", "Walker", "Hall", "Young",
    "King", "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Nelson"
]

# ============================================================================
# PERSONALITY TRAITS
# ============================================================================

TRAITS = {
    "positive": [
        "calm under pressure", "quick-thinking", "naturally empathetic",
        "remarkably focused", "endlessly curious", "fiercely determined",
        "incredibly adaptable", "detail-oriented", "naturally charismatic",
        "refreshingly honest", "deeply analytical", "creatively brilliant"
    ],
    "challenges": [
        "sometimes too perfectionist", "occasionally impatient",
        "prone to overthinking", "can be too trusting", "struggles with delegation",
        "sometimes too ambitious", "occasionally stubborn", "can be overly cautious"
    ]
}

# ============================================================================
# CAREER TEMPLATES - RICH NARRATIVE DATA
# ============================================================================

CAREER_TEMPLATES = {
    "Doctor": {
        "titles": [
            "Emergency Physician", "Trauma Surgeon", "General Practitioner",
            "Pediatric Specialist", "Cardiologist", "Neurologist"
        ],
        "workplaces": [
            "City General Hospital's busy ER",
            "the renowned Mercy Medical Center",
            "a state-of-the-art trauma unit",
            "the community health clinic downtown",
            "St. Elizabeth's renowned cardiac wing"
        ],
        "scenarios": [
            {
                "setup": "Multiple ambulances arrive simultaneously after a highway pileup.",
                "challenge": "You must triage patients quickly—every second counts.",
                "stakes": "Lives hang in the balance as you prioritize who needs help first."
            },
            {
                "setup": "A mysterious illness spreads through a local school.",
                "challenge": "Students show varied symptoms and you must identify the cause.",
                "stakes": "The health of dozens of children depends on your diagnosis."
            },
            {
                "setup": "The ER is overwhelmed during a severe flu outbreak.",
                "challenge": "Resources are limited and patients keep arriving.",
                "stakes": "Your decisions determine who gets treated immediately."
            },
            {
                "setup": "A VIP patient arrives with conflicting medical records.",
                "challenge": "You must piece together their history while treating symptoms.",
                "stakes": "A wrong diagnosis could be catastrophic."
            }
        ],
        "mentors": [
            "Dr. Helena Cross, a 30-year ER veteran",
            "Dr. Marcus Webb, the no-nonsense Chief of Medicine",
            "Dr. Yuki Tanaka, a brilliant diagnostician",
            "Dr. Samuel Brooks, a compassionate senior physician"
        ],
        "skills_taught": [
            "rapid patient assessment", "critical decision-making",
            "working under extreme pressure", "medical prioritization"
        ],
        "real_world_connection": "Real doctors in emergency rooms make split-second decisions that save lives every day. They combine medical knowledge with quick thinking and emotional resilience."
    },
    
    "Lawyer": {
        "titles": [
            "Defense Attorney", "Prosecutor", "Corporate Litigator",
            "Civil Rights Lawyer", "Public Defender", "Legal Counsel"
        ],
        "workplaces": [
            "the downtown Superior Court",
            "a prestigious law firm on Main Street",
            "the District Attorney's office",
            "the Public Defender's courthouse office",
            "a renowned civil rights legal center"
        ],
        "scenarios": [
            {
                "setup": "A high-profile case lands on your desk with contradicting testimonies.",
                "challenge": "You must find the truth hidden in layers of statements.",
                "stakes": "An innocent person's freedom depends on your analysis."
            },
            {
                "setup": "Key evidence emerges hours before trial begins.",
                "challenge": "You must quickly understand its implications and adapt.",
                "stakes": "The outcome of the case hangs on your ability to think fast."
            },
            {
                "setup": "The opposing counsel presents a surprise witness.",
                "challenge": "You must cross-examine them effectively despite no preparation.",
                "stakes": "Your client's case could crumble without a strong response."
            },
            {
                "setup": "Multiple witnesses give conflicting accounts of the same event.",
                "challenge": "You must identify who's telling the truth.",
                "stakes": "Justice itself depends on finding the inconsistencies."
            }
        ],
        "mentors": [
            "Judge Patricia Monroe, known for her sharp legal mind",
            "Attorney David Park, an undefeated trial lawyer",
            "Sarah Mitchell, a legendary defense strategist",
            "Commissioner James Blake, a veteran of complex cases"
        ],
        "skills_taught": [
            "logical reasoning", "finding contradictions",
            "persuasive argumentation", "critical thinking"
        ],
        "real_world_connection": "Real lawyers analyze evidence, detect inconsistencies, and build logical arguments. They must think critically and communicate persuasively to seek justice."
    },
    
    "Influencer": {
        "titles": [
            "Content Creator", "Social Media Star", "Digital Storyteller",
            "Brand Ambassador", "Lifestyle Vlogger", "Creative Director"
        ],
        "workplaces": [
            "a trendy downtown content studio",
            "a high-tech streaming setup",
            "the buzzing social media agency HQ",
            "a creative co-working space",
            "your personalized home studio"
        ],
        "scenarios": [
            {
                "setup": "A major brand offers you a sponsorship deal—but there's a catch.",
                "challenge": "You must create perfect content under tight time pressure.",
                "stakes": "This could be your big break or a missed opportunity."
            },
            {
                "setup": "You're going live for a product launch with millions watching.",
                "challenge": "Everything must be timed perfectly—lighting, audio, and delivery.",
                "stakes": "Your reputation and future deals depend on this performance."
            },
            {
                "setup": "A viral trend is sweeping social media and you need to capitalize.",
                "challenge": "You must create engaging content that stands out from the crowd.",
                "stakes": "Missing this wave could set your growth back months."
            },
            {
                "setup": "Your latest video is getting negative comments despite your effort.",
                "challenge": "You must adapt your style while staying authentic.",
                "stakes": "Your audience loyalty is being tested."
            }
        ],
        "mentors": [
            "Maya Sterling, a 10-million follower lifestyle guru",
            "Alex Zhang, a viral video mastermind",
            "Jasmine Cole, a brand partnership expert",
            "Derek Foster, a legendary content strategist"
        ],
        "skills_taught": [
            "timing and rhythm", "performance under pressure",
            "creative consistency", "audience engagement"
        ],
        "real_world_connection": "Real content creators must master timing, maintain energy, and consistently deliver quality. They blend creativity with business sense to build their personal brand."
    },
    
    "Politician": {
        "titles": [
            "City Council Member", "State Representative", "Campaign Manager",
            "Policy Advisor", "Mayor's Chief of Staff", "Community Organizer"
        ],
        "workplaces": [
            "City Hall's council chambers",
            "a bustling campaign headquarters",
            "the state capitol building",
            "a packed community town hall",
            "the mayor's executive office"
        ],
        "scenarios": [
            {
                "setup": "A controversial policy decision divides your constituents.",
                "challenge": "You must address concerns while staying true to your values.",
                "stakes": "Public trust is on the line with every word you speak."
            },
            {
                "setup": "Breaking news hits during a live press conference.",
                "challenge": "You must respond thoughtfully without all the facts.",
                "stakes": "Your response will be analyzed and quoted for days."
            },
            {
                "setup": "A rival politician spreads misleading information about you.",
                "challenge": "You must counter the narrative without appearing defensive.",
                "stakes": "Your approval rating hangs in the balance."
            },
            {
                "setup": "Budget cuts force you to choose between popular programs.",
                "challenge": "You must make tough choices and explain them to the public.",
                "stakes": "Communities depend on your fair and wise decision-making."
            }
        ],
        "mentors": [
            "Senator Margaret Hayes, a three-term political veteran",
            "Governor Robert Chen, known for crisis management",
            "Diana Okoye, a grassroots organizing legend",
            "Commissioner Michael Torres, a master negotiator"
        ],
        "skills_taught": [
            "strategic communication", "public relations",
            "crisis management", "balancing competing interests"
        ],
        "real_world_connection": "Real politicians must communicate effectively, manage public perception, and make decisions that affect thousands. They balance idealism with practical governance."
    },
    
    "Engineer": {
        "titles": [
            "Systems Engineer", "Robotics Specialist", "Civil Engineer",
            "Software Developer", "Aerospace Engineer", "Mechanical Designer"
        ],
        "workplaces": [
            "a cutting-edge robotics laboratory",
            "the R&D floor of a tech giant",
            "an innovative startup workspace",
            "a major construction engineering firm",
            "the prototype testing facility"
        ],
        "scenarios": [
            {
                "setup": "The prototype fails testing hours before the client demo.",
                "challenge": "You must diagnose the problem and implement a fix quickly.",
                "stakes": "A million-dollar contract depends on your solution."
            },
            {
                "setup": "A critical component is unavailable due to supply chain issues.",
                "challenge": "You must redesign part of the system with what you have.",
                "stakes": "The project deadline cannot be moved."
            },
            {
                "setup": "Multiple systems need to integrate, but they're not compatible.",
                "challenge": "You must find a creative solution to connect everything.",
                "stakes": "The entire project depends on making these pieces work together."
            },
            {
                "setup": "User testing reveals the design is confusing for non-engineers.",
                "challenge": "You must simplify without sacrificing functionality.",
                "stakes": "The product's success depends on being user-friendly."
            }
        ],
        "mentors": [
            "Dr. Aisha Rahman, a systems integration genius",
            "Chief Engineer Victor Santos, a 25-year industry veteran",
            "Professor Lin Wei, an innovation thought leader",
            "Director Sarah Kowalski, a robotics pioneer"
        ],
        "skills_taught": [
            "spatial reasoning", "systematic problem-solving",
            "iterative design thinking", "working under constraints"
        ],
        "real_world_connection": "Real engineers solve complex puzzles daily, balancing constraints of time, resources, and physics. They turn abstract problems into working solutions."
    }
}

# ============================================================================
# STORY GENERATION ENGINE
# ============================================================================

def generate_character_name():
    """Generate a random full name."""
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def generate_backstory(career_name, difficulty="normal"):
    """
    Generate a rich, dynamic backstory for a career world.
    
    Args:
        career_name: The career type (Doctor, Lawyer, etc.)
        difficulty: Story intensity (easy, normal, hard)
    
    Returns:
        A formatted backstory string.
    """
    template = CAREER_TEMPLATES.get(career_name)
    if not template:
        return generate_generic_backstory(career_name)
    
    # Generate character
    name = generate_character_name()
    title = random.choice(template["titles"])
    trait = random.choice(TRAITS["positive"])
    
    # Select scenario
    scenario = random.choice(template["scenarios"])
    workplace = random.choice(template["workplaces"])
    mentor = random.choice(template["mentors"])
    
    # Difficulty modifiers
    intensity_words = {
        "easy": "manageable",
        "normal": "challenging",
        "hard": "intense"
    }
    intensity = intensity_words.get(difficulty, "challenging")
    
    # Build the narrative
    backstory = f"""You are {name}, a {trait} {title} working at {workplace}.

{scenario['setup']}

{scenario['challenge']}

Your mentor, {mentor}, has prepared you for moments like this. But nothing compares to the real thing.

{scenario['stakes']}

This {intensity} situation will test everything you've learned. Your skills in {random.choice(template['skills_taught'])} will be crucial.

Are you ready to step into these shoes?"""
    
    return backstory

def generate_generic_backstory(career_name):
    """Fallback for unknown careers."""
    name = generate_character_name()
    trait = random.choice(TRAITS["positive"])
    
    return f"""You are {name}, a {trait} professional embarking on a career in {career_name}.

Today brings unexpected challenges that will test your abilities.

Your mentors have prepared you, but the real test begins now.

Show what you're made of!"""

def get_career_skills(career_name):
    """Get the real-world skills associated with a career."""
    template = CAREER_TEMPLATES.get(career_name)
    if template:
        return template.get("skills_taught", [])
    return ["problem-solving", "critical thinking"]

def get_career_lesson(career_name):
    """Get the educational message for a career."""
    template = CAREER_TEMPLATES.get(career_name)
    if template:
        return template.get("real_world_connection", "")
    return "Every career requires dedication, skill, and continuous learning."

def get_performance_feedback(career_name, score, max_score):
    """Generate feedback based on performance."""
    percentage = (score / max_score) * 100 if max_score > 0 else 0
    template = CAREER_TEMPLATES.get(career_name, {})
    skills = template.get("skills_taught", ["your skills"])
    
    if percentage >= 90:
        return f"Outstanding! You demonstrated exceptional {random.choice(skills)}. You have what it takes to excel in this field!"
    elif percentage >= 70:
        return f"Great work! Your {random.choice(skills)} skills are developing well. Keep practicing!"
    elif percentage >= 50:
        return f"Good effort! With more practice on {random.choice(skills)}, you'll improve significantly."
    else:
        return f"This career is challenging! Focus on developing your {random.choice(skills)} skills. Every expert started somewhere."
