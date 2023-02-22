from tkinter import *
from tkinter import messagebox
import pandas
from os import path
import random

# ---------------------------- CONSTANTS ------------------------------- #
FONT = ("Ariel", 16, "normal")
FILE = "./pass.csv"
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password = ""
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)
    for char in range(0, nr_letters):
        # chosen_char = random.randint(0,len(letters)-1)
        # password+=letters[chosen_char]
        password += random.choice(LETTERS)

    for char in range(0, nr_symbols):
        password += random.choice(SYMBOLS)

    for char in range(0, nr_numbers):
        password += random.choice(NUMBERS)
    password_list = list(password)
    random.shuffle(password_list)
    result = ''.join(password_list)
    password_input.delete(0, END)
    password_input.insert(0, result)
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

password_generate_button = Button(text="Generate Password", width=13, command=generate_password)
password_generate_button.grid(row=3, column=2)

# Add button UI config
add_button = Button(text="Add", width=38, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
