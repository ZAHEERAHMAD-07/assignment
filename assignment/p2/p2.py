import threading
import numpy as np
import matplotlib.pyplot as plt

class Student:
    def __init__(self, name, quiz, test, assignment):
        self.name = name
        self.quiz = quiz
        self.test = test
        self.assignment = assignment

    def calculate_average_score(self):
        return (self.quiz + self.test + self.assignment) / 3

class Assessment:
    def __init__(self, name):
        self.name = name
        self.scores = []

    def add_score(self, score):
        self.scores.append(score)

    def calculate_average_score(self):
        return sum(self.scores) / len(self.scores)

def read_file(filename, students):
    with open(filename, 'r') as file:
        for line in file:
            data = line.strip().split(',')
            if len(data) == 4:  # Ensure there are 4 elements in the list
                name = data[0].strip()
                quiz = int(data[1].strip())
                test = int(data[2].strip())
                assignment = int(data[3].strip())
                student = Student(name, quiz, test, assignment)
                students.append(student)
            else:
                print(f"Ignoring invalid data: {line}")


def plot_histograms(students):
    quiz_scores = [student.quiz for student in students]
    test_scores = [student.test for student in students]
    assignment_scores = [student.assignment for student in students]

    plt.figure(figsize=(10, 6))
    plt.hist(quiz_scores, bins=10, alpha=0.5, label='Quiz')
    plt.hist(test_scores, bins=10, alpha=0.5, label='Test')
    plt.hist(assignment_scores, bins=10, alpha=0.5, label='Assignment')
    plt.title('Distribution of Scores for Each Assessment Type')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_average_scores_bar_chart(avg_scores):
    assessments = list(avg_scores.keys())
    scores = list(avg_scores.values())

    plt.figure(figsize=(8, 5))
    plt.bar(assessments, scores, color='skyblue')
    plt.title('Average Scores for Each Assessment Type')
    plt.xlabel('Assessment Type')
    plt.ylabel('Average Score')
    plt.grid(axis='y')
    plt.show()

def main():
    filename = "C:/Users/Yasin/Desktop/assignment/p2/student_grades.txt"
    students = []

    # Utilize multithreading to read and process the file concurrently
    thread = threading.Thread(target=read_file, args=(filename, students))
    thread.start()
    thread.join()

    # Plot histograms for each type of assessment
    plot_histograms(students)

    # Calculate average score for each type of assessment
    quiz_scores = [student.quiz for student in students]
    test_scores = [student.test for student in students]
    assignment_scores = [student.assignment for student in students]
    avg_scores = {
        'Quiz': np.mean(quiz_scores),
        'Test': np.mean(test_scores),
        'Assignment': np.mean(assignment_scores)
    }

    # Plot a bar chart to compare the average scores of each assessment type
    plot_average_scores_bar_chart(avg_scores)

if __name__ == "__main__":
    main()
