import pandas as pd
import random
import tkinter as tk
import tkinter.font as font
from tkinter import ttk


def read_file(filename):
    return pd.read_json(filename)


def generate_question(questions):
    number_of_questions = len(questions)
    possible_questions_id = [x for x in range(number_of_questions)]
    r = 2  # random.choice(possible_questions_id)
    possible_questions_id.remove(r)
    print("question ID:", r+1)
    with open(f"questions/Q{r+1}.txt", 'r') as f:
        lines = f.readlines()
        question = ""
        for line in lines:
            question += line
    print(question+"\n")
    choices = questions[r]["choices"]
    answer = questions[r]["answer"]
    for k, v in choices.items():
        print(k, ":", v)
    print()
    a = ""
    possible_answers = choices.keys()
    print(possible_answers)
    """while a not in possible_answers:
        a = input("What is your answer? ")
        if a not in possible_answers:
            print("Wrong input, please enter one of the following possible answer:", possible_answers)
        elif a == answer:
            print("well done")
        else:
            print("wrong, sorry, the answer was", answer)"""
    return question, choices, answer


def select(choice, answer):
    print(choice, answer)
    if choice == answer:
        print("well done")
    else:
        print("wrong, sorry, the answer was", answer)


def create_quiz():
    data = read_file("all questions.json")
    questions = data["questions"]

    question, choices, answer = generate_question(questions)

    root = tk.Tk()
    root.title('Python Certification Quiz')

    window_width = 1000
    window_height = 600

    s = ttk.Style()
    s.configure('my.TButton', font=('Helvetica', 18), width=37)

    #text_font = font.Font(size=30, family='Helvetica')

    # get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    # set the position of the window to the center of the screen
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.resizable(False, False)

    question_frame = tk.Frame(root)
    question_frame.pack(expand=True, fill='x')

    buttons_frame = tk.Frame(root)
    buttons_frame.pack(fill='x')

    label_question = tk.Label(
        question_frame,
        text=question,
        font=('Helvetica', 18),
        bd=1, relief='sunken',
        justify='left'
    )

    label_question.pack(
        ipadx=5,
        ipady=5,
        expand=True
    )

    number_of_choices = len(choices.items())
    x = 0
    y = 0
    for k, v in choices.items():
        if number_of_choices == 2:
            button = ttk.Button(master=buttons_frame,
                                text=f'{k}: {v}',
                                style='my.TButton',
                                command=lambda t=k: select(t, answer))
            button.grid(row=x, column=y, ipadx=10, ipady=10)
            y += 1
        elif number_of_choices == 4:
            button = ttk.Button(master=buttons_frame,
                                text=f'{k}: {v}',
                                style='my.TButton',
                                command=lambda t=k: select(t, answer))
            button.grid(row=x, column=y, ipadx=10, ipady=10)
            y += 1
            if y == 2:
                y = 0
                x += 1

    root.mainloop()


create_quiz()
