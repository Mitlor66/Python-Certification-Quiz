import pandas as pd
import random
import tkinter as tk


def parse_file(filename):
    q_d = {}
    q_n = 0
    q = ""
    flag = True
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip("\n")
            if flag:
                q_n = int(line)
                flag = False
            else:
                q += line + "\n"
            if line == "":
                q = q.strip("\n")
                q_d[q_n] = q
                q = ""
                flag = True
    q_d[q_n] = q
    return q_d


def initialize_window():
    window = tk.Tk()
    window.title('Python Certification Quiz')

    window_width = 1000
    window_height = 600

    # get the screen dimension
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # set the position of the window to the center of the screen
    window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    window.resizable(False, False)
    return window


def initialize_buttons():
    next_b = tk.Button(master=next_frame,
                       text='Start',
                       font=('Consolas', 14),
                       width=22,
                       command=next_question)

    next_b.pack(pady=20)

    r, c = 0, 0
    for i in range(4):
        _ = tk.Button(master=buttons_frame,
                      text=button_values[i],
                      font=('Consolas', 14),
                      state='disabled',
                      width=47)
        buttons.append(_)
        _.grid(row=r, column=c, ipadx=10, ipady=10)
        c += 1
        if c == 2:
            c = 0
            r += 1
    return next_b


def initialize_frames():
    global question_frame, next_frame, buttons_frame
    q_frame = tk.Frame(root)
    q_frame.pack(expand=True, fill='x')

    n_frame = tk.Frame(root)
    n_frame.pack(fill='x')

    b_frame = tk.Frame(root)
    b_frame.pack(fill='both')
    return q_frame, n_frame, b_frame


def initialize_label_question():
    label = tk.Label(
        question_frame,
        text='Welcome to Python Certification Quiz!',
        font=('Consolas', 14),
        bd=1, relief='sunken',
        justify='left'
    )

    label.pack(
        ipadx=5,
        ipady=5,
        padx=5,
        pady=5,
        expand=True
    )
    return label


def generate_question():
    global question, question_id, choices, answer
    while True:
        question_id = random.choice(possible_questions_id)
        section = questions_info[question_id]["section"]
        if current_sections[section] < sections[section]:
            current_sections[section] += 1
            break
    question = questions_dictionary[question_id+1]
    choices = questions_info[question_id]["choices"]
    answer = questions_info[question_id]["answer"]
    possible_questions_id.remove(question_id)


def select(button_id, choice, button_id_answer):
    global buttons, next_button, answer, score
    next_button['state'] = 'normal'
    if choice == answer:
        score += 1
        is_correct = True
    else:
        is_correct = False
    if is_correct:
        buttons[button_id]['bg'] = '#32ff00'
    else:
        buttons[button_id]['bg'] = 'red'
        buttons[button_id_answer]['bg'] = '#32ff00'
    for button in buttons:
        button['state'] = 'disabled'


def next_question():
    global question_id, choices, answer, question_no
    generate_question()

    label_question['text'] = question
    next_button['state'] = 'disabled'
    next_button['text'] = 'Next question'

    number_of_choices = len(choices.items())
    x = 0
    y = 0
    count = 0
    for k, v in choices.items():
        if k == answer:
            button_id_answer = count
        if number_of_choices == 2:
            buttons[count]['text'] = f'{k}: {v}'
            buttons[count]['command'] = lambda t=k, button_id=count: select(button_id, t, button_id_answer)
            buttons[count]['state'] = 'normal'
            buttons[count]['bg'] = '#f0f0f0'
            count += 1
            if count == 2:
                for i in range(2, 4):
                    buttons[i]['text'] = button_values[i]
                    buttons[i]['state'] = 'disabled'
                    buttons[i]['bg'] = '#f0f0f0'
        elif number_of_choices == 4:
            buttons[count]['text'] = f'{k}: {v}'
            buttons[count]['command'] = lambda t=k, button_id=count: select(button_id, t, button_id_answer)
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


# Global variables declaration
data = pd.read_json("all questions.json")
questions_dictionary = parse_file("questions/all_questions.txt")
questions_info = data["questions"]
sections = {1: 7, 2: 8, 3: 7, 4: 8}
current_sections = {1: 0, 2: 0, 3: 0, 4: 0}
number_of_questions = sum(sections.values())
possible_questions_id = [x for x in range(len(questions_info))]
question_no = 0
question_id = -1
question = ""
choices = {}
answer = ""
score = 0
buttons = []
button_values = ['A', 'B', 'C', 'D']

#  SETUP
root = initialize_window()
question_frame, next_frame, buttons_frame = initialize_frames()
label_question = initialize_label_question()
next_button = initialize_buttons()
root.mainloop()
