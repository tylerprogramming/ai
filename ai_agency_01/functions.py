import agents


def create_csv(message):
    agents.csv_user.initiate_chat(agents.excel, message=message)

    with open("workout/workout.csv", "w") as file:
        file.write(f"{message}\n")

    last_message = agents.csv_user.last_message()["content"]
    return last_message


def create_doc(message):
    agents.doc_user.initiate_chat(agents.document, message=message)

    last_doc_message = agents.doc_user.last_message()["content"]

    with open("workout/summary.txt", "w") as file:
        file.write(f"{last_doc_message}")

    return last_doc_message
