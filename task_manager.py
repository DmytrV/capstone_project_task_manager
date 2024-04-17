# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

# =====importing libraries===========
import os
import ast
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"


def reg_user(new_username_password):
    # Function to register a new user
    try:
        new_username = input("New Username: ")

        # Validate Username Format
        if not new_username.isalnum():
            raise ValueError("Username can only contain alphanumeric characters.")

        # Check if the username already exists
        if new_username in new_username_password:
            raise ValueError("Username already exists. Please choose a different username.")

        new_password = input("New Password: ")

        # Validate Password Format
        if len(new_password) < 6:
            raise ValueError("Password must be at least 6 characters long.")

        confirm_password = input("Confirm Password: ")

        if new_password != confirm_password:
            raise ValueError("Passwords do not match")

        # Add the new user to the dictionary
        new_username_password[new_username] = new_password

        # Write the new user to the user.txt file
        with open("user.txt", "a") as out_file:
            out_file.write(f"\n{new_username};{new_password}")

        print(f"New user '{new_username}' successfully added.")

    except ValueError as ve:
        print(f"Input validation error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")


def add_task(new_task_list, new_username_password):
    # Function to add a new task
    try:
        task_username = input("Name of person assigned to task: ")

        # Validate if the username exists
        if task_username not in new_username_password:
            raise ValueError("User does not exist. Please enter a valid username.")

        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")

        while True:
            task_due_date_str = input("Due date of task (YYYY-MM-DD): ")
            try:
                task_due_date = datetime.strptime(task_due_date_str, DATETIME_STRING_FORMAT)
                if task_due_date.date() < datetime.now().date():
                    raise ValueError("Due date must be in the future.")
                break
            except ValueError as ve:
                print(ve)

        curr_date = date.today()

        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": task_due_date,  # Store due_date as datetime object
            "assigned_date": curr_date,
            "completed": False
        }

        # Add the new task to the task list
        new_task_list.append(new_task)

        # Write the updated task list to the tasks.txt file
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in new_task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),  # Convert datetime to string
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))

        print("Task successfully added.")

    except ValueError as ve:
        print(f"Input validation error: {ve}")
    except FileNotFoundError as fnfe:
        print(f"File not found error: {fnfe}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


def view_my_tasks(task_list_param, curr_user_param):
    try:
        tasks_assigned_to_user = [task for task in task_list_param if task['username'] == curr_user_param]

        if not tasks_assigned_to_user:
            print("No tasks assigned to you.")
            return

        print("Tasks assigned to you:")
        for i, task in enumerate(tasks_assigned_to_user, start=1):
            print(f"{i}. Title: {task['title']}")
            print(f"   Description: {task['description']}")
            print(f"   Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"   Assigned Date: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"   Completed: {'Yes' if task['completed'] else 'No'}")
            print()

        while True:
            try:
                task_choice = int(input("Enter the number of the task you want to select (or type '-1' to return to the main menu): "))
                if task_choice == -1:
                    return
                elif task_choice < 1 or task_choice > len(tasks_assigned_to_user):
                    raise ValueError("Invalid task number.")
                else:
                    selected_task = tasks_assigned_to_user[task_choice - 1]
                    break
            except ValueError:
                print("Invalid input. Please enter a valid task number.")

        action_choice = input("Do you want to (1) mark the task as complete or (2) edit the task? (enter '1' or '2'): ")

        if action_choice == '1':
            # Update task completion status
            for task in task_list_param:
                if task['username'] == selected_task['username'] and task['title'] == selected_task['title']:
                    task['completed'] = True
                    break
            print("Task marked as complete.")
            # Write the updated task list back to the file
            write_tasks_to_file(task_list_param)
        elif action_choice == '2':
            # Edit task
            if not selected_task['completed']:
                new_username = input("Enter new username (leave blank to keep current): ")
                new_due_date = input("Enter new due date (YYYY-MM-DD) (leave blank to keep current): ")

                if new_username:
                    selected_task['username'] = new_username
                if new_due_date:
                    selected_task['due_date'] = new_due_date
                print("Task edited successfully.")
                # Write the updated task list back to the file
                write_tasks_to_file(task_list_param)
            else:
                print("Completed tasks cannot be edited.")
        else:
            print("Invalid choice.")

    except ValueError as ve:
        print(f"Error: {ve}. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")


def generate_user_overview(task_list_param, username_password_param):
    # Generate user overview report
    total_users = len(username_password_param)

    task_overview = generate_task_overview(task_list_param)
    total_tasks = task_overview["Total number of tasks"]

    user_task_count = {user: sum(1 for task in task_list_param if task['username'] == user) for user in
                       username_password_param}

    report_content = "User Overview\n\n"
    report_content += f"Total number of users: {total_users}\n"
    report_content += f"Total number of tasks: {total_tasks}\n\n"

    for user_param, tasks_assigned in user_task_count.items():
        completed_tasks = sum(1 for task in task_list_param if task['username'] == user_param and task['completed'])
        incomplete_tasks = tasks_assigned - completed_tasks
        percentage_completed = 0
        if incomplete_tasks != 0:
            percentage_completed = (completed_tasks / incomplete_tasks) * 100
        overdue_tasks = sum(
            1 for task in task_list_param if task['username'] == user_param and not task['completed'] and task[
                'due_date'] < datetime.now())

        report_content += f"User: {user_param}\n"
        report_content += f"Total number of tasks assigned: {tasks_assigned}\n"
        if total_tasks != 0:  # Avoid division by zero
            report_content += f"Percentage of total tasks assigned: {(tasks_assigned / total_tasks) * 100:.2f}%\n"
        else:
            report_content += "No tasks available.\n"
        report_content += f"Percentage of completed tasks: {percentage_completed:.2f}%\n"
        if tasks_assigned != 0:
            report_content += f"Percentage of incomplete tasks: {(incomplete_tasks / tasks_assigned) * 100:.2f}%\n"
            report_content += f"Percentage of overdue tasks: {(overdue_tasks / tasks_assigned) * 100:.2f}%\n\n"
        else:
            report_content += "No tasks available.\n\n"

    return report_content


def generate_task_overview(task_list_param):
    """Generate task overview report."""
    try:
        total_tasks = len(task_list_param)
        completed_tasks = sum(1 for task in task_list_param if task['completed'])
        incomplete_tasks = total_tasks - completed_tasks
        overdue_tasks = sum(1 for task in task_list_param if not task['completed'] and task['due_date'] < datetime.now())

        overview_dict = {
            "Total number of tasks": total_tasks,
            "Total number of completed tasks": completed_tasks,
            "Total number of incomplete tasks": incomplete_tasks,
            "Total number of overdue tasks": overdue_tasks
        }

        return overview_dict
    except Exception as e:
        print(f"An error occurred while generating task overview report: {e}")


def generate_reports(task_list_param, username_password_param, task_report_path="task_overview.txt", user_report_path="user_overview.txt"):
    """Generate reports."""
    try:
        if not isinstance(task_list_param, list):
            raise ValueError("Task list parameter must be a list of tasks.")

        task_overview = generate_task_overview(task_list_param)
        with open(task_report_path, "w") as task_file_param:
            task_file_param.write(str(task_overview))
        print("Task overview report generated successfully.")

        user_overview = generate_user_overview(task_list_param, username_password_param)
        with open(user_report_path, "w") as user_file_param:
            user_file_param.write(user_overview)
        print("User overview report generated successfully.")
    except ValueError as ve:
        print(f"Input validation error: {ve}")
    except Exception as e:
        print(f"An error occurred while generating reports: {e}")


def display_task_statistics(task_statistics):
    """Display task statistics in a readable format."""
    print("\nTask Statistics:")
    print(f"Total number of tasks: {task_statistics['Total number of tasks']}")
    print(f"Total number of completed tasks: {task_statistics['Total number of completed tasks']}")
    print(f"Total number of incomplete tasks: {task_statistics['Total number of incomplete tasks']}")
    print(f"Total number of overdue tasks: {task_statistics['Total number of overdue tasks']}")


def display_statistics():
    try:
        global task_list
        global new_username_password

        # Check if task overview file exists, if not, generate reports
        if not os.path.exists("task_overview.txt"):
            generate_reports(task_list, new_username_password)

        # Read task overview file and display content
        with open("task_overview.txt", "r") as task_file_param:
            task_stats = ast.literal_eval(task_file_param.read())

        # Check if user overview file exists, if not, generate reports
        if not os.path.exists("user_overview.txt"):
            generate_reports(task_list, new_username_password)

        # Read user overview file and display content
        with open("user_overview.txt", "r") as user_file_param:
            user_stats = user_file_param.read()

        # Display statistics
        print("\nTask Statistics:")
        display_task_statistics(task_stats)
        print("\nUser Statistics:")
        print(user_stats)
    except Exception as e:
        print(f"An error occurred while displaying statistics: {e}")


def read_tasks_from_file():
    """Read tasks from the tasks.txt file."""
    try:
        with open("tasks.txt", "r") as task_file:
            task_data = task_file.readlines()
            task_list = []
            for t_str in task_data:
                curr_t = {}
                # Split by semicolon and manually add each component
                task_components = t_str.strip().split(";")
                curr_t['username'] = task_components[0]
                curr_t['title'] = task_components[1]
                curr_t['description'] = task_components[2]
                curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
                curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
                curr_t['completed'] = True if task_components[5] == "Yes" else False
                task_list.append(curr_t)
            return task_list
    except FileNotFoundError:
        print("Tasks file not found.")
        return []

def write_tasks_to_file(task_list):
    """Write the updated task list to the tasks.txt file."""
    try:
        with open("tasks.txt", "w") as task_file:
            for task in task_list:
                completed_str = "Yes" if task['completed'] else "No"
                task_info = [
                    task['username'],
                    task['title'],
                    task['description'],
                    task['due_date'].strftime(DATETIME_STRING_FORMAT),
                    task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    completed_str
                ]
                task_file.write(";".join(task_info) + "\n")
        print("Task list updated successfully.")
    except Exception as e:
        print(f"An error occurred while writing tasks to file: {e}")


def display_tasks(task_list):
    """Display tasks from the provided list of task dictionaries."""
    if not task_list:
        print("No tasks available.")
        return

    print("All Tasks:\n")
    for index, task in enumerate(task_list, start=1):
        print("#" * 65)  # Print decorative border
        print(f"{index}.")
        print(f"Task:              {task['title']}")
        print(f"Task Description:  {task['description']}")
        print(f"Assigned to:       {task['username']}")
        print(f"Due Date:          {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Assigned Date:     {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Task Completed:    {'Yes' if task['completed'] else 'No'}")


def view_all():
    """View all tasks."""
    task_lines = read_tasks_from_file()
    display_tasks(task_lines)


# ====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
curr_user = ""

# Loop for user login
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

# After successful login, update task_list with tasks from the file
task_list = read_tasks_from_file()

while True:
    # Presenting the menu to the user and
    # ensuring that the user input is converted to lower case.
    print("\nPlease select one of the following options:")
    print("r - Register a new user")
    print("a - Add a new task")
    print("va - View all tasks")
    print("vm - View my tasks")
    print("gr - Generate reports")
    print("ds - Display statistics")
    print("e - Exit")

    menu = input("Enter your choice: ").lower()

    if menu == 'r':
        '''Add a new user to the user.txt file'''
        reg_user(username_password)

    elif menu == 'a':
        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task, and 
             - the due date of the task.'''
        add_task(task_list, username_password)

    elif menu == 'va':
        '''View all tasks'''
        view_all()

    elif menu == 'vm':
        '''View tasks assigned to the current user'''
        view_my_tasks(task_list, curr_user)

    elif menu == 'gr':
        '''Generate reports'''
        generate_reports(task_list, username_password)

    elif menu == 'ds':
        '''Display statistics'''
        display_statistics()

    elif menu == 'e':
        print('Goodbye!!!')
        # Write the updated task list back to the file before exiting
        write_tasks_to_file(task_list)
        exit()

    else:
        print("Invalid choice. Please try again.")
