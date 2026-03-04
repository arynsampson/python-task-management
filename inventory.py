from tabulate import tabulate


# ========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
        pass

    def get_code(self):
        return self.code

    def get_product(self):
        return self.product

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def set_quantity(self, quantity):
        self.quantity = quantity

    def __str__(self):
        return (
            f"{self.country},{self.code},{self.product},"
            f"{self.cost},{self.quantity}"
        )


# =============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
shoe_list = []


# ==========Functions outside the class==============
def print_tabulated_output(shoe_list):
    """
    Prints out the shoe list in tabulated format.

    Parameters:
        shoe_list (list): The shoe_list is a list of dictionaries where each
        dictionary is a shoe.

    Returns:
        Nothing is returned.
    """
    print("\n" + tabulate(shoe_list, headers="keys") + "\n")


def transform_shoe_list(add_shoe_value=False):
    """
    Transforms each shoe object in the shoe list to a dictionary that can be
    used in the tabulate function.

    Parameters:
        add_shoe_value (Boolean): A Boolean that dictates if the shoe value
        must be added or not.

    Returns:
        list: A list of dictionaries where each dictionary represents a shoe.
    """
    transformed_shoe_list = []

    for shoe in shoe_list:
        data = {
            "Country": shoe.country,
            "Code": shoe.code,
            "Product": shoe.product,
            "Price": shoe.cost,
            "Quantity": shoe.quantity
        }

        # Include the value of all shoes
        if add_shoe_value is True:
            data["Shoe value"] = f"R{int(shoe.cost) * int(shoe.quantity)}"

        transformed_shoe_list.append(data)

    return transformed_shoe_list


def transform_single_shoe(shoe_data):
    """
    Transforms a single shoe object into a dictionary that can be used in the
    tabulate function.

    Parameters:
        shoe_data (Object): This variable is an instance of the Shoe class.

    Returns:
        dictionary: Represnting the shoe in dictionary format.
    """
    shoe_data = {
        "Country": shoe_data.country,
        "Code": shoe_data.code,
        "Product": shoe_data.product,
        "Price": shoe_data.cost,
        "Quantity": shoe_data.quantity
    }

    return shoe_data


def read_shoes_data():
    """
    This function reads the data from the text file and creates a Shoe object
    from each line.

    Parameters:
        None.

    Returns:
        None.
    """
    try:
        with open('inventory.txt', 'r') as file:
            lines = file.readlines()[1:]

            for line in lines:
                shoe_object = Shoe(
                    line.split(',')[0],
                    line.split(',')[1],
                    line.split(',')[2],
                    line.split(',')[3],
                    line.split(',')[4]
                )

                shoe_list.append(shoe_object)
            print("\nShoe list has been populated.\n")
    except IOError:
        print("File does not exist.")


def add_shoe_to_txt_file(new_shoe):
    """
    This function adds a new shoe to the text file.

    Parameters:
        new_shoe (str): This is the value of the __str__() method in the Shoe
        class.

    Returns:
        None.
    """
    with open("inventory.txt", "a") as file:
        file.seek(0)
        file.write(f"\n{new_shoe.__str__()}")


def validate_user_input(key):
    """
    This function validates the users input for the shoe details.

    Parameters:
        key (str): The Key determines which validation is applied to the input.

    Returns:
        shoe_data_input (str): The users' valid input
    """
    while True:
        if key == "country" or key == "product_name":
            shoe_data_input = input().strip()
            if (len(shoe_data_input) != 0):
                return shoe_data_input
            else:
                print("Invalid entry. Please try again.")

        elif key == "code":
            shoe_data_input = input().strip()
            if len(shoe_data_input) == 5 and shoe_data_input.isdigit():
                return shoe_data_input
            else:
                print("Invalid entry. Please try again.")

        elif key == "cost" or key == "quantity":
            shoe_data_input = input().strip()
            if (len(shoe_data_input) > 0
                and shoe_data_input.isdigit()
                    and int(shoe_data_input) > 0):
                return shoe_data_input
            else:
                print("Invalid entry. Please try again.")


def capture_shoes():
    """
    This function captures input data for a new shoe object.

    Parameters:
        None.

    Returns:
        None.
    """
    print("\nYou selected: \'Capture a shoe\'")
    print("Please enter shoe details:")

    print("\nWhat country is the shoe from?")
    shoe_country = validate_user_input("country")

    print("\nWhat is the five digit shoe code?")
    shoe_code = validate_user_input("code")

    print("\nWhat is the name of the shoe?")
    shoe_product_name = validate_user_input("product_name")

    print("\nWhat is the cost of the shoe?")
    shoe_cost = validate_user_input("cost")

    print("\nHow many pairs will be stocked?")
    shoe_quantity = validate_user_input("quantity")

    shoe_object = Shoe(
        shoe_country,
        f"SKU{shoe_code}",
        shoe_product_name,
        shoe_cost,
        shoe_quantity
    )
    shoe_list.append(shoe_object)

    print("\nYour shoe has been added to the shoe list.")

    transformed_shoe_list = transform_shoe_list()
    print_tabulated_output(transformed_shoe_list)
    add_shoe_to_txt_file(shoe_object)


def view_all_shoes():
    """
    This function prints all the shoes in the shoe list.

    Parameters:
        None.

    Returns:
        None.
    """
    if len(shoe_list) == 0:
        print("\nNo shoes found. Please populate the shoe list.\n")
    else:
        transformed_shoe_list = transform_shoe_list()
        print_tabulated_output(transformed_shoe_list)


