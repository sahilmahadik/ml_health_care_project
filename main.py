import time
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from Database.database import MyDatabase
from Hepatitis import hepatitis_pred
from Diabetes import diabetes_pred
from Heart import heart_pred

main_header = st.empty()
image_header = st.empty()

html_temp = """
            <div style="background-color:red;padding:10px;border-radius:10px;margin-bottom:10px;">
            <h1 style="color:white;text-align:center;">Health Care Project </h1>
            <h5 style="color:white;text-align:center;"> Machince Learning </h5>
            </div>
                <div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px; margin-bottom:10px;">
            <h3 style="text-align:justify;color:black;padding:10px">Home</h3>
            <p style="font-size:larger; padding-left:11px;">This HealthCare Project is modern way of take care of people around you in modern way nowdays because Machince are getting evolved to work like human in better than that in every future field industry   .</p>
            </div>
            """

@st.cache(allow_output_mutation=True)
def load_image():
    image = Image.open('img.jpeg')
    return image

main_header.markdown(html_temp,unsafe_allow_html=True)

with st.container():
    with image_header:
        img = load_image()
        st.image(img, caption='HealthCare with Machince Learning',width=600)

with st.sidebar:
    choice = st.selectbox('Menu',options=['Home','Login','SignUp'])

if choice == "Login":
    Login_Obj = MyDatabase()

    user_container = st.sidebar.empty()
    passw_container = st.sidebar.empty()
    login_container = st.sidebar.empty()
    logout_container = st.sidebar.empty()

    username = user_container.text_input("Username", key="uname")
    password = passw_container.text_input("Password",key='upass')

    if 'Menu' not in st.session_state:
        st.session_state.Menu = False


    def logout_btn():
        try :
            st.session_state.uname = ""
            st.session_state.upass = ""
            st.session_state.Menu = False
        except:
            st.session_state.Menu = False

    def disabled_checkbox():
        login_container.empty()


    if st.session_state.uname != "" and st.session_state.upass != "" and Login_Obj.check_login(st.session_state.uname,st.session_state.upass):
        if login_container.checkbox("login",key='log_checkbox'):
            user_container.empty()
            passw_container.empty()
            disabled_checkbox()
            st.session_state.Menu = True
            main_header.empty()
            image_header.empty()
            
            if st.session_state.Menu == True:
                with st.sidebar:
                        selected = option_menu("Main Menu", ["Hepatitis","Diabetes","Heart"], 
                        icons=['activity',"droplet-fill","heart-fill"], menu_icon="cast", default_index=0,orientation="vertical")
                if selected == "Hepatitis":
                    hepatitis_pred.hepatitis()
                elif selected == "Diabetes":
                    time.sleep(2)
                    diabetes_pred.diabetes()
                elif selected == "Heart":
                    time.sleep(2)
                    heart_pred.heart()

            st.sidebar.button("Logout",on_click=logout_btn)
    else:
        login_container.checkbox("login",disabled=True)

elif choice == "SignUp":
    st.header("Free SignUP Account")
    main_header.empty()
    image_header.empty()
    SignUp = MyDatabase()
    new_username = st.text_input("User name")

    col1,col2 = st.columns([3,3])
    new_password = col1.text_input("Password", type='password')
    confirm_password = col2.text_input("Confirm Password",type='password')

    if st.button("Submit"):
        SignUp.check_signup(new_username,new_password,confirm_password)
