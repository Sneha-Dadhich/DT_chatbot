import streamlit as st
import pandas as pd
import warnings
import flask as f
import random
import pyttsx3 as psp
import webbrowser as web
import wikipedia 
import time as t
import requests
from streamlit.components.v1 import html

# Filter out warnings related to Streamlit widget keys
warnings.filterwarnings("ignore")

#BACKEND

# CHATBOT BACKEND
responses = {
    "hi": ["Hello!", "Hi there!", "Hey!"],
    "how are you?": ["I'm good, thank you!", "I'm doing well, thanks for asking.", "All good!"],
    "what's your name?": ["I'm just a humble chatbot.", "I'm your friendly neighborhood bot!", "You can call me ChatBot."],
    "bye": ["Goodbye!", "See you later!", "Bye! Take care!"]
}

#fetch data from wikipedia 
def fetch_wiki_results(user_input):
    result=wikipedia.summary(user_input,sentences=5)
    return result
    
# Function to 
def generate_response(user_input):
    user_input = user_input.lower()
    if user_input in responses:
        return random.choice(responses[user_input])
    else:
        try:
            results = fetch_wiki_results(user_input)
            return results
        except(wikipedia.exceptions.PageError):
            return "Sorry Result Not Found"
        except(wikipedia.exceptions.DisambiguationError):
            return "The given word have multiple answers . Please be specific"


#Fetching the data
file="C:\\Sneha\\Programs1\\Python\\Internship\\DreamTeam\\Chatbot_part1\\Login_file.csv"
df = pd.read_csv(file,header=None)
data = dict(zip(df[0], df[1]))

# Extract usernames and passwords from DataFrame
usernames = list(df[0])
passwords = list(df[1])

#LOGIN AND REGISTRATION BACKEND
def login_check_pass(username, password):
# Checking the constraints of the data for login

    if username in usernames:
        if password == data[username]:  # Check if password matches for the given username    
            return 1  # Successful login
        else:
            password=st.error("Invalid password")
            return 0  # Incorrect password
    else:
        username=st.error("Invalid username")
        return 0  # Username not found

#Checking the constraints of the data for registration
def regis_check_pass(username,password,confirm_password):
    if(confirm_password==password and username not in usernames and " " not in username and password ):
        global file
        with open(file, 'a') as file:
            file.write(f"{username},{password}\n")
        return 1
    elif(" " in username):
        username = st.error("Please don't add space in username")
        return 0
    elif(" " in password):
        password = st.error("Please don't add space in username")
        return 0
    elif(username==""):
        username = st.error("Please write username")
        return 0
    elif(password==""):
        password = st.error("Please write password")
        return 0
    elif(confirm_password==""):
        username = st.error("Please write confirmation password")
        return 0
    elif(username in usernames):
        username = st.error("Username already exists")
        return 0    
    elif(confirm_password!=password):
        confirm_password=st.error("Confirmation password does not match given password")
        return 0


#FRONTEND
st.markdown(
        """
        <style>
            .st.title 
            {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction:row
            } 
            .stRadio 
            {
                display: flex;
                bottom: 50px
            }
        .stTextInput {
            background-color: #51e2f5 !important;
            padding-left: 10px !important;
            padding-top:10 px;    
            margin-left:0px;
            border-radius: 10px !important; /* Adjust the radius as needed */
        }
        .stTextArea {
            background-color: #9df9ef !important;
            padding-right: 10px !important;
            padding-top:10 px;
            margin-right:10px;
            border-radius: 10px !important; /* Adjust the radius as needed */      
        }
        .stButton>button {
            background-color: #a0d2eb !important;
            color: white !important;
            font-weight: bold !important;
        }
        .stsidebar
            {
            background-color: #e8f9fd !important;
            font-weight: bold !important;
            top:
            }
        .header
            {
            position: fixed;
            top:10px;
            font-size:15px;
            }
        </style>

        """,
        unsafe_allow_html=True
    )

return_heading=True

def chats(input_index):
    user_input = st.text_input("User Input",key=f"input{input_index}")
    input_index=input_index+1
    if user_input:
        # Call the chatbot function to generate a response
        bot_response = generate_response(user_input)
        # Display the chatbot response
        st.text_area("Chatbot Response", value=bot_response, height=200)
        history=st.sidebar.button(user_input,use_container_width=15,key=f"sidebar_button{input_index}")
     
        # Calls the new chatbot for new command
        return_heading=False
        chats(input_index+1)

# def close_form():
#     st.session_state.form_open = False

# show_chat=False

def login__register():
    b=st.empty()
    st.title("DT Bot :)")
    page_options = ["Login", "Register"]

    choice=b.radio("Would you like to :       ",options=page_options,horizontal=True,label_visibility="collapsed")    
    if choice=="Register":
        with st.form("Registration",clear_on_submit=False):
            st.title("Registration Page")

            # Load an image from a file
            #image_url="C:\\Users\\HP\\Pictures\\Camera Roll\\DT_chatbotImages.jpg"
            #image = st.file_uploader(image_url, type=["jpg"])
            #st.sidebar.image(image_url, caption='Uploaded Image', use_column_width=True)

            username = st.text_input("Username")
            password = st.text_input("Password",key="pass1")
            confirm_password=st.text_input("Confirm Password",key="pass2")
            st.form_submit_button("Register")

        if 'FormSubmitter:Login-Login':
            if regis_check_pass(username,password,confirm_password):
                st.success("Logged in as {}".format(username))
                t.sleep(2)
                
                # You can redirect the user to another page or do other actions here after successful login
                #st.experimental_rerun()
    else:
        a=st.empty()
        with a.container():
            with a.form("Login"):
                st.title("Login Window")

                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                st.form_submit_button("Login")
    
        if 'FormSubmitter:Login-Login':
                if login_check_pass(username,password):
                    a.success("Logged in as {}".format(username))
                    a.empty()
                    b.empty()
                    main()
        else:
            pass
                        

def main():
    st.title('Dreamteam Chatbot')
    #Sidebar for additional features 
    st.sidebar.header('History')
   

    chats(1)

if __name__=="__main__":
    login__register()