import csv

class Student:
    def __init__(self, student_id, name, age, grade):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade

    def __str__(self):
        return f"ID: {self.student_id}, Name: {self.name}, Age: {self.age}, Grade: {self.grade}"

class StudentManagementSystem:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        if self._is_unique_id(student.student_id):
            self.students.append(student)
            print("Student added successfully.")
        else:
            print("Student ID already exists. Please choose a different ID.")

    def display_students(self):
        if self.students:
            for student in self.students:
                print(student)
        else:
            print("No student records found.")

    def search_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                print("Student found:")
                print(student)
                return
        print("Student not found.")

    def update_student(self, student_id, new_name, new_age, new_grade):
        for student in self.students:
            if student.student_id == student_id:
                student.name = new_name
                student.age = new_age
                student.grade = new_grade
                print("Student information updated successfully.")
                return
        print("Student not found.")

    def delete_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                self.students.remove(student)
                print("Student deleted successfully.")
                return
        print("Student not found.")

    def load_students_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    student = Student(*row)
                    self.add_student(student)  # Utilize add_student to ensure uniqueness
            print("Students loaded successfully from file.")
        except FileNotFoundError:
            print("File not found.")

    def save_students_to_file(self, filename):
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                for student in self.students:
                    writer.writerow([student.student_id, student.name, student.age, student.grade])
            print("Students saved successfully to file.")
        except IOError:
            print("Error occurred while saving to file.")

    def _is_unique_id(self, student_id):
        return all(student.student_id != student_id for student in self.students)

# Example usage
def main():
    sms = StudentManagementSystem()

    # Load student records from a file
    sms.load_students_from_file("C:/Users/Yasin/Desktop/assignment/p1/students.csv")

    while True:
        print("\n1. Add Student")
        print("2. Display Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Save and Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            student_id = input("Enter student ID: ")
            name = input("Enter student name: ")
            age = input("Enter student age: ")
            grade = input("Enter student grade: ")
            student = Student(student_id, name, age, grade)
            sms.add_student(student)

        elif choice == "2":
            sms.display_students()

        elif choice == "3":
            student_id = input("Enter student ID to search: ")
            sms.search_student(student_id)

        elif choice == "4":
            student_id = input("Enter student ID to update: ")
            new_name = input("Enter new name: ")
            new_age = input("Enter new age: ")
            new_grade = input("Enter new grade: ")
            sms.update_student(student_id, new_name, new_age, new_grade)

        elif choice == "5":
            student_id = input("Enter student ID to delete: ")
            sms.delete_student(student_id)

        elif choice == "6":
            # Save students to a file and exit
            sms.save_students_to_file("students.csv")
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
