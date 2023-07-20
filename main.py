from tkinter import *
from tkinter import messagebox
from random import choice, shuffle, randint
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(6,8))]
    password_symbols = [choice(symbols) for _ in range(randint(2,4))]
    password_numbers = [choice(numbers) for _ in range(randint(2,4))]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    #joining the password list into one string with join method, using empty string as the connector.
    final_password = "".join(password_list)

    #Erasing the previously generated password and adding the newly created random password to the password entry field
    password_entry.delete(0, END)
    password_entry.insert(0, final_password)

    #Copying the generated password to the clipboard to be pasted without the need of doing the copy paste effort manually.
    pyperclip.copy(final_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_and_clear():
    website_data = website_entry.get()
    email_data = email_entry.get()
    password_data = password_entry.get()

    new_data = {
        website_data: {
            "email": email_data,
            "password": password_data,
        }
    }

    if len(website_data) == 0 or len(password_data) == 0:
        messagebox.showinfo(title="Oops!", message="Please don't leave any field empty.")

    else:
        try:
            with open("data.json", "r") as data_file:
                # reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                #creating new file and writing the inputted data in it
                json.dump(new_data, data_file, indent=4)
        else:
            #Update the data with what user has inputted if it finds the data.json file existing already
            data.update(new_data)
            #dumping the updated data to existing file data.json
            with open("data.json", "w") as data_file:
                # writing data to data.json
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END),

# ---------------------------- SEARCH SAVED DATA ------------------------------- #
def search_data():
    query = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found.")

    else:
        if query in data:
            messagebox.showinfo(title=query,
                                message=f"Email: {data[query]['email']}\nPassword: {data[query]['password']}")
        else:
            messagebox.showinfo(title="Error", message="No details of the website exist.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=240, width=240)
logo = PhotoImage(file="logo.png")
canvas.create_image(120,120, image=logo)
canvas.grid(row=0, column=1)

website_label = Label()
website_label.config(text="Website:")
website_label.grid(row=1, column=0, padx=2, pady=2)

website_entry = Entry()
website_entry.config(width=40, borderwidth=2)
website_entry.grid(row=1, column=1, padx=2, pady=2)
website_entry.focus()

search_button = Button()
search_button.config(text="Search", width=10, command=search_data)
search_button.grid(row=1, column=2, padx=2, pady=2)

email_label = Label()
email_label.config(text="Email/Username:")
email_label.grid(row=2, column=0, padx=2, pady=2)

email_entry = Entry()
email_entry.config(width=54, borderwidth=2)
email_entry.grid(row=2, column=1, columnspan=2, padx=2, pady=2)
email_entry.insert(0, "abc@gmail.com")

password_label = Label()
password_label.config(text="Password:")
password_label.grid(row=3, column=0, padx=2, pady=2)

password_entry = Entry()
password_entry.config(width=40, borderwidth=2)
password_entry.grid(row=3, column=1, padx=2, pady=2)

password_button = Button()
password_button.config(text="Generate", width=10, command=generate_password)
password_button.grid(row=3, column=2, padx=2, pady=2)

add_button = Button()
add_button.config(text="Add", width=46, command=save_and_clear)
add_button.grid(row=4, column=1, columnspan=2, padx=2, pady=2)

window.mainloop()