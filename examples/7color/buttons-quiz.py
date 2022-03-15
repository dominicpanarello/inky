#!/usr/bin/env python3

import signal
import RPi.GPIO as GPIO
import subprocess

class Quiz:
    
    def __init__(self):
        self.question = -1
        self.score = 0
        self.questions = [
        {
            "mainText": "In what year did you surprise Dom with a Sydney trip?",
            "image": "/home/pi/Pictures/quiz-01-cropped.jpg",
            "answers": ["2011", "2012", "2013", "2014"],
            "answerPosition": 2
        },
        {
            "mainText": "In what season did we float into the sky together?",
            "image": "/home/pi/Pictures/quiz-02-cropped.jpg",
            "answers": ["Winter", "Spring", "Summer", "Autumn"],
            "answerPosition": 4
        },
        {
            "mainText": "What's the name of this famous Frasier Island lake?",
            "image": "/home/pi/Pictures/quiz-03-cropped.jpg",
            "answers": ["Lake Mcflurry", "Lake Mcintyre", "Lake Mckenzie", "Lake Mcdonald"],
            "answerPosition": 3
        },
        {
            "mainText": "At whose friends' wedding was this photo taken?",
            "image": "/home/pi/Pictures/quiz-05-cropped.jpg",
            "answers": ["David", "Anna", "Ben", "None"],
            "answerPosition": 2
        },
        {
            "mainText": "What is the name of this flower festival?",
            "image": "/home/pi/Pictures/quiz-06-cropped.jpg",
            "answers": ["Florence", "Floral", "Florist", "Floriade"],
            "answerPosition": 4
        },
        {
            "mainText": "In which city was this maiko photoshoot?",
            "image": "/home/pi/Pictures/quiz-07-cropped.jpg",
            "answers": ["Kyoto", "Tokyo", "Hiroshima", "Matsumoto"],
            "answerPosition": 1
        },
        {
            "mainText": "Where did the iconic balloon race take place?",
            "image": "/home/pi/Pictures/quiz-08-cropped.jpg",
            "answers": ["Roma St", "Albert St", "Queen St", "Mary St"],
            "answerPosition": 1
        },
        {
            "mainText": "Who else was present during the photo?",
            "image": "/home/pi/Pictures/quiz-09-cropped.jpg",
            "answers": ["Michael Huo", "Michael Ottopal", "Anna", "Katy"],
            "answerPosition": 2
        },
        {
            "mainText": "Who was the victor of the mens final here?",
            "image": "/home/pi/Pictures/quiz-10-cropped.jpg",
            "answers": ["Roger", "Nadal", "Murray", "Hewitt"],
            "answerPosition": 4
        },
        {
            "mainText": "What month was our engagement shoot?",
            "image": "/home/pi/Pictures/quiz-08-cropped.jpg",
            "answers": ["January", "Feburary", "March", "April"],
            "answerPosition": 3
        }
    ]
    
    def next(self, responseAnswerPosition=None):
        # check answer
        resultText = ""
        if responseAnswerPosition and self.haveAskedQuestion() and self.haveMoreQuestions():
            if responseAnswerPosition == self.questions[self.question]["answerPosition"]:
                resultText = "Correct!"
                self.score = self.score + 1
            else:
                resultText = "Incorrect!"
            
        # check terminal condition
        self.question = self.question + 1
        if not self.haveMoreQuestions():
            return {"image": "/home/pi/Pictures/quiz-summary.jpg", "resultText": resultText, "mainText": "You scored {}/{}. \&#9829; Happy anniversary Sally! \&#9829;".format(self.score, len(self.questions))}
        
        # get next question
        nextQuestion = self.questions[self.question]
        nextQuestion["resultText"] = resultText
        
        return nextQuestion
    
    def haveAskedQuestion(self):
        return self.question >= 0
    
    def haveMoreQuestions(self):
        return self.question < len(self.questions)
        
print("""buttons-quiz.py - A simple button multi-choice quiz.

Press Ctrl+C to exit!

""")

# Gpio pins for each button (from top to bottom)
BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, C and D respectively
LABELS = [1, 2, 3, 4]

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

quiz = Quiz()
                    
# "handle_button" will be called every time a button is pressed
# It receives one argument: the associated input pin.
def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    print("Button press detected on pin: {} label: {}".format(pin, label))
    response = quiz.next(label)
    
    print(response)
    answers = ''
    if response.get("answers"):
        answers = ''.join(["<li>"+answer+"</li>" for answer in response["answers"]])
        print(answers)
        
    subprocess.run(["./html/html-quiz.sh", "./html/quiz-template.html", response["resultText"], response["mainText"], answers, response["image"]])

# Loop through out buttons and attach the "handle_button" function to each
# We're watching the "FALLING" edge (transition from 3.3V to Ground) and
# picking a generous bouncetime of 250ms to smooth out button presses.
for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)

# Finally, since button handlers don't require a "while True" loop,
# we pause the script to prevent it exiting immediately.
signal.pause()
