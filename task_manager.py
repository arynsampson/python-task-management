# ===== Importing external modules ===========
'''This is the section where you will import modules'''
from tabulate import tabulate
from datetime import datetime

app_state = {
    "logged_in_user": False,
    "list_of_users": [],
    "list_of_all_tasks": [],
    "list_of_current_users_tasks": [],
    "list_of_completed_tasks": [],
    "list_of_incomplete_tasks": [],
    "list_of_overdue_tasks": [],
    "task_overview_data": [],
    "user_overview_data": []
}

# ===== User input validation ===========


def validate_user_input(key, prompt=""):
    """
    Validates user input based on the type of data identified by `key`.

    Parameters:
        key (str): Determines which type of validation should be applied.
                   Accepted values include:
                   "username", "password", "assigned_user",
                   "task_title", "task_description", "task_due_date"

        prompt (str): The message shown when asking the user for input.

    Returns:
        str: The user's validated input.
    """
    while True:
        if key in ["username", "password", "assigned_user", "task_title",
                   "task_description", "task_due_date"]:
            user_detail_input = input(prompt).strip()
            if (len(user_detail_input) != 0):
                return user_detail_input
            else:
                print("\nInvalid entry. Please try again.\n")


def get_valid_date(prompt="Enter the due date (e.g. format - 26 Oct 2025): "):
    """
    Continuously prompts the user for a valid date until the input matches
    the required format: DD Mon YYYY (e.g., 26 Oct 2025).

    Parameters:
        prompt (str): The message displayed when asking the user for a date.

    Returns:
        str: A valid date string formatted as "DD Mon YYYY".
    """
    while True:
        date_input = input(prompt)
        try:
            # Convert to datetime object
            valid_date = datetime.strptime(date_input, "%d %b %Y")

            return valid_date.strftime("%d %b %Y")

        except ValueError:
            print("\nInvalid date format. "
                  "Please use DD Mon YYYY (e.g., 26 Oct 2025).\n")

# ===== Helper functions ===========


def check_if_user_exists(username_to_find):
    """
    Checks whether a given username already exists in the application's
    user list.

    Parameters:
        username_to_find (str): The username to look for.

    Returns:
        bool: True if the username exists, False otherwise.
    """
    user = any(
        user[0].lower().strip()
        == username_to_find.lower().strip()
        for user in app_state["list_of_users"])

    return user


def find_task(list_of_tasks):
    """
    Allows the user to select a task from a list by entering its ID.
    The function validates input and returns the matching task.

    Parameters:
        list_of_tasks (list): A list of tasks.

    Returns:
        The task that matches the user's selection.
    """
    while True:
        try:
            task_id = input("\nSelect the task by entering its ID:\n")
            task_id = int(task_id)

            if task_id > len(list_of_tasks):
                print("\nInvalid ID. Please try again.")
                continue
            else:
                for index, task in (enumerate(list_of_tasks, start=1)):
                    if task_id == index:
                        return task
            break
        except ValueError:
            print("Invalid entry. Please try again")


def transform_list_item_to_string(task):
    """
    Converts a task dictionary into a single comma-separated string.
    This is typically used when writing the task back into a text file.

    Parameters:
        task (dict): A dictionary containing task fields such as:
                     'Assigned to', 'Title', 'Description',
                     'Date assigned', 'Due date', 'Completed'

    Returns:
        str: A comma-separated string representing the task.
    """

    transformed_task = (
        f"{task['Assigned to']},"
        f"{task['Title']},"
        f"{task['Description']},"
        f"{task['Date assigned']},"
        f"{task['Due date']},"
        f"{task['Completed']}"
    )

    return transformed_task


def transform_task_to_list(task):
    """
    Converts a task dictionary into a list of values,
    excluding the Task ID and trimming the Completed field.

    Parameters:
        task (dict): A dictionary where each key is a task field.

    Returns:
        list: A list of task values in the order they appear in the dictionary,
              except 'Task ID', which is skipped.
    """
    task_as_list = []

    for key, value in task.items():
        if key == "Task ID":
            continue

        if key == "Completed":
            value = value[0:3]

        value.strip()

        task_as_list.append(value)

    return task_as_list


