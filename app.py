import os
import json
import time
import streamlit as st

from utils.llm import generate_result

with st.sidebar:
    country = st.selectbox(
        "Choose the country", 
        [
            "None", 
            "Singapore - English", 
            "Thailand - ภาษาไทย", 
            "Vietnam - Tiếng Việt", 
            "Indonesia - Bahasa Indonesia",
        ]
    )

    if country == "None":
        pass
    else:
        # Extract the country name from the selected language
        country_name = country.split(" - ")[0]

        # Construct the path to the template directory based on the country name
        template_path = os.path.join("template", country_name)

        # Get the list of JSON files in the template directory
        template_list = [f[:-5] for f in os.listdir(template_path) if f.endswith(".json")]

        # Add the template options to the sidebar
        template = st.selectbox(
            "Choose the template", 
            ["Blank"] + template_list
        )

# Set the title of the app based on the selected language
st.set_page_config(
    page_title="Scam Detection App",
    page_icon="🚨",
)

# If no country is selected, display a welcome message
if country == "None":
    st.title("Welcome to the Scam Detection App 🚨")
    st.write("Please select a country from the sidebar to proceed.")
    st.write("This app will help you detect scams based on the selected country's context.")

# If the user selects "Blank" template, allow them to create a new dialogue
elif template == "Blank":
    st.title(f"Scam Detection App Demo for {country} 🚨")

    if 'chat_num' not in st.session_state:
        st.session_state.chat_num = 1
    
    chat = {
        "receiver_country": country.split(" - ")[0], 
        "sender": None,
        "chat_history": []
    }

    sender = st.text_input("Sender:", placeholder="Type the sender...", value=None)
    chat["sender"] = sender

    st.subheader("Conversation", divider="orange")

    # Display the text areas for each feature
    for i in range(st.session_state.chat_num):
        role = st.selectbox(
                "Role:", 
                ["Sender", "Receiver"], 
                key=f'role_{i}',
                width=150
            )
        msg = st.text_area(
                "Message:",
                placeholder="Type the message...",
                height=150,
                key=f'msg_{i}'
            )

        # Store the chat history in session state
        chat["chat_history"].append({
            "role": role.lower(),
            "message": msg,
        })

        st.divider()

    col1, _, col3 = st.columns(3)
    # Button to add more message
    with col1:
        def add_new_message():
            st.session_state.chat_num += 1
    
        st.button(
            "Add a new message", 
            type="tertiary", 
            icon="➕", 
            on_click=add_new_message
        )

    # Remove the last message from chat history
    with col3:
        def remove_last_message():
            st.session_state.chat_num -= 1
            chat["chat_history"].pop()

        st.button(
            "Remove the last message", 
            type="tertiary", 
            icon="➖", 
            disabled=(not st.session_state.chat_num > 1),
            on_click=remove_last_message
        )
    
    _, col2, _ = st.columns(3)
    with col2:
        submit = st.button(
            "Submit", 
            type="primary", 
            disabled=(chat["sender"] is None) or (chat["chat_history"][0]["message"] == ""),
        )

    if submit:
        import time
        with st.spinner("Processing..."):
            time.sleep(2)
            result = generate_result(chat=chat)

        st.subheader("Scam Detection Result", divider="blue")
        st.write("Result: {}".format(result))

# If a specific template is selected
else:
    st.title(f"Scam Detection App Demo for {country} 🚨")
    st.markdown(f"**Template:** {template}")

    with open(os.path.join(template_path, f"{template}.json"), "r") as f:
        template_chat = json.load(f)
    
    st.text_input("Sender:", value=template_chat.get("sender", "Unknown"), disabled=True)

    st.subheader("Conversation", divider="orange")
    
    for i, message in enumerate(template_chat.get("chat_history", [])):
        role = message.get("role", "Sender").capitalize()
        msg = message.get("message", "")

        st.text_input("Role:", value=role, disabled=True, width=150, key=f'role_{i}')
        
        st.text_area(
            "Message:",
            value=msg,
            height=150,
            key=f'msg_{i}',
            disabled=True
        )

        st.divider()

    _, col2, _ = st.columns(3)
    with col2:
        submit = st.button("Submit", type="primary")

    if submit:
        with st.spinner("Processing..."):
            time.sleep(2)
            result = generate_result(chat=template_chat)

        st.subheader("Scam Detection Result", divider="blue")
        st.write("Result: {}".format(result))