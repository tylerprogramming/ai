def create_workout_plan_prompt(wake_up_time, bedtime, workout_active, run):
    messages = [
        {"role": "system", "content": "You are a helpful assistant designed to output workout plans."},
        {"role": "user", "content": f"""
        Create a workout plan for a day based on the following information:
        - Wake up time: {wake_up_time}
        - Bedtime: {bedtime}
        - Workout active: {workout_active}
        - Run: {run}
        
        Only return the workout plan, nothing else.
        """}
    ]
    
    return messages