import random

import streamlit as st
from PIL import Image


import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


import joblib
from streamlit_option_menu import option_menu

@st.cache(allow_output_mutation=True)
def scale_data(new_data):
    data = pd.read_csv("Heart/dataset/heart.csv")
    sc = StandardScaler()
    col_to_scale = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
    data[col_to_scale] = sc.fit_transform(data[col_to_scale]) 

    new_data[col_to_scale] = sc.transform(new_data[col_to_scale])  
    return new_data




def heart():

    columns_name = ["age","sex"	,"cp","trestbps","chol","fbs","restecg","thalach","exang","oldpeak","slope","ca","thal"]
    gender_dict = {"Male":1,"Female":0}
    fbs_dict = {"True":1,"False":0}
    exang_dict = {"Yes":1,"No":0}



    # restecg = {"Normal":0,"Having ST-T Wave abnormality ":1,"Showing Probable":2}
    # slope  = {"up slope":0,"flat slope":1,"down slope":2}
    # thal = {"fixed detect":1,"normal blood flow":2,"reversable defect":3}    


    chest_pain_str = """Chest Pain\n
                        \n0 : Typical Angina
                        \n1 : Atypical Angina
                        \n2 : Non-Anginal Pain
                        \n3 : Asymptomatic"""

    trestbps_str = """ Resting Blood Pressure (trestbps):\n \nThe person's resting blood pressure (mm Hg on admission to the hospital)"""

    fbs_str = """ Fasting blood sugar > 120 mg/dl\n"""

    restecg_str= """Resting Electrocardiographic (restecg)\n
                    \n0: normal
                    \n1: having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV)
                    \n2: showing probable or definite left ventricular hypertrophy by Estes' criteria"""

    thalach_str = """Maximum Heart Rate Achieved"""


    oldpeak_str = """Stress test depression induced by exercise relative to rest"""

    slope_str=""" Slope for the Peak Exercise ST segment\n
                    \n 1: Upsloping
                    \n 2: Flat
                    \n 3: Downsloping"""

    ca_str=""" Number of major vessels (0-3) colored by fluoroscopy"""

    thal_str = """A blood disorder called Thalassemia\n
                    \n1: Fixed defect (no blood flow in some part of the heart)
                    \n2: Normal blood flow
                    \n3: Reversible defect (a blood flow is observed but it is not normal)"""

        # feature_dict = {"No":1,"Yes":2}
    html_temp = """
        <div style="background-color:red;padding:10px;border-radius:10px;margin-bottom:10px;">
        <h1 style="color:white;text-align:center;">Heart Disease Prediction </h1>
        <h5 style="color:white;text-align:center;">Machince Learning </h5>
        </div>
        """

    descriptive_message_temp ="""
    <div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px; margin-bottom:10px;">
        <h3 style="text-align:justify;color:black;padding:10px">Definition</h3>
        <p style="font-size:larger; padding-left:11px;">Heart disease is a selection of diseases and conditions that cause cardiovascular problems. Each type of heart disease is caused by something entirely unique to that condition. Atherosclerosis and CAD result from plaque buildup in the arteries
</p>
    </div>
    """
    


    @st.cache(allow_output_mutation=True)
    def load_image():
        image = Image.open('Heart/img.jpg')
        return image

    def get_value(val,my_dict):
        for key,value in my_dict.items():
            if val == key:
                return value

    st.markdown(html_temp,unsafe_allow_html=True)


    with st.container():
        selected = option_menu(None, ["Home","Predict"], 
        icons=['house','bar-chart','search'], menu_icon="cast", default_index=0,orientation="horizontal")


    if selected == "Home":
        st.markdown(descriptive_message_temp,unsafe_allow_html=True)
        img = load_image()
        with st.container():
            st.image(img, caption='Heart Image',width=500)


    elif selected == "Predict":
        def random_fun(*args,**kwargs):
            st.session_state.sex = random.choice(list(gender_dict.keys()))
            st.session_state.exang = random.choice(list(exang_dict.keys()))
            st.session_state.fbs = random.choice(list(fbs_dict.keys()))

            st.session_state.age = random.randint(31,75)
            st.session_state.cp = random.randint(0,3)
            st.session_state.trestbps = random.randint(94,200)

            st.session_state.chol = random.randint(126,564)
            st.session_state.restecg = random.randint(0,2) 
            st.session_state.thalach = random.randint(72,202)


            st.session_state.oldpeak = round(random.uniform(0.01,6.10),1)
            st.session_state.slope = random.randint(0,2) 
            st.session_state.ca = random.randint(0,4)

            st.session_state.thal = random.randint(1,3)


        with st.form("my"):
            r1,r2,r3 = st.columns([2,2,2])
            sex = r1.radio("Sex",tuple(gender_dict.keys()),key='sex')
            fbs = r2.radio("Fasting Blood Sugar",tuple(fbs_dict.keys()),key='fbs',help=fbs_str)
            exang = r3.radio("Exercise Induced Angina",tuple(exang_dict.keys()),key='exang')

            # sex = st.radio("Sex",tuple(gender_dict.keys()),key='sex')


            col1,col2,col3 = st.columns([1,1,1])
            age = col1.number_input("Age",min_value=29,max_value=77,key="age")
            cp = col2.number_input("Chest Pain",min_value=0,max_value=3,key='cp',help=chest_pain_str)
            trestbps = col3.number_input("Resting Blood Pressure",min_value=38,max_value=200,key='trestbps', help=trestbps_str)

            col4,col5,col6 = st.columns([1,1,1])
            chol =  col4.number_input("Cholestoral",min_value=126,max_value=564,key='chol',help="serum cholestoral in mg/dl")
            restecg = col5.number_input("Resting Electrocardiographic",min_value=0,max_value=2,key='restecg',help=restecg_str)
            thalach =  col6.number_input("Thalach",min_value=71,max_value=202,key='thalach',help=thalach_str)

            col7,col8,col9 = st.columns([1,1,1])
            oldpeak = col7.number_input("Oldpeak",min_value=0.00,max_value=6.20,key='oldpeak',help=oldpeak_str)
            slope = col8.number_input("Slope",min_value=0,max_value=2,key='slope',help=slope_str)
            ca = col9.number_input("ca",min_value=0,max_value=4,key="ca",help=ca_str)

            thal =  st.number_input("Thal",min_value=1,max_value=3,key='thal',help=thal_str)


            feature_list = [age,get_value(sex,gender_dict) ,cp	,trestbps,chol,get_value(fbs, fbs_dict),restecg,thalach,get_value(exang,exang_dict),oldpeak,slope,ca,thal]

            pretty_result = {"Sex":sex,"Fasting Blood Sugar":fbs,"Exercise Induced Angina":exang,"Age":age,"Chest Pain": cp,"Resting Blood Pressure":trestbps,"Cholestoral":chol,
                            "Resting Electrocardiographic":restecg,"Thalach":thalach,"Oldpeak":oldpeak,"Slope":slope,"ca":ca,"Thal":thal}
            single_sample = np.array(feature_list,dtype=object).reshape(1,-1)

            st.form_submit_button("Submit",)	
            st.form_submit_button('Random Input',on_click=random_fun)

        if st.checkbox("Show/Hide Input "):
            st.json(pretty_result)

        data = pd.DataFrame(single_sample,columns=columns_name)
        # st.write(std_data)

        model_choice = st.selectbox("Select Model",["KNN"])	
        if st.button("Predict"):
            data = pd.DataFrame(single_sample,columns=columns_name)
            std_data = scale_data(data)
            if model_choice == "KNN":
                loaded_model = joblib.load('Heart/models/Heart_KNN.pkl','r+')
                prediction =loaded_model.predict(std_data)
                pred_prob  =loaded_model.predict_proba(std_data)
        
            pred_probability_score = {"Non-Diabetes":round((pred_prob[0][0]*100), 2),"Diabetes":round((pred_prob[0][1]*100), 2)}

            if prediction == 1:
                st.error("Patients 💔 Heart Problem")
                st.subheader("Prescriptive Analytics")

                st.markdown(f"""<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
                            <h4 style="color:white;text-align:center;">Algorithm:: {model_choice}</h4>
                            <br/>	
                            <p style="text-align:justify;color:white">{pred_probability_score["Diabetes"]} % probalibilty that Patients Die</p>
                            </div>""",unsafe_allow_html=True)


            else:
                st.success("Patients 💖 Heart is Health")
                st.subheader("Prescriptive Analytics")

                st.markdown(f"""<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
                    <h4 style="color:white;text-align:center;">Algorithm:: {model_choice}</h4>
                    <br/>	
                    <p style="text-align:justify;color:white">{pred_probability_score["Non-Diabetes"]} % probalibilty that Patients Live</p>
                    </div>
                    """,unsafe_allow_html=True)





if __name__ == '__main__':
    heart()
