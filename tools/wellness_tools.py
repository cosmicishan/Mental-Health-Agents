from langchain.tools import tool
from typing import Dict, Any, List

@tool
def generate_wellness_plan(user_preferences: dict, current_mood: str) -> Dict[str, Any]:
    """Create personalized wellness and self-care plan based on preferences and current state."""
    
    print("Inside wellness plan")

    # Base wellness activities
    base_activities = {
        "physical": ["Walking", "Stretching", "Yoga", "Dancing", "Swimming"],
        "mental": ["Reading", "Puzzles", "Learning new skill", "Journaling", "Meditation"],
        "social": ["Call a friend", "Join a group", "Volunteer", "Family time", "Pet interaction"],
        "creative": ["Drawing", "Music", "Writing", "Crafts", "Cooking", "Gardening"],
        "relaxation": ["Bath", "Massage", "Nature time", "Breathing exercises", "Progressive muscle relaxation"]
    }
    
    # Mood-specific recommendations
    mood_adjustments = {
        "low": {
            "focus": "gentle, achievable activities",
            "avoid": "overwhelming or high-energy activities",
            "emphasis": ["relaxation", "social", "physical"]
        },
        "anxious": {
            "focus": "calming, grounding activities", 
            "avoid": "stimulating or competitive activities",
            "emphasis": ["relaxation", "mental", "physical"]
        },
        "stressed": {
            "focus": "stress-relief and restoration",
            "avoid": "additional pressures or deadlines",
            "emphasis": ["relaxation", "physical", "creative"]
        },
        "neutral": {
            "focus": "balanced mix of activities",
            "avoid": "nothing specific",
            "emphasis": ["physical", "mental", "social", "creative"]
        }
    }
    
    mood_info = mood_adjustments.get(current_mood.lower(), mood_adjustments["neutral"])
    
    return {
        "daily_wellness_plan": {
            "morning_routine": [
                "5-minute mindfulness or breathing exercise",
                "Gentle stretching or movement",
                "Set positive intention for the day",
                "Healthy breakfast and hydration"
            ],
            "midday_check_in": [
                "Brief mood check-in",
                "5-minute walk or movement break",
                "Healthy lunch and water",
                "Practice gratitude (3 things)"
            ],
            "evening_routine": [
                "Reflect on the day's positives",
                "Relaxing activity (bath, reading, music)",
                "Prepare for restful sleep",
                "Limit screen time before bed"
            ]
        },
        "weekly_goals": {
            "physical_wellness": "Exercise 3-4 times per week (walking, yoga, etc.)",
            "social_connection": "Meaningful interaction with 2-3 people",
            "creative_expression": "Engage in 1-2 creative activities",
            "learning_growth": "Learn something new or practice a skill",
            "nature_time": "Spend time outdoors 2-3 times"
        },
        "mood_specific_recommendations": {
            "current_mood": current_mood,
            "focus_areas": mood_info["focus"],
            "recommended_activities": [base_activities[category] for category in mood_info["emphasis"]],
            "things_to_avoid": mood_info["avoid"]
        },
        "emergency_self_care_toolkit": [
            "Call a trusted friend or family member",
            "Take 10 deep breaths",
            "Go for a short walk",
            "Listen to calming music",
            "Practice 5-4-3-2-1 grounding technique",
            "Take a warm shower or bath",
            "Write in a journal",
            "Pet an animal",
            "Look at photos that make you smile"
        ],
        "weekly_check_in_questions": [
            "What activities brought me the most joy this week?",
            "What was most challenging, and how did I cope?",
            "What am I grateful for this week?",
            "What would I like to focus on next week?",
            "How is my energy level and sleep quality?"
        ]
    }

