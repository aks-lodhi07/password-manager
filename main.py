from tkinter import *
from tkinter import messagebox # it is different that's why not included in *
from random import choice,randint,shuffle
import pyperclip
import string
import json
from tkinter import ttk
FONT_NAME = "Courier"
#PASSWORD GENERATOR
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = [ '#', '$', '%', '&', '(', ')', '*']

    password_letter =[choice(letters) for _ in range(randint(7, 9))]
    password_symbols=[choice(symbols) for _ in range(randint(2, 4))]
    password_numbers=[choice(numbers) for _ in range(randint(2, 4))]
    password_list=password_letter+password_symbols+password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    # clear the password input before inserting new one
    password_input.delete(0,END)
    password_input.insert(0,password)
    #copy password to clipboard
    pyperclip.copy(password)
    messagebox.showinfo(title="Copied",message="Password copied to clipboard!")


    #check the strength
    strength=get_password_strength(password)
    strength_label.config(text=f"Strength:{strength}",fg="green" if strength=="Strong" else "orange" if strength=="Medium" else "red")
# PASSWORD STRENGTH
def get_password_strength(password):
    length=len(password)
    has_upper=any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    score=sum([has_upper,has_symbol,has_digit,has_lower])
    if length>=12 and score==4:
        return "Strong"
    elif length>=8 and score>=3:
        return "Medium"
    else:
        return "Weak"

# SAVE PASSWORD
def save_password():
    web_name=website_input.get()
    email=email_input.get()
    password=password_input.get()
    entered_data={
        web_name:{
            "Email":email,
            "Password":password
        }
    }

    if (len(web_name) and len(email) and len(password)) == 0:
        messagebox.showinfo(title="Oops!",message="Please don't leave any fields empty!")

    else:
        is_ok = messagebox.askokcancel(title=web_name, message=f"These are the details entered:\nEmail: {email}\nPassword: {password}\nIs it ok to save?")
        if is_ok:
            try:
                with open("savedPassword.json",'r') as f:
                    data=json.load(f)
            except FileNotFoundError:
                data={}

        data.update(entered_data)
        with open("savedPassword.json",'w') as f:
            json.dump(data,f,indent=4)
        website_input.delete(0,END)
        password_input.delete(0,END)
        messagebox.showinfo(title="Saved",message="Password saved successfully!")

# SEARCH PASSWORD
def search_password():
    web_name=website_input.get()
    try:
        with open("savedPassword.json",'r') as f:
            data=json.load(f)
    except FileNotFoundError:
        messagebox.showinfo(title="Error",message="No data file found!")
        return
    if web_name in data:
        email=data[web_name]["Email"]
        password=data[web_name]["Password"]
        messagebox.showinfo(title=web_name,message=f"Email: {email}\nPassword: {password}")
        pyperclip.copy(password)
    else:
        messagebox.showinfo(title="Not Found",message=f"No details for '{web_name}' exist.")

# AKSHAT 'S UI

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50,bg="#f0f4f8")


canvas = Canvas(height=200, width=200,highlightthickness=0,bg="#f0f4f8")
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=0, columnspan=3, sticky="n", pady=10)

label_fg = "#1e293b"
entry_bg = "white"
button_bg = "#3b82f6"
button_fg = "white"
add_button_bg = "#10b981"


website_label =Label(text="Website:",bg="#f0f4f8",fg=label_fg,font=(FONT_NAME, 10, "bold"))
website_label.grid(row=1, column=0, pady=5, sticky="e")
email_label =Label(text="Email/Username:",bg="#f0f4f8", fg=label_fg, font=(FONT_NAME, 10, "bold"))
email_label.grid(row=2, column=0, pady=5, sticky="e")
password_label =Label(text="Password:",bg="#f0f4f8", fg=label_fg, font=(FONT_NAME, 10, "bold"))
password_label.grid(row=3, column=0, pady=5, sticky="e")

website_input =Entry(width=33,bg=entry_bg)
website_input.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
website_input.focus()
email_input =Entry(width=52,bg=entry_bg)
email_input.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
email_input.insert(0, "akshatlodhi777@gmail.com")
password_input =Entry(width=33, bg=entry_bg)
password_input.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

search_button =Button(text="Search", width=15, bg=button_bg, fg=button_fg, command=search_password)
search_button.grid(row=1, column=2, sticky="ew", padx=5)
generate_password_button =Button(text="Generate Password", width=15, bg=button_bg, fg=button_fg, command=generate_password)

generate_password_button.grid(row=3, column=2, sticky="ew", padx=5)
add_button =Button(text="Add", width=44, bg=add_button_bg, fg="white", command=save_password)
add_button.grid(row=4, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

strength_label = Label(text="", font=(FONT_NAME, 10, "bold"), bg="#f0f4f8")
strength_label.grid(row=5, column=1, columnspan=2, sticky="w")

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=3)
window.columnconfigure(2, weight=1)

for i in range(6):
    window.rowconfigure(i, weight=1)


window.mainloop()