def create_data_dictionary(line, task_id):
    """
    Converts a comma-separated string representing a task into a dictionary.

    Parameters:
        line (str): A string with task fields separated by commas, in
        the order: Assigned to, Title, Description, Date assigned,
        Due date, Completed
        task_id (int): The unique ID to assign to this task.

    Returns:
        dict: A dictionary representing the task with keys
    """

    data_dictionary = {
        "Task ID": task_id,
        "Assigned to": line.split(',')[0],
        "Title": line.split(',')[1],
        "Description": line.split(',')[2],
        "Date assigned": line.split(',')[3],
        "Due date": line.split(',')[4],
        "Completed": line.split(',')[5],
    }

    return data_dictionary


def exit_program():
    print("\nGoodbye!!!!!!\n")
    exit()


# ==== Presentation logic ====


def print_single_task(task):
    """
    This function prints a single task.

    Parameters:
        None.

    Returns:
        None.
    """
    print(f"\n{tabulate([task], headers="keys")}\n")


def print_all_tasks():
    """
    This function prints all the tasks.

    Parameters:
        None.

    Returns:
        None.
    """
    if len(app_state["list_of_all_tasks"]) > 1:
        print(
            f"\n{tabulate(app_state["list_of_all_tasks"], headers="keys")}\n")
    else:
        print("\nThere are no tasks to display.\n")


def print_user_overview_data():
    print(f"\n{tabulate(app_state["user_overview_data"], headers="keys")}\n")


def print_task_overview_data():
    print(f"\n{tabulate(app_state["task_overview_data"], headers="keys")}\n")


def print_user_specific_tasks():
    """
    This function prints all the tasks assigned to the logged in user.

    Parameters:
        None.

    Returns:
        None.
    """
    if len(app_state["list_of_current_users_tasks"]) > 0:
        print(
            f"\n{tabulate(app_state["list_of_current_users_tasks"],
                          headers="keys")}\n")
        manage_task()
    else:
        print("\nYou do not have any tasks assigned.\n")


def print_completed_tasks():
    """
    Prints all the completed tasks.

    Parameters:
        None.

    Returns:
        None.
    """
    if len(app_state["list_of_completed_tasks"]) > 0:
        print(
            f"\n{tabulate(app_state["list_of_completed_tasks"],
                          headers="keys")}\n")
    else:
        print("\nThere are no completed tasks.\n")


# ==== Data access logic ====
def fetch_list_of_users():
    """
    Fetches the users from the external text file and populates
    the app state with the data

    Parameters:
        None.

    Returns:
        None.
    """
    try:
        with open('users.txt', 'a+') as file:
            file.seek(0)
            lines = file.readlines()
            if len(lines) == 0:
                print("No existing users. Admin will be logged in.\n")
                return

            for line in lines:
                username = line.split(',')[0].strip()
                password = line.split(',')[1].strip()
                app_state["list_of_users"].append([username, password])
    except IOError:
        print("File does not exist.")


