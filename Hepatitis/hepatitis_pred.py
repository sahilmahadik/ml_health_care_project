import random
import time

import streamlit as st
from PIL import Image


import pandas as pd
import numpy as np

import joblib



from streamlit_option_menu import option_menu


def hepatitis():
    gender_dict = {"Male":1,"Female":2}
    feature_dict = {"No":1,"Yes":2}

    def get_value(val,my_dict):
        for key,value in my_dict.items():
            if val == key:
                return value 

    def get_fvalue(val):
        feature_dict = {"No":1,"Yes":2}
        for key,value in feature_dict.items():
            if val == key:
                return value 

    html_temp = """
        <div style="background-color:red;padding:10px;border-radius:10px;margin-bottom:10px;">
        <h1 style="color:white;text-align:center;">Hepatitis Disease Prediction </h1>
        <h5 style="color:white;text-align:center;">Hepatitis B </h5>
        </div>
        """

    descriptive_message_temp ="""
    <div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px; margin-bottom:10px;">
        <h3 style="text-align:justify;color:black;padding:10px">Definition</h3>
        <p style="font-size:larger; padding-left:11px;">Hepatitis B is a viral infection that attacks the liver and can cause both acute and chronic disease.</p>
    </div>
    """


    @st.cache(allow_output_mutation=True)
    def load_image():
        image = Image.open('Hepatitis/images/hepatitis-B.jpg')
        return image

    st.markdown(html_temp,unsafe_allow_html=True)


    with st.container():
        selected = option_menu(None, ["Home","Predict"], 
        icons=['house','search'], menu_icon="cast",orientation="horizontal")


    if selected == "Home":
        st.markdown(descriptive_message_temp,unsafe_allow_html=True)
        img = load_image()
        with st.container():
            st.image(img, caption='Hepatitis B Virus')

    else:
        def random_fun(*args,**kwargs):
            st.session_state.age = random.randint(7,80)
            st.session_state.sex = random.choice(list(gender_dict.keys()))
            st.session_state.steroid = random.choice(list(feature_dict.keys()))
            st.session_state.antivirals = random.choice(list(feature_dict.keys()))
            st.session_state.fatigue = random.choice(list(feature_dict.keys()))
            st.session_state.spiders = random.choice(list(feature_dict.keys()))
            st.session_state.ascites = random.choice(list(feature_dict.keys()))
            st.session_state.varices = random.choice(list(feature_dict.keys()))
            

            st.session_state.bilirubin = round(random.uniform(0.00, 8.0),2)
            st.session_state.alk_phosphate = round(random.uniform(0.0,296.0),2)
            st.session_state.sgot = round(random.uniform(0.0,648),2)
            st.session_state.albumin = round(random.uniform(0.0,6.4),2)
            st.session_state.protime = round(random.uniform(0.0,100.0),2)
            st.session_state.histology =  random.choice(list(feature_dict.keys()))

        with st.form("my"):
            age = st.number_input("Age",7,80,key="age")

            r1,r2,r3 = st.columns([3,3,3,])
            st.write("\n")
            r4,r5,r6,r7 = st.columns([3,3,2,3])
            sex = 		r1.radio("Sex",tuple(gender_dict),key='sex')
            steroid = 	r2.radio("Do You Take Steroids?",tuple(feature_dict.keys()),key='steroid')
            antivirals = r3.radio("Do You Take Antivirals?",tuple(feature_dict.keys()),key='antivirals')
            fatigue = 	r4.radio("Do You Have Fatigue",tuple(feature_dict.keys()),help="Sahil1",key='fatigue')
            spiders = 	r5.radio("Presence of Spider Naeve",tuple(feature_dict.keys()),key='spiders')
            ascites = 	r6.radio("Ascities",tuple(feature_dict.keys()),key='ascites')
            varices = 	r7.radio("Presence of Varices",tuple(feature_dict.keys()),help="Sahil",key='varices')
            
            n1,n2,n3 = st.columns([3,3,3])
            n4,n5,n6 = st.columns([3,3,3])
            bilirubin = n1.number_input("bilirubin Content",0.0,8.0,key="bilirubin")
            alk_phosphate = n2.number_input("Alkaline Phosphate Content",0.0,296.0,key='alk_phosphate')
            sgot = n3.number_input("Sgot",0.0,648.0,key='sgot')
            albumin = n4.number_input("Albumin",0.0,6.4,key='albumin')
            protime = n5.number_input("Prothrombin Time",0.0,100.0,key='protime')
            histology = n6.selectbox("Histology",tuple(feature_dict.keys()),key='histology')



            feature_list = [age,get_value(sex,gender_dict),get_fvalue(steroid),get_fvalue(antivirals),get_fvalue(fatigue),get_fvalue(spiders),get_fvalue(ascites),get_fvalue(varices),bilirubin,alk_phosphate,sgot,albumin,int(protime),get_fvalue(histology)]

            pretty_result = {"age":age,"sex":sex,"steroid":steroid,"antivirals":antivirals,"fatigue":fatigue,"spiders":spiders,"ascites":ascites,"varices":varices,"bilirubin":bilirubin,"alk_phosphate":alk_phosphate,"sgot":sgot,"albumin":albumin,"protime":protime,"histolog":histology}
            single_sample = np.array(feature_list).reshape(1,-1)

            st.form_submit_button("Submit",)	
            st.form_submit_button('Random Input',on_click=random_fun)

        if st.checkbox("Show/Hide Input "):
            st.json(pretty_result)



        model_choice = st.selectbox("Select Model",["LR","KNN","DecisionTree"])		
        if st.button("Predict"):

            if model_choice == "KNN":
                loaded_model = joblib.load('Hepatitis/models/hepB_knn_model.pkl','r+')
                prediction =loaded_model.predict(single_sample)
                pred_prob  =loaded_model.predict_proba(single_sample)
                

            elif model_choice == "DecisionTree":
                loaded_model = joblib.load("Hepatitis/models/hepB_decidion_tree_clf_model.pkl",'r+')
                prediction = loaded_model.predict(single_sample)
                pred_prob = loaded_model.predict_proba(single_sample)

            else:
                loaded_model = joblib.load("Hepatitis/models/hepB_logistic_regression_model.pkl",'r+')
                prediction = loaded_model.predict(single_sample)
                pred_prob = loaded_model.predict_proba(single_sample)

            if prediction == 1:
                pred_probability_score = {"Die":round((pred_prob[0][0]*100), 2),"Live":round((pred_prob[0][1]*100), 2)}
                st.error("Patients is not safe")
                st.subheader("Prediction Probability Score using {}".format(model_choice))
                st.subheader("Prescriptive Analytics")
                st.markdown(f"""<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
                            <h4 style="color:white;text-align:center;">Algorithm:: {model_choice}</h4>
                            <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
                            <br/>
                            <br/>	
                            <p style="text-align:justify;color:white">{pred_probability_score["Die"]} % probalibilty that Patients Die</p>
                            </div>""",unsafe_allow_html=True)

                
            else:
                pred_probability_score = {"Die":round((pred_prob[0][0]*100), 2),"Live":round((pred_prob[0][1]*100), 2)}
                st.success("Patient is Safe")
                st.subheader("Prediction Probability Score using {}".format(model_choice))
                st.markdown(f"""
                    <div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
                    <h4 style="color:white;text-align:center;">Algorithm:: {model_choice}</h4>
                    <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
                    <br/>
                    <br/>	
                    <p style="text-align:justify;color:white">{pred_probability_score["Live"]} % probalibilty that Patients Lives</p>
                    </div>
                    """,unsafe_allow_html=True)
  



if __name__ == '__main__':
    hepatitis()
