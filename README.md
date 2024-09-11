# Task Organizer Application
## Introduction
The Task Organizer Application is a GUI-based tool developed using the tkinter library, providing users with an intuitive interface to manage their tasks, set alarms and reminders, document activities, and even search for music—all integrated within a user-friendly environment.

The application emphasizes time management, productivity tracking, and personalized task organization, offering features like task sorting by duration, background alarms, and persistent data storage.

## Features

1. **Organize Tasks**
   - Input tasks with their expected duration (minutes or hours).
   - Tasks are automatically parsed and sorted based on duration, allowing for effective time management.

2. **Set Alarms and Reminders**
   - Set alarms for specific tasks with notifications.
   - Alarms run in the background using threading, ensuring they do not interrupt the main program.
  
3. **Music Search**
   - A clickable music icon allows users to search for and play music directly from the application.
  
4. **Daily Documentation**
   - Users can document their activities, particularly between 10:00 PM and 10:30 PM, fostering a daily logging or journaling habit.
   - The documentation is saved for future reference.
  
5. **Task View**
   - A separate GUI allows users to view saved tasks and documentation, with tasks stored along with their respective dates.
  
6. **Alarm Management**
   - Alarms play sounds and trigger pop-up windows, enabling users to stop or manage alarms when necessary.
  
7. **Data Persistence**
   - Tasks and documentation are stored in JSON format, allowing for data persistence across sessions.
  
8. **Interactive GUI**
   - The interface features a sidebar with clickable icons for tasks, projects, music, and documentation.
   - The main content area includes input fields for tasks, a documentation section, and buttons to organize tasks and save notes.
  
## Installation
### Prerequisites
Ensure you have Python 3.x installed on your system. Additionally, you’ll need to install the following libraries:
```python
pip install tk pillow playsound openai python-dotenv
```

### Steps

1. Clone the repository or download the project files:
   ```python
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```python
   cd task-organizer-application
   ```
3. Run the application:
   ```python
   python app.py
   ```

### Usage

1. *Add Tasks*: Use the task input field to add tasks with their expected time (e.g., "Complete report in 2 hours").
2. *Set Alarms*: Set an alarm for each task to receive a notification when it's time to work on that task.
3. *Search for Music*: Click on the music icon to search for and play music while organizing tasks.
4. *Document Activities*: Use the documentation section to log activities from 10:00 PM to 10:30 PM, and save them for future reference.
5. *View Saved Tasks*: Access previously saved tasks and documentation via the task view section.

### Dependencies

The application relies on the following Python libraries:
- **tkinter**: GUI development.
- **smtplib**: Handling email notifications (if configured).
- **json**: Storing and retrieving task and documentation data.
- **threading**: Running alarms in the background.
- **PIL (Pillow)**: Handling images for the GUI icons.
- **openai**: Integrating AI-based features (if enabled).
- **playsound**: Playing sounds for alarms.
- **dotenv**: Managing environment variables.

### Configuration

1. **Environment Variables:**
   - Use a `.env` file to store sensitive data such as API keys for integrating OpenAI or email servers.
     ```python
     OPENAI_API_KEY=<your-api-key>
     EMAIL_USER=<your-email>
     EMAIL_PASS=<your-email-password>
     ```
2. **Sound Files:**
   - Ensure the alarm sound files are available in the correct directory.

## Documentation
The application includes a built-in documentation feature that allows users to log their activities between 10:00 PM and 10:30 PM. This can be used for journaling, daily reflections, or productivity tracking. The documentation is saved persistently and can be viewed later through the task view feature.

### Examples
#### Adding a Task
1. Enter a task like :
   ```task
   DSA will take 3 hours.
   ```
2. Click the "Add Task" button. The task will be parsed and added to the task list based on its duration.

#### Setting an Alarm
1. Select a task and choose a specific time to set an alarm.
2. The alarm will notify you when it's time to begin the task.

#### Troubleshooting
- **Alarm not sounding**: Ensure that the `playsound` module is correctly installed, and the sound file path is accurate.
- **ask not saving**: Check if the `tasks.json` file is accessible and has write permissions.
- **Application freezing**: The alarm system uses threading, but if tasks are too long or memory-heavy, this may cause delays. Consider optimizing your system resources.

#### Future Scope and Improvements
- Cloud Integration: Integrate with cloud storage services like Google Drive or Dropbox for task and documentation syncing.
- Task Notification System: Expand reminders to mobile or email notifications using services like Twilio for SMS alerts.
- Calendar Integration: Sync tasks with Google Calendar or Outlook for better task scheduling.
- Voice Control: Integrate voice-based commands for adding or managing tasks using voice recognition services.
- Mobile and Web Versions: Develop a mobile or web application for broader access.
- AI-Based Task Suggestions: Utilize machine learning to offer personalized suggestions based on user task history.

## Scope of the Project:
This project provides a powerful yet user-friendly task management tool with several important features, including real-time alarms and reminders. The application's potential includes:
1. **Task Management**: Organizing tasks by priority based on time requirements can help users manage their day more effectively. Sorting tasks by duration helps ensure that longer or more time-consuming tasks are prioritized accordingly.
2. **Alarms and Reminders**: The ability to set alarms for specific tasks allows for better time management, ensuring that users are notified when it’s time to focus on a task. Reminders also add a layer of interactivity by notifying users about task deadlines.
3. **Daily Documentation**: Encouraging users to document their daily activities creates a useful habit of reflection and logging. This feature can be extended to integrate journaling for professionals, students, or anyone looking to track their daily productivity.
4. **Music Search**: This feature adds a layer of customization and user engagement by allowing music integration into the task organization process. Future development could expand on this to integrate with music streaming services like Spotify or YouTube.
5. **Real-Time Task Display**: The saved tasks can be displayed in a well-organized manner, and since the data is stored persistently, users can access previously entered data anytime. This adds significant long-term value, especially for recurring tasks.
6. **Customizable GUI**: The use of icons and the flexible design allow for potential expansion of the GUI, such as adding more productivity tools or integrating more interactive features like project management, task grouping, etc.

## Future Scope and Improvements:

1. Integration with Cloud Services: Storing tasks and documentation locally is great, but integrating cloud-based services (e.g., Google Drive or Dropbox) for data storage could allow users to access their task lists and documents from multiple devices.

  
