# Python-Certification-Quiz
A graphical tool to automatically provide questions to students that prepare for their Python Certification and 
give them the score at the end of the Quiz.

## Version 0.1.0
The program is able to load a json file in Python, read all the questions from it, select a random one and display
it in the terminal. The user can then enter their answer. A check is made to ensure the answer entered by the user is 
valid. If the input is valid, then the user's answer is compared with the correct answer. If the user is wrong, the
correct answer is displayed.

## Version 0.1.1
Add of a GUI using Tkinter with a single question being displayed at the top as well as 2 or 4 buttons 
(depending on how many possible answers).

## Version 0.2.0
Fully working version with only a sample of questions (5 so far).
The user can now move from one question to another. The user is able to see their final score at the end as well as 
if they passed the certification (70% required). The button will now display whether the user was wrong or not when
answering (red = wrong, green = correct). Cannot click buttons that shouldn't be clicked.
next_button correctly change its text depending on where the user is in the test (start, next, end, quit).
To Do:
Still have some duplicated code, cleaning required.
Add more questions to the test (at least 30)
Add a category to each question
Add feedback when answer is wrong (if possible)
Highlight correct answer when answer is wrong