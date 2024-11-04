from flask import Flask, render_template, request, redirect, url_for, session
from main import Jumpscare
import tkinter as tk
import random
import multiprocessing

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key_here'

def launch_jumpscare():
    root = tk.Tk()
    Jumpscare(root)
    root.mainloop()

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize attempts if not in session
    if 'attempts' not in session:
        session['attempts'] = 0
    if 'threshold' not in session:
        session['threshold'] = random.randint(1, 4)

    print(f"Current attempts (start of request): {session['attempts']}")
    
    # Process form submission
    if request.method == 'POST':
        answer = request.form.get('answer')

        # Check if answer is correct
        if answer == 'tralaicongbangchotoi':
            session['attempts'] = 0  # Reset on correct answer
            session['threshold'] = random.randint(1, 4)
            print("Correct answer submitted. Resetting attempts.")
            return render_template('hint.html')

        # Increment attempts for incorrect answers
        session['attempts'] += 1
        print(f"Incorrect answer. Attempts incremented to: {session['attempts']}")

        # Check if jumpscare should be triggered
        if session['attempts'] >= session['threshold']:
            session['attempts'] = 0  # Reset after jumpscare
            session['threshold'] = random.randint(1, 4)
            print("Triggering jumpscare after max attempts.")
            # Launch jumpscare in a separate process
            jumpscare_process = multiprocessing.Process(target=launch_jumpscare)
            jumpscare_process.start()

    # Initial page load or GET request
    return render_template('layout.html')

if __name__ == '__main__':
    # Required for Windows
    multiprocessing.freeze_support()
    # Start Flask app
    app.run(debug=True)