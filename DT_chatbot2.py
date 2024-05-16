import streamlit as st
import pandas as pd
import random
import wikipedia 
import requests
import time as t
import csv
import fileinput
import base64

# CHATBOT BACKEND
responses = {
    "hi": ["Hello!", "Hi there!", "Hey!"],
    "how are you?": ["I'm good, thank you!", "I'm doing well, thanks for asking.", "All good!"],
    "what is your name?": ["I'm just a humble chatbot.", "I'm your friendly neighborhood bot!", "You can call me ChatBot."],
    "bye": ["Goodbye!", "See you later!", "Bye! Take care!"]
}

# Fetch data from wikipedia 
def fetch_wiki_results(user_input):
    result = wikipedia.summary(user_input, sentences=5)
    return result
    
# Function to generate response
def generate_response(user_input, username):
    user_input = user_input.lower()
    file_url = f"C:\\Sneha\\Programs1\\Python\\Internship\\DreamTeam\\Chatbot_part1\\{username}.csv"
    try:
        if user_input in responses.keys():
            file=open(file_url,"a+")
            file.write(f"{user_input}, \n")
            file.close()
            return random.choice(responses[user_input])
        else:
            results = fetch_wiki_results(user_input)
            file=open(file_url,"a")
            file.write(f"{user_input}, \n")
            file.close()
            return results
        
    except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
        return "Sorry, result not found"
    except requests.exceptions.ConnectionError:
        return "Sorry, there is no internet connection"
    except(wikipedia.exceptions.WikipediaException):
        pass

# Fetching the data
file = "C:\\Sneha\\Programs1\\Python\\Internship\\DreamTeam\\Chatbot_part1\\Login_file.csv"
df = pd.read_csv(file, header=None)
data = dict(zip(df[0], df[1]))

# Extract usernames and passwords from DataFrame
usernames = list(df[0])
passwords = list(df[1])

# Login and registration backend
def login_check_pass(username, password):
    if username in usernames:
        if password == data[username]:
            folder_url = f"C:\\Sneha\\Programs1\\Python\\Internship\\DreamTeam\\Chatbot_part1\\{username}.csv"
            return 1  # Successful login
        else:
            return 0  # Incorrect password
    else:
        return 0  # Username not found

def regis_check_pass(username, password, confirm_password):
    file = f"C:\\Sneha\\Programs1\\Python\\Internship\\DreamTeam\\Chatbot_part1\\Login_file.csv"
    
    if confirm_password == password and username not in usernames and " " not in username and password:
        with open(file, 'a') as file:
            file.write(f"\n{username},{password}")
        
        folder_url = f"C:\\Sneha\\Programs1\\Python\\Internship\\DreamTeam\\Chatbot_part1\\{username}.csv"
        with open(folder_url, "w") as f:
            f.write("________,\n")
        return 1
    elif " " in username or " " in password:
        return 0
    elif username == "" or password == "" or confirm_password == "":
        return 0
    elif username in usernames:
        return 0
    elif confirm_password != password:
        return 0

# Frontend

bg_image_url="C:\\Sneha\\Programs1\\Python\\Internship\\DreamTeam\\Chatbot_part1\\DT_bg_image.jpg"

#st.set_png_as_page_bg(bg_image_url)
# Your Streamlit code here

login_regis_css=f"""
      <style>
        .stApp 
        {{
          background: url(data:image/{bg_image_url};base64,{base64.b64encode(open(bg_image_url, "rb").read()).decode()});
        }}
        [data-testid=stHeading] 
        {{  
            position:relative;
            height:5%;
            padding-left:35%;
        }}
        [data-testid=stVerticalBlock]
        {{
            height:0;
        }}
        [data-testid=stVerticalBlockBorderWrapper] 
        {{
            background-color: #FFFFF0;
            opacity: 0.80; 
            border-radius: 10px;
            display:flex;  
        }}
        .stTextInput 
        {{
            padding-left:5% !important;
            width: 90%;
            border-radius: 10px !important; /* Adjust the radius as needed */
            opacity:1 !important;
        }}
        .stTextArea 
        {{
            background-color: #9df9ef !important;
            margin-right: 10px;
            border-radius: 10px !important; /* Adjust the radius as needed */      
        }}
        .stButton > button 
        {{
            display:flex;
            color: black;
            font-weight: bold !important;
            width: 10%; /* Setting the width of the button to 95% of its container */
            opacity:1 !important;
        }}
        div.row-widget.stRadio
        {{
            border-radius: 5px;
            padding-top: 20px !important;
            border-bottom: 1px solid rgba(128, 128, 128, 0.2);
        }}
        div.row-widget.stRadio > div[role="radiogroup"]  
        {{
            display:flex;
            flex-direction:row;
            justify-content:center;      
            gap:50px;
            font-weight:bold;
        }}
        div.row-widget.stRadio > [data-testid=stWidgetLabel]  
        {{
            display:flex;
            flex-direction:row;
            justify-content:center;
            font-weight:bold;                    
        }}    
      </style>
      """


