# Refer to https://www.youtube.com/watch?v=BHwVRI9N8B0&t=327s
import openai
import streamlit as st
from streamlit_chat import message


#api_secret is taken from the file, secrets.toml from the folder with path, /Users/Machintosh/.streamlit
openai.api_key = st.secrets["api_secret"]
#api_secret = "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" Dr Lai
#api_secret = "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" mine

# creating a function which will generate the calls from the api
def generate_response(prompt, temperature):
    try:
        completions = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-0613:personal::8gVyTjRE",  # This should match the available chat models
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        # Extract the response message
        message_content = completions.choices[0].message['content']
        return message_content
    except Exception as e:
        return f"Error: {e}"


# Main Streamlit code
def main():

    # Display image
    st.sidebar.image("/Users/Machintosh/Downloads/bot.webp", use_column_width=True) #,caption="GPT–EMR")

    # Create a slider for temperature
    temperature = st.sidebar.slider('Creativity of generated responses', min_value=0.1, max_value=1.0, step=0.1, value=0.5)
    #st.sidebar.write("Adjust temperature with low temperature for accurate response, high temperature for creativity.")


    # Display title
    st.title("GPT–EMR Chatbot")

    # Display prompt box
    def get_text():
        input_text = st.text_area("Medical Inquiries: ", key="input")
        return input_text

    # Define user input
    user_input = get_text()

    if user_input:
        # Generate response
        response = generate_response(user_input, temperature)

        # Insert the user input at the beginning of the list
        st.session_state['past'].insert(0, user_input)  # This is the user input (prompt)

        # Insert the generated response just after the user input
        st.session_state['past'].insert(1, response)  # This is the generated response

    # create empty container to store the chat
    if 'past' not in st.session_state:
        st.session_state['past'] = []

    if st.session_state['past']:
        for i in range(len(st.session_state['past'])):
            is_user = i % 2 == 0  # True if i is even, False if i is odd
            key = str(i) + ('_user' if is_user else '_generated')
            bot_image = ("https://raw.githubusercontent.com/LimVictoria/GPT-EMR-Chatbot/main/bot.webp")
            avatar_style = "adventurer" if is_user else bot_image  # Set avatar style to "adventurer" for user messages and "dinosaur" for bot messages
            message(st.session_state['past'][i], is_user=is_user, key=key, avatar_style=avatar_style)



if __name__ == '__main__':
    main()

        # Clear the generated responses from the previous session
        # st.session_state['generated'] = []

        # Display response
        #message(user_input, is_user=True)  # Displaying user input
        #message(response)  # Displaying generated response

        # Store the output
        #st.session_state['past'].append(user_input)  # This is the user input (prompt)
        #st.session_state['past'].append(response)  # This is the generated response