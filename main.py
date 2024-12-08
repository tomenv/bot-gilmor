import streamlit as st
import google.generativeai as gen_ai


def home_screen():
    st.title("Welocome to Bot Gilmor")
    options = ["LORELAI", "RORI", "EMILY", "RICHARD", "LUKE"]
    selected_option = st.selectbox("Who do you want to talk to:", options)
    if st.button("Continue"):
        if selected_option:
            st.session_state.selected_option = selected_option
            st.session_state.next_screen = True
        else:
            st.warning("Please select an option.")

def next_screen():
    # GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    # # Set up Google Gemini-Pro AI model
    # gen_ai.configure(api_key=GOOGLE_API_KEY)
    # model = gen_ai.GenerativeModel('gemini-pro')

    # Configure Streamlit page settings
    st.set_page_config(
        page_title="Chat with Gemini-Pro!",
        page_icon=":brain:",  # Favicon emoji
        layout="centered",  # Page layout option
        )


    # Function to translate roles between Gemini-Pro and Streamlit terminology
    def translate_role_for_streamlit(user_role):
        if user_role == "model":
            return "assistant"
        else:
            return user_role


    # Initialize chat session in Streamlit if not already present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])


    # Display the chatbot's title on the page
    st.title("🤖 BOT GILMOR")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input(f"Ask {st.session_state.selected_option}")
    if user_prompt:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
        # st.write(f"You selected: {st.session_state.selected_option}")

def main():
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    # Set up Google Gemini-Pro AI model
    gen_ai.configure(api_key=GOOGLE_API_KEY)
    model = gen_ai.GenerativeModel('gemini-pro')
    if 'next_screen' not in st.session_state:
        st.session_state.next_screen = False

    if not st.session_state.next_screen:
        home_screen()
    else:
        next_screen()

if __name__ == "__main__":
  main()
