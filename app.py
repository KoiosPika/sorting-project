from flask import Flask, render_template, request, redirect, url_for
import matplotlib.pyplot as plt
import numpy as np
import random
import io
import base64

app = Flask(__name__)

# Sorting algorithms implementations
def bubble_sort(arr):
    arr = arr.copy()  # Don't modify the original list
    steps = []
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                steps.append(arr.copy())
    return steps

# Create a visualization for the steps
def create_plot(steps):
    images = []
    for step in steps:
        plt.figure(figsize=(6, 4))
        plt.bar(range(len(step)), step, color='blue')
        plt.xlabel('Index')
        plt.ylabel('Value')

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_b64 = base64.b64encode(img.getvalue()).decode('utf8')
        plt.close()
        images.append(img_b64)
    return images

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualize', methods=['POST'])
def visualize():
    if request.method == 'POST':
        algorithm = request.form['algorithm']
        array_size = int(request.form['size'])
        arr = random.sample(range(1, 100), array_size)
        
        # Select the appropriate algorithm
        if algorithm == 'bubble':
            steps = bubble_sort(arr)
        else:
            return redirect(url_for('index'))
        
        images = create_plot(steps)
        return render_template('visualization.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
