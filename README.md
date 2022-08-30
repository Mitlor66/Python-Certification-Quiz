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

## Version 0.2.1
Correct answer highlighted when user is wrong. Additionally, all questions will now be in the same file, reducing
drastically the amount of files to generate for the Quiz. Suppression of any useless question files from previous
versions.  The number of questions for each section of the certification will now be correctly generated 
(7 for section 1 and 3, 8 for section 2 and 4). 60 questions for the quiz so far.

## Version 0.2.2
Always 4 choices per question. Optimisation of code.
To do:
Add a timer + Timeout when timer is over
Number of questions left for students
Menu bar with some options to define

## Version 0.2.3
Timer depending on the number of questions selected by the user (1.30 minute per question). Progress bar showing
the progress so far through the quiz. When timeout, final score displayed for the user to see with how many questions
they answered in total. 

## Version 0.2.4
A new dark theme has been added for the user. Quiz pause option. Pause the timer when quiz is
over. 7 more questions added to the quiz.

## Version 0.3.0
Full transformation of code from procedural to Object-Oriented. Addition of 8 questions to the code.

## Version 0.3.1
Main page for user to decide how many questions in total (only works for 30 so far), time per question and which
theme they would like to use during the quiz.