from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/', methods=['GET', 'POST'])
def index():
    accuracy = None
    chart_data = None

    if request.method == 'POST':
        file = request.files['csv_file']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Read CSV
            df = pd.read_csv(filepath)

            # Ensure correct columns
            if set(['Timestamp','Actual','Predicted']).issubset(df.columns):
                # Calculate accuracy
                correct = (df['Actual'] == df['Predicted']).sum()
                accuracy_percent = round((correct / len(df)) * 100, 2)
                accuracy = f"{accuracy_percent}% ({correct}/{len(df)})"

                # Prepare data for Chart.js
                chart_data = {
                    'timestamps': df['Timestamp'].tolist(),
                    'actual': df['Actual'].tolist(),
                    'predicted': df['Predicted'].tolist()
                }

    return render_template('index.html', accuracy=accuracy, chart_data=chart_data)

if __name__ == '__main__':
    app.run(debug=True)
