from customtkinter import *
from tkinter import *
import re
from tkinter import ttk

# Colors
background_color = '#10181c'
entry_color = '#192028'
button_color = '#256bfe'
footer_color = '#ff4c4c'  # Red color for footer button
tab_button_color = '#3b5998'  # Color for tab buttons
tab_button_hover_color = '#8b9dc3'  # Hover color for tab buttons
tab_button_pressed_color = '#2e4d6d'  # Color when button is pressed
tab_button_selected_color = '#1a1a1a'  # Color for selected tab button

root = Tk()
root.resizable(False, False)
root.title('Modern TK Login')
root.config(bg=background_color)

logo = Label(root,
             text='Login UI',
             font=('Comic sans Bold', 30),
             bg=background_color,
             fg='white')
logo.pack(pady=20)

# Create frames for Login and Sign Up
login_frame = Frame(root, bg=background_color)
signup_frame = Frame(root, bg=background_color)

# Function to show login frame
def show_login_frame():
    signup_frame.pack_forget()  # Hide signup frame
    login_frame.pack(pady=20)  # Show login frame

# Function to show signup frame
def show_signup_frame():
    login_frame.pack_forget()  # Hide login frame
    signup_frame.pack(pady=20)  # Show signup frame

# Email validation function
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

# Function to log out and return to login screen
def logout(main_window):
    main_window.destroy()
    root.deiconify()  # Show the login window again

# Function to switch between tabs using buttons
def switch_tab(notebook, index, buttons):
    notebook.select(index)
    for i, button in enumerate(buttons):
        if i == index:
            button.configure(fg_color=tab_button_selected_color)
        else:
            button.configure(fg_color=tab_button_color)

# Function to create navigation buttons with effects
def create_tab_button(parent, text, command, buttons, index):
    button = CTkButton(parent, text=text,
                       command=lambda: switch_tab(notebook, index, buttons),
                       fg_color=tab_button_color,
                       hover_color=tab_button_hover_color,
                       width=200, height=60)  # Adjusted height
    button.bind("<ButtonPress-1>", lambda e: button.configure(fg_color=tab_button_pressed_color))
    button.bind("<ButtonRelease-1>", lambda e: button.configure(fg_color=tab_button_color))
    button.pack(padx=10, pady=10, fill=X)
    buttons.append(button)  # Add button to the list
    return button

# Function to create buttons with effects for login/signup
def create_action_button(parent, text, command):
    button = CTkButton(parent,
                       text=text,
                       command=command,
                       fg_color=button_color,
                       hover_color='black',
                       width=300, height=60)
    button.bind("<ButtonPress-1>", lambda e: button.configure(fg_color=tab_button_pressed_color))
    button.bind("<ButtonRelease-1>", lambda e: button.configure(fg_color=button_color))
    return button

# Function to check credentials and open a new window with tabs and navigation on the right
def check_credentials():
    user_email = txt_email.get()
    user_password = txt_password.get()

    if is_valid_email(user_email) and user_password:
        # Create main application window
        main_window = Toplevel(root)
        main_window.title("Main Application")
        main_window.config(bg=background_color)
        main_window.geometry("1366x768")  # Set window size

        # Create a frame for the main content
        main_frame = CTkFrame(main_window, fg_color=background_color)
        main_frame.pack(fill=BOTH, expand=True)

        # Create a frame for the sidebar with greeting label and tab buttons
        left_frame = CTkFrame(main_frame, fg_color=background_color, width=250)
        left_frame.pack(side=LEFT, fill=Y)

        # Top frame for greeting (inside right_frame)
        top_frame = CTkFrame(left_frame, fg_color=background_color)
        top_frame.pack(fill=X, padx=20, pady=20)

        # Greeting label aligned to the left
        user_name = user_email.split('@')[0].capitalize()
        greeting_label = Label(top_frame,
                               text=f"Hello, {user_name}!",
                               font=('Montserrat Bold', 24),
                               bg=background_color,
                               fg='white',
                               anchor='w')  # Align text to the left
        greeting_label.pack(side=LEFT)

        # Create a style for the notebook
        style = ttk.Style()
        style.configure("TNotebook", tabposition=LEFT)  # Tab position
        style.configure("TNotebook.Tab", padding=[70, 9.99])  # Padding for tabs
        style.configure("TNotebook.Tab", font=("Comic Sans", 10))  # Font for tabs
        # Adding more styles
        style.configure("TNotebook.Tab", background="lightblue", foreground="black")  # Background and text color
        style.map("TNotebook.Tab",
                  background=[("selected", "yellow"), ("active", "lightgreen")],  # Hover and selected colors
                  foreground=[("selected", "black"), ("active", "blue")])  # Text color on hover and selected

        style.configure("TNotebook.Tab", borderwidth=2, relief="raised")  # Border style


        # Create a notebook (tabs content)
        global notebook  # Make notebook global to access in the function
        notebook = ttk.Notebook(main_frame)
        notebook.pack(side=LEFT, fill=BOTH, expand=True)

        # Create a list of tabs
        columns = ('Código', 'Nome', 'Tipo', 'Produto', 'Descrição')
        tab_names = [f"Tab {i}" for i in range(1, 7)]
        buttons = []  # List to hold tab buttons

        for i in range(6):
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=tab_names[i])

            # Create a table in each tab
            tree = ttk.Treeview(tab, columns=columns, show='headings')
            for col in columns:
                tree.heading(col, text=col)

            # Sample data
            for j in range(1, 6):
                tree.insert('', 'end', values=(f'Code {j}', f'Name {j}', f'Type {j}', f'Product {j}', f'Description {j}'))

            tree.pack(fill=BOTH, expand=True)

            # Create buttons to navigate between tabs with effects
            create_tab_button(left_frame, tab_names[i], None, buttons, i)

        # Create footer with logout button (at bottom of right_frame)
        footer_frame = CTkFrame(left_frame, fg_color=background_color)
        footer_frame.pack(side=BOTTOM, fill=X)

        # Menu button
        menu_button = CTkButton(footer_frame, text="Logout", fg_color=footer_color, width=100, height=40,
                                command=lambda: logout(main_window))
        menu_button.pack(side=LEFT, padx=10, pady=10)

        root.withdraw()  # Hide the login window
    else:
        error_label = Label(login_frame,
                            text="Please fill in valid email and password.",
                            bg=background_color,
                            fg='red',
                            font=('Montserrat', 10))
        error_label.pack(pady=10)

