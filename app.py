from flask import Flask, render_template, request, send_file
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import random
import pandas as pd
import base64
import time
import tempfile
import sys, io

app = Flask(__name__)

sys.setrecursionlimit(2000)

# Bubble Sort
def bubble_sort(arr, visualize_steps=False):
    arr = arr.copy()
    n = len(arr)
    start_time = time.perf_counter()
    steps = []

    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            if visualize_steps:
                steps.append(arr.copy())

    full_time = time.perf_counter() - start_time

    if visualize_steps:
        images = create_plot(steps)
        return full_time * 1000, images
    return full_time * 1000

def merge_sort(arr, visualize_steps=False):
    arr = arr.copy()
    steps = []

    def merge_sort_helper(arr, left, right):
        if left < right:
            mid = (left + right) // 2
            merge_sort_helper(arr, left, mid)
            merge_sort_helper(arr, mid + 1, right)
            merge(arr, left, mid, right)

    def merge(arr, left, mid, right):
        left_arr = arr[left:mid + 1]
        right_arr = arr[mid + 1:right + 1]
        i = j = 0
        k = left

        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] <= right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1
            if visualize_steps:
                steps.append(arr.copy())

        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1
            if visualize_steps:
                steps.append(arr.copy())

        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1
            if visualize_steps:
                steps.append(arr.copy())

    start_time = time.perf_counter()
    merge_sort_helper(arr, 0, len(arr) - 1)
    total_time = time.perf_counter() - start_time
    
    if visualize_steps:
        images = create_plot(steps)
        return total_time * 1000, images
    return total_time * 1000

def quick_sort(arr, visualize_steps=False):
    arr = arr.copy()
    steps = []

    def quick_sort_helper(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            if visualize_steps:
                steps.append(arr.copy())
            quick_sort_helper(arr, low, pi - 1)
            quick_sort_helper(arr, pi + 1, high)

    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                if visualize_steps:
                    steps.append(arr.copy())
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        if visualize_steps:
            steps.append(arr.copy())
        return i + 1

    start_time = time.perf_counter()
    quick_sort_helper(arr, 0, len(arr) - 1)
    total_time = time.perf_counter() - start_time
    
    if visualize_steps:
        images = create_plot(steps)
        return total_time * 1000, images
    return total_time * 100

def radix_sort(arr, visualize_steps = False):
    arr = arr.copy()
    max_value = max(arr)
    exp = 1
    start_time = time.perf_counter()
    steps = []

    while max_value // exp > 0:
        counting_sort(arr, exp)
        if visualize_steps:
            steps.append(arr.copy())
        exp *= 10

    total_time = time.perf_counter() - start_time
    
    if visualize_steps:
        images = create_plot(steps)
        return total_time * 1000, images
    return total_time * 1000

def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(n):
        arr[i] = output[i]

def linear_search(arr,target):
    for i, x in enumerate(arr):
        if x == target : return i
    return -1

def create_plot(steps):
    images = []
    for i, step in enumerate(steps):

        fig, ax = plt.subplots()
        ax.bar(range(len(step)), step, color='blue')
        ax.set_xlabel("Index")
        ax.set_ylabel("Value")
        ax.set_title(f"Step {i}")

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        image_base64 = base64.b64encode(buf.getvalue()).decode('utf8')
        images.append(f"data:image/png;base64,{image_base64}")
    
    return images

def create_performance_plot(size):
    algorithms = {
        "Bubble Sort": lambda arr: bubble_sort(arr, visualize_steps=False),
        "Merge Sort": lambda arr: merge_sort(arr, visualize_steps=False),
        "Quick Sort": lambda arr: quick_sort(arr, visualize_steps=False),
        "Radix Sort": lambda arr: radix_sort(arr, visualize_steps=False)
    }

    performance_data = {}
    for name, func in algorithms.items():
        arr = random.sample(range(-10000, 10000), size)
        time_taken = func(arr)
        performance_data[name] = time_taken

    fig, ax = plt.subplots()
    ax.bar(performance_data.keys(), performance_data.values(), color='blue')

    ax.set_ylabel("Time (milliseconds)")
    ax.set_xlabel("Sorting Algorithms")
    ax.set_title(f"Sorting Algorithm Performance for Input Size {size}")

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        plt.savefig(tmpfile.name, format='png')
        tmpfile.seek(0)
        img_b64 = base64.b64encode(tmpfile.read()).decode('utf8')

    plt.close()
    print("Plot created successfully")
    return img_b64, performance_data


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualize', methods=['POST'])
def visualize():
    if request.method == 'POST':
        size = int(request.form['size'])
        action = request.form['action']

        if action == 'performance':
            plot_img, performance_data = create_performance_plot(size)
            df = pd.DataFrame(list(performance_data.items()), columns=['Algorithm', 'Time (ms)'])
            table_html = df.to_html(classes='data-table', index=False)

            return render_template('visualization.html', plot_img=plot_img, table_html=table_html)
        
@app.route('/visualize_animation', methods=['POST'])
def visualize_animation():
    if request.method == 'POST':
        size = int(request.form['size'])
        selected_algorithms = request.form.getlist('algorithms')

        all_images = {}

        arr = random.sample(range(10, 100), size)

        for algorithm in selected_algorithms:

            if algorithm == 'Bubble Sort':
                images = bubble_sort(arr, visualize_steps=True)[1]

            elif algorithm == 'Merge Sort':
                images = merge_sort(arr, visualize_steps=True)[1]

            elif algorithm == 'Quick Sort':
                images = quick_sort(arr, visualize_steps=True)[1]

            elif algorithm == 'Radix Sort':
                images = radix_sort(arr, visualize_steps=True)[1]

            all_images[algorithm] = images

        return render_template('visualize_animation.html', all_images=all_images)

if __name__ == '__main__':
    app.run(debug=True)
