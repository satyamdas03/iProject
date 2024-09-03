import customtkinter as ctk
import json  # or any other storage solution you prefer
import threading
import time
import re

def organize_tasks(corpus):
    # Initialize a list to store tasks with their times
    tasks = []

    # Regular expression to find tasks and their time from sentences like "task1 will take 20 minutes"
    pattern = r"(.*?)(?:will take|needs|takes|requires)\s*(\d+)\s*(minutes|minute|hours|hour)"

    # Find all matches in the input corpus
    matches = re.findall(pattern, corpus, re.IGNORECASE)

    for match in matches:
        task_name = match[0].strip()
        time_value = int(match[1])
        time_unit = match[2].lower()

        # Convert hours to minutes if needed
        if 'hour' in time_unit:
            time_value *= 60

        # Append the task and its duration to the list
        tasks.append((task_name, time_value))

    # Sort tasks based on time in descending order
    tasks.sort(key=lambda x: x[1], reverse=True)

    # Format the sorted tasks for display
    sorted_tasks = [f"{task[0]}: {task[1]} minutes" for task in tasks]

    return sorted_tasks


def set_alarm(task, time_duration):
    # Implement alarm logic here
    pass

def send_reminder(task):
    # Implement SMS sending logic
    pass

class TaskOrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Task Organizer")
        self.geometry("400x600")  # Adjusted width for single-column layout
        
        # Configure grid layout (single column)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(list(range(6)), weight=1)
        
        # Single Column: Task Input and Organize Button
        self.task_input = ctk.CTkTextbox(self, width=300, height=150)
        self.task_input.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.organize_button = ctk.CTkButton(self, text="Organize", command=self.organize_tasks)
        self.organize_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.tasks_label = ctk.CTkLabel(self, text="Tasks of the Day")
        self.tasks_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="n")

        self.task_list = ctk.CTkTextbox(self, width=300, height=150)
        self.task_list.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        # Documentation and Save Button
        self.doc_label = ctk.CTkLabel(self, text="Document your day @10 pm to 10:30pm")
        self.doc_label.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="s")

        self.doc_input = ctk.CTkTextbox(self, width=300, height=100)
        self.doc_input.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")

        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_documentation)
        self.save_button.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

    def organize_tasks(self):
        corpus = self.task_input.get("1.0", "end-1c")
        tasks = organize_tasks(corpus)
        self.task_list.delete("1.0", "end")
        for task in tasks:
            self.task_list.insert("end", task + "\n")

    def save_documentation(self):
        # Implement the save logic here
        pass

if __name__ == "__main__":
    app = TaskOrganizerApp()
    app.mainloop()