# LOGIN UI
# EMAIL
email_frame = CTkFrame(login_frame,
                       corner_radius=20,
                       fg_color=entry_color,
                       border_width=1,
                       border_color=background_color,
                       bg_color=background_color)
email_frame.pack(pady=10)

txt_email = CTkEntry(email_frame,
                     placeholder_text_color='gray',
                     placeholder_text='Enter your Email',
                     border_width=0,
                     fg_color=entry_color,
                     font=('Montserrat', 16))
txt_email.pack(padx=10, pady=10)

# PASSWORD
password_frame = CTkFrame(login_frame,
                          fg_color=entry_color,
                          corner_radius=20,
                          border_width=1,
                          border_color=background_color,
                          bg_color=background_color)
password_frame.pack(pady=10)

txt_password = CTkEntry(password_frame,
                        placeholder_text_color='gray',
                        placeholder_text='Enter your Password',
                        show='•',
                        border_width=0,
                        fg_color=entry_color,
                        font=('Montserrat', 16))
txt_password.pack(padx=10, pady=10)

# FORGOT PASSWORD
btn_forgot_password = Button(login_frame,
                             border=0,
                             relief='flat',
                             bg=background_color,
                             fg='#236cfe',
                             text='Forgot Password?',
                             font=('Montserrat Medium', 10),
                             cursor='hand2',
                             activebackground=background_color,
                             activeforeground='white')
btn_forgot_password.pack(pady=5)

# LOGIN
btn_login = create_action_button(login_frame, 'LOGIN', check_credentials)
btn_login.pack(pady=10)

# CREATE ACCOUNT
lbl_signup = Label(login_frame,
                   border=0,
                   relief='flat',
                   bg=background_color,
                   fg='gray',
                   text='Don\'t have an account?',
                   font=('Montserrat Medium', 10))
lbl_signup.pack(pady=5)

btn_signup = Button(login_frame,
                    border=0,
                    relief='flat',
                    bg=background_color,
                    fg='#236cfe',
                    text='Sign Up',
                    font=('Montserrat Medium', 10),
                    cursor='hand2',
                    activebackground=background_color,
                    activeforeground='white',
                    command=show_signup_frame)
btn_signup.pack(pady=5)

# SIGN UP UI
# EMAIL
signup_email_frame = CTkFrame(signup_frame,
                              fg_color=entry_color,
                              corner_radius=20,
                              border_width=1,
                              border_color=background_color,
                              bg_color=background_color)
signup_email_frame.pack(pady=10)

txt_signup_email = CTkEntry(signup_email_frame,
                            placeholder_text_color='gray',
                            placeholder_text='Enter your Email',
                            border_width=0,
                            fg_color=entry_color,
                            font=('Montserrat', 16))
txt_signup_email.pack(padx=10, pady=10)

# PASSWORD
signup_password_frame = CTkFrame(signup_frame,
                                 fg_color=entry_color,
                                 corner_radius=20,
                                 border_width=1,
                                 border_color=background_color,
                                 bg_color=background_color)
signup_password_frame.pack(pady=10)

txt_signup_password = CTkEntry(signup_password_frame,
                               placeholder_text_color='gray',
                               placeholder_text='Enter your Password',
                               show='•',
                               border_width=0,
                               fg_color=entry_color,
                               font=('Montserrat', 16))
txt_signup_password.pack(padx=10, pady=10)

# CREATE ACCOUNT BUTTON
btn_create_account = create_action_button(signup_frame, 'CREATE ACCOUNT', lambda: None)
btn_create_account.pack(pady=10)

# BACK TO LOGIN BUTTON
btn_back_to_login = Button(signup_frame,
                           border=0,
                           relief='flat',
                           bg=background_color,
                           fg='#236cfe',
                           text='Back to Login',
                           font=('Montserrat Medium', 10),
                           cursor='hand2',
                           activebackground=background_color,
                           activeforeground='white',
                           command=show_login_frame)
btn_back_to_login.pack(pady=5)

show_login_frame()  # Show the login frame initially
root.mainloop()
