import pandas as pd
import random


def read_file(filename):
    return pd.read_json(filename)


def generate_question():
    r = random.choice(possible_questions_id)
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
    while a not in possible_answers:
        a = input("What is your answer? ")
        if a not in possible_answers:
            print("Wrong input, please enter one of the following possible answer:", possible_answers)
        elif a == answer:
            print("well done")
        else:
            print("wrong, sorry, the answer was", answer)


data = read_file("all questions.json")
questions = data["questions"]
number_of_questions = len(questions)
possible_questions_id = [x for x in range(number_of_questions)]
generate_question()