def populate_list_of_tasks(key):
    """
    Allows the user to manage tasks assigned to them.
    Users can edit tasks or mark them as complete.

    Parameters:
        str(key): The key will dictate which task list to update. The lists
        are: all the tasks, user specific tasks, and the completed tasks.

    Returns:
        None.
    """
    task_id = 1
    try:
        with open('tasks.txt', 'a+') as file:
            file.seek(0)
            lines = file.readlines()
            for line in lines:
                if key == "all_tasks":
                    task_dictionary = create_data_dictionary(
                        line, task_id)
                    app_state["list_of_all_tasks"].append(task_dictionary)
                    task_id += 1

                elif key == "current_users_tasks":
                    if (line.split(',')[0].strip()
                            != app_state["logged_in_user"][0].strip()):
                        continue
                    else:
                        user_dictionary = create_data_dictionary(line, task_id)
                        app_state["list_of_current_users_tasks"].append(
                            user_dictionary)
                        task_id += 1
                        continue

                elif key == "completed_tasks":
                    if "yes" in line.split(',')[5].strip().lower():
                        completed_task = create_data_dictionary(line, task_id)
                        app_state["list_of_completed_tasks"].append(
                            completed_task)

                    elif "no" in line.split(',')[5].strip().lower():
                        incomplete_task = create_data_dictionary(line, task_id)
                        app_state["list_of_incomplete_tasks"].append(
                            incomplete_task)
                        task_id += 1

                    else:
                        continue

                elif key == "overdue_tasks":
                    task = create_data_dictionary(line, task_id)

                    task_due_date = datetime.strptime(
                        task["Due date"], "%d %b %Y")
                    todays_date = datetime.today()

                    if (task_due_date < todays_date
                            and "No" in task["Completed"]):
                        app_state["list_of_overdue_tasks"].append(task)
                        task_id += 1
                    else:
                        continue
    except IOError:
        print("File does not exist.")


def trigger_task_lists_population():
    """
    Clears the task lists and then populates calls the
    `populate_list_of_tasks()` to repopulate.

    Lists populated:
        - "all_tasks": All tasks in the app state
        - "current_users_tasks": Tasks assigned to the currently logged-in user
        - "completed_tasks": Tasks that have been marked as completed

    Returns:
        None.
    """
    app_state["list_of_all_tasks"] = []
    app_state["list_of_current_users_tasks"] = []
    app_state["list_of_completed_tasks"] = []
    app_state["list_of_incomplete_tasks"] = []
    app_state["list_of_overdue_tasks"] = []

    populate_list_of_tasks("all_tasks")
    populate_list_of_tasks("current_users_tasks")
    populate_list_of_tasks("completed_tasks")
    populate_list_of_tasks("incomplete_tasks")
    populate_list_of_tasks("overdue_tasks")


# ==== Data  persistance logic


def add_user_to_file(user_details):
    """
    This function adds a new user to the external text file.

    Parameters:
        (str) user_details: The users details as a string

    Returns:
        None.
    """
    with open("users.txt", "a") as file:
        file.write(user_details)


def add_task_to_file(task):
    """
    This function adds a new task to the external text file.

    Parameters:
        str(task): The task data, to be added, as a string

    Returns:
        None.
    """
    with open("tasks.txt", "a") as file:
        file.seek(0)
        file.write(task + "\n")


def update_task_in_file(task, value_to_update):
    """
    This function updates the task in the external text file.

    Parameters:
        str(task): The task data, to be added, as a string.
        str(value_to_update): The task data item that needs to be updated.

    Returns:
        None.
    """
    transformed_task = transform_list_item_to_string(task)

    updated_lines = []

    with open("tasks.txt", "r") as file:
        for line in file:
            if line == transformed_task:
                parts = line.strip().split(",")

                if value_to_update[0] == "username":
                    parts[0] = value_to_update[1]

                elif value_to_update[0] == "due_date":
                    parts[-2] = value_to_update[1]
                    pass

                elif value_to_update[0] == "completed":
                    parts[-1] = value_to_update[1]

                new_line = ",".join(parts) + "\n"
                updated_lines.append(new_line)

            else:
                updated_lines.append(line)

    with open("tasks.txt", "w") as file:
        file.writelines(updated_lines)


def delete_task_from_file(task):
    """
    Deletes a task from the external text file.

    Parameters:
        (dict) task: The task to be deleted

    Returns:
        None.
    """
    transformed_task = transform_task_to_list(task)

    with open("tasks.txt", "r") as file:
        lines = file.readlines()

    with open("tasks.txt", "w") as file:
        for line in lines:
            parts = line.strip().split(",")

            if parts == transformed_task:
                continue

            file.write(line)


# ===== Business logic ======