chat_css=f"""
        <style>
        .stApp 
        {{
          background: url(data:image/{bg_image_url};base64,{base64.b64encode(open(bg_image_url, "rb").read()).decode()});
        }}
        .stTextInput 
        {{
            padding-left: 10px !important;
            padding-top: 10px;    
            margin-left: 0px;
            border-radius: 10px !important; /* Adjust the radius as needed */
        }}
        [data-testid=stSidebar]
        {{
            padding-left: 0px; 
            padding-right: 0px; 
            margin-top: 10 px;
            background-color:  #36454F50;
            opacity:0.8;
        }}
        .stTextArea 
        {{
            padding-right: 10px !important;
            padding-top: 10px;
            margin-right: 10px;
            border-radius: 10px !important; /* Adjust the radius as needed */      
        }}
        [data-testid=.stVerticalBlockBorderWrapper]
        {{
            background-color:transparent !important;
        }}
        .stButton > button 
        {{
            display: flex;
            font-weight: bold !important;
            width: 90%; /* Setting the width of the button to 90% of its container */
            align-content: center; 
            justify-content: center;
        }}
        </style>
        """
      
def apply_css(css):
    st.markdown(css,unsafe_allow_html=True)

def chats(input_index, username):    
    apply_css(chat_css)
    i=-1*input_index
    file_url = f"C:\\Sneha\\Programs1\\Python\\Internship\\DreamTeam\\Chatbot_part1\\{username}.csv"            
    df = pd.read_csv(file_url)

    # Get the last 5 rows
    history = df.tail().drop_duplicates()
    history = history.sort_index(ascending=False)
    history = history.drop_duplicates()
    history=history.values
            
    temp_sidebar = st.empty()
    with temp_sidebar.container():
        index = 0
        for h in history:
            st.sidebar.button(h[0], key=f"sd{input_index}{index}")
            index += 1

    user_input = st.text_input("You:", key=f"{input_index}",value="")
    #,style=" background-image: url(f'C:\\Users\\HP\\Pictures\\DT_bg_image.jpg');background-size: cover;"
    #print(user_input)
    if user_input:
        temp_sidebar.empty()      
        # Call the chatbot function to generate a response
        bot_response = generate_response(user_input, username)
        # Display the bot response in a text area
        st.text_area(f"Chatbot Response {input_index}", value=f"{bot_response}",  height=200, key=f"sidebar{input_index}")
        
        # if(i<-1): #delete previous data
        #     file=open(file_url,"w+")
        #     #line=file.read()
        #     file.write(user_input)
        #     file.close()
        #     print("file updated")
        
        # Calls the new chatbot for new command 
        chats(input_index + 1, username)
        
def login__register():
    apply_css(login_regis_css)
    b = st.empty()
    st.title("DT Bot :)")
    #st.header("DT Bot :)")
    page_options = ["Login", "Register"]

    choice = b.radio("Would you like to:", options=page_options, horizontal=True, key="login_register_radio")    
    if choice == "Register":
        with st.form("Registration", clear_on_submit=False):
            st.title("Registration Page")

            username = st.text_input("Username",key="regis_username")
            password = st.text_input("Password", key="regis_pass")
            confirm_password = st.text_input("Confirm Password", key="confirm_pass")
            st.form_submit_button("Register")

        if 'FormSubmitter:Registration-Submit':
            if regis_check_pass(username, password, confirm_password):
                st.success("Registered successfully! Please login now.")
                t.sleep(2)
    else:
        a = st.empty()
        with a.container():
            with a.form("Login"):
                st.title("Login Window")

                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                st.form_submit_button("Login")
    
        if 'FormSubmitter:Login-Submit':
                if login_check_pass(username, password):
                    a.success("Logged in as {}".format(username))
                    a.empty()
                    b.empty()
                    main(username)
                    
        else:
            pass
                        
def main(username):
    st.title('Dreamteam Chatbot')
    st.sidebar.header('History')
    chats(1, username)

if __name__ == "__main__":
    login__register()
