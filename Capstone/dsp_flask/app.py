from flask import Flask, render_template, request, redirect, url_for
import numpy as np
from dsp_model import best_model

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get user input values from the form
            input1 = float(request.form['input1'])
            input2 = float(request.form['input2'])
            input3 = float(request.form['input3'])
            input4 = float(request.form['input4'])
            input5 = float(request.form['input5'])
            input6 = float(request.form['input6'])
            input7 = float(request.form['input7'])
            input8 = float(request.form['input8'])
            input9 = float(request.form['input9'])

            # Create a list of user inputs
            user_input = [input1, input2, input3, input4, input5, input6, input7, input8, input9]

            # Make a prediction using the imported model
            prediction = best_model.predict([user_input])

            # Display the prediction result
            if prediction == 0:
                result = "Low risk of the specified disease."
            else:
                result = "High risk of the specified disease."

            return render_template('result.html', result=result)
        except ValueError:
            error_message = "Invalid input. Please enter valid numerical values."
            return render_template('index.html', error_message=error_message)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