@tool
def sleep_hygiene_assessment(sleep_issues: str) -> Dict[str, Any]:
    """Assess sleep patterns and provide personalized sleep hygiene recommendations."""
    
    sleep_recommendations = {
        "difficulty_falling_asleep": {
            "primary_strategies": [
                "Establish consistent bedtime routine",
                "Avoid screens 1 hour before bed",
                "Practice relaxation techniques",
                "Keep bedroom cool and dark"
            ],
            "avoid": ["Caffeine after 2 PM", "Large meals before bed", "Intense exercise 3 hours before sleep"]
        },
        "frequent_waking": {
            "primary_strategies": [
                "Maintain consistent sleep schedule",
                "Address underlying anxiety or stress",
                "Optimize sleep environment",
                "Consider sleep study if persistent"
            ],
            "avoid": ["Alcohol before bed", "Looking at clock when awake", "Staying in bed when unable to sleep"]
        },
        "early_waking": {
            "primary_strategies": [
                "Gradual bedtime adjustment",
                "Light therapy in evening",
                "Address depression or anxiety",
                "Consistent wake time"
            ],
            "avoid": ["Napping during day", "Bright lights in morning if waking too early"]
        },
        "poor_quality": {
            "primary_strategies": [
                "Sleep environment optimization",
                "Stress management techniques",
                "Regular exercise (not close to bedtime)",
                "Nutrition and timing of meals"
            ],
            "avoid": ["Irregular sleep schedule", "Stimulants", "Heavy meals before bed"]
        }
    }
    
    # Determine primary issue
    issue_key = "poor_quality"  # Default
    for key in sleep_recommendations.keys():
        if key.replace("_", " ") in sleep_issues.lower():
            issue_key = key
            break
    
    recommendations = sleep_recommendations[issue_key]
    
    return {
        "identified_issue": sleep_issues,
        "sleep_hygiene_checklist": {
            "bedroom_environment": [
                "Temperature: 65-68°F (18-20°C)",
                "Darkness: Blackout curtains or eye mask",
                "Quiet: Earplugs or white noise machine",
                "Comfortable mattress and pillows",
                "Remove electronic devices"
            ],
            "bedtime_routine": [
                "Same bedtime and wake time daily",
                "30-60 minute wind-down routine",
                "Relaxing activities (reading, gentle stretching)",
                "Avoid stimulating content",
                "Prepare for next day to reduce worry"
            ],
            "daytime_habits": [
                "Get natural sunlight exposure",
                "Regular exercise (not within 3 hours of bedtime)",
                "Limit caffeine after 2 PM",
                "Avoid long or late naps",
                "Manage stress throughout the day"
            ]
        },
        "specific_recommendations": recommendations["primary_strategies"],
        "things_to_avoid": recommendations["avoid"],
        "relaxation_techniques": [
            "Progressive muscle relaxation",
            "4-7-8 breathing technique",
            "Body scan meditation",
            "Visualization of peaceful scenes",
            "Gentle yoga or stretching"
        ],
        "when_to_seek_help": [
            "Sleep issues persist for more than 3 weeks",
            "Daytime functioning is significantly impacted",
            "Loud snoring or breathing interruptions",
            "Excessive daytime sleepiness",
            "Sleep issues worsen despite good sleep hygiene"
        ]
    }

