from tkinter import *
import pandas
import os.path
from os import path

# ---------------------------- CONSTANTS ------------------------------- #
FONT = ("Ariel", 16, "normal")
FILE = "./pass.csv"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    # check if file exists and if not then create it
    place_header = not path.exists(FILE)
    print(place_header)

    # Get the data
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()

    # Organize the data
    data = {
        'Website': [website],
        'Email': [email],
        'Password': [password]
    }

    # Create DataFrame from data
    df = pandas.DataFrame(data)
    print(df)

    # Append DataFrame to CSV file
    df. to_csv(FILE, mode='a', index=False, header=place_header)

    # Clear form
    website_input.delete(0, END)
    password_input.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
# Get default email to use
if path.exists(FILE):
    passwords_file = pandas.read_csv(FILE)
    email_address = passwords_file.iloc[-1].Email
else:
    email_address = ""

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

website_input = Entry(width=40)
website_input.focus()
website_input.grid(row=1, column=1, columnspan=2)

# Email/Username UI Config
email_title = Label(text="Email/Username:", font=FONT)
email_title.grid(row=2, column=0)

email_input= Entry(width=40)
email_input.insert(END, email_address)
email_input.grid(row=2, column=1, columnspan=3)

# Password UI config
password_title = Label(text="Password:", font=FONT)
password_title.grid(row=3, column=0)

password_input = Entry(width=22)
password_input.grid(row=3, column=1)

password_generate_button = Button(text="Generate Password", width=13)
password_generate_button.grid(row=3, column=2)

# Add button UI config
add_button = Button(text="Add", width=38, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
