from flask import Flask, render_template, request, redirect, url_for
import matplotlib.pyplot as plt
import numpy as np
import random
import io
import base64

app = Flask(__name__)

# Sorting algorithms implementations

# Bubble sort
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

# Merge sort
def merge_sort(arr):
    steps = []
    def merge_sort_helper(arr, left, right):
        if left < right:
            mid = (left + right) // 2
            merge_sort_helper(arr, left, mid)
            merge_sort_helper(arr, mid + 1, right)
            merge(arr, left, mid, right)
            steps.append(arr.copy())

    def merge(arr, left, mid, right):
        left_arr = arr[left:mid+1]
        right_arr = arr[mid+1:right+1]
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
        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1
        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1

    merge_sort_helper(arr, 0, len(arr) - 1)
    return steps

# Quick sort
def quick_sort(arr):
    steps = []
    def partition(arr, low, high):
        i = low - 1
        pivot = arr[high]
        for j in range(low, high):
            if arr[j] <= pivot:
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]
                steps.append(arr.copy())
        arr[i+1], arr[high] = arr[high], arr[i+1]
        steps.append(arr.copy())
        return i + 1

    def quick_sort_helper(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort_helper(arr, low, pi-1)
            quick_sort_helper(arr, pi+1, high)

    quick_sort_helper(arr, 0, len(arr)-1)
    return steps

# Radix sort
def radix_sort(arr):
    steps = []
    max_value = max(arr)
    exp = 1
    while max_value // exp > 0:
        counting_sort(arr, exp, steps)
        exp *= 10
    return steps

def counting_sort(arr, exp, steps):
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
        steps.append(arr.copy())

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
        elif algorithm == 'merge':
            steps = merge_sort(arr)
        elif algorithm == 'quick_sort':
            steps = quick_sort(arr)
        elif algorithm == 'radix_sort':
            steps = radix_sort(arr)
        else:
            return redirect(url_for('index'))
        
        images = create_plot(steps)
        return render_template('visualization.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
