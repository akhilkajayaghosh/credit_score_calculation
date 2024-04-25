import csv
import pickle as pk
import random
import string

import pandas as pd
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

model = pk.load(open('model.pkl','rb'))
scaler = pk.load(open('scaler.pkl','rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/page3')
def page3():
    return render_template('page3.html')

@app.route('/page4')
def page4():
    return render_template('page4.html')

@app.route('/submit', methods=['GET','POST'])
def submit():
    if request.method=="POST":
        accounts =float(request.form.get('acc'))
        education = float(request.form.get('edu'))
        employ=float(request.form.get('employment'))
        payhis=float(request.form.get('his'))
        balance=float(request.form.get('bal'))
        lim=float(request.form.get('limit'))
        credit_utilization_ratio=balance/lim
        credit_score = (payhis*0.35)+(credit_utilization_ratio*0.30)+(accounts*0.15)+(education*0.10)+(employ* 0.10)
        # return (f"Credit Score: {credit_score}")
        return render_template('page2.html', value=credit_score)
# Define other routes and backend logic as needed

@app.route('/predict', methods=['POST'])
def predict():
    if request.method=="POST":
        dependents =request.form.get('dependents')
        education=request.form.get('education')
        job =request.form.get('employ')
        income =request.form.get('income')
        amount =request.form.get('amount')
        duration =request.form.get('duration')
        score =request.form.get('score')
        assets =request.form.get('asset')
        pred_data = pd.DataFrame([[dependents,education,job,income,amount,duration,score,assets]],
                                 columns=['no_of_dependents', 'education', 'self_employed', 'income_annum',
                                          'loan_amount', 'loan_term', 'cibil_score', 'Assets'])
        pred_data = scaler.transform(pred_data)
        prediction = model.predict(pred_data)
        if prediction[0] == 1:
            loan= 'Loan Is Approved'
        else:
            loan ='Loan Is Rejected'
        print(loan)
    return render_template('page4.html',answer=loan)
# Define other routes and backend logic as needed

if __name__ == '__main__':
    app.run(debug=True)