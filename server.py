from flask import Flask, render_template, request, jsonify
import csv
from glob import glob
from scipy.interpolate import interp1d
from numpy import array

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
            for row in reader: # Add all rows to dict
                subject = row['Subject']
                scaling_list = [float(row[str(i)]) for i in range(20, 50, 5)]
                current[subject] = {}

                # Interpolate scaling data with extrapolation
                x = array(range(20, 50, 5))
                y = array(scaling_list)
                f = interp1d(x, y, kind='cubic', fill_value='extrapolate')
                # Add interpolated data to dict
                for i in range(51):
                    current[subject][str(i)] = int(f(i))
    return dict(sorted(data.items(), key=lambda x: x[0])) # Sort by year
                

app = Flask(__name__)

csv_list = glob('scaling/*.csv') # Get all csv files in ./scaling

scaling_data = read_csv(csv_list)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template(
                'index.html', 
                years=scaling_data.keys(),
                subjects=next(iter(scaling_data.values())).keys() # Pass latest subject list
                )
    else:
        data = dict(request.json) # POST request headers

        # Get interpolated scaling data for given subject and raw score
        scaling = {}
        for year, subjects in scaling_data.items():
            if data["subject"] in subjects:
                scaling[year] = subjects[data["subject"]][str(data['rawScore'])]
                break
        return jsonify(scaling)
