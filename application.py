from flask import Flask, render_template, request
import requests
import pickle
import numpy as np
import sklearn
import pandas as pd
app = Flask(__name__)
ct = pickle.load(open("D:\\Users\\rselvaganapathy\\Documents\\HeartDiseasePredictor\\transform.pkl", 'rb'))
model = pickle.load(open('model.pkl', 'rb'))


@app.route('/',methods=['GET'])
def Home():
    return render_template('home.html')

@app.route("/predict", methods=['POST'])
def predict():  
    # features=['Age','Sex','ChestPainType','RestingBP','Cholesterol','FastingBS','RestingECG','MaxHR','ExerciseAngina','Oldpeak','ST_Slope']
    if request.method == 'POST':
        Age = int(request.form['Age'])
        Sex=request.form['Sex']
        if Sex=="Male":
            Sex=0
        else:
            Sex=1
        ChestPainType=request.form['ChestPainType']
        RestingBP = int(request.form['RestingBP'])
        Cholesterol = int(request.form['Cholesterol'])
        FastingBS=request.form['FastingBS']
        if FastingBS=="False":
            FastingBS=0
        else:
            FastingBS=1
        RestingECG=request.form['RestingECG']
        MaxHR = int(request.form['MaxHR'])
        ExerciseAngina=request.form['ExerciseAngina']
        if ExerciseAngina == "Yes":
            ExerciseAngina=1
        else:
            ExerciseAngina=0
        Oldpeak =  float(request.form['Oldpeak'])
        ST_Slope = request.form['ST_Slope']
        results={"Age":[Age],"Sex":[Sex],"ChestPainType":[ChestPainType],"RestingBP":[RestingBP],"Cholesterol":[Cholesterol],"FastingBS":[FastingBS],"RestingECG":[RestingECG],"MaxHR":[MaxHR],"ExerciseAngina":[ExerciseAngina],"Oldpeak":[Oldpeak],"ST_Slope":[ST_Slope]}
        df_predict=pd.DataFrame(results)
        x_test_scaled=ct.transform(df_predict)
        output=(model.predict(x_test_scaled)).astype(int)
        print(output)
        if output==[0]:
            print("No")
            return render_template('home.html',prediction_text="You don't have any issue with your Heart")
        elif output==[1]:
            print("Yes")
            return render_template('home.html',prediction_text="Seems like you have Heart Issue,Kindly consult a Cardiologist")
        else:
            pass
    else:
        return render_template('home.html')

if __name__=="__main__":
    app.run(debug=True)