def add_task():
    """
    Adds a new task

    Parameters:
        None.

    Returns:
        None.
    """
    assigned_user_input = validate_user_input(
        "assigned_user", "Enter the username to assign this task to: ")

    unique_user = check_if_user_exists(assigned_user_input)

    if unique_user is False:
        print("\nUser does not exist. Please try again.\n")
        add_task()

    task_title_input = validate_user_input(
        "task_title", "Enter the title of this task: ")

    task_description_input = validate_user_input(
        "task_description", "Enter the description of this task: ")

    task_due_date_input = get_valid_date()

    # get current time
    current_date = datetime.now().strftime("%d %b %Y")

    task = {
        "Assigned to": assigned_user_input.strip(),
        "Title": task_title_input.strip(),
        "Description": task_description_input.strip(),
        "Date assigned": current_date,
        "Due date": task_due_date_input.strip(),
        "Completed": "No",
    }

    transformed_task = transform_list_item_to_string(task)

    # save task to external file
    add_task_to_file(transformed_task)
    trigger_task_lists_population()
    print("\nTask has been added successfully.")
    print_single_task(task)


def edit_task_details(task):
    """
    Manages the editing of the assigned user and due date of a task.

    Parameters:
        dict(task): The task to be edited.

    Returns:
        None.
    """
    print("\nYou have selected the following task to edit: ")
    print(f"\n{tabulate([task], headers="keys")}\n")

    print("You can update the assigned user and due date.\n")

    while True:
        edit_choice = input('''Please select an option:
                        uas - update assigned user
                        udd - update task due date
                        e - return to main menu
        ''').lower()

        if edit_choice == "uas":
            assigned_user_input = (validate_user_input(
                "assigned_user",
                "Enter the username to assign this task to: ").lower())

            existing_user = check_if_user_exists(assigned_user_input)

            if existing_user is False:
                print("\nUser does not exist.\n")
                continue

            update_task_in_file(task, ["username", assigned_user_input])
            trigger_task_lists_population()
            print("\nTask assigned user has been updated.\n")
            print_single_task(task)
            return

        elif edit_choice == "udd":
            task_due_date_input = get_valid_date()
            update_task_in_file(task, ["due_date", f" {task_due_date_input}"])
            trigger_task_lists_population()
            print("\nTask due date has been updated.\n")
            print_single_task(task)
            return

        elif edit_choice == "e":
            print("\nReturning to main menu.\n")
            return

        else:
            print("Invalid entry. Please try again.")


def manage_task():
    """
    Allows the user to manage tasks assigned to them.
    Users can edit tasks or mark them as complete.

    Parameters:
        None.

    Returns:
        None.

    """
    while True:

        input_choice = input('''Please select one of the following options:
                et - edit a task
                e - exit
                ''').lower()

        if input_choice == "et":
            task = find_task(app_state["list_of_current_users_tasks"])
            print_single_task(task)
            if "No" in task["Completed"]:
                while True:
                    task_action = input('''Select an option
                    etd - edit task details
                    m - mark task as complete
                    e - exit
                    ''').lower()

                    if task_action == "etd":
                        edit_task_details(task)
                        return
                    elif task_action == "m":
                        update_task_in_file(task, ["completed", "Yes"])
                        trigger_task_lists_population()
                        print("\nTask has marked as complete.\n")
                        return

                    elif input_choice == "e":
                        print("\nReturning to menu.\n")
                        return

                    else:
                        print("\nInvalid input. Please try again.\n")
            else:
                print("Completed tasks cannot be edited.")

        elif input_choice == "e":
            print("\nReturning to menu.\n")
            break
        else:
            print("\nInvalid input. Please try again.\n")


