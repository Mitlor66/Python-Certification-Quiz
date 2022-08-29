import threading
import time
import pandas as pd
import random
import tkinter as tk
from tkinter import ttk
from colors import Color


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
    global dark_theme
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
    # set the window color
    window.configure(bg=Color.DARK_GRAY.value if dark_theme else Color.NORMAL_BG_GRAY.value)
    return window


def initialize_buttons():
    next_b = tk.Button(master=next_frame,
                       text='Start',
                       font=('Consolas', 14),
                       bg=Color.LIGHT_GRAY.value if dark_theme else Color.NORMAL_BG_GRAY.value,
                       fg=Color.WHITE.value if dark_theme else Color.BLACK.value,
                       disabledforeground=Color.DISABLED_GRAY.value if dark_theme else Color.NORMAL_TEXT_GRAY.value,
                       width=22,
                       command=next_question)

    next_b.pack(pady=20)

    for i in range(4):
        _ = tk.Button(master=buttons_frame,
                      text=button_values[i],
                      font=('Consolas', 14),
                      bg=Color.LIGHT_GRAY.value if dark_theme else Color.NORMAL_BG_GRAY.value,
                      fg=Color.WHITE.value if dark_theme else Color.BLACK.value,
                      disabledforeground=Color.DISABLED_GRAY.value if dark_theme else Color.NORMAL_TEXT_GRAY.value,
                      state='disabled',
                      width=47)
        buttons.append(_)
        _.grid(row=i//2, column=i % 2, ipadx=10, ipady=10)
    return next_b


def initialize_frames():
    global progress_frame, question_frame, next_frame, buttons_frame
    p_frame = tk.Frame(root, bg=Color.DARK_GRAY.value if dark_theme else Color.NORMAL_BG_GRAY.value)
    p_frame.pack(fill='both', pady=20)

    q_frame = tk.Frame(root, bg=Color.DARK_GRAY.value if dark_theme else Color.NORMAL_BG_GRAY.value)
    q_frame.pack(expand=True, fill='x')

    n_frame = tk.Frame(root, bg=Color.DARK_GRAY.value if dark_theme else Color.NORMAL_BG_GRAY.value)
    n_frame.pack(fill='x')

    b_frame = tk.Frame(root, bg=Color.DARK_GRAY.value if dark_theme else Color.NORMAL_BG_GRAY.value)
    b_frame.pack(fill='both')
    return p_frame, q_frame, n_frame, b_frame


def initialize_progress_frame_widgets():
    total_time_minutes = 1.5 * number_of_questions
    hours = int(total_time_minutes // 60)
    minutes = int(total_time_minutes % 60)
    seconds = 0

    pb = ttk.Progressbar(
        progress_frame,
        orient='horizontal',
        mode='determinate',
        length=500,
    )

    pb.pack(side='left', ipadx=5, ipady=5, expand=True)

    label = tk.Label(
        progress_frame,
        text=f"{hours:02d}:{minutes:02d}:{seconds:02d}",
        font=('Consolas', 14),
        bd=1, relief='sunken',
        justify='left',
        bg=Color.LIGHT_GRAY.value if dark_theme else Color.NORMAL_BG_GRAY.value,
        fg=Color.WHITE.value if dark_theme else Color.BLACK.value,
    )

    label.pack(ipadx=5, ipady=5, padx=10, expand=True)

    return label, pb


def initialize_label_question():
    label = tk.Label(
        question_frame,
        text='Welcome to Python Certification Quiz!',
        font=('Consolas', 14),
        bd=1, relief='sunken',
        justify='left',
        bg=Color.LIGHT_GRAY.value if dark_theme else Color.NORMAL_BG_GRAY.value,
        fg=Color.WHITE.value if dark_theme else Color.BLACK.value,
    )

    label.pack(ipadx=5, ipady=5, padx=5, pady=5, expand=True)

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
    global buttons, next_button, answer, score, correct, wrong, question_no
    question_no += 1
    calculation = 500/number_of_questions
    calculation = calculation / 500
    calculation *= 100
    progress_bar['value'] += calculation
    next_button['state'] = 'normal'
    if choice == answer:
        score += 1
        correct += 1
        is_correct = True
    else:
        wrong += 1
        is_correct = False
    if is_correct:
        buttons[button_id]['bg'] = '#32ff00'
    else:
        buttons[button_id]['bg'] = 'red'
        buttons[button_id_answer]['bg'] = '#32ff00'
    for button in buttons:
        button['state'] = 'disabled'
    if number_of_questions == question_no:
        next_button['text'] = 'End Quiz'
        next_button['command'] = end_quiz


def next_question():
    global question_id, choices, answer, question_no
    generate_question()
    if question_no == 0:
        x = threading.Thread(target=timer, args=(number_of_questions,), daemon=True)
        x.start()
    label_question['text'] = question
    next_button['state'] = 'disabled'
    next_button['text'] = 'Next question'

    count = 0
    for k, v in choices.items():
        if k == answer:
            button_id_answer = count
        buttons[count]['text'] = f'{k}: {v}'
        buttons[count]['command'] = lambda t=k, button_id=count: select(button_id, t, button_id_answer)
        buttons[count]['state'] = 'normal'
        buttons[count]['bg'] = Color.LIGHT_GRAY.value if dark_theme else Color.NORMAL_BG_GRAY.value
        count += 1


def end_quiz():
    global correct, wrong
    for button in buttons:
        button['text'] = ''
        button['bg'] = Color.LIGHT_GRAY.value if dark_theme else Color.NORMAL_BG_GRAY.value,
    percentage = (score/number_of_questions)*100
    final_score = f'Score: {percentage:.2f}%\n'
    final_score += f'Correct: {correct}/{question_no}\nWrong: {wrong}/{question_no}\n'
    final_score += f'Questions answered: {question_no}/{number_of_questions}\n'
    if percentage > 70:
        final_score += 'Well done! You passed the certification'
    elif percentage > 60:
        final_score += 'That was close! Just a little bit more of revision!'
    elif percentage > 50:
        final_score += 'More than 50%! That\'s great! You will do better next time!'
    else:
        final_score += 'Sorry, you will have to revise a bit more to succeed! Don\'t give up'
    label_question['text'] = final_score
    next_button['text'] = 'Quit'
    next_button['command'] = close_window


def close_window():
    root.destroy()


def timer(no_of_questions):
    total_time_minutes = 1.5 * no_of_questions
    total_time_seconds = total_time_minutes * 60
    hours = int(total_time_minutes // 60)
    minutes = int(total_time_minutes % 60)
    seconds = 0
    while total_time_seconds > 0:
        label_timer['text'] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        total_time_seconds -= 1
        if seconds == 0:
            seconds = 59
            if minutes == 0:
                minutes = 59
                if hours != 0:
                    hours -= 1
            else:
                minutes -= 1
        else:
            seconds -= 1
        time.sleep(1)
    timeout()


def timeout():
    for button in buttons:
        button['text'] = ''
        button['bg'] = '#f0f0f0'
        button['state'] = 'disabled'
    next_button['text'] = 'end quiz'
    next_button['state'] = 'normal'
    next_button['command'] = end_quiz
    label_question['text'] = "Timeout...\nPress 'end quiz' to see your results"


# Global variables declaration
if __name__ == "__main__":
    data = pd.read_json("questions/all questions.json")
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
    correct = 0
    wrong = 0
    buttons = []
    button_values = ['A', 'B', 'C', 'D']
    dark_theme = False

    #  SETUP
    root = initialize_window()
    progress_frame, question_frame, next_frame, buttons_frame = initialize_frames()
    label_timer, progress_bar = initialize_progress_frame_widgets()
    label_question = initialize_label_question()
    next_button = initialize_buttons()
    root.mainloop()