@tool
def nutrition_guidance(nutrition_goals: str, dietary_restrictions: str = "none") -> Dict[str, Any]:
    """Provide mental health-focused nutrition guidance and meal planning suggestions."""
    
    brain_healthy_foods = {
        "omega_3_rich": ["Salmon", "Walnuts", "Chia seeds", "Flaxseeds", "Sardines"],
        "antioxidant_rich": ["Blueberries", "Dark chocolate", "Green tea", "Spinach", "Broccoli"],
        "complex_carbs": ["Oats", "Quinoa", "Sweet potatoes", "Brown rice", "Whole grain bread"],
        "protein_sources": ["Eggs", "Greek yogurt", "Lean poultry", "Legumes", "Tofu"],
        "mood_supporting": ["Bananas", "Avocados", "Turkey", "Pumpkin seeds", "Dark leafy greens"]
    }
    
    nutrition_for_mental_health = {
        "mood_stability": {
            "focus": "Stable blood sugar and neurotransmitter support",
            "key_nutrients": ["Omega-3 fatty acids", "B vitamins", "Vitamin D", "Magnesium"],
            "meal_timing": "Regular meals every 3-4 hours",
            "hydration": "8-10 glasses of water daily"
        },
        "energy_levels": {
            "focus": "Sustained energy without crashes",
            "key_nutrients": ["Complex carbohydrates", "Iron", "B vitamins", "Protein"],
            "meal_timing": "Balanced breakfast, avoid skipping meals",
            "limit": "Refined sugars and processed foods"
        },
        "stress_management": {
            "focus": "Foods that support stress response",
            "key_nutrients": ["Magnesium", "Vitamin C", "Omega-3s", "Probiotics"],
            "beneficial": "Herbal teas (chamomile, green tea)",
            "limit": "Excessive caffeine and alcohol"
        },
        "sleep_quality": {
            "focus": "Foods that promote restful sleep",
            "key_nutrients": ["Tryptophan", "Magnesium", "Melatonin precursors"],
            "evening_foods": ["Turkey", "Tart cherries", "Almonds", "Herbal tea"],
            "avoid_evening": "Large meals, caffeine, alcohol"
        }
    }
    
    # Process dietary restrictions
    restrictions = dietary_restrictions.lower().split(",") if dietary_restrictions != "none" else []
    
    return {
        "nutrition_goals": nutrition_goals,
        "dietary_restrictions": dietary_restrictions,
        "brain_healthy_meal_plan": {
            "breakfast_ideas": [
                "Oatmeal with berries and walnuts",
                "Greek yogurt with chia seeds and fruit",
                "Whole grain toast with avocado and eggs",
                "Smoothie with spinach, banana, and protein"
            ],
            "lunch_ideas": [
                "Salmon salad with dark leafy greens",
                "Quinoa bowl with vegetables and legumes",
                "Turkey and avocado wrap with whole grain tortilla",
                "Lentil soup with whole grain bread"
            ],
            "dinner_ideas": [
                "Baked fish with sweet potato and broccoli",
                "Stir-fry with tofu and colorful vegetables",
                "Lean protein with quinoa and roasted vegetables",
                "Bean and vegetable curry with brown rice"
            ],
            "snack_ideas": [
                "Apple with almond butter",
                "Handful of walnuts and berries",
                "Greek yogurt with pumpkin seeds",
                "Dark chocolate (70%+ cacao) and nuts"
            ]
        },
        "mood_supporting_nutrients": nutrition_for_mental_health,
        "hydration_plan": {
            "daily_goal": "8-10 glasses of water",
            "timing": "Glass upon waking, before meals, during exercise",
            "alternatives": "Herbal teas, water with lemon, coconut water",
            "limit": "Excessive caffeine, sugary drinks, alcohol"
        },
        "meal_prep_tips": [
            "Plan and prep meals on weekends",
            "Keep healthy snacks readily available",
            "Batch cook grains and proteins",
            "Wash and chop vegetables in advance",
            "Have backup healthy options for busy days"
        ],
        "mindful_eating_practices": [
            "Eat without distractions (TV, phone)",
            "Chew slowly and savor flavors",
            "Pay attention to hunger and fullness cues",
            "Practice gratitude for your food",
            "Notice how different foods affect your mood and energy"
        ]
    }

@tool
def exercise_recommendations(fitness_level: str, exercise_preferences: str) -> Dict[str, Any]:
    """Provide personalized exercise recommendations focused on mental health benefits."""
    
    exercise_programs = {
        "beginner": {
            "weekly_goal": "3-4 sessions, 20-30 minutes each",
            "activities": [
                "Walking (start with 15 minutes, increase gradually)",
                "Gentle yoga or stretching",
                "Bodyweight exercises (modified as needed)",
                "Swimming or water aerobics",
                "Dancing to favorite music"
            ],
            "progression": "Increase duration by 5 minutes every 2 weeks"
        },
        "intermediate": {
            "weekly_goal": "4-5 sessions, 30-45 minutes each",
            "activities": [
                "Brisk walking or jogging",
                "Strength training 2x per week",
                "Yoga or Pilates",
                "Cycling or swimming",
                "Group fitness classes"
            ],
            "progression": "Increase intensity or add variety every 3-4 weeks"
        },
        "advanced": {
            "weekly_goal": "5-6 sessions, 45-60 minutes each",
            "activities": [
                "Running or high-intensity cardio",
                "Strength training 3x per week",
                "Advanced yoga or martial arts",
                "Competitive sports",
                "Cross-training activities"
            ],
            "progression": "Focus on performance goals and new challenges"
        }
    }
    
    mental_health_benefits = {
        "cardio": {
            "benefits": ["Releases endorphins", "Reduces anxiety", "Improves mood", "Enhances sleep"],
            "examples": ["Walking", "Running", "Cycling", "Swimming", "Dancing"]
        },
        "strength_training": {
            "benefits": ["Builds confidence", "Improves body image", "Reduces depression", "Increases energy"],
            "examples": ["Bodyweight exercises", "Weight lifting", "Resistance bands", "Functional movements"]
        },
        "mind_body": {
            "benefits": ["Reduces stress", "Improves mindfulness", "Enhances flexibility", "Promotes relaxation"],
            "examples": ["Yoga", "Tai Chi", "Pilates", "Qigong", "Stretching"]
        },
        "outdoor": {
            "benefits": ["Vitamin D exposure", "Nature connection", "Fresh air", "Stress reduction"],
            "examples": ["Hiking", "Outdoor cycling", "Gardening", "Outdoor sports", "Walking in parks"]
        }
    }
    
    program = exercise_programs.get(fitness_level.lower(), exercise_programs["beginner"])
    
    return {
        "fitness_level": fitness_level,
        "exercise_preferences": exercise_preferences,
        "recommended_program": program,
        "mental_health_focused_routine": {
            "monday": "Cardio activity (mood boost)",
            "tuesday": "Strength training (confidence building)",
            "wednesday": "Mind-body practice (stress relief)",
            "thursday": "Cardio activity (anxiety reduction)",
            "friday": "Strength training (energy boost)",
            "saturday": "Outdoor activity (nature connection)",
            "sunday": "Gentle movement or rest (recovery)"
        },
        "exercise_types_benefits": mental_health_benefits,
        "getting_started_tips": [
            "Start slowly and build gradually",
            "Choose activities you enjoy",
            "Set realistic, achievable goals",
            "Track your mood before and after exercise",
            "Find an exercise buddy for motivation",
            "Celebrate small victories",
            "Listen to your body and rest when needed"
        ],
        "motivation_strategies": [
            "Focus on how exercise makes you feel",
            "Set process goals, not just outcome goals",
            "Create a reward system for consistency",
            "Keep a workout journal",
            "Try new activities to prevent boredom",
            "Remember that some movement is better than none"
        ],
        "safety_considerations": [
            "Consult healthcare provider before starting new program",
            "Warm up before and cool down after exercise",
            "Stay hydrated",
            "Use proper form to prevent injury",
            "Stop if you experience pain or dizziness"
        ]
    }

