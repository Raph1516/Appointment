import sqlite3
from tkinter import *
from tkinter import messagebox

root = Tk()

bg = PhotoImage(file='background.png') 
show_img = PhotoImage(file='show.png') 
hide_img = PhotoImage(file='hide.png') 

root.geometry('800x530+400+100')
root.title("Appointment System")

canvas = Canvas(root, width=800, height=530)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg, anchor="nw")

canvas_text_items = []

def create_tables():
    conn = sqlite3.connect('appointment_system.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS patients (
                    name TEXT,
                    contact TEXT,
                    address TEXT)''')

    conn.commit()
    conn.close()

create_tables()

def clear_canvas():
    for widget in root.winfo_children():
        if widget != canvas:
            widget.destroy()
    for text_item in canvas_text_items:
        canvas.delete(text_item)
    canvas_text_items.clear()

def toggle_password(entry_field, toggle_button, show_state):
    if show_state[0]:
        entry_field.config(show="")
        toggle_button.config(image=hide_img)
    else:
        entry_field.config(show="*")
        toggle_button.config(image=show_img)
    show_state[0] = not show_state[0]

def login():
    clear_canvas()

    canvas_text_items.append(canvas.create_text(400, 80, text="Login", font=("Arial", 20, "bold"), fill="white"))

    entry_height = 30

    Label(root, text="Username:", font=("Arial", 12), bg="#ffffff").place(x=250, y=150, width=100, height=entry_height)
    username_entry = Entry(root, font=("Arial", 12))
    username_entry.place(x=400, y=150, width=200, height=entry_height)

    Label(root, text="Password:", font=("Arial", 12), bg="#ffffff").place(x=250, y=200, width=100, height=entry_height)
    password_entry = Entry(root, font=("Arial", 12), show="*")
    password_entry.place(x=400, y=200, width=200, height=entry_height)

    show_password_state = [True]
    toggle_button = Button(root, image=show_img, command=lambda: toggle_password(password_entry, toggle_button, show_password_state))
    toggle_button.place(x=610, y=200, width=30, height=30)

    def submit_login():
        username = username_entry.get()
        password = password_entry.get()
        
        if username and password:
            # Check if the username and password exist in the database
            conn = sqlite3.connect('appointment_system.db')
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = c.fetchone()
            conn.close()

            if user:
                messagebox.showinfo("Login", f"Welcome, {username}!")
                main_menu()
            else:
                messagebox.showerror("Error", "Invalid username or password!")
        else:
            messagebox.showerror("Error", "Both fields are required!")

    Button(root, text="Submit", command=submit_login, font=("Arial", 12), bg="#3498db", fg="white").place(x=350, y=260, width=100, height=30)
    Button(root, text="Back", command=show_main_menu, font=("Arial", 12), bg="#e74c3c", fg="white").place(x=350, y=320, width=100, height=30)

def signup():
    clear_canvas()

    canvas_text_items.append(canvas.create_text(400, 80, text="Sign Up", font=("Arial", 20, "bold"), fill="white"))

    entry_height = 30

    Label(root, text="Username:", font=("Arial", 12), bg="#ffffff").place(x=250, y=150, width=130, height=entry_height)
    username_entry = Entry(root, font=("Arial", 12))
    username_entry.place(x=400, y=150, width=200, height=entry_height)

    Label(root, text="Password:", font=("Arial", 12), bg="#ffffff").place(x=250, y=200, width=130, height=entry_height)
    password_entry = Entry(root, font=("Arial", 12), show="*")
    password_entry.place(x=400, y=200, width=200, height=entry_height)

    Label(root, text="Confirm Password:", font=("Arial", 12), bg="#ffffff").place(x=250, y=250, width=135, height=entry_height)
    confirm_password_entry = Entry(root, font=("Arial", 12), show="*")
    confirm_password_entry.place(x=400, y=250, width=200, height=entry_height)

    show_password_state = [True]
    toggle_button = Button(root, image=show_img, command=lambda: toggle_password(password_entry, toggle_button, show_password_state))
    toggle_button.place(x=610, y=200, width=30, height=30)

    show_confirm_password_state = [True]
    toggle_button_confirm = Button(root, image=show_img, command=lambda: toggle_password(confirm_password_entry, toggle_button_confirm, show_confirm_password_state))
    toggle_button_confirm.place(x=610, y=250, width=30, height=30)

    def submit_signup():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required!")
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
        else:
            # Add the new user to the database
            conn = sqlite3.connect('appointment_system.db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                messagebox.showinfo("Sign Up", "Account created successfully!")
                show_main_menu()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists!")
            finally:
                conn.close()

    Button(root, text="Submit", command=submit_signup, font=("Arial", 12), bg="#2ecc71", fg="white").place(x=350, y=320, width=100, height=30)
    Button(root, text="Back", command=show_main_menu, font=("Arial", 12), bg="#e74c3c", fg="white").place(x=350, y=380, width=100, height=30)

def patients_info():
    clear_canvas()

    canvas_text_items.append(canvas.create_text(400, 80, text="Patient's Information", font=("Arial", 20, "bold"), fill="white"))

    entry_height = 30

    # Patient details input fields
    Label(root, text="Name:", font=("Arial", 12), bg="#ffffff").place(x=250, y=150, width=100, height=entry_height)
    name_entry = Entry(root, font=("Arial", 12))
    name_entry.place(x=400, y=150, width=200, height=entry_height)

    Label(root, text="Contact No.:", font=("Arial", 12), bg="#ffffff").place(x=250, y=200, width=100, height=entry_height)
    contact_entry = Entry(root, font=("Arial", 12))
    contact_entry.place(x=400, y=200, width=200, height=entry_height)

    Label(root, text="Address:", font=("Arial", 12), bg="#ffffff").place(x=250, y=250, width=100, height=entry_height)
    address_entry = Entry(root, font=("Arial", 12))
    address_entry.place(x=400, y=250, width=200, height=entry_height)

    canvas_text_items.append(canvas.create_text(400, 320, text="Confirm Appointment", font=("Arial", 14, "bold"), fill="white"))

    def confirm_info():
        name = name_entry.get()
        contact = contact_entry.get()
        address = address_entry.get()
        if name and contact and address:
            # Add patient info to the database
            conn = sqlite3.connect('appointment_system.db')
            c = conn.cursor()
            c.execute("INSERT INTO patients (name, contact, address) VALUES (?, ?, ?)", (name, contact, address))
            conn.commit()
            conn.close()
            messagebox.showinfo("Confirmation", "Information saved successfully!")
            main_menu()
        else:
            messagebox.showerror("Error", "All fields are required!")

    Button(root, text="Yes", command=confirm_info, font=("Arial", 12), bg="#2ecc71", fg="white").place(x=300, y=370, width=100, height=30)
    Button(root, text="No", command=main_menu, font=("Arial", 12), bg="#e74c3c", fg="white").place(x=450, y=370, width=100, height=30)

selected_patient_rowid = None

def show_data():
    global selected_patient_rowid  
    clear_canvas() 

    canvas_text_items.append(canvas.create_text(400, 80, text="Patient Data", font=("Arial", 20, "bold"), fill="white"))

    
    conn = sqlite3.connect('appointment_system.db')
    c = conn.cursor()
    c.execute("SELECT rowid, name, contact, address FROM patients") 
    patients = c.fetchall()
    conn.close()

    if patients:
        y_position = 150
        canvas_text_items.append(canvas.create_text(150, y_position, text="Name", font=("Arial", 12, "bold"), fill="white"))
        canvas_text_items.append(canvas.create_text(300, y_position, text="Contact No.", font=("Arial", 12, "bold"), fill="white"))
        canvas_text_items.append(canvas.create_text(500, y_position, text="Address", font=("Arial", 12, "bold"), fill="white"))
        y_position += 30  # Adjust for the header row

        for patient in patients:
            rowid, name, contact, address = patient
            name_item = canvas.create_text(150, y_position, text=name, font=("Arial", 12), fill="white", tags=f"name_{rowid}")
            contact_item = canvas.create_text(300, y_position, text=contact, font=("Arial", 12), fill="white", tags=f"contact_{rowid}")
            address_item = canvas.create_text(500, y_position, text=address, font=("Arial", 12), fill="white", tags=f"address_{rowid}")

            canvas.tag_bind(f"name_{rowid}", "<Button-1>", lambda event, id=rowid: select_patient(event, id))
            canvas.tag_bind(f"contact_{rowid}", "<Button-1>", lambda event, id=rowid: select_patient(event, id))
            canvas.tag_bind(f"address_{rowid}", "<Button-1>", lambda event, id=rowid: select_patient(event, id))

            y_position += 60 

        Button(root, text="Delete", command=delete_selected_patient, font=("Arial", 12), bg="#e74c3c", fg="white").place(x=325, y=y_position + 30, width=150, height=30)

    else:
        canvas_text_items.append(canvas.create_text(400, 150, text="No patient data found", font=("Arial", 12), fill="white"))

    Button(root, text="Back", command=main_menu, font=("Arial", 12), bg="#e74c3c", fg="white").place(x=350, y=y_position + 80, width=100, height=30)


def main_menu():
    clear_canvas()

    canvas_text_items.append(canvas.create_text(400, 100, text="Main Menu", font=("Arial", 24, "bold"), fill="white"))

    Button(root, text="Patient's Info", command=patients_info, font=("Arial", 12), bg="#1abc9c", fg="white").place(relx=0.5, rely=0.4, anchor="center", width=150, height=40)
    Button(root, text="Show Data", command=show_data, font=("Arial", 12), bg="#3498db", fg="white").place(relx=0.5, rely=0.5, anchor="center", width=150, height=40)
    Button(root, text="Log Out", font=("Arial", 12), bg="#e74c3c", fg="white", command=show_main_menu).place(relx=0.5, rely=0.6, anchor="center", width=150, height=40)


def select_patient(event, rowid):
    global selected_patient_rowid

    if selected_patient_rowid is not None:
        canvas.itemconfig(f"name_{selected_patient_rowid}", fill="white")
        canvas.itemconfig(f"contact_{selected_patient_rowid}", fill="white")
        canvas.itemconfig(f"address_{selected_patient_rowid}", fill="white")

    canvas.itemconfig(f"name_{rowid}", fill="yellow")
    canvas.itemconfig(f"contact_{rowid}", fill="yellow")
    canvas.itemconfig(f"address_{rowid}", fill="yellow")

    selected_patient_rowid = rowid

def delete_selected_patient():
    global selected_patient_rowid

    if selected_patient_rowid is None:
        messagebox.showerror("Error", "No patient selected!")
    else:
        if messagebox.askyesno("Delete", "Are you sure you want to delete this patient?"):
            conn = sqlite3.connect('appointment_system.db')
            c = conn.cursor()
            c.execute("DELETE FROM patients WHERE rowid=?", (selected_patient_rowid,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Patient data deleted successfully.")
            selected_patient_rowid = None 
            show_data() 

def main_menu():
    clear_canvas() 

    canvas_text_items.append(canvas.create_text(400, 100, text="Main Menu", font=("Arial", 24, "bold"), fill="white"))

    Button(root, text="Patient's Info", command=patients_info, font=("Arial", 12), bg="#1abc9c", fg="white").place(relx=0.5, rely=0.4, anchor="center", width=150, height=40)
    Button(root, text="Show Data", command=show_data, font=("Arial", 12), bg="#3498db", fg="white").place(relx=0.5, rely=0.5, anchor="center", width=150, height=40)
    Button(root, text="Log Out", font=("Arial", 12), bg="#e74c3c", fg="white", command=show_main_menu).place(relx=0.5, rely=0.6, anchor="center", width=150, height=40)

def show_main_menu():
    clear_canvas() 

    canvas_text_items.append(canvas.create_text(400, 100, text="Appointment System", font=("Arial", 24, "bold"), fill="white"))

    Button(root, text="Login", command=login, font=("Arial", 12, "bold"), bg="#3498db", fg="white", width=15, height=2).place(relx=0.5, rely=0.4, anchor="center")
    Button(root, text="Sign Up", command=signup, font=("Arial", 12, "bold"), bg="#2ecc71", fg="white", width=15, height=2).place(relx=0.5, rely=0.6, anchor="center")
    
show_main_menu()

root.mainloop()
