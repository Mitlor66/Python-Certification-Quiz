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


class Question:
    def __init__(self, q_id, q_section, q_text, q_choices, q_answer):
        self.id = q_id
        self.section = q_section
        self.text = q_text
        self.choices = q_choices
        self.answer = q_answer


class Window:
    def __init__(self, quiz):
        self.window = tk.Tk()
        self.window.title('Python Certification Quiz')

        window_width = 1000
        window_height = 600

        # get the screen dimension
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # set the position of the window to the center of the screen
        self.window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.window.resizable(False, False)
        # set the window color
        self.window.configure(bg=Color.DARK_GRAY.value if quiz.dark_theme else Color.NORMAL_BG_GRAY.value)
        self.create_menu_bar(quiz)
        self.all_info = self.get_user_input(quiz)

    def create_menu_bar(self, quiz):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        # create the file_menu
        file_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        # add menu items to the File menu
        file_menu.add_command(label='Restart', command=quiz.restart_quiz)
        file_menu.add_command(label='Pause', command=quiz.pause_quiz)
        file_menu.add_command(label='Close', command=self.window.destroy)

        preference_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        # add menu items to the File menu
        preference_menu.add_command(label='Switch theme', command=lambda q=quiz: self.switch_theme(q))

        menubar.add_cascade(
            label="Quiz",
            menu=file_menu,
            underline=0
        )

        # add the File menu to the menubar
        menubar.add_cascade(
            label="Preferences",
            menu=preference_menu
        )

    def get_user_input(self, quiz):
        # store email address and password
        no_of_questions = tk.StringVar()
        t_per_question = tk.StringVar()

        # Sign in frame
        all_info = ttk.Frame(self.window)
        all_info.pack(padx=10, pady=10)

        no_of_question_label = ttk.Label(all_info, text="Number of questions:")
        no_of_question_label.pack()

        no_of_question_entry = ttk.Entry(all_info, textvariable=no_of_questions)
        no_of_question_entry.pack()
        no_of_question_entry.focus()

        t_per_question_label = ttk.Label(all_info, text="Time per question:")
        t_per_question_label.pack()

        t_per_question_entry = ttk.Entry(all_info, textvariable=t_per_question)
        t_per_question_entry.pack()

        # login button
        validate_button = ttk.Button(all_info,
                                     text="Start Quiz",
                                     command=lambda noq=no_of_questions, tpq=t_per_question:
                                     self.validate(quiz, noq, tpq))

        validate_button.pack(pady=10)
        return all_info

    def validate(self, quiz, noq, tpq):
        quiz.number_of_questions = int(noq.get())
        quiz.time_per_question = float(tpq.get())
        self.all_info.pack_forget()
        print(quiz.number_of_questions, quiz.time_per_question)
        self.initialize_frames(quiz)

    def initialize_frames(self, quiz):
        quiz.progress_frame = tk.Frame(self.window,
                                       bg=Color.DARK_GRAY.value if quiz.dark_theme else Color.NORMAL_BG_GRAY.value)
        quiz.progress_frame.pack(fill='both', pady=20)

        quiz.question_frame = tk.Frame(self.window,
                                       bg=Color.DARK_GRAY.value if quiz.dark_theme else Color.NORMAL_BG_GRAY.value)
        quiz.question_frame.pack(expand=True, fill='x')

        quiz.next_frame = tk.Frame(self.window,
                                   bg=Color.DARK_GRAY.value if quiz.dark_theme else Color.NORMAL_BG_GRAY.value)
        quiz.next_frame.pack(fill='x')

        quiz.buttons_frame = tk.Frame(self.window,
                                      bg=Color.DARK_GRAY.value if quiz.dark_theme else Color.NORMAL_BG_GRAY.value)
        quiz.buttons_frame.pack(fill='both')

        quiz.initialize_progress_frame_widgets()
        quiz.initialize_question_frame_widget()
        quiz.initialize_next_and_buttons_frames_widget()
        quiz.create_all_questions()

    def switch_theme(self, quiz):
        quiz.dark_theme = not quiz.dark_theme
        self.window['bg'] = Color.DARK_GRAY.value if quiz.dark_theme else Color.NORMAL_BG_GRAY.value
        quiz.progress_frame['bg'] = Color.DARK_GRAY.value if quiz.dark_theme else Color.NORMAL_BG_GRAY.value
        quiz.question_frame['bg'] = Color.DARK_GRAY.value if quiz.dark_theme else Color.NORMAL_BG_GRAY.value
        quiz.next_frame['bg'] = Color.DARK_GRAY.value if quiz.dark_theme else Color.NORMAL_BG_GRAY.value
        quiz.buttons_frame['bg'] = Color.DARK_GRAY.value if quiz.dark_theme else Color.NORMAL_BG_GRAY.value
        quiz.next_button['bg'] = Color.LIGHT_GRAY.value if quiz.dark_theme else Color.NORMAL_BG_GRAY.value
        quiz.next_button['fg'] = Color.WHITE.value if quiz.dark_theme else Color.BLACK.value
        quiz.next_button['disabledforeground'] = \
            Color.DISABLED_GRAY.value if quiz.dark_theme else Color.NORMAL_TEXT_GRAY.value
        for button in quiz.buttons:
            button['bg'] = Color.LIGHT_GRAY.value if quiz.dark_theme else Color.NORMAL_BG_GRAY.value
            button['fg'] = Color.WHITE.value if quiz.dark_theme else Color.BLACK.value
            button['disabledforeground'] = \
                Color.DISABLED_GRAY.value if quiz.dark_theme else Color.NORMAL_TEXT_GRAY.value
        quiz.label_question['bg'] = Color.LIGHT_GRAY.value if quiz.dark_theme else Color.NORMAL_BG_GRAY.value
        quiz.label_question['fg'] = Color.WHITE.value if quiz.dark_theme else Color.BLACK.value
        quiz.label_timer['bg'] = Color.LIGHT_GRAY.value if quiz.dark_theme else Color.NORMAL_BG_GRAY.value
        quiz.label_timer['fg'] = Color.WHITE.value if quiz.dark_theme else Color.BLACK.value

    def mainloop(self):
        self.window.mainloop()


