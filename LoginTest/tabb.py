import tkinter as tk
from tkinter import ttk

root = tk.Tk()

style = ttk.Style()
style.configure("TNotebook", tabposition='wn')  # Tab position
style.configure("TNotebook.Tab", padding=[70, 9.99])  # Padding for tabs
style.configure("TNotebook.Tab", font=("Arial", 12))  # Font for tabs

# Adding hover effect
style.map("TNotebook.Tab",
          background=[("selected", "red"), ("active", "red")])

notebook = ttk.Notebook(root, style="TNotebook")
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)

notebook.add(frame1, text='Tab 1')
notebook.add(frame2, text='Tab 2')
notebook.pack(expand=1, fill='both')

root.mainloop()