def delete_task():
    """
    Deletes a task from the data

    Parameters:
        None.

    Returns:
        None.
    """
    print_all_tasks()

    while True:
        task = find_task(app_state["list_of_all_tasks"])

        print_single_task(task)

        delete_confirmation = input('''Confirm task deletion?
            - yes
            - no
        ''').lower()

        if delete_confirmation == "yes":
            delete_task_from_file(task)
            trigger_task_lists_population()
            print("\nTask has been deleted.\n")
            return
        elif delete_confirmation == "no":
            print("\nReturning to menu.\n")
            return
        else:
            print("\nInvalid input. Please try again.\n")


# ==== Authentication logic ====
def login():
    """
    This function will log in a valid user.

    Parameters:
        None.

    Returns:
        None.
    """
    while True:

        if len(app_state["list_of_users"]) == 0:
            app_state["list_of_users"].append(["admin", "adm1n"])
            add_user_to_file("admin, adm1n")
            app_state["logged_in_user"] = ["admin", "adm1n"]
            trigger_task_lists_population()
            return

        prompt = (
            "Would you like to login or exit?\n"
            "l - login\n"
            "e - exit\n"
        )

        user_login_actions = input(prompt).lower()

        if user_login_actions == "l":

            while True:
                print("\nPlease enter username and password:")
                username = input("Username: ")
                if username.lower() == "exit":
                    exit_program()

                password = input("Password: ")
                if password.lower() == "exit":
                    exit_program()

                if [username, password] in app_state["list_of_users"]:
                    print("\nYou're logged in!\n")
                    app_state["logged_in_user"] = [
                        username, password]
                    trigger_task_lists_population()
                    return
                else:
                    print("\nInvalid credentials. Please try again or exit.")
                    print("Type 'exit' in either field to exit.")
        elif user_login_actions == "e":
            exit_program()

        else:
            print("\nInvalid input. Please try again.\n")


def register_a_user():
    """
    This function will register a new user.

    Parameters:
        None.

    Returns:
        None.
    """
    while True:
        print("Please enter the username and password.")

        username_input = validate_user_input("username", "Username: ")
        password_input = validate_user_input("password", "Password: ")
        password_confirmation_input = validate_user_input(
            "password", "Confirm password: ")

        does_user_exist = check_if_user_exists(username_input)

        if does_user_exist is True:
            print("\nUsername already taken. Please try again.\n")
            continue

        if (password_input.lower().strip() !=
                password_confirmation_input.lower().strip()):
            print("\nPasswords do not match. Please try again.\n")
            continue

        app_state["list_of_users"].append(
            [username_input, password_input])

        user_stringified = f"\n{username_input + ", " + password_input}"

        add_user_to_file(user_stringified)

        print("\nUser has been resgistered successfully!\n")
        return


# ==== Reporting data logic =====
def calculate_user_tasks_percentages(task, task_data):
    """
    Updates task_data with percentage-based statistics for a specific user.
    This function is called once per task that belongs to the user.
    """

    if task_data["Task count"] == 0:
        return task_data

    task_data["Overall task percentage"] = int(
        (task_data["Task count"] / len(app_state["list_of_all_tasks"])
            * 100))

    if "Yes" in task["Completed"]:
        task_data["Completed tasks"] += 1
    else:
        task_data["Incompleted tasks"] += 1

    task_due_date = datetime.strptime(task["Due date"], "%d %b %Y")
    if "No" in task["Completed"] and datetime.today() > task_due_date:
        task_data["Overdue tasks"] += 1

    task_data["Completed percentage"] = (
        task_data["Completed tasks"] / task_data["Task count"] * 100
    )

    task_data["Incomplete percentage"] = (
        task_data["Incompleted tasks"] / task_data["Task count"] * 100
    )

    task_data["Overdue percentage"] = (
        task_data["Overdue tasks"] / task_data["Task count"] * 100
    )

    return task_data


