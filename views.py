from flask import Flask, render_template, request, redirect, url_for, session
from main import Jumpscare
import tkinter as tk
import threading

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for session management

jumpscare_instance = None
MAX_ATTEMPTS = 3

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'attempts' not in session:
        session['attempts'] = 0

    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer == 'tra lai cong bang cho toi':
            session['attempts'] = 0
            return render_template('layout.html', message='Correct! Unlocking next chapter...')
        else:
            session['attempts'] += 1
            if session['attempts'] >= MAX_ATTEMPTS:
                return trigger_jumpscare()
            else:
                return render_template('layout.html', 
                                       message=f'Incorrect. You have {MAX_ATTEMPTS - session["attempts"]} attempts left.')

    return render_template('layout.html')

@app.route('/trigger-jumpscare', methods=['POST'])
def trigger_jumpscare():
    global jumpscare_instance
    
    if jumpscare_instance is None:
        def run_jumpscare():
            global jumpscare_instance
            root = tk.Tk()
            jumpscare_instance = Jumpscare(root)
            root.mainloop()

        jumpscare_thread = threading.Thread(target=run_jumpscare)
        jumpscare_thread.start()
        return render_template('layout.html', message='Too many incorrect attempts!')
    else:
        return render_template('layout.html', message='Jumpscare already running')

if __name__ == '__main__':
    app.run(debug=True)
