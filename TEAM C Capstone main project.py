import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import shelve
import matplotlib.pyplot as plt

class QuizGame:
    def __init__(self, root, num_students=40):
        self.root = root
        self.num_students = num_students
        self.students = self.load_data()  # Load student data from the shelve
        self.last_student = None  # To store the last student number accessed for edit or delete
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        self.root.title("SIMATS ENGINEERING QUIZ SESSION - Login - Coded karthick balaji  by Team C")
        tk.Label(self.root, text="Enter your registration number:", font=("Arial", 14)).pack(pady=10)
        self.reg_entry = tk.Entry(self.root, font=("Arial", 12))
        self.reg_entry.pack(pady=5)
        tk.Button(self.root, text="Login", command=self.login, font=("Arial", 12), width=30).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.confirm_exit, font=("Arial", 12), width=30, bg="red").pack(pady=10)

    def confirm_exit(self):
        if messagebox.askokcancel("Confirm Exit", "Are you sure you want to exit?"):
            self.root.quit()

    def create_faculty_menu(self):
        self.clear_screen()
        self.root.title("SIMATS ENGINEERING QUIZ SESSION - Faculty Menu - Coded by Team C")
        menu_options = [
            ("Enter marks for a student", self.enter_marks_faculty),
            ("Edit marks for a student", self.edit_marks_faculty),
            ("Delete marks for a student", self.delete_marks_faculty),
            ("View all marks", self.display_marks),
            ("Calculate and Display Scores", self.calculate_and_display_scores),
            ("Switch to Student Menu", self.create_student_menu),
            ("Logout (Faculty)", self.create_login_screen),
            ("Number of Students to Ask Quiz", self.count_students_to_quiz),
            ("Plot Individual Marks (Pie Chart)", self.plot_individual_marks),
            ("Plot Student Marks (Bar Graph)", self.plot_bar_graph),
            ("Clear All Marks", self.clear_all_marks)  # New option for clearing all marks
        ]
        for text, command in menu_options:
            tk.Button(self.root, text=text, command=command, font=("Arial", 12), width=50).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.confirm_exit, font=("Arial", 12), width=50, bg="red").pack(pady=5)

    def create_student_menu(self):
        self.clear_screen()
        self.root.title("SIMATS ENGINEERING QUIZ SESSION - Student Menu - Coded by Team C")
        menu_options = [
            ("View all marks", self.display_marks),
            ("View Individual Marks (Pie Chart)", self.plot_individual_marks),
            ("View Student Marks (Bar Graph)", self.plot_bar_graph),
            ("Logout (Student)", self.create_login_screen),
        ]
        for text, command in menu_options:
            tk.Button(self.root, text=text, command=command, font=("Arial", 12), width=50).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.confirm_exit, font=("Arial", 12), width=50, bg="red").pack(pady=5)

    def login(self):
        registration_number = self.reg_entry.get()
        if registration_number.isalnum() and not registration_number.isdigit():
            self.create_faculty_menu()
        elif registration_number.isdigit():
            self.create_student_menu()
        else:
            messagebox.showerror("Invalid registration number", "Please enter a valid registration number.")

    def pick_random_student(self):
        if len(self.students) >= self.num_students:
            messagebox.showinfo("Info", "All students have been picked.")
            return None
        student = random.randint(1, self.num_students)
        while student in self.students:
            student = random.randint(1, self.num_students)
        return student

    def enter_marks_faculty(self):
        student = self.pick_random_student()
        if student:
            marks = simpledialog.askinteger("Enter Marks", f"Enter marks for student {student}:")
            if marks is not None:
                self.enter_marks(student, marks)

    def edit_marks_faculty(self):
        student = simpledialog.askinteger("Edit Marks", "Enter the student number to edit marks:")
        if student in self.students:
            marks = simpledialog.askinteger("Edit Marks", f"Enter new marks for student {student}:")
            if marks is not None:
                self.edit_marks(student, marks)
        else:
            messagebox.showerror("Error", f"Student {student} does not have marks entered yet.")

    def delete_marks_faculty(self):
        student = simpledialog.askinteger("Delete Marks", "Enter the student number to delete marks:")
        if student in self.students:
            self.delete_marks(student)
        else:
            messagebox.showerror("Error", f"Student {student} does not have marks entered yet.")

    def enter_marks(self, student, marks):
        self.students[student] = marks
        self.save_data()  # Save data to shelve

    def edit_marks(self, student, marks):
        if student in self.students:
            self.students[student] = marks
            self.save_data()  # Save data to shelve
        else:
            messagebox.showerror("Error", f"Student {student} does not have marks entered yet.")

    def delete_marks(self, student):
        if student in self.students:
            del self.students[student]
            self.save_data()  # Save data to shelve
        else:
            messagebox.showerror("Error", f"Student {student} does not have marks entered yet.")

    def display_marks(self):
        if not self.students:
            messagebox.showinfo("Info", "Marks are not assigned yet.")
        else:
            sorted_students = sorted(self.students.items())
            marks_str = ""
            for student, marks in sorted_students:
                grade = self.calculate_grade(marks)
                marks_str += f"Student {student}: {marks} marks (Grade: {grade})\n"
            messagebox.showinfo("Marks and Grades (in order):", marks_str)

    def calculate_and_display_scores(self):
        if not self.students:
            messagebox.showinfo("Info", "No students have marks entered yet.")
            return

        scores = [marks for marks in self.students.values()]
        total_students = len(scores)
        average_score = sum(scores) / total_students
        highest_score = max(scores)
        lowest_score = min(scores)

        score_summary = f"Total Students: {total_students}\n"
        score_summary += f"Average Score: {average_score:.2f}\n"
        score_summary += f"Highest Score: {highest_score}\n"
        score_summary += f"Lowest Score: {lowest_score}"

        messagebox.showinfo("Score Summary", score_summary)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def save_data(self):
        with shelve.open('quiz_data') as db:
            db['students'] = self.students

    def load_data(self):
        with shelve.open('quiz_data') as db:
            return db.get('students', {})

    def count_students_to_quiz(self):
        students_to_quiz = self.num_students - len(self.students)
        messagebox.showinfo("Students to Quiz", f"{students_to_quiz} students are yet to be asked to enter quiz marks.")

    def plot_individual_marks(self):
        if not self.students:
            messagebox.showinfo("Info", "No students have marks entered yet.")
            return

        student_marks = list(self.students.values())
        student_ids = list(self.students.keys())

        plt.figure(figsize=(8, 8))
        plt.pie(student_marks, labels=student_ids, autopct='%1.1f%%', startangle=140)
        plt.title('SIMATS ENGINEERING QUIZ SESSION - Individual Marks Distribution', fontdict={'fontsize': 14})
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()

    def plot_bar_graph(self):
        if not self.students:
            messagebox.showinfo("Info", "No students have marks entered yet.")
            return

        student_ids = list(self.students.keys())
        student_marks = list(self.students.values())

        plt.figure(figsize=(10, 6))
        plt.bar(student_ids, student_marks, color='blue')
        plt.xlabel('Student ID')
        plt.ylabel('Marks')
        plt.title('SIMATS ENGINEERING QUIZ SESSION - Student Marks Bar Graph', fontdict={'fontsize': 14})
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def calculate_grade(self, marks):
        if marks >= 90:
            return "S"
        elif marks >= 70:
            return "A"
        elif marks >= 55:
            return "B"
        elif marks >= 40:
            return "C"
        else:
            return "D"

    def clear_all_marks(self):
        if messagebox.askokcancel("Confirm Clear All Marks", "Are you sure you want to clear all marks?"):
            self.students.clear()
            self.save_data()
            messagebox.showinfo("Success", "All marks have been cleared.")

if __name__ == "__main__":
    root = tk.Tk()
    game = QuizGame(root)
    root.mainloop()
