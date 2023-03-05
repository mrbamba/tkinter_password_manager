from tkinter import *
from tkinter import messagebox
import pandas
import json
from os import path
from random import choice, randint, shuffle
import pyperclip

# ---------------------------- CONSTANTS ------------------------------- #
FONT = ("Ariel", 16, "normal")
FILE = "./pass.csv"
DEFAULT_EMAIL_FILE = "./default_email.txt"
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


# ---------------------------- EXPORT TO CSV ------------------------------- #


def export():
    # Checking for saved data
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)

    # If no saved data then notifying the user
    except FileNotFoundError:
        messagebox.showinfo("No passwords saved yet")

    # If there is saved data then
    else:
        # Creating pandas dataframe
        df = pandas.DataFrame.from_dict(data, orient="index")

        # Giving the index a name since not present in the json file
        df.index.name = 'Domain'

        # Saving the DataFrame to file while overwriting past export if one exists
        df.to_csv(FILE, mode='w', index=True, header=True)

        # Notifying the user the task is done
        messagebox.showinfo("Downloaded", "File 'pass.csv' downloaded to the main software folder.")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def clear_label():
    notification.config(text="")


def generate_password():
    # Generate the password
    password_list = [choice(LETTERS) for i in range(randint(10, 12))]
    password_list += [choice(NUMBERS) for i in range(randint(2, 4))]
    password_list += [choice(SYMBOLS) for i in range(randint(2, 4))]
    shuffle(password_list)
    password = ''.join(password_list)

    # Save the password to the clipboard for immediate usage
    pyperclip.copy(password)
    notification.config(text="Password copied to clipboard!")
    notification.after(3000, clear_label)

    # Update the password input field in the GUI
    password_input.delete(0, END)
    password_input.insert(0, password)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_password():
    search_keyword = website_input.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No passwords saved yet")
    else:
        if search_keyword in data:
            result = data[search_keyword]
            copy_password = messagebox.askokcancel(f"Matching information for {search_keyword}:\n",
                                                   f"{search_keyword} information\n\n"
                                                   f"Username/Email: {result['Email']}\n\n"
                                                   f"Password: \n{result['Password']}\n\n\n"
                                                   f"Copy Password to clipboard?")
            if copy_password:
                pyperclip.copy(result['Password'])
        else:
            messagebox.showinfo("No matches", "I looked everywhere but I couldn't find your password, sorry, try again")


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    # check if file exists and if not then create it
    place_header = not path.exists(FILE)

    # Get the data
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()

    # Validate all fields are filled
    if len(website) < 1 or len(email) < 1 or len(password) < 1:
        messagebox.showinfo("Missing fields", "Some of your fields are empty, Try again")
    else:
        # Confirm save
        is_data_correct = messagebox.askokcancel(title=website,
                                                 message=f"Please verify the data:\n\n"
                                                         f"Website:\n{website}\n\n"
                                                         f"Email:\n{email}\n\n"
                                                         f"Password:\n{password}\n\n"
                                                         f"Save the info?"
                                                 )
        # Save data is it looks good
        if is_data_correct:
            # Organize the data
            new_data = {
                website: {
                    'Email': email,
                    'Password': password
                }
            }

            # Save to json file
            try:
                # Try opening the file and see if it exists to read old data
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)

            except FileNotFoundError:
                # if the file does not exist then just dump new data into it
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                # If the file existed then update the old data with the new data
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)

            finally:
                # Clear form
                website_input.delete(0, END)
                password_input.delete(0, END)
                with open(DEFAULT_EMAIL_FILE, "w") as new_default_email_file:
                    new_default_email_file.write(email)


# ---------------------------- UI SETUP ------------------------------- #
# Get default email to use
if path.exists(DEFAULT_EMAIL_FILE):
    with open(DEFAULT_EMAIL_FILE, "r") as default_email_file:
        email_address = default_email_file.read()
else:
    email_address = ""

# if path.exists(FILE):
#     passwords_file = pandas.read_csv(FILE)
#     email_address = passwords_file.iloc[-1].Email
# else:
#     email_address = ""


# Main window config
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Logo UI config
LOGO = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200, highlightthickness=0)
canvas.create_image(100, 100, image=LOGO)
canvas.grid(row=0, column=1)

# Website data UI config
website_title = Label(text="Website:", font=FONT)
website_title.grid(row=1, column=0)

website_input = Entry(width=22)
website_input.focus()
website_input.grid(row=1, column=1)

website_search = Button(text="Search", width=13, command=search_password)
website_search.grid(row=1, column=2)

# Email/Username UI Config
email_title = Label(text="Email/Username:", font=FONT)
email_title.grid(row=2, column=0)

email_input = Entry(width=40)
email_input.insert(END, email_address)
email_input.grid(row=2, column=1, columnspan=3)

# Password UI config
password_title = Label(text="Password:", font=FONT)
password_title.grid(row=3, column=0)

password_input = Entry(width=22)
password_input.grid(row=3, column=1)

password_generate_button = Button(text="Generate Password", width=13, command=generate_password)
password_generate_button.grid(row=3, column=2)

# Add button UI config
add_button = Button(text="Add", width=38, command=save)
add_button.grid(row=4, column=1, columnspan=2)

# Export button
export_button = Button(text="Export all data to CSV", width=53, command=export)
export_button.grid(row=5, column=0, columnspan=3)

# Password copied to clipboard notification area
notification = Label(text="", font=FONT, fg="green")
notification.grid(row=6, column=0, columnspan=3)

window.mainloop()
