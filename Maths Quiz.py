import random

#Function Definitions

def displayMenu():
    """Displays the difficulty menu and returns the user's choice."""
    print("\nDIFFICULTY LEVEL")
    print("1. Easy")
    print("2. Moderate")
    print("3. Advanced")

    while True:
        try:
            level = int(input("Choose a difficulty level (1-3): "))
            if level in [1, 2, 3]:
                return level
            else:
                print("Please enter a number between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def randomInt(level):
    """Returns a random integer based on the selected difficulty level."""
    if level == 1:
        return random.randint(1, 9)        # Easy → single-digit
    elif level == 2:
        return random.randint(10, 99)      # Moderate → double-digit
    elif level == 3:
        return random.randint(1000, 9999)  # Advanced → 4-digit


def decideOperation():
    """Randomly returns '+' for addition or '-' for subtraction."""
    return random.choice(['+', '-'])


def displayProblem(num1, num2, operation):
    """Displays the problem and gets the user's answer."""
    print(f"\nWhat is {num1} {operation} {num2}?")
    while True:
        try:
            answer = int(input("Your answer: "))
            return answer
        except ValueError:
            print("Please enter a valid number.")


def isCorrect(user_answer, correct_answer, attempt):
    """Checks if the user's answer is correct and returns the score for this question."""
    if user_answer == correct_answer:
        if attempt == 1:
            print("✅ Correct on first try! (+10 points)")
            return 10
        else:
            print("✅ Correct on second try! (+5 points)")
            return 5
    else:
        print("❌ Incorrect.")
        return 0


def displayResults(score):
    """Displays the final score and grade."""
    print("\n--- QUIZ RESULTS ---")
    print(f"Your total score: {score}/100")

    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    elif score >= 50:
        grade = "D"
    else:
        grade = "F"

    print(f"Your grade: {grade}")
    print("--------------------\n")

#Main Program

def playQuiz():
    level = displayMenu()
    score = 0

    for i in range(1, 11):  # 10 questions
        num1 = randomInt(level)
        num2 = randomInt(level)
        operation = decideOperation()

        # Compute correct answer
        if operation == '+':
            correct_answer = num1 + num2
        else:
            correct_answer = num1 - num2

        print(f"\nQuestion {i}:")
        user_answer = displayProblem(num1, num2, operation)
        attempt = 1

        # Check answer
        points = isCorrect(user_answer, correct_answer, attempt)
        if points == 0:
            # One more chance
            user_answer = int(input("Try again: "))
            points = isCorrect(user_answer, correct_answer, 2)

        score += points

    displayResults(score)

#Game-Loop
while True:
    playQuiz()
    again = input("Would you like to play again? (y/n): ").lower()
    if again != 'y':
        print("\nThanks for playing! Goodbye!")
        break