def update_shoe_in_file(updated_shoe):
    """
    This function updates the shoe, in the text file, that has a new quantity.

    Parameters:
        updated_shoe (Object): This is the updated shoe as a Shoe Object.

    Returns:
        None.
    """
    updated_line = []

    with open("inventory.txt", "a+") as file:
        file.seek(0)
        for line in file:
            if updated_shoe.code in line:
                parts = line.strip().split(",")
                parts[4] = str(updated_shoe.get_quantity())
                line = ",".join(parts) + "\n"
            updated_line.append(line)

    with open("inventory.txt", "w") as file:
        file.writelines(updated_line)


def search_shoe():
    """
    This function searches for a shoe in the shoe list.

    Parameters:
        None.

    Returns:
        None.
    """
    if len(shoe_list) == 0:
        print("\nNo shoes found. Please populate the shoe list.\n")
    else:
        while True:
            shoe_code_input = input("Please enter the 5 digit shoe code: ")

            for shoe in shoe_list:
                if shoe_code_input == shoe.code[3:]:
                    print("Shoe has been found:")

                    transformed_single_shoe = transform_single_shoe(shoe)
                    print_tabulated_output([transformed_single_shoe])
                    return


def value_per_item():
    """
    This function calculates the value of each shoe.

    Parameters:
        None.

    Returns:
        None.
    """
    if len(shoe_list) == 0:
        print("\nNo shoes found. Please populate the shoe list.\n")
    else:
        transformed_shoe_list = transform_shoe_list(add_shoe_value=True)
        print_tabulated_output(transformed_shoe_list)


def re_stock():
    """
    This function searches for the shoe with the lowest quantity and allows the
    user to increases the quantity of the shoe.

    Parameters:
        None.

    Returns:
        None.
    """
    if len(shoe_list) == 0:
        print("\nNo shoes found. Please populate the shoe list.\n")
    else:
        shoe_with_min_quantity = find_min_max_value(shoe_list, "<")

        if shoe_with_min_quantity:
            shoe_data = transform_single_shoe(shoe_with_min_quantity)

            print("\nThe following shoe has low stock:")
            print_tabulated_output([shoe_data])

            while True:
                print("Do you want to restock: ")
                print("1 - Yes")
                print("2 - No")
                shoe_restock_choice = input()

                while True:
                    if shoe_restock_choice == "1":
                        shoe_restock_amount = input(
                            "How many pairs should be restocked: ")
                        shoe_restock_amount = (
                            int(shoe_restock_amount)
                            + int(shoe_with_min_quantity.quantity)
                        )

                        shoe_with_min_quantity.set_quantity(
                            str(shoe_restock_amount))
                        shoe_data['Quantity'] = str(shoe_restock_amount)

                        print("The following shoe has been restocked:")
                        print_tabulated_output([shoe_data])

                        update_shoe_in_file(shoe_with_min_quantity)
                        return
                    elif shoe_restock_choice == "2":
                        print("Process exited.\n")
                        return
                    else:
                        print("Invalid selection. Please try again.\n")
                        break


def highest_qty():
    """
    This function searches for the shoe with the highest quantity and prints
    it.

    Parameters:
        None.

    Returns:
        None.
    """
    if len(shoe_list) == 0:
        print("\nNo shoes found. Please populate the shoe list.\n")
    else:
        shoe_with_max_quantity = find_min_max_value(shoe_list, mode=">")

        if shoe_with_max_quantity:
            shoe_data = transform_single_shoe(shoe_with_max_quantity)
            print("This shoe is on sale:")
            print_tabulated_output([shoe_data])


def find_min_max_value(shoe_list, mode=">"):
    """
    Recursively find and return either the shoe with the minimum quantity
    or the maximum quantity in the given list.

    Parameters:
        shoe_list (list): A list of Shoe objects, each containing a 'quantity'
                          attribute.
        mode (str): Determines whether to search for the minimum ("<")
                    or maximum (">") quantity value. Default is ">".

    Returns:
        Shoe: The Shoe object with the minimum or maximum quantity, depending
        on the mode provided.
    """
    if len(shoe_list) == 1:
        return shoe_list[0]

    # Find shoe with lowest quantity
    if mode == "<":
        if int(shoe_list[0].quantity) < int(shoe_list[-1].quantity):
            return find_min_max_value(shoe_list[0:-1], mode="<")
        else:
            return find_min_max_value(shoe_list[1:], mode="<")

    # Find shoe with highest quantity
    else:
        if int(shoe_list[0].quantity) > int(shoe_list[-1].quantity):
            return find_min_max_value(shoe_list[0:-1], mode)
        else:
            return find_min_max_value(shoe_list[1:], mode)


# ==========Main Menu=============
while True:
    """
    User selects an action by entering the related number.

    Parameters:
        None

    Returns:
        None.
    """
    print("Please select an option: ")
    print("1 - Read shoe data from file")
    print("2 - Capture a shoe")
    print("3 - View all shoes")
    print("4 - Restock a shoe")
    print("5 - Search for a shoe")
    print("6 - Check value of all shoes")
    print("7 - Highest quantity")

    user_choice = input("\nEnter a number: ")

    if user_choice == "1":
        read_shoes_data()
    elif user_choice == "2":
        capture_shoes()
    elif user_choice == "3":
        view_all_shoes()
    elif user_choice == "4":
        re_stock()
    elif user_choice == "5":
        search_shoe()
    elif user_choice == "6":
        value_per_item()
    elif user_choice == "7":
        highest_qty()
    else:
        print("\nInvalid option. Please try again.\n")
