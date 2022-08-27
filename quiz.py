import pandas as pd
import random
import tkinter as tk
from tkinter import ttk


def generate_question():
    global possible_questions_id, question, question_id, choices, answer
    question_id = random.choice(possible_questions_id)
    with open(f"questions/Q{question_id + 1}.txt", 'r') as f:
        lines = f.readlines()
        question = ""
        for line in lines:
            question += line
    choices = questions[question_id]["choices"]
    answer = questions[question_id]["answer"]


def select(button_id, choice):
    global isCorrect, buttons, answer, score
    next_button['state'] = 'normal'
    if choice == answer:
        score += 1
        isCorrect = True
    else:
        isCorrect = False
    if isCorrect:
        buttons[button_id]['bg'] = '#32ff00'
    else:
        buttons[button_id]['bg'] = 'red'
    for button in buttons:
        button['state'] = 'disabled'


def next_question():
    global question_id, question, choices, answer, questions, possible_questions_id, question_no
    generate_question()
    possible_questions_id.remove(question_id)

    label_question['text'] = question
    next_button['state'] = 'disabled'
    next_button['text'] = 'Next question'

    number_of_choices = len(choices.items())
    x = 0
    y = 0
    count = 0
    for k, v in choices.items():
        if number_of_choices == 2:
            buttons[count]['text'] = f'{k}: {v}'
            buttons[count]['command'] = lambda t=k, button_id=count: select(button_id, t)
            buttons[count]['state'] = 'normal'
            buttons[count]['bg'] = '#f0f0f0'
            count += 1
            if count == 2:
                buttons[2]['text'] = 'C'
                buttons[3]['text'] = 'D'
                buttons[2]['state'] = 'disabled'
                buttons[3]['state'] = 'disabled'
                buttons[2]['bg'] = '#f0f0f0'
                buttons[3]['bg'] = '#f0f0f0'
        elif number_of_choices == 4:
            buttons[count]['text'] = f'{k}: {v}'
            buttons[count]['command'] = lambda t=k, button_id=count: select(button_id, t)
            buttons[count]['state'] = 'normal'
            buttons[count]['bg'] = '#f0f0f0'
            y += 1
            count += 1
            if y == 2:
                y = 0
                x += 1
    question_no += 1
    if number_of_questions == question_no:
        next_button['text'] = 'End Quiz'
        next_button['command'] = end_quiz


def end_quiz():
    for button in buttons:
        button['text'] = ''
        button['bg'] = '#f0f0f0'
    percentage = (score/number_of_questions)*100
    final_score = f'Score: {percentage}%\n'
    if percentage > 70:
        final_score += 'Well done! You passed the certification'
    else:
        final_score += 'Sorry, you will have to revise a bit more to succeed! Don\'t give up'
    label_question['text'] = final_score
    next_button['text'] = 'Quit'
    next_button['command'] = close_window


def close_window():
    root.destroy()


isCorrect = None
buttons = []
data = pd.read_json("all questions.json")
questions = data["questions"]
number_of_questions = len(questions)
possible_questions_id = [x for x in range(number_of_questions)]
question_no = 0
question_id = -1
question = None
choices = {}
answer = None
score = 0

#  SETUP
root = tk.Tk()
root.title('Python Certification Quiz')

window_width = 1000
window_height = 600

s = ttk.Style()
s.configure('my.TButton', font=('Helvetica', 18), width=37)

# text_font = font.Font(size=30, family='Helvetica')

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)

question_frame = tk.Frame(root)
question_frame.pack(expand=True, fill='x')

next_frame = tk.Frame(root)
next_frame.pack(fill='x')

buttons_frame = tk.Frame(root)
buttons_frame.pack(fill='x')

label_question = tk.Label(
    question_frame,
    text='Welcome to Python Certification Quiz!',
    font=('Helvetica', 18),
    bd=1, relief='sunken',
    justify='left'
)

label_question.pack(
    ipadx=5,
    ipady=5,
    expand=True
)

next_button = tk.Button(master=next_frame,
                        text='Start',
                        font=('Helvetica', 18),
                        width=14,
                        command=next_question)

next_button.pack(pady=20)

r, c = 0, 0
texts = ['A', 'B', 'C', 'D']
for i in range(4):
    _ = tk.Button(master=buttons_frame,
                  text=texts[i],
                  font=('Helvetica', 18),
                  state='disabled',
                  width=34)
    buttons.append(_)
    _.grid(row=r, column=c, ipadx=10, ipady=10)
    c += 1
    if c == 2:
        c = 0
        r += 1


root.mainloop()
