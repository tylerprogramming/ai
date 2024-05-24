import streamlit as st

st.title("Your First Streamlit App")

name = st.text_input("Enter your name:")
age = st.number_input("Enter your age: ", min_value=0, max_value=120, step=1)

color = st.selectbox("Select your favorite color: ", ["Red", "Yellow", "Orange", "Blue", "Green"])

show_more = st.checkbox("Show more information")

if st.button("Submit"):
    age_in_dog_years = age * 7
    st.write(f"Hello, {name}")
    st.write(f"You are {age} years old, which is {age_in_dog_years} years old in dog years.")
    st.write(f"Your favorite color is {color}.")

if show_more:
    st.write("Here's more information just for you!")
    st.write("Dogs typically live to be around 10-13 years old in human years.")


