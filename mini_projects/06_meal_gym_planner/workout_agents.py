import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
from typing_extensions import Annotated

load_dotenv()  # OPENAI_API_KEY from .env


class WorkoutPlannerSystem:
    def __init__(self):
        self.model_client = OpenAIChatCompletionClient(model="gpt-5.4-mini")

        self.workout_planning_agent = AssistantAgent(
            name="workout_planning_agent",
            system_message="""
                You are a fitness expert, known for creating personalized workout plans.
                You transform complex concepts into compelling narratives.  Make sure to include the following:

                - Frequency
                - Duration
                - Intensity
                - Equipment
                - Focus Areas
                - Daily Structure
                - Weekly Summary

                "frequency": "3 days a week (Monday, Wednesday, Friday)",
                "duration": "30 minutes per session",
                "intensity": "Low",
                "equipment": "Dumbbells",
                "focus_areas": "Upper Body, Lower Body",
                "daily_structure": {
                    "Monday": {
                        "duration": "30 minutes",
                        "warm_up": {
                            "duration": "5 minutes",
                            "exercises": [
                                {"name": "Arm Circles", "duration": "30 seconds"},
                                {"name": "Leg Swings", "duration": "1 minute"},
                                {"name": "March in Place", "duration": "3.5 minutes"}
                            ]
                        },
                        "main_workout": {
                            "duration": "20 minutes",
                            "circuit": {
                                "exercise_duration": "30 seconds",
                                "rest_duration": "30 seconds",
                                "repeat": "2 times",
                                "exercises": [
                                    "Dumbbell Shoulder Press",
                                    "Dumbbell Bent Over Rows",
                                    "Dumbbell Goblet Squats",
                                    "Dumbbell Bicep Curls",
                                    "Dumbbell Tricep Extensions"
                                ]
                            }
                        },
                        "cool_down": {
                            "duration": "5 minutes",
                            "exercises": [
                                {"name": "Shoulder Stretch", "duration": "30 seconds per arm"},
                                {"name": "Standing Quad Stretch", "duration": "30 seconds per leg"},
                                {"name": "Deep Breathing", "duration": "2 minutes"}
                            ]
                        }
                    },
                    "Wednesday": {
                        "duration": "30 minutes",
                        "warm_up": {
                            "duration": "5 minutes",
                            "exercises": [
                                {"name": "Side Lunges", "duration": "1 minute"},
                                {"name": "Arm Circles", "duration": "30 seconds"},
                                {"name": "High Knees", "duration": "3.5 minutes"}
                            ]
                        },
                        "main_workout": {
                            "duration": "20 minutes",
                            "circuit": {
                                "exercise_duration": "30 seconds",
                                "rest_duration": "30 seconds",
                                "repeat": "2 times",
                                "exercises": [
                                    "Dumbbell Chest Press",
                                    "Dumbbell Deadlifts",
                                    "Dumbbell Lateral Raises",
                                    "Dumbbell Front Raises",
                                    "Standing Calf Raises"
                                ]
                            }
                        },
                        "cool_down": {
                            "duration": "5 minutes",
                            "exercises": [
                                {"name": "Arm Across Chest Stretch", "duration": "30 seconds per arm"},
                                {"name": "Standing Hamstring Stretch", "duration": "30 seconds per leg"},
                                {"name": "Neck Stretch", "duration": "30 seconds"},
                                {"name": "Deep Breathing", "duration": "2 minutes"}
                            ]
                        }
                    },
                    "Friday": {
                        "duration": "30 minutes",
                        "warm_up": {
                            "duration": "5 minutes",
                            "exercises": [
                                {"name": "Dynamic Hip Flexor Stretch", "duration": "1 minute"},
                                {"name": "Arm Circles", "duration": "30 seconds"},
                                {"name": "Jumping Jacks", "duration": "3.5 minutes"}
                            ]
                        },
                        "main_workout": {
                            "duration": "20 minutes",
                            "circuit": {
                                "exercise_duration": "30 seconds",
                                "rest_duration": "30 seconds",
                                "repeat": "2 times",
                                "exercises": [
                                    "Dumbbell Push Press",
                                    "Dumbbell Step-Ups",
                                    "Dumbbell Russian Twists",
                                    "Dumbbell Sumo Squats",
                                    "Plank Hold"
                                ]
                            }
                        },
                        "cool_down": {
                            "duration": "5 minutes",
                            "exercises": [
                                {"name": "Child’s Pose", "duration": "1 minute"},
                                {"name": "Seated Forward Bend", "duration": "1 minute"},
                                {"name": "Side Stretch", "duration": "30 seconds per side"},
                                {"name": "Deep Breathing", "duration": "2 minutes"}
                            ]
                        }
                    }
                },
                "weekly_summary": {
                    "Monday": "Upper Body & Lower Body Workout A",
                    "Wednesday": "Upper Body & Lower Body Workout B",
                    "Friday": "Upper Body & Lower Body Workout C",
                    "Saturday": "Rest Days / Optional light activity like walking or stretching",
                    "Sunday": ""
                }
            }

                
                This is an example of what you should fill in and return.  Don't add any other properties, only these. It can be in markdown format.
            """,
            model_client=self.model_client,
        )
        self.meal_planning_agent = AssistantAgent(
            name="meal_planning_agent",
            system_message="""
                You are a fitness expert, known for creating personalized meal plans.
                You transform complex concepts into compelling narratives.  Make sure to include the following:

                - Nutritional Goals
                - Meal Timing
                - Weekly Meals
                - Additional Tips

                "meal_plan": {
                        "nutritional_goals": {
                            "protein": "Lean meats, fish, eggs, legumes",
                            "carbohydrates": "Whole grains, fruits, vegetables",
                            "fats": "Avocado, nuts, olive oil"
                        },
                        "meal_timing": "Breakfast, Lunch, Dinner, and Snacks around workout sessions",
                        "weekly_meals": {
                            "Monday": {
                                "Breakfast": "Greek yogurt with mixed berries and a sprinkle of nuts",
                                "Snack": "A banana",
                                "Lunch": "Grilled chicken salad with mixed greens, cherry tomatoes, cucumbers, and balsamic dressing",
                                "Snack": "Hummus with carrot sticks",
                                "Dinner": "Baked salmon with quinoa and steamed broccoli"
                            },
                            "Tuesday": {
                                "Breakfast": "Oatmeal topped with sliced apple and cinnamon",
                                "Snack": "A handful of almonds",
                                "Lunch": "Turkey wrap with whole grain tortilla, lettuce, tomato, and mustard",
                                "Snack": "Cottage cheese with pineapple chunks",
                                "Dinner": "Stir-fried tofu with mixed vegetables and brown rice"
                            },
                            "Wednesday": {
                                "break": "Rest Day",
                                "Breakfast": "Smoothie with spinach, banana, protein powder, and almond milk",
                                "Snack": "Hard-boiled eggs",
                                "Lunch": "Quinoa salad with chickpeas, bell peppers, and lemon vinaigrette",
                                "Snack": "Rice cakes with peanut butter",
                                "Dinner": "Roast chicken with sweet potatoes and green beans"
                            },
                            "Thursday": {
                                "Breakfast": "Whole grain toast with avocado and poached egg",
                                "Snack": "Greek yogurt with honey and walnuts",
                                "Lunch": "Lentil soup with a side salad",
                                "Snack": "Sliced cucumbers with tzatziki",
                                "Dinner": "Grilled shrimp tacos with cabbage slaw"
                            },
                            "Friday": {
                                "Breakfast": "Chia seed pudding made with almond milk and topped with fresh fruit",
                                "Snack": "Protein bar",
                                "Lunch": "Spinach and feta omelet with whole grain toast",
                                "Snack": "A small apple with almond butter",
                                "Dinner": "Ground turkey stuffed peppers"
                            }
                        },
                        "additional_tips": [
                            "Stay hydrated and drink plenty of water throughout the day",
                            "Adjust portion sizes based on personal needs and weight loss goals",
                            "Consider incorporating a variety of spices and herbs to enhance flavor and nutrition"
                        ]
                    }

                This is an example of what you should fill in and return.  Don't add any other properties, only these. It can be in markdown format.
                For the nutritional_goals property, you can include other things, and this can differ from person to person.  Take into account 
                their age, gender, and fitness level. 
            """,
            model_client=self.model_client,
        )
        self.writer = AssistantAgent(
            name="writer",
            model_client=self.model_client,
            system_message="""
                You are a professional writer, known for
                your insightful and engaging articles.
                You transform complex concepts into compelling narratives.

                You are going to turn the workout plan and the meal plan into a json format.  The json format is going to be like this:

                {
                    "workout_plan": {
                        "frequency": "3 days a week (Monday, Wednesday, Friday)",
                        "duration": "30 minutes per session",
                        "intensity": "Low",
                        "equipment": "Dumbbells",
                        "focus_areas": "Upper Body, Lower Body",
                        "daily_structure": {
                            "Monday": {
                                "duration": "30 minutes",
                                "warm_up": {
                                    "duration": "5 minutes",
                                    "exercises": [
                                        {"name": "Arm Circles", "duration": "30 seconds"},
                                        {"name": "Leg Swings", "duration": "1 minute"},
                                        {"name": "March in Place", "duration": "3.5 minutes"}
                                    ]
                                },
                                "main_workout": {
                                    "duration": "20 minutes",
                                    "circuit": {
                                        "exercise_duration": "30 seconds",
                                        "rest_duration": "30 seconds",
                                        "repeat": "2 times",
                                        "exercises": [
                                            "Dumbbell Shoulder Press",
                                            "Dumbbell Bent Over Rows",
                                            "Dumbbell Goblet Squats",
                                            "Dumbbell Bicep Curls",
                                            "Dumbbell Tricep Extensions"
                                        ]
                                    }
                                },
                                "cool_down": {
                                    "duration": "5 minutes",
                                    "exercises": [
                                        {"name": "Shoulder Stretch", "duration": "30 seconds per arm"},
                                        {"name": "Standing Quad Stretch", "duration": "30 seconds per leg"},
                                        {"name": "Deep Breathing", "duration": "2 minutes"}
                                    ]
                                }
                            },
                            "Wednesday": {
                                "duration": "30 minutes",
                                "warm_up": {
                                    "duration": "5 minutes",
                                    "exercises": [
                                        {"name": "Side Lunges", "duration": "1 minute"},
                                        {"name": "Arm Circles", "duration": "30 seconds"},
                                        {"name": "High Knees", "duration": "3.5 minutes"}
                                    ]
                                },
                                "main_workout": {
                                    "duration": "20 minutes",
                                    "circuit": {
                                        "exercise_duration": "30 seconds",
                                        "rest_duration": "30 seconds",
                                        "repeat": "2 times",
                                        "exercises": [
                                            "Dumbbell Chest Press",
                                            "Dumbbell Deadlifts",
                                            "Dumbbell Lateral Raises",
                                            "Dumbbell Front Raises",
                                            "Standing Calf Raises"
                                        ]
                                    }
                                },
                                "cool_down": {
                                    "duration": "5 minutes",
                                    "exercises": [
                                        {"name": "Arm Across Chest Stretch", "duration": "30 seconds per arm"},
                                        {"name": "Standing Hamstring Stretch", "duration": "30 seconds per leg"},
                                        {"name": "Neck Stretch", "duration": "30 seconds"},
                                        {"name": "Deep Breathing", "duration": "2 minutes"}
                                    ]
                                }
                            },
                            "Friday": {
                                "duration": "30 minutes",
                                "warm_up": {
                                    "duration": "5 minutes",
                                    "exercises": [
                                        {"name": "Dynamic Hip Flexor Stretch", "duration": "1 minute"},
                                        {"name": "Arm Circles", "duration": "30 seconds"},
                                        {"name": "Jumping Jacks", "duration": "3.5 minutes"}
                                    ]
                                },
                                "main_workout": {
                                    "duration": "20 minutes",
                                    "circuit": {
                                        "exercise_duration": "30 seconds",
                                        "rest_duration": "30 seconds",
                                        "repeat": "2 times",
                                        "exercises": [
                                            "Dumbbell Push Press",
                                            "Dumbbell Step-Ups",
                                            "Dumbbell Russian Twists",
                                            "Dumbbell Sumo Squats",
                                            "Plank Hold"
                                        ]
                                    }
                                },
                                "cool_down": {
                                    "duration": "5 minutes",
                                    "exercises": [
                                        {"name": "Childs Pose", "duration": "1 minute"},
                                        {"name": "Seated Forward Bend", "duration": "1 minute"},
                                        {"name": "Side Stretch", "duration": "30 seconds per side"},
                                        {"name": "Deep Breathing", "duration": "2 minutes"}
                                    ]
                                }
                            }
                        },
                        "weekly_summary": {
                            "Monday": "Upper Body & Lower Body Workout A",
                            "Wednesday": "Upper Body & Lower Body Workout B",
                            "Friday": "Upper Body & Lower Body Workout C",
                            "Saturday": "Rest Days / Optional light activity like walking or stretching",
                            "Sunday": ""
                        }
                    },
                    "meal_plan": {
                        "nutritional_goals": {
                            "protein": "Lean meats, fish, eggs, legumes",
                            "carbohydrates": "Whole grains, fruits, vegetables",
                            "fats": "Avocado, nuts, olive oil"
                        },
                        "meal_timing": "Breakfast, Lunch, Dinner, and Snacks around workout sessions",
                        "weekly_meals": {
                            "Monday": {
                                "Breakfast": "Greek yogurt with mixed berries and a sprinkle of nuts",
                                "Snack": "A banana",
                                "Lunch": "Grilled chicken salad with mixed greens, cherry tomatoes, cucumbers, and balsamic dressing",
                                "Snack": "Hummus with carrot sticks",
                                "Dinner": "Baked salmon with quinoa and steamed broccoli"
                            },
                            "Tuesday": {
                                "Breakfast": "Oatmeal topped with sliced apple and cinnamon",
                                "Snack": "A handful of almonds",
                                "Lunch": "Turkey wrap with whole grain tortilla, lettuce, tomato, and mustard",
                                "Snack": "Cottage cheese with pineapple chunks",
                                "Dinner": "Stir-fried tofu with mixed vegetables and brown rice"
                            },
                            "Wednesday": {
                                "break": "Rest Day",
                                "Breakfast": "Smoothie with spinach, banana, protein powder, and almond milk",
                                "Snack": "Hard-boiled eggs",
                                "Lunch": "Quinoa salad with chickpeas, bell peppers, and lemon vinaigrette",
                                "Snack": "Rice cakes with peanut butter",
                                "Dinner": "Roast chicken with sweet potatoes and green beans"
                            },
                            "Thursday": {
                                "Breakfast": "Whole grain toast with avocado and poached egg",
                                "Snack": "Greek yogurt with honey and walnuts",
                                "Lunch": "Lentil soup with a side salad",
                                "Snack": "Sliced cucumbers with tzatziki",
                                "Dinner": "Grilled shrimp tacos with cabbage slaw"
                            },
                            "Friday": {
                                "Breakfast": "Chia seed pudding made with almond milk and topped with fresh fruit",
                                "Snack": "Protein bar",
                                "Lunch": "Spinach and feta omelet with whole grain toast",
                                "Snack": "A small apple with almond butter",
                                "Dinner": "Ground turkey stuffed peppers"
                            }
                        },
                        "additional_tips": [
                            "Stay hydrated and drink plenty of water throughout the day",
                            "Adjust portion sizes based on personal needs and weight loss goals",
                            "Consider incorporating a variety of spices and herbs to enhance flavor and nutrition"
                        ]
                    }
                }
                
                Just make sure you fill it out properly, the above is how it should look.  If there is no information for a property or day,
                just leave it with an empty string.  Also ensure the json is formatted properly.  All the informatino gathered should be 
                formatted in the json above. Don't do anything else, or add anything else.  Just output the json.  Don't add any other json 
                properties.  
                
                Reply "TERMINATE" in the end when everything is done.
                """,
        )
        # The tool is a plain function with type hints; the file_saver_agent calls it itself
        def file_saver(text: Annotated[str, "The converted markdown to be saved"]) -> str:
            """File Saver"""
            with open("workout_plan.md", 'w') as text_file:
                text_file.write(text)
            return text

        self.file_saver_agent = AssistantAgent(
            name="file_saver_agent",
            system_message="""
                You are a file saver, known for saving files to a specified directory.
                You transform complex concepts into compelling narratives.  
                Convert the text which may look like a dict or json, and format it nicely into markdown.
                When you are done, you should return TERMINATE.
            """,
            model_client=self.model_client,
            tools=[file_saver],
            reflect_on_tool_use=True,
        )

    async def generate_plan(self, user_info):
        workout_task = f"""Create a workout plan for me as I am a beginner. Here is information about me:
        {user_info}"""
        
        meal_plan_task = """Create a meal plan for me based on the workout plan."""
        
        writing_task = """Take the workout plan and the meal plan and write them neatly for the user. Make the output in json format."""

        # The old initiate_chats ran these chats one after another, and each chat got the
        # last message of the earlier chats as carryover. Each agent here gets its task plus that.
        chats = [
            (self.workout_planning_agent, workout_task),
            (self.meal_planning_agent, meal_plan_task),
            (self.writer, writing_task),
            (self.file_saver_agent, "Save the file."),
        ]

        carryover = []
        try:
            for agent, message in chats:
                task = message
                if carryover:
                    task += "\nContext: \n" + "\n".join(carryover)
                result = await agent.run(task=task)
                carryover.append(result.messages[-1].to_text())  # like summary_method="last_msg"
        finally:
            await self.model_client.close()

        # The writer's json reply (the file saver's markdown goes to workout_plan.md)
        return carryover[-2]

# Usage example:
if __name__ == "__main__":
    planner = WorkoutPlannerSystem()
    user_info = """
    Age: 34
    Gender: Male,
    Fitness Level: Beginner,
    Goals: Weight Loss,
    Workout Duration: 15 minutes,
    Workout Type: Cardio,
    Equipment: Dumbbells,
    Workout Days: 5 days per week,
    Intensity: Low,
    Preferred Time: Morning,
    Warm-up/Cool-down: Yes,
    Focus Areas: Upper Body
    """
    result = asyncio.run(planner.generate_plan(user_info))
    print(result)