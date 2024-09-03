import tkinter as tk
from tkinter import Text, Label, Button, Frame
from PIL import Image, ImageTk
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


class TaskOrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Organizer")
        self.geometry("700x600")  # Increased width to accommodate sidebar

        # Create the sidebar frame
        sidebar = Frame(self, width=100, bg='grey')
        sidebar.pack(side='left', fill='y')

        # Load icons with Pillow and resize them
        self.music_icon = Image.open('music_icon.png')
        self.music_icon = self.music_icon.resize((50, 50), Image.LANCZOS)  # Resize icon
        self.music_icon = ImageTk.PhotoImage(self.music_icon)

        self.docs_icon = Image.open('docs_icon.png')
        self.docs_icon = self.docs_icon.resize((50, 50), Image.LANCZOS)  # Resize icon
        self.docs_icon = ImageTk.PhotoImage(self.docs_icon)

        # Add the music icon to the top of the sidebar
        music_label = Label(sidebar, image=self.music_icon, bg='grey')
        music_label.pack(pady=10)

        # Add the DOCs icon to the bottom of the sidebar
        docs_label = Label(sidebar, image=self.docs_icon, bg='grey')
        docs_label.pack(side='bottom', pady=10)

        # Create a frame for the main content
        main_frame = Frame(self)
        main_frame.pack(side='left', fill='both', expand=True)  # Allow main_frame to expand

        # Configure grid layout (single column)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(list(range(7)), weight=1)

        # Single Column: Task Input and Organize Button
        self.task_input = Text(main_frame, width=40, height=8)
        self.task_input.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.organize_button = Button(main_frame, text="Organize", command=self.organize_tasks)
        self.organize_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.tasks_label = Label(main_frame, text="Tasks of the Day", font=("Arial", 12, "bold"))
        self.tasks_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="n")

        self.task_list = Text(main_frame, width=40, height=8)
        self.task_list.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        # Documentation and Save Button
        self.doc_label = Label(main_frame, text="Document your day from 10 pm to 10:30pm", font=("Arial", 12, "bold"))
        self.doc_label.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="s")

        self.doc_input = Text(main_frame, width=40, height=6)
        self.doc_input.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")

        self.save_button = Button(main_frame, text="Save", command=self.save_documentation)
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
