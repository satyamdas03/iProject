import tkinter as tk
from tkinter import Text, Label, Button, Frame, Toplevel, Scrollbar, Entry, Canvas
from PIL import Image, ImageTk
import json
import threading
import time
import re
import webbrowser
import os  # Add this line to import the os module
from playsound import playsound  

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
        self.geometry("600x1000")

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

        #delete icon
        self.delete_icon = Image.open('icons/delete_icon.png').resize((20, 20), Image.LANCZOS)
        self.delete_icon = ImageTk.PhotoImage(self.delete_icon)

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

        # Task Input Section
        self.task_date_label = Label(main_frame, text="Enter Date (YYYY-MM-DD):")
        self.task_date_label.pack(padx=10, pady=(10, 0))

        self.task_date_entry = Entry(main_frame)
        self.task_date_entry.pack(padx=10, pady=5)

        self.task_input = Text(main_frame, width=60, height=8)
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

        # Documentation Section
        self.doc_label = Label(main_frame, text="Document your day from 10 pm to 10:30pm", font=("Arial", 12, "bold"))
        self.doc_label.pack(padx=10, pady=(10, 0))

        self.doc_input = Text(main_frame, width=40, height=6)
        self.doc_input.pack(padx=10, pady=10)

        self.save_button = Button(main_frame, text="Save", command=self.save_documentation)
        self.save_button.pack(padx=10, pady=(5, 20))

        # Data storage
        self.documentation = {}
        self.saved_tasks = {}
        self.alarms = {}  # Dictionary to store alarm threads

        # Load previously saved data
        self.load_saved_data()

    def organize_tasks(self):
        date = self.task_date_entry.get()
        corpus = self.task_input.get("1.0", "end-1c")
        tasks = organize_tasks(corpus)

        # Save tasks by date
        if date not in self.saved_tasks:
            self.saved_tasks[date] = []

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
            self.saved_tasks[date].append(task_with_time)

        # Save data to file
        self.save_to_file()

    def set_alarm_dialog(self, task):
        """Open a dialog to set alarm time for the task."""
        alarm_window = Toplevel(self)
        alarm_window.title(f"Set Alarm for {task}")
        alarm_window.geometry("300x200")

        Label(alarm_window, text=f"Set alarm for {task}").pack(pady=10)

        self.hour_entry = Entry(alarm_window, width=5)
        self.hour_entry.insert(0, "HH")
        self.hour_entry.pack(pady=5)

        self.minute_entry = Entry(alarm_window, width=5)
        self.minute_entry.insert(0, "MM")
        self.minute_entry.pack(pady=5)

        set_alarm_button = Button(alarm_window, text="Set Alarm", command=lambda: self.set_alarm(task, alarm_window))
        set_alarm_button.pack(pady=10)

    def set_alarm(self, task, window):
        """Set an alarm for a specific task."""
        hour = int(self.hour_entry.get())
        minute = int(self.minute_entry.get())

        alarm_time = f"{hour:02}:{minute:02}"

        # Save the alarm for the task
        if task not in self.alarms:
            self.alarms[task] = []

        alarm_thread = threading.Thread(target=self.monitor_alarm, args=(task, alarm_time), daemon=True)
        alarm_thread.start()

        self.alarms[task].append(alarm_thread)

        # Close the alarm setting window
        window.destroy()

    def monitor_alarm(self, task, alarm_time):
        """Monitor the alarm time and sound an alarm when time is matched."""
        while True:
            current_time = time.strftime("%H:%M")

            if current_time == alarm_time:
                # Play the alarm sound and wait until turned off
                self.sound_alarm(task)
                break

            time.sleep(10)  # Check every 10 seconds

    def sound_alarm(self, task):
        """Play an alarm sound until the user turns it off."""
        alarm_window = Toplevel(self)
        alarm_window.title(f"Alarm for {task}")
        alarm_window.geometry("300x150")

        Label(alarm_window, text=f"Alarm for task: {task}").pack(pady=20)

        stop_button = Button(alarm_window, text="Stop Alarm", command=lambda: self.stop_alarm(alarm_window))
        stop_button.pack(pady=10)

        # Sound alarm until stopped
        def play_alarm():
            while True:
                playsound("alarm_sound.mp3")  # Replace with your alarm sound path
                time.sleep(5)  # Play every 5 seconds until stopped

        self.alarm_thread = threading.Thread(target=play_alarm, daemon=True)
        self.alarm_thread.start()

    def stop_alarm(self, window):
        """Stop the alarm and close the alarm window."""
        self.alarm_thread = None  # Stop the alarm thread
        window.destroy()


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

        # Insert saved tasks into the text widget by date
        for date, tasks in self.saved_tasks.items():
            # Create a frame for the date and delete icon
            date_frame = Frame(task_window)
            date_frame.pack(fill='x', pady=5)

            # Add the date label with some padding on the bottom
            date_label = Label(date_frame, text=f"Date: {date}", anchor='w')
            date_label.pack(side='left', fill='x', padx=(5, 0))

            # Add the delete button with the delete icon
            delete_button = Button(date_frame, image=self.delete_icon, command=lambda d=date: self.delete_tasks(d, task_window))
            delete_button.pack(side='right', padx=5)

            # Place the date and delete icon frame into the Text widget
            text_area.window_create('end', window=date_frame)
            text_area.insert('end', '\n')

            # Insert tasks for the date below the date frame
            for task in tasks:
                task_text = f"  - {task}\n"
                text_area.insert('end', task_text)
            text_area.insert('end', "\n")  # Add extra newline after tasks



    def save_documentation(self):
        date = self.task_date_entry.get()  # Use the date from the task section
        doc_text = self.doc_input.get("1.0", "end-1c")
        if doc_text:
            if date not in self.documentation:
                self.documentation[date] = []
            self.documentation[date].append(doc_text)  # Save documentation
            self.doc_input.delete("1.0", "end")  # Clear the input field

        # Save data to file
        self.save_to_file()


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

        # Insert saved documentation into the text widget by date
        for date, docs in self.documentation.items():
            # Create a frame for the date and delete icon
            date_frame = Frame(doc_window)
            date_frame.pack(fill='x', pady=5)

            # Add the date label with some padding on the bottom
            date_label = Label(date_frame, text=f"Date: {date}", anchor='w')
            date_label.pack(side='left', fill='x', padx=(5, 0))

            # Add the delete button with the delete icon
            delete_button = Button(date_frame, image=self.delete_icon, command=lambda d=date: self.delete_documentation(d, doc_window))
            delete_button.pack(side='right', padx=5)

            # Place the date and delete icon frame into the Text widget
            text_area.window_create('end', window=date_frame)
            text_area.insert('end', '\n')

            # Insert documentation for the date below the date frame
            for doc in docs:
                doc_text = f"  - {doc}\n"
                text_area.insert('end', doc_text)
            text_area.insert('end', "\n")  # Add extra newline after documentation



    def delete_tasks(self, date, window):
        # Delete the tasks for the given date
        if date in self.saved_tasks:
            del self.saved_tasks[date]
            self.save_to_file()  # Save the updated data
            window.destroy()  # Close the window
            self.show_tasks(None)  # Reopen to refresh the display

    def delete_documentation(self, date, window):
        # Delete the documentation for the given date
        if date in self.documentation:
            del self.documentation[date]
            self.save_to_file()  # Save the updated data
            window.destroy()  # Close the window
            self.show_documentation(None)  # Reopen to refresh the display


    def open_music_search(self, event):
        search_window = Toplevel(self)
        search_window.title("Music Search")
        search_window.geometry("400x200")

        search_label = Label(search_window, text="Enter Music Name:")
        search_label.pack(pady=10)

        search_entry = Entry(search_window, width=40)
        search_entry.pack(pady=10)

        play_button = Button(search_window, text="Play", command=lambda: self.play_music(search_entry.get()))
        play_button.pack(pady=10)

    def play_music(self, music_name):
        search_url = f"https://www.google.com/search?q={music_name}+song"
        webbrowser.open(search_url)


    def save_to_file(self):
        """Save tasks and documentation to a file."""
        data = {
            "tasks": self.saved_tasks,
            "documentation": self.documentation,
        }
        with open("task_data.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_saved_data(self):
        """Load tasks and documentation from a file."""
        if os.path.exists("task_data.json"):
            with open("task_data.json", "r") as f:
                data = json.load(f)
                self.saved_tasks = data.get("tasks", {})
                self.documentation = data.get("documentation", {})

    def set_alarm(self, task):
        # Implement alarm logic
        pass

    def send_reminder(self, task):
        # Implement reminder logic
        pass

if __name__ == "__main__":
    app = TaskOrganizerApp()
    app.mainloop()