@tool
def stress_management_plan(main_stressors: str, lifestyle_factors: str) -> Dict[str, Any]:
    """Create comprehensive stress management plan based on individual stressors and lifestyle."""
    
    stress_management_techniques = {
        "immediate_relief": {
            "breathing_exercises": [
                "4-7-8 breathing (inhale 4, hold 7, exhale 8)",
                "Box breathing (4-4-4-4 pattern)",
                "Belly breathing (deep diaphragmatic breaths)"
            ],
            "quick_techniques": [
                "Progressive muscle relaxation",
                "5-4-3-2-1 grounding technique",
                "Cold water on wrists/face",
                "Brief walk or movement"
            ]
        },
        "daily_practices": {
            "morning_routine": [
                "10-minute meditation or mindfulness",
                "Intention setting for the day",
                "Gentle stretching or yoga",
                "Positive affirmations"
            ],
            "throughout_day": [
                "Regular check-ins with stress level",
                "Mini-breaks every 2 hours",
                "Mindful transitions between activities",
                "Gratitude practice"
            ],
            "evening_routine": [
                "Reflection on day's positives",
                "Stress release activities",
                "Preparation for restful sleep",
                "Worry time (15 minutes max)"
            ]
        },
        "weekly_practices": {
            "self_care": [
                "Schedule enjoyable activities",
                "Social connection with supportive people",
                "Time in nature",
                "Creative expression"
            ],
            "life_management": [
                "Weekly planning and organization",
                "Boundary setting practice",
                "Problem-solving session",
                "Review and adjust stress management strategies"
            ]
        }
    }
    
    stressor_specific_strategies = {
        "work": [
            "Time management and prioritization",
            "Boundary setting with work hours",
            "Communication with supervisor about workload",
            "Workplace stress reduction techniques"
        ],
        "relationships": [
            "Communication skills practice",
            "Conflict resolution strategies",
            "Boundary setting in relationships",
            "Social support network building"
        ],
        "financial": [
            "Budget planning and financial organization",
            "Seeking financial counseling if needed",
            "Focus on what you can control",
            "Long-term financial planning"
        ],
        "health": [
            "Working with healthcare providers",
            "Focus on healthy lifestyle choices",
            "Acceptance and adaptation strategies",
            "Support group participation"
        ],
        "family": [
            "Family communication improvement",
            "Role clarification and boundary setting",
            "Family therapy or counseling",
            "Self-care while caregiving"
        ]
    }
    
    return {
        "identified_stressors": main_stressors,
        "lifestyle_factors": lifestyle_factors,
        "comprehensive_stress_plan": stress_management_techniques,
        "stressor_specific_strategies": {
            stressor: strategies for stressor, strategies in stressor_specific_strategies.items()
            if stressor in main_stressors.lower()
        },
        "stress_prevention": [
            "Regular exercise routine",
            "Adequate sleep (7-9 hours)",
            "Healthy nutrition",
            "Strong social support network",
            "Regular relaxation practice",
            "Time management skills",
            "Realistic goal setting"
        ],
        "warning_signs": [
            "Physical symptoms (headaches, muscle tension)",
            "Emotional symptoms (irritability, anxiety)",
            "Behavioral changes (sleep, appetite, social withdrawal)",
            "Cognitive symptoms (difficulty concentrating, worry)"
        ],
        "when_to_seek_help": [
            "Stress interferes with daily functioning",
            "Physical symptoms persist",
            "Unhealthy coping mechanisms develop",
            "Feeling overwhelmed despite stress management efforts",
            "Thoughts of self-harm or substance use"
        ],
        "emergency_stress_toolkit": [
            "Call a trusted friend or family member",
            "Practice immediate breathing technique",
            "Go for a walk or do physical movement",
            "Listen to calming music",
            "Take a warm shower or bath",
            "Write thoughts in a journal",
            "Use a stress management app",
            "Practice self-compassion"
        ]
    }

