import random

import streamlit as st
from PIL import Image
import numpy as np

import joblib

from streamlit_option_menu import option_menu

def diabetes():
    html_temp = """
        <div style="background-color:red;padding:10px;border-radius:10px;margin-bottom:10px;">
        <h1 style="color:white;text-align:center;">Diabetes Prediction </h1>
        <h5 style="color:white;text-align:center;">Machince Learning </h5>
        </div>
        """

    descriptive_message_temp ="""
    <div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px; margin-bottom:10px;">
        <h3 style="text-align:justify;color:black;padding:10px">Definition</h3>
        <p style="font-size:larger; padding-left:11px;">Diabetes is a chronic disease that occurs when the pancreas is no longer able to make insulin, or when the body cannot make good use of the insulin it produces.</p>
    </div>
    """


    @st.cache(allow_output_mutation=True)
    def load_image():
        image = Image.open('Diabetes/img.jpg')
        return image

    st.markdown(html_temp,unsafe_allow_html=True)


    with st.container():
        selected = option_menu(None, ["Home","Predict"], 
        icons=['house','bar-chart','search'], menu_icon="cast", default_index=0,orientation="horizontal")


    if selected == "Home":
        st.markdown(descriptive_message_temp,unsafe_allow_html=True)
        img = load_image()
        with st.container():
            st.image(img, caption='Diabetes Image',width=700)


    elif selected == "Predict":
    # 	Glucose	BloodPressure	SkinThickness	Insulin	BMI	DiabetesPedigreeFunction	Age
        def random_fun(*args,**kwargs):
            st.session_state.Age = random.randint(21,66)
            st.session_state.Pregnancies = random.randint(1,13)
            st.session_state.Glucose = random.randint(44,198)
            st.session_state.BloodPressure = random.randint(38,106)
            st.session_state.SkinThicknessue = random.randint(1,60)
            st.session_state.Insulin = random.randint(1,318)
            st.session_state.BMI = round(random.uniform(18,50),2)
            st.session_state.DiabetesPedigreeFunction = round(random.uniform(0,1),2)


        with st.form("my"):
            col1,col2 = st.columns([3,3])
            age = col1.number_input("Age",min_value=21,max_value=66,key="Age")
            pregnancies =  col2.number_input("Pregnancies",min_value=1,max_value=13,key='Pregnancies')


            col3,col4,col5 = st.columns([2,2,2])
            glucose = 	col3.number_input("Glucose",min_value=44,max_value=198,key='Glucose')
            bloodpressure = col4.number_input("BloodPressure",min_value=38,max_value=106,key='BloodPressure')
            skinthickness = 	col5.number_input("SkinThickness",help="Sahil1",min_value=1,max_value=60,key='SkinThickness')



            col6,col7,col8 = st.columns([2,2,2])
            insulin = 	col6.number_input("Insulin",min_value=1,max_value=318,key='Insulin')
            bmi = 	col7.number_input("BMI",min_value=18.00,max_value=50.00,key='BMI')
            diabetespedigreefunction = 	col8.number_input("DiabetesPedigreeFunction",min_value=0.00,max_value=1.00,help="Sahil",key='DiabetesPedigreeFunction')

            feature_list = [pregnancies,glucose,bloodpressure,skinthickness,insulin,bmi,diabetespedigreefunction,age]

            pretty_result = {"Age":age,"Pregnancies":pregnancies,"Glucose":glucose,"BloodPressure":bloodpressure,"SkinThickness": skinthickness,"Insulin":insulin,"BMI":bmi,
                            "DiabetesPedigreeFunction":diabetespedigreefunction}
            single_sample = np.array(feature_list).reshape(1,-1)

            st.form_submit_button("Submit",)	
            st.form_submit_button('Random Input',on_click=random_fun)

        if st.checkbox("Show/Hide Input "):
            st.json(pretty_result)

        model_choice = st.selectbox("Select Model",["Logistic Regression","Random Forest","Support Vector Classifier"])	
        if st.button("Predict"):
            if model_choice == "Logistic Regression":
                loaded_model = joblib.load('Diabetes/models/Diabetes_Logistic_Regression.pkl','r+')
                prediction =loaded_model.predict(single_sample)
                pred_prob  =loaded_model.predict_proba(single_sample)

            if model_choice == "Random Forest":
                loaded_model = joblib.load('Diabetes/models/Diabetes_Random_Forest.pkl','r+')
                prediction =loaded_model.predict(single_sample)
                pred_prob  =loaded_model.predict_proba(single_sample)

            if model_choice == "Support Vector Classifier":
                loaded_model = joblib.load('Diabetes/models/Diabetes_Support_Vector_Classifier.pkl','r+')
                prediction =loaded_model.predict(single_sample)
                pred_prob  =loaded_model.predict_proba(single_sample)

            pred_probability_score = {"Non-Diabetes":round((pred_prob[0][0]*100), 2),"Diabetes":round((pred_prob[0][1]*100), 2)}

            if prediction == 1:
                st.error("Patients is Diabetes")
                st.subheader("Prescriptive Analytics")

                st.markdown(f"""<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
                            <h4 style="color:white;text-align:center;">Algorithm:: {model_choice}</h4>
                            <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
                            <br/>
                            <br/>	
                            <p style="text-align:justify;color:white">{pred_probability_score["Diabetes"]} % probalibilty that Patients Die</p>
                            </div>""",unsafe_allow_html=True)


            else:
                st.success("Patients is Non-Diabetes")
                st.subheader("Prescriptive Analytics")

                st.markdown(f"""<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
                    <h4 style="color:white;text-align:center;">Algorithm:: {model_choice}</h4>
                    <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
                    <br/>
                    <br/>	
                    <p style="text-align:justify;color:white">{pred_probability_score["Non-Diabetes"]} % probalibilty that Patients Live</p>
                    </div>
                    """,unsafe_allow_html=True)



if __name__ == '__main__':
    diabetes()