def get_user_overview_data():
    """
    Builds a list of dictionaries, where each dictionary contains
    reporting statistics for each user (task count, completed, overdue, etc.).
    The results are saved into app_state["user_overview_data"].
    """

    list_of_users_with_tasks_total = []

    for user in app_state["list_of_users"]:
        user_reporting_data = {
            "Username": user[0],
            "Task count": 0,
            "Incompleted tasks": 0,
            "Completed tasks": 0,
            "Overdue tasks": 0
        }

        for task in app_state["list_of_all_tasks"]:
            if user[0] == task["Assigned to"]:
                user_reporting_data["Task count"] += 1

                calculate_user_tasks_percentages(task, user_reporting_data)

        list_of_users_with_tasks_total.append(user_reporting_data)

    app_state["user_overview_data"] = list_of_users_with_tasks_total


def get_task_overview_data():
    trigger_task_lists_population()
    total_number_of_tasks = len(app_state["list_of_all_tasks"])
    total_number_of_completed_tasks = len(app_state["list_of_completed_tasks"])
    total_number_of_incompleted_tasks = len(
        app_state["list_of_incomplete_tasks"])
    total_number_of_overdue_tasks = len(app_state["list_of_overdue_tasks"])

    incomplete_tasks_percentage = (
        total_number_of_incompleted_tasks / total_number_of_tasks) * 100

    overdue_tasks_percentage = (
        total_number_of_overdue_tasks / total_number_of_tasks) * 100

    task_overview_data = {
        "All tasks": total_number_of_tasks,
        "Completed tasks": total_number_of_completed_tasks,
        "Incomplete tasks": total_number_of_incompleted_tasks,
        "Overdue tasks": total_number_of_overdue_tasks,
        "Incomplete tasks percentage": f"{int(incomplete_tasks_percentage)}%",
        "Overdue tasks percentage": f"{int(overdue_tasks_percentage)}%"
    }

    app_state["task_overview_data"].append(task_overview_data)


# ==== Reporting ====


def display_statistics():
    '''
    Prints the overview data in tabulated format.
    '''
    if len(app_state["task_overview_data"]) > 0:
        print_task_overview_data()
        print_user_overview_data()
    else:
        print("\nNo data. Please generate reports.\n")


def update_or_create_external_files():
    """
    Creates or overwrites the user_overview.txt and task_overview.txt files
    using data stored inside app_state.
    """
    with open("user_overview.txt", "w") as file:
        for user_data in app_state["user_overview_data"]:
            file.write(str(user_data) + "\n")

    with open("task_overview.txt", "w") as file:
        for task_data in app_state["task_overview_data"]:
            file.write(str(task_data) + "\n")


def generate_reports():
    """
    Generates both task and user overview reports by:
    1. Calculating task overview data
    2. Calculating user overview data
    3. Writing both results into external text files
    """

    get_task_overview_data()
    get_user_overview_data()

    update_or_create_external_files()

    print("\nTask and User reports have been generated. You can now view "
          "statistics\n")


while True:

    if app_state["logged_in_user"] is False:
        print("\nWelcome!\n")
        fetch_list_of_users()
        login()
    else:
        if app_state["logged_in_user"][0] == "admin":
            menu_selection = input('''Select one of the following options:
                    r - register a user
                    a - add task
                    va - view all tasks
                    vm - view my tasks
                    vc - view completed tasks
                    del - delete tasks
                    ds - display statistics
                    gr - generate reports
                    e - exit
                    ''').lower()
        else:
            menu_selection = input('''Select one of the following options:
                a - add task
                va - view all tasks
                vm - view my tasks
                e - exit
                ''').lower()

            if menu_selection in ["r", "vc", "del"]:
                print("\nInvalid input. Please try again\n")
                continue

        if menu_selection == 'r':
            register_a_user()

        elif menu_selection == 'a':
            add_task()

        elif menu_selection == 'va':
            print_all_tasks()

        elif menu_selection == 'vm':
            print_user_specific_tasks()

        elif menu_selection == "vc":
            print_completed_tasks()

        elif menu_selection == "del":
            delete_task()

        elif menu_selection == "ds":
            display_statistics()

        elif menu_selection == "gr":
            generate_reports()

        elif menu_selection == 'e':
            exit_program()

        else:
            print("Invalid input. Please try again")
