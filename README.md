# To-Do List Application

## Introduction

This is a To-Do List Application is a web-based task management system developed by using the popular Flask web framework in Python.
This Application allows users to register, log in, create tasks, edit tasks, mark tasks as completed, and delete tasks. 
The application is aimed to help me build my still with python, html and css with the usage of a un-native python framworks
to help build and run this Application.

This was built as well for general usage and to help organize daily
tasks effectively for me and other users.

## Usage
To Use The To-Do List Applition:
1. Install dependencies:
    ```
    pip install Flask
    pip install flask-bcrypt
    ```
  or  
    ```
    pip install -r requirements.txt
    ```

2. Clone the repository:
    ```
    git clone https://github.com/Birdo1221/Users-Todo-WebApp.git
    cd Users-Todo-WebApp
## File Structure

The application comprises several files and directories, each serving a specific purpose:

- **Flask File Structure:**
  - **app.py:** This is the main Flask application file where the routes and functionality of the web application are defined.
  - **templates directory:** Contains HTML templates for rendering the pages to the users.
  - **static directory:** Stores static files such as CSS, JavaScript, and images used by the application.
   
- **Created Directories / Files:**
  - **user_tasks directory:** Holds JSON files that store task data for each user.
  -  Each user has a unique task file associated with their account that is named by based64 encoding
  -  their username as the file name
 
  - E.g
  - [task_(UsernameBase64).json]   [tasks_YWRtaW4=.json]  This is an admin example [YWRtaW4=  is admin]
 
  -  Now for each user, every tasks that is generated is using uuid to name the tasks to save / store them in the users independant
  -  .json file that will contain:
  -      ```[UUID Generated Id
  -      Task Name
  -      The Task Description
  -      If marked it completed or not]
  -      ```
        ```
        [
        {
      "id": "ac9e4bb7-0a75-47d3-b5a5-6c7a184dbb27",        
      "name": "update to-do ",                                  
      "description": "Make to update to-do app for profile pfp's and clean-up code ", 
      "completed": false                                         
        },
        {
          "id": "d1f51f41-c7dd-4206-8575-6408a0c1695e",
          "name": "hands",
          "description": "get some gloves",
          "completed": true,
          "additional_description": "i need to go buy some gloves for the winter time"
        }
        ]
        ```
## Functionalities

### 1. Registration and Login

- Users can register for an account by providing a unique username, password, security question, and answer.
- Passwords are securely hashed using the `bcrypt` library to ensure data security.
- Upon successful registration, users can log in using their oorrect credentials.

### 2. Dashboard

- Authenticated users are directed to the dashboard upon login.
- The dashboard displays a web GUI for the creation of user's tasks as well as, allowing them to view, edit, delete, and mark tasks as completed.
- Tasks are stored in JSON files associated with each user to maintain privacy and data simplicity .

### 3. Task Management

- Users can create new tasks by providing a task name and description.
- Tasks can be edited to update their details, such as a description and additional notes.
- Completed tasks can be marked as such to track progress and productivity.
- Users have the option to delete tasks they no longer need, helping them maintain a clutter-free task list.

### 4. Security Features

- Passwords are hashed using the bcrypt algorithm to ensure confidentiality and integrity.
- Security questions and answers provide an additional layer of authentication, enhancing account security.

## Feedback and Improvement

### Positive Feedback

- Users appreciate the simplicity and intuitiveness of the application's user interface.
- The ability to manage tasks efficiently helps users stay organized and productive.
- Security measures such as password hashing and security questions instill confidence in the application's security.

### Areas for Improvement

- Enhance user experience with interactive features such as drag-and-drop task reordering.
- Implement notifications and reminders to alert users of approaching deadlines or overdue tasks.
- Introduce collaboration features to enable users to share tasks and collaborate on projects with team members.
- Add more user control and user profiling such as user pfp's and additional settings.

## Conclusion

The To-Do List Application serves as a valuable tool for users seeking to manage their tasks effectively. With its user-friendly interface, robust functionality, and emphasis on security, the application aims to streamline task management and improve productivity. Continual feedback and iterative improvements ensure that the application remains responsive to user needs and preferences.