@tool
def generate_coping_strategies(situation: str) -> Dict[str, Any]:
    """Generate personalized coping strategies for specific situations or challenges."""
    
    coping_strategies = {
        "problem_focused": {
            "description": "Strategies that address the root cause of stress",
            "techniques": [
                "Problem-solving steps (identify, brainstorm, evaluate, implement)",
                "Time management and organization",
                "Seeking information or resources",
                "Setting boundaries and saying no",
                "Asking for help or support",
                "Breaking large problems into smaller steps"
            ]
        },
        "emotion_focused": {
            "description": "Strategies that help manage emotional responses",
            "techniques": [
                "Mindfulness and acceptance",
                "Emotional regulation skills",
                "Reframing and perspective-taking",
                "Self-compassion practices",
                "Expressive writing or art",
                "Seeking emotional support"
            ]
        },
        "meaning_focused": {
            "description": "Strategies that find purpose and growth in challenges",
            "techniques": [
                "Identifying personal values and meaning",
                "Finding benefits or learning in difficulties",
                "Spiritual or philosophical practices",
                "Helping others in similar situations",
                "Creating legacy or positive impact",
                "Gratitude and appreciation practices"
            ]
        }
    }
    
    situation_specific = {
        "grief": ["Allow yourself to feel emotions", "Create memorial rituals", "Join grief support group", "Professional grief counseling"],
        "anxiety": ["Challenge anxious thoughts", "Practice exposure gradually", "Use grounding techniques", "Develop safety behaviors"],
        "depression": ["Behavioral activation", "Social connection", "Pleasant activity scheduling", "Professional treatment"],
        "trauma": ["Safety and stabilization first", "Trauma-informed therapy", "Grounding and self-soothing", "Building support network"],
        "relationship": ["Communication skills", "Boundary setting", "Couples therapy", "Individual self-care"],
        "work": ["Time management", "Workplace boundaries", "Career counseling", "Stress reduction techniques"]
    }
    
    # Determine most relevant situation-specific strategies
    relevant_strategies = []
    for key, strategies in situation_specific.items():
        if key in situation.lower():
            relevant_strategies.extend(strategies)
    
    return {
        "situation": situation,
        "comprehensive_coping_framework": coping_strategies,
        "situation_specific_strategies": relevant_strategies if relevant_strategies else ["General stress management", "Professional support", "Self-care practices", "Social support"],
        "immediate_coping_tools": [
            "Deep breathing exercises",
            "Grounding techniques (5-4-3-2-1)",
            "Progressive muscle relaxation",
            "Mindful observation",
            "Positive self-talk",
            "Brief physical movement"
        ],
        "long_term_resilience_building": [
            "Regular self-care routine",
            "Strong social support network",
            "Healthy lifestyle habits",
            "Stress management skills",
            "Professional therapy or counseling",
            "Spiritual or philosophical practices",
            "Continuous learning and growth mindset"
        ],
        "adaptive_vs_maladaptive": {
            "adaptive_coping": [
                "Seeking support from others",
                "Problem-solving and planning",
                "Positive reframing",
                "Acceptance of what cannot be changed",
                "Self-care and stress management",
                "Professional help when needed"
            ],
            "maladaptive_coping_to_avoid": [
                "Substance use or abuse",
                "Social isolation and withdrawal",
                "Avoidance of all stressors",
                "Aggressive or harmful behaviors",
                "Excessive rumination or worry",
                "Self-blame and harsh self-criticism"
            ]
        }
    }
