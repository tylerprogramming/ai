import streamlit as st
import json
import reddit

st.title = "Reddit App"

with st.container(border=True):
    mode = st.radio(
        "Choose a mode",
        [":rainbow[Random]", "***Specific Subreddit***"],
        captions=["Laugh out loud.", "Get the popcorn."]
    )

    number = st.slider("Pick a number", 1, 10)

    response = ""

    if mode == ":rainbow[Random]":
        prompt = f"Get me {number} random subreddit(s)!"
        submit = st.button(prompt)

        if submit:
            response = reddit.start_chat(prompt)

    if mode == "***Specific Subreddit***":
        input = st.text_input("")
        submit = st.button(f"Give me content!")
        prompt = f"Give me {number} subreddit posts on: {input}"

        if submit:
            response = reddit.start_chat(prompt)

with st.spinner('Wait for it...'):
    if response:
        st.success('Done!')
        response = json.loads(response)
        st.divider()

        for data in response:
            # Extracting 'content'
            content = data["content"]

            # Extracting 'meta_data'
            meta_data = data["meta_data"]

            # Extracting each property from 'meta_data'
            post_subreddit = meta_data["subreddit"]
            post_category = meta_data["category"]
            post_title = meta_data["title"]
            post_score = meta_data["score"]
            post_url = meta_data["url"]
            post_author = meta_data["author"]

            st.header("Metadata")
            st.divider()
            st.markdown('**Subreddit**: ' + post_subreddit)
            st.markdown('**Category**: ' + post_category)
            st.markdown('**Title**: ' + post_title)
            st.markdown('**URL**: ' + post_url)
            st.markdown('**Author**: ' + post_author)

            st.header("Content")
            st.divider()
            st.write(content)









