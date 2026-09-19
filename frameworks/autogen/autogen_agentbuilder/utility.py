building_task = "Be able to create a python function with documentation on how it works."

execution_task = "Create a python function that reverses a string."

agent_sys_msg_prompt = """Considering the following position:

POSITION: {position}

What requirements should this position be satisfied?

Hint:
# Your answer should be in one sentence.
# Your answer should be natural, starting from "As a ...".
# People with the above position need to complete a task given by a leader or colleague.
# People will work in a group chat, solving tasks with other people with different jobs.
# The modified requirement should not contain the code interpreter skill.
# Coding skill is limited to Python.
"""

position_list = [
    "Environmental_Scientist",
    "Astronomer",
    "Software_Developer",
    "Data_Analyst",
    "Journalist",
    "Teacher",
    "Lawyer",
    "Programmer",
    "Accountant",
    "Mathematician",
    "Physicist",
    "Biologist",
    "Chemist",
    "Statistician",
    "IT_Specialist",
    "Cybersecurity_Expert",
    "Artificial_Intelligence_Engineer",
    "Financial_Analyst",
]