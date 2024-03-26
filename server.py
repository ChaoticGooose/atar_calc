from flask import Flask, render_template, request
import csv
from glob import glob

"""
Parameters:
    csv_list (list): List of csv files
Returns:
    dict: Dictionary of scaling data, sorted by year
"""
def read_csv(csv_list: list) -> dict:
    data = {}
    for csv_file in csv_list:
        year = csv_file.split('/')[-1].split('.')[0]
        data[year] = current = {}
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                subject = row.pop('Subject')
                current[subject] = row
    return dict(sorted(data.items(), key=lambda x: x[0]))
                

app = Flask(__name__)

csv_list = glob('scaling/*.csv')

scaling_data = read_csv(csv_list)
print(scaling_data)
# Sort by year
scaling_data = dict(sorted(scaling_data.items(), key=lambda x: x[0]))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template(
                'index.html', 
                years=scaling_data.keys(),
                subjects=next(iter(scaling_data.values())).keys()
                )


