fitness_expert_name = "fitness_expert"

fitness_expert_message = ("The Fitness Expert leverages their knowledge to create a beginner-friendly workout plan for "
                          "a month. Collaborating with the Product Manager, they outline the fitness metrics and "
                          "training"
                          "methodologies necessary for the Excel Expert to implement into the tracker. Their focus is "
                          "on ensuring the workouts are suitable for beginners, progressively challenging, and align "
                          "with the user's fitness goals. The Fitness Expert's input guides the creation of a plan "
                          "tailored to the needs of individuals starting their fitness journey.")

user_proxy_message = "A human admin."


def get_initiate_message(days_option, selection_options, level_option):
    initiate_message = (f"Create a plan for {days_option} days of a body workout to ONLY include these body parts "
                        f"{selection_options}.  The plan should be made for a(n) {level_option}.  It should have the "
                        f"workouts from fitness expert and the document expert will put it into a word document with "
                        f"exact workout and days, followed by a summary.  Be done once everything is complete.  No "
                        f"extra filler, only exactly what the workout plan is.")
    return initiate_message
