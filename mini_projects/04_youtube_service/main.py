import agents
import gradio as gr

title = "YouTube Services"


def create_youtube_info(type, topic, tone, length, camera):
    description = ""
    script_maker = ""

    agents.user_proxy.initiate_chat(
        agents.manager,
        message=f"The type of YouTube Script I want to create is {type} and the topic is about {topic}.  The tone I "
                f"want is {tone} and be a total of {length} minutes.  The camera style will be {camera}."
                f"The script_maker will create a script and the "
                f"description_maker will create a separate description for the script.  Make it fun and"
                f"engaging and formatted nicely.  Make sure the script and description are separated."
    )

    for content in agents.group_chat.messages:
        if content["name"] == 'script_maker':
            script_maker = content["content"]
        if content["name"] == 'description_maker':
            description = content["content"]

    return script_maker, description


demo = gr.Interface(
    fn=create_youtube_info,
    inputs=[
        gr.Dropdown(["Comedy", "Educational", "Review"], label="Type", info="Type of Content"),
        gr.Dropdown(
            ["Animals", "Technology", "Travel"], label="Topic", info="Main Topic/Niche"
        ),
        gr.Radio(["Casual", "Formal", "Informative"], label="Tone", info="Script Tone:"),
        gr.Slider(1, 10, value=2, label="Length", info="Choose between 1 and 10 Minutes"),
        gr.Dropdown(
            ["Vlog", "Cinematic", "Tutorial", "Interview"], label="Camera", info="The Camera Style"
        )],
    outputs=[gr.Text(label="Script"), gr.Text(label="Description")], theme=gr.themes.Soft())

if __name__ == "__main__":
    demo.launch()
