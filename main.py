import tkinter as tk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import Text, Label, Button, Frame, Toplevel, Scrollbar, Entry, Canvas, messagebox
from PIL import Image, ImageTk
import json
import openai
import threading
import time
import re
import webbrowser
import os  # Add this line to import the os module
from playsound import playsound 
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


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
        self.alarm_stop_flag = threading.Event() 
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
        self.project_label.bind("<Button-1>", self.open_project_gui)

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
            alarm_button = Button(task_item_frame, image=self.alarm_icon, command=lambda t=task_with_time: self.set_alarm_dialog(t))
            alarm_button.pack(side='right', padx=5)

            # Add reminder icon
            reminder_button = Button(task_item_frame, image=self.reminder_icon, command=lambda t=task_with_time: self.send_reminder(t))
            reminder_button.pack(side='right')

            # Save the task
            self.saved_tasks[date].append(task_with_time)

        # Save data to file
        self.save_to_file()

    
    def set_alarm_from_button(self, task, alarm_window):
        """Handle the setting of the alarm from the button and close the window."""
        try:
            # Extract time from entry fields
            hour = int(self.hour_entry.get())
            minute = int(self.minute_entry.get())
            alarm_time = f"{hour:02}:{minute:02}"
            print(f"Alarm set for {task} at {alarm_time}")  # Debugging output

            # Save the alarm for the task
            if task not in self.alarms:
                self.alarms[task] = []

            alarm_thread = threading.Thread(target=self.monitor_alarm, args=(task, alarm_time), daemon=True)
            alarm_thread.start()

            self.alarms[task].append(alarm_thread)

            # Close the alarm window after setting the alarm
            alarm_window.destroy()

        except ValueError:
            print("Invalid time entered. Please ensure you input the correct hour and minute.")



    def set_alarm_dialog(self, task):
        """Open a dialog to set alarm time for the task."""
        print(f"Alarm dialog triggered for task: {task}")  # Debugging output
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

        # Modify the button to call set_alarm_from_button
        set_alarm_button = Button(alarm_window, text="Set Alarm", command=lambda: self.set_alarm_from_button(task, alarm_window))
        set_alarm_button.pack(pady=10)

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
        alarm_window = tk.Toplevel(self)
        alarm_window.title(f"Alarm for {task}")
        alarm_window.geometry("300x150")

        tk.Label(alarm_window, text=f"Alarm for task: {task}").pack(pady=20)

        stop_button = tk.Button(alarm_window, text="Stop Alarm", command=lambda: self.stop_alarm(alarm_window))
        stop_button.pack(pady=10)

        # Reset the stop flag in case it's set from a previous alarm
        self.alarm_stop_flag.clear()

        # Sound alarm until stopped
        def play_alarm():
            while not self.alarm_stop_flag.is_set():
                playsound("alarm_sound.mp3")  # Replace with your alarm sound path
                time.sleep(5)  # Play every 5 seconds until stopped

        self.alarm_thread = threading.Thread(target=play_alarm, daemon=True)
        self.alarm_thread.start()


    def stop_alarm(self, window):
        """Stop the alarm and close the alarm window."""
        self.alarm_stop_flag.set()  # Signal the alarm thread to stop
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

    def open_project_gui(self, event):
        # Create a new window for the project section
        project_window = Toplevel(self)
        project_window.title("Project Idea to Steps")
        project_window.geometry("600x600")

        # Project Name Entry
        Label(project_window, text="Enter Project Name:", font=("Arial", 12)).pack(pady=10)
        project_name_entry = Entry(project_window, width=50)
        project_name_entry.pack(pady=5)

        # Project Idea Entry
        Label(project_window, text="Enter the Idea of the Project:", font=("Arial", 12)).pack(pady=10)
        project_idea_text = Text(project_window, height=5, width=50)
        project_idea_text.pack(pady=5)

        # Stepify Button
        stepify_button = Button(project_window, text="Stepify", command=lambda: self.generate_steps(project_name_entry.get(), project_idea_text.get("1.0", "end-1c"), project_window))
        stepify_button.pack(pady=10)

        # Stepwise Instructions Label
        Label(project_window, text="Stepwise Instructions:", font=("Arial", 12)).pack(pady=10)

        # Text box to show AI-generated instructions
        self.stepwise_instructions_text = Text(project_window, height=25, width=65)
        self.stepwise_instructions_text.pack(pady=5)


    def generate_steps(self, project_name, project_idea, window):
        if not project_name or not project_idea:
            messagebox.showerror("Error", "Please fill out both the project name and project idea.")
            return

        try:
            # Generate stepwise instructions using OpenAI's Chat Completion API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Or gpt-4 if you're using that model
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an assistant that helps people break down complex project ideas "
                            "into detailed, actionable steps. For each project, provide specific steps with "
                            "clear instructions, timelines, resources needed, tools to be used, potential challenges, "
                            "and how to overcome them. Make sure the steps are organized into phases like "
                            "'Planning', 'Execution', and 'Finalization'."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Break down the following project idea into detailed stepwise instructions, "
                            f"including sub-tasks, required tools, resources, timelines, potential challenges, "
                            f"and solutions. Here's the project idea: {project_idea}"
                        )
                    }
                ],
                temperature=0.7,
                max_tokens=500,  # Increase token limit for more detailed responses
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            # Extract the generated steps
            steps = response.choices[0].message['content'].strip()

            # Insert AI-generated steps into the text box
            self.stepwise_instructions_text.delete("1.0", "end")
            self.stepwise_instructions_text.insert("end", steps)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating steps: {str(e)}")


if __name__ == "__main__":
    app = TaskOrganizerApp()
    app.mainloop()
# check 