class Quiz:
    def __init__(self):
        self.dark_theme = False
        self.all_info = None
        self.root = Window(self)
        self.all_data = pd.read_json("questions/all questions.json")
        self.questions_dictionary = parse_file("questions/all_questions.txt")
        self.questions_info = self.all_data["questions"]
        self.sections = {1: 7, 2: 8, 3: 7, 4: 8}
        self.current_sections = {1: 0, 2: 0, 3: 0, 4: 0}
        self.number_of_questions = 0
        self.possible_questions_id = [x for x in range(len(self.questions_info))]
        self.time_per_question = 0
        self.question_no = 0
        self.question_id = -1
        self.all_question = []
        self.current_question = None
        self.score = 0
        self.correct = 0
        self.wrong = 0
        self.buttons = []
        self.pause = False
        self.progress_frame = None
        self.question_frame = None
        self.next_frame = None
        self.buttons_frame = None
        self.label_timer = None
        self.progress_bar = None
        self.label_question = None
        self.next_button = None

    def initialize_progress_frame_widgets(self):
        total_time_minutes = self.time_per_question * self.number_of_questions
        hours = int(total_time_minutes // 60)
        minutes = int(total_time_minutes % 60)
        seconds = 0

        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            orient='horizontal',
            mode='determinate',
            length=500,
        )

        self.progress_bar.pack(side='left', ipadx=5, ipady=5, expand=True)

        self.label_timer = tk.Label(
            self.progress_frame,
            text=f"{hours:02d}:{minutes:02d}:{seconds:02d}",
            font=('Consolas', 14),
            bd=1, relief='sunken',
            justify='left',
            bg=Color.LIGHT_GRAY.value if self.dark_theme else Color.NORMAL_BG_GRAY.value,
            fg=Color.WHITE.value if self.dark_theme else Color.BLACK.value,
        )

        self.label_timer.pack(ipadx=5, ipady=5, padx=10, expand=True)

    def initialize_question_frame_widget(self):
        self.label_question = tk.Label(
            self.question_frame,
            text='Welcome to Python Certification Quiz!',
            font=('Consolas', 14),
            bd=1, relief='sunken',
            justify='left',
            bg=Color.LIGHT_GRAY.value if self.dark_theme else Color.NORMAL_BG_GRAY.value,
            fg=Color.WHITE.value if self.dark_theme else Color.BLACK.value,
        )

        self.label_question.pack(ipadx=5, ipady=5, padx=5, pady=5, expand=True)

    def initialize_next_and_buttons_frames_widget(self):
        self.next_button = tk.Button(master=self.next_frame,
                                     text='Start',
                                     font=('Consolas', 14),
                                     bg=Color.LIGHT_GRAY.value if self.dark_theme else Color.NORMAL_BG_GRAY.value,
                                     fg=Color.WHITE.value if self.dark_theme else Color.BLACK.value,
                                     disabledforeground=Color.DISABLED_GRAY.value
                                     if self.dark_theme else Color.NORMAL_TEXT_GRAY.value,
                                     width=22,
                                     command=self.next_question)

        self.next_button.pack(pady=20)

        button_values = ['A', 'B', 'C', 'D']
        for i in range(4):
            _ = tk.Button(master=self.buttons_frame,
                          text=button_values[i],
                          font=('Consolas', 14),
                          bg=Color.LIGHT_GRAY.value if self.dark_theme else Color.NORMAL_BG_GRAY.value,
                          fg=Color.WHITE.value if self.dark_theme else Color.BLACK.value,
                          disabledforeground=Color.DISABLED_GRAY.value
                          if self.dark_theme else Color.NORMAL_TEXT_GRAY.value,
                          state='disabled',
                          width=47)
            self.buttons.append(_)
            _.grid(row=i//2, column=i % 2, ipadx=10, ipady=10)

    def create_all_questions(self):
        for k, v in self.questions_dictionary.items():
            qid = k-1
            section = self.questions_info[qid]['section']
            text = v
            choices = self.questions_info[qid]['choices']
            answer = self.questions_info[qid]['answer']
            question = Question(qid, section, text, choices, answer)
            self.all_question.append(question)

    def generate_question(self):
        while True:
            q_id = random.choice(self.possible_questions_id)
            section = self.all_question[q_id].section
            if self.current_sections[section] < self.sections[section]:
                self.current_sections[section] += 1
                break
        self.current_question = self.all_question[q_id]
        self.possible_questions_id.remove(q_id)

    def select(self, button_id, choice, button_id_answer):
        self.question_no += 1
        calculation = 500/self.number_of_questions
        calculation = calculation / 500
        calculation *= 100
        self.progress_bar['value'] += calculation
        self.next_button['state'] = 'normal'
        if choice == self.current_question.answer:
            self.score += 1
            self.correct += 1
            is_correct = True
        else:
            self.wrong += 1
            is_correct = False
        if is_correct:
            self.buttons[button_id]['bg'] = '#32ff00'
        else:
            self.buttons[button_id]['bg'] = 'red'
            self.buttons[button_id_answer]['bg'] = '#32ff00'
        for button in self.buttons:
            button['state'] = 'disabled'
        if self.number_of_questions == self.question_no:
            self.next_button['text'] = 'End Quiz'
            self.next_button['command'] = self.end_quiz

    def next_question(self):
        self.generate_question()
        if self.question_no == 0:
            x = threading.Thread(target=self.timer, daemon=True)
            x.start()
        self.label_question['text'] = self.current_question.text
        self.next_button['state'] = 'disabled'
        self.next_button['text'] = 'Next question'

        count = 0
        for k, v in self.current_question.choices.items():
            if k == self.current_question.answer:
                button_id_answer = count
            self.buttons[count]['text'] = f'{k}: {v}'
            self.buttons[count]['command'] = lambda t=k, button_id=count: self.select(button_id, t, button_id_answer)
            self.buttons[count]['state'] = 'normal'
            self.buttons[count]['bg'] = Color.LIGHT_GRAY.value if self.dark_theme else Color.NORMAL_BG_GRAY.value
            count += 1

    def end_quiz(self):
        self.pause_quiz()
        for button in self.buttons:
            button['text'] = ''
            button['bg'] = Color.LIGHT_GRAY.value if self.dark_theme else Color.NORMAL_BG_GRAY.value,
        percentage = (self.score/self.number_of_questions)*100
        final_score = f'Score: {percentage:.2f}%\n'
        final_score += f'Correct: {self.correct}/{self.question_no}\nWrong: {self.wrong}/{self.question_no}\n'
        final_score += f'Questions answered: {self.question_no}/{self.number_of_questions}\n'
        if percentage > 70:
            final_score += 'Well done! You passed the certification'
        elif percentage > 60:
            final_score += 'That was close! Just a little bit more of revision!'
        elif percentage > 50:
            final_score += 'More than 50%! That\'s great! You will do better next time!'
        else:
            final_score += 'Sorry, you will have to revise a bit more to succeed! Don\'t give up'
        self.label_question['text'] = final_score
        self.next_button['text'] = 'Quit'
        self.next_button['command'] = self.close_window

    def close_window(self):
        self.root.window.destroy()

    def timer(self):
        total_time_minutes = self.time_per_question * self.number_of_questions
        total_time_seconds = total_time_minutes * 60
        hours = int(total_time_minutes // 60)
        minutes = int(total_time_minutes % 60)
        seconds = 0
        while total_time_seconds > 0:
            if not self.pause:
                self.label_timer['text'] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
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
        self.timeout()

    def timeout(self):
        for button in self.buttons:
            button['text'] = ''
            button['bg'] = '#f0f0f0'
            button['state'] = 'disabled'
        self.next_button['text'] = 'end quiz'
        self.next_button['state'] = 'normal'
        self.next_button['command'] = self.end_quiz
        self.label_question['text'] = "Timeout...\nPress 'end quiz' to see your results"

    def pause_quiz(self):
        self.pause = not self.pause

    def restart_quiz(self):
        pass


# Global variables declaration
if __name__ == "__main__":
    python_quiz = Quiz()
    python_quiz.root.mainloop()
