import tkinter as tk
from tkinter import messagebox
import json

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App with Timer and Next Button")
        self.root.geometry("500x400")
        self.root['bg'] = 'light green'
        
        self.questions = self.load_questions("python_quiz.json")
        self.score = 0
        self.q_index = 0
        self.selected_option = tk.StringVar()
        self.timer_label = None
        self.time_left = 30  # 30 seconds for each question
        
        self.create_widgets()
        self.display_question()
        self.start_timer()
 
    def create_widgets(self):
        self.question_label = tk.Label(self.root, font=("Arial", 15), wraplength=450, bg='light green')
        self.question_label.pack(pady=20)

        self.radiobuttons = []
        for _ in range(4):
            rb = tk.Radiobutton(self.root, text="", variable=self.selected_option, value="", font=("Arial", 13), bg='light green')
            rb.pack(anchor='w', padx=50)
            self.radiobuttons.append(rb)
        
        # Next Button
        self.next_button = tk.Button(self.root, text="Next", command=self.next_question, font=("Arial", 14), bg='blue', fg='white')
        self.next_button.pack(pady=20)

        # Timer Label
        self.timer_label = tk.Label(self.root, text="Time Left: 30 sec", font=("Arial", 14), bg='light green')
        self.timer_label.pack()

    def display_question(self):
        self.selected_option.set("")  # reset selection
        q = self.questions[str(self.q_index + 1)]   # json keys are string type
        self.question_label.config(text=f"{self.q_index+1}. {q['question']}")
        for i, option in enumerate(q['options']):
            self.radiobuttons[i].config(text=option, value=option)

    def load_questions(self, file):
        with open(file, "r") as f:
            Q = json.load(f)
        return Q

    def next_question(self):
        self.check_answer()
        self.q_index += 1
        if self.q_index < len(self.questions):
            self.display_question()
            self.time_left = 30  # reset timer
        else:
            self.show_result()

    def check_answer(self):
        selected = self.selected_option.get()
        correct_answer = self.questions[str(self.q_index + 1)]["answer"]
        if selected != "":
            # 'A', 'B', 'C', 'D' se option text match karna padega
            for option_text in self.questions[str(self.q_index + 1)]["options"]:
                if option_text.startswith(correct_answer):
                    if selected == option_text:
                        self.score += 1
                        break

    def show_result(self):
        messagebox.showinfo("Quiz Over", f"Your Score is {self.score}/{len(self.questions)}")
        self.root.destroy()  # Close the app

    def start_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time Left: {self.time_left} sec")
            self.time_left -= 1
            self.root.after(1000, self.start_timer)
        else:
            messagebox.showinfo("Time's Up", "Moving to next question!")
            self.next_question()

root = tk.Tk()
app = QuizApp(root)
root.mainloop()
