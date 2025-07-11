from flask import Flask, render_template, request, send_file
import os
import uuid
import pandas as pd
from collections import defaultdict

def group_by_slot(schedule_data):
    slots = defaultdict(list)
    for panel, slot in schedule_data:
        slots[slot].append(panel)
    return dict(slots)


from algorithms.dsatur import dsatur_from_excel
from algorithms.greedy import greedy_from_excel
from algorithms.genetic import genetic_from_excel
from algorithms.tabu import tabu_from_excel

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_uploaded_file(file):
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return filepath

def run_selected_algorithm(filepath, goal):
    if goal == 'fastest':
        return greedy_from_excel(filepath), 'Greedy'
    elif goal == 'balanced':
        return dsatur_from_excel(filepath), 'DSATUR'
    elif goal == 'minimal_tech':
        return tabu_from_excel(filepath), 'Tabu Search'
    elif goal == 'all_compare':
        results = {
            'Greedy': greedy_from_excel(filepath),
            'DSATUR': dsatur_from_excel(filepath),
            'Genetic': genetic_from_excel(filepath),
            'Tabu Search': tabu_from_excel(filepath)
        }
        # Pick algorithm using fewest slots
        best_algo = min(results, key=lambda k: len(set(slot for _, slot in results[k])))
        return results[best_algo], best_algo
    else:
        return None, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule', methods=['POST'])
def schedule():
    file = request.files.get('conflict_file')
    goal = request.form.get('goal')

    if not file or file.filename == '':
        return "No file uploaded. Please go back and upload a file."

    filepath = save_uploaded_file(file)
    schedule_data, algorithm_used = run_selected_algorithm(filepath, goal)

    if schedule_data is None:
        return "Invalid scheduling goal selected."
    grouped_schedule = group_by_slot(schedule_data)

    # Also save Excel as before
    df = pd.DataFrame(schedule_data, columns=['Panel', 'Assigned Slot'])
    output_path = os.path.join(UPLOAD_FOLDER, 'schedule_result.xlsx')
    df.to_excel(output_path, index=False)

    return render_template('result.html', grouped_schedule=grouped_schedule, best_algo=algorithm_used)


@app.route('/download')
def download():
    path = os.path.join(UPLOAD_FOLDER, 'schedule_result.xlsx')
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
