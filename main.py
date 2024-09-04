import tkinter as tk
from tkinter import Text, Label, Button, Frame, Toplevel, Scrollbar, Entry
from PIL import Image, ImageTk
import json
import threading
import time
import re
import webbrowser


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
        self.geometry("600x550")  # Increased width to accommodate sidebar

        # Create the sidebar frame
        sidebar = Frame(self, width=80, bg='grey')
        sidebar.pack(side='right', fill='y')

        # Load icons with Pillow and resize them
        self.music_icon = Image.open('icons/music_icon.png')
        self.music_icon = self.music_icon.resize((30, 30), Image.LANCZOS)  # Resize icon
        self.music_icon = ImageTk.PhotoImage(self.music_icon)

        self.docs_icon = Image.open('icons/docs_icon.png')
        self.docs_icon = self.docs_icon.resize((30, 30), Image.LANCZOS)  # Resize icon
        self.docs_icon = ImageTk.PhotoImage(self.docs_icon)

        # Add the music icon to the top of the sidebar
        music_label = Label(sidebar, image=self.music_icon, bg='grey')
        music_label.pack(pady=10)

        # Add the DOCs icon to the bottom of the sidebar
        self.docs_label = Label(sidebar, image=self.docs_icon, bg='grey')
        self.docs_label.pack(side='bottom', pady=10)

        # Bind the docs icon to the method
        self.docs_label.bind("<Button-1>", self.show_documentation)

        # Bind the music icon to the method
        music_label.bind("<Button-1>", self.open_music_search)

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

        self.documentation = []  # List to store documentation entries

    def organize_tasks(self):
        corpus = self.task_input.get("1.0", "end-1c")
        tasks = organize_tasks(corpus)
        self.task_list.delete("1.0", "end")
        for task in tasks:
            self.task_list.insert("end", task + "\n")

    def save_documentation(self):
        doc_text = self.doc_input.get("1.0", "end-1c")
        if doc_text:
            self.documentation.append(doc_text)  # Save documentation
            self.doc_input.delete("1.0", "end")  # Clear the input field

    def show_documentation(self, event):
        # Create a new window to display documentation
        doc_window = Toplevel(self)
        doc_window.title("Saved Documentation")
        doc_window.geometry("400x400")

        # Add a text widget to the new window
        text_area = Text(doc_window, wrap='word')
        text_area.pack(expand=True, fill='both')

        # Add a scrollbar
        scrollbar = Scrollbar(text_area)
        scrollbar.pack(side='right', fill='y')
        text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_area.yview)

        # Insert saved documentation into the text widget
        for entry in self.documentation:
            text_area.insert('end', entry + "\n\n")

    def open_music_search(self, event):
        # Create a new window for music search
        search_window = Toplevel(self)
        search_window.title("Music Search")
        search_window.geometry("300x150")

        # Add an entry widget for music search
        search_label = Label(search_window, text="Enter music name:")
        search_label.pack(pady=5)

        self.search_entry = Entry(search_window, width=30)
        self.search_entry.pack(pady=5)

        # Add a play button
        play_button = Button(search_window, text="Play", command=self.play_music)
        play_button.pack(pady=10)

    def play_music(self):
        music_name = self.search_entry.get()
        if music_name:
            # Open a web browser to search for the music on YouTube
            search_query = '+'.join(music_name.split())
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

if __name__ == "__main__":
    app = TaskOrganizerApp()
    app.mainloop()
