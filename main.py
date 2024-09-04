import tkinter as tk
from tkinter import Text, Label, Button, Frame, Toplevel, Scrollbar, Entry, Canvas
from PIL import Image, ImageTk
import json
import threading
import time
import re
import webbrowser


def organize_tasks(corpus):
    tasks = []
    pattern = r"(.*?)(?:will take|needs|takes|requires)\s*(\d+)\s*(minutes|minute|hours|hour)"
    matches = re.findall(pattern, corpus, re.IGNORECASE)
    
    for match in matches:
        task_name = match[0].strip()
        time_value = int(match[1])
        time_unit = match[2].lower()
        if 'hour' in time_unit:
            time_value *= 60
        tasks.append((task_name, time_value))
    
    tasks.sort(key=lambda x: x[1], reverse=True)
    sorted_tasks = [f"{task[0]}: {task[1]} minutes" for task in tasks]
    
    return tasks


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
        self.geometry("600x750")

        # Sidebar
        sidebar = Frame(self, width=80, bg='grey')
        sidebar.pack(side='right', fill='y')

        # Load icons with Pillow and resize them
        self.music_icon = Image.open('icons/music_icon.png').resize((30, 30), Image.LANCZOS)
        self.music_icon = ImageTk.PhotoImage(self.music_icon)

        self.docs_icon = Image.open('icons/docs_icon.png').resize((30, 30), Image.LANCZOS)
        self.docs_icon = ImageTk.PhotoImage(self.docs_icon)

        self.task_icon = Image.open('icons/task_icon.png').resize((30, 30), Image.LANCZOS)  # Task icon
        self.task_icon = ImageTk.PhotoImage(self.task_icon)

        self.project_icon = Image.open('icons/project_icon.png').resize((30, 30), Image.LANCZOS)  # Task icon
        self.project_icon = ImageTk.PhotoImage(self.project_icon)

        self.alarm_icon = Image.open('icons/alarm_icon.png').resize((20, 20), Image.LANCZOS)  # Alarm icon
        self.alarm_icon = ImageTk.PhotoImage(self.alarm_icon)

        self.reminder_icon = Image.open('icons/reminder_icon.png').resize((20, 20), Image.LANCZOS)  # Reminder icon
        self.reminder_icon = ImageTk.PhotoImage(self.reminder_icon)

        # Add icons to the sidebar
        music_label = Label(sidebar, image=self.music_icon, bg='grey')
        music_label.pack(pady=10)

        self.docs_label = Label(sidebar, image=self.docs_icon, bg='grey')
        self.docs_label.pack(side='bottom', pady=10)

        self.task_label = Label(sidebar, image=self.task_icon, bg='grey')
        self.task_label.pack(pady=10)

        self.project_label = Label(sidebar, image=self.project_icon, bg='grey')
        self.project_label.pack(pady=10)

        # Bind icon actions
        self.docs_label.bind("<Button-1>", self.show_documentation)
        music_label.bind("<Button-1>", self.open_music_search)
        self.task_label.bind("<Button-1>", self.show_tasks)

        # Main Frame
        main_frame = Frame(self)
        main_frame.pack(side='left', fill='both', expand=True)

        self.task_input = Text(main_frame, width=40, height=8)
        self.task_input.pack(padx=10, pady=10)

        self.organize_button = Button(main_frame, text="Organize", command=self.organize_tasks)
        self.organize_button.pack(padx=10, pady=10)

        self.tasks_label = Label(main_frame, text="Tasks of the Day", font=("Arial", 12, "bold"))
        self.tasks_label.pack(padx=10, pady=(10, 0))

        # Task Display Frame
        task_display_frame = Frame(main_frame)
        task_display_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.task_canvas = Canvas(task_display_frame)
        self.task_canvas.pack(side='left', fill='both', expand=True)

        # Create a scrollbar for the canvas
        scrollbar = Scrollbar(task_display_frame, orient="vertical", command=self.task_canvas.yview)
        scrollbar.pack(side='right', fill='y')
        self.task_canvas.configure(yscrollcommand=scrollbar.set)

        self.task_frame = Frame(self.task_canvas)
        self.task_canvas.create_window((0, 0), window=self.task_frame, anchor='nw')

        # Update the scroll region whenever the frame size changes
        self.task_frame.bind("<Configure>", lambda e: self.task_canvas.configure(scrollregion=self.task_canvas.bbox("all")))

        self.doc_label = Label(main_frame, text="Document your day from 10 pm to 10:30pm", font=("Arial", 12, "bold"))
        self.doc_label.pack(padx=10, pady=(10, 0))

        self.doc_input = Text(main_frame, width=40, height=6)
        self.doc_input.pack(padx=10, pady=10)

        self.save_button = Button(main_frame, text="Save", command=self.save_documentation)
        self.save_button.pack(padx=10, pady=10)

        # Data storage
        self.documentation = []
        self.saved_tasks = []

    def organize_tasks(self):
        corpus = self.task_input.get("1.0", "end-1c")
        tasks = organize_tasks(corpus)

        # Clear the previous tasks
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        for task_name, time_value in tasks:
            task_with_time = f"{task_name}: {time_value} minutes"

            # Create a new frame for each task
            task_item_frame = Frame(self.task_frame)
            task_item_frame.pack(fill='x', pady=5)

            # Add the task text to the frame
            task_label = Label(task_item_frame, text=task_with_time)
            task_label.pack(side='left')

            # Add alarm icon
            alarm_button = Button(task_item_frame, image=self.alarm_icon, command=lambda t=task_with_time: self.set_alarm(t))
            alarm_button.pack(side='right', padx=5)

            # Add reminder icon
            reminder_button = Button(task_item_frame, image=self.reminder_icon, command=lambda t=task_with_time: self.send_reminder(t))
            reminder_button.pack(side='right')

            # Save the task
            self.save_tasks(task_with_time)

    def save_tasks(self, task):
        self.saved_tasks.append(task)

    def show_tasks(self, event):
        # Create a new window to display saved tasks
        task_window = Toplevel(self)
        task_window.title("Saved Tasks")
        task_window.geometry("400x400")

        # Add a text widget to the new window
        text_area = Text(task_window, wrap='word')
        text_area.pack(expand=True, fill='both')

        # Add a scrollbar
        scrollbar = Scrollbar(text_area)
        scrollbar.pack(side='right', fill='y')
        text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_area.yview)

        # Insert saved tasks into the text widget
        for entry in self.saved_tasks:
            text_area.insert('end', entry + "\n\n")

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

        text_area = Text(doc_window, wrap='word')
        text_area.pack(expand=True, fill='both')

        scrollbar = Scrollbar(text_area)
        scrollbar.pack(side='right', fill='y')
        text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_area.yview)

        for entry in self.documentation:
            text_area.insert('end', entry + "\n\n")

    def open_music_search(self, event):
        music_window = Toplevel(self)
        music_window.title("Music Search")
        music_window.geometry("400x200")

        search_label = Label(music_window, text="Enter Music Name:")
        search_label.pack(pady=10)

        search_entry = Entry(music_window, width=50)
        search_entry.pack(pady=5)

        play_button = Button(music_window, text="Play", command=lambda: self.play_music(search_entry.get()))
        play_button.pack(pady=10)

    def play_music(self, music_name):
        if music_name:
            search_query = music_name.replace(' ', '+')
            url = f"https://www.youtube.com/results?search_query={search_query}"
            webbrowser.open(url)

    def set_alarm(self, task):
        time.sleep(2)  # Simulate the delay
        threading.Thread(target=set_alarm, args=(task,)).start()

    def send_reminder(self, task):
        threading.Thread(target=send_reminder, args=(task,)).start()


if __name__ == "__main__":
    app = TaskOrganizerApp()
    app.mainloop()
