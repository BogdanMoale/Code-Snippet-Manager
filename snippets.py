import json
import tkinter as tk
from tkinter import messagebox

# Function to load snippets from file
def load_snippets():
    try:
        with open("snippets.json", "r") as file:
            snippets = json.load(file)
    except FileNotFoundError:
        snippets = {}
    return snippets

# Function to save snippets to file
def save_snippets(snippets):
    with open("snippets.json", "w") as file:
        json.dump(snippets, file, indent=4)

# Function to add a new snippet
def add_snippet():
    title = title_entry.get().strip()
    code = code_text.get("1.0", tk.END).strip()
    language = language_entry.get().strip()
    if title and code and language:
        snippets[title] = {"code": code, "language": language}
        save_snippets(snippets)
        messagebox.showinfo("Success", "Snippet added successfully!")
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

# Function to view all snippets
def view_snippets():
    result_text.delete("1.0", tk.END)
    if snippets:
        for title, snippet in snippets.items():
            result_text.insert(tk.END, f"Title: {title}\nLanguage: {snippet['language']}\nCode: {snippet['code']}\n\n")
    else:
        result_text.insert(tk.END, "No snippets found!")

# Function to search for a snippet
def search_snippet():
    result_text.delete("1.0", tk.END)
    keyword = keyword_entry.get().strip().lower()
    language_filter = language_filter_entry.get().strip().lower()
    found = False
    for title, snippet in snippets.items():
        if (keyword in title.lower() or keyword in snippet['code'].lower()) and (not language_filter or language_filter == snippet['language'].lower()):
            result_text.insert(tk.END, f"Title: {title}\nLanguage: {snippet['language']}\nCode: {snippet['code']}\n\n")
            found = True
    if not found:
        result_text.insert(tk.END, "No matching snippets found!")

# Function to edit a snippet
def edit_snippet():
    title = edit_title_entry.get().strip()
    if title in snippets:
        code = edit_code_text.get("1.0", tk.END).strip()
        language = edit_language_entry.get().strip()
        if code and language:
            snippets[title] = {"code": code, "language": language}
            save_snippets(snippets)
            messagebox.showinfo("Success", "Snippet edited successfully!")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    else:
        messagebox.showerror("Error", "Snippet not found!")

# Function to delete a snippet
def delete_snippet():
    title = delete_title_entry.get().strip()
    if title in snippets:
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this snippet?")
        if confirmation:
            del snippets[title]
            save_snippets(snippets)
            messagebox.showinfo("Success", "Snippet deleted successfully!")
    else:
        messagebox.showerror("Error", "Snippet not found!")

# Main window
root = tk.Tk()
root.title("Code Snippet Manager")

# Load snippets
snippets = load_snippets()

# Style for labels
label_style = {"font": ("Helvetica", 10, "bold"), "padx": 10, "pady": 5}

# Add a snippet
add_frame = tk.Frame(root)
add_frame.pack(pady=10)

tk.Label(add_frame, text="Title:", **label_style).grid(row=0, column=0)
title_entry = tk.Entry(add_frame, width=40)
title_entry.grid(row=0, column=1)

tk.Label(add_frame, text="Code:", **label_style).grid(row=1, column=0)
code_text = tk.Text(add_frame, height=5, width=40)
code_text.grid(row=1, column=1)

tk.Label(add_frame, text="Language:", **label_style).grid(row=2, column=0)
language_entry = tk.Entry(add_frame, width=40)
language_entry.grid(row=2, column=1)

add_button = tk.Button(add_frame, text="Add Snippet", command=add_snippet)
add_button.grid(row=3, column=0, columnspan=2, pady=5)

# View all snippets
view_button = tk.Button(root, text="View All Snippets", command=view_snippets)
view_button.pack()

# Result text area with scrollbar
result_frame = tk.Frame(root)
result_frame.pack(pady=10)

result_scrollbar = tk.Scrollbar(result_frame)
result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text = tk.Text(result_frame, height=15, width=70, wrap=tk.WORD, yscrollcommand=result_scrollbar.set)
result_text.pack()

result_scrollbar.config(command=result_text.yview)

# Search for a snippet
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

tk.Label(search_frame, text="Keyword:", **label_style).grid(row=0, column=0)
keyword_entry = tk.Entry(search_frame, width=30)
keyword_entry.grid(row=0, column=1)

tk.Label(search_frame, text="Language Filter:", **label_style).grid(row=0, column=2)
language_filter_entry = tk.Entry(search_frame, width=30)
language_filter_entry.grid(row=0, column=3)

search_button = tk.Button(search_frame, text="Search", command=search_snippet)
search_button.grid(row=1, column=0, columnspan=4, pady=5)

# Edit a snippet
edit_frame = tk.Frame(root)
edit_frame.pack(pady=10)

tk.Label(edit_frame, text="Title to Edit:", **label_style).grid(row=0, column=0)
edit_title_entry = tk.Entry(edit_frame, width=40)
edit_title_entry.grid(row=0, column=1)

tk.Label(edit_frame, text="New Code:", **label_style).grid(row=1, column=0)
edit_code_text = tk.Text(edit_frame, height=5, width=40)
edit_code_text.grid(row=1, column=1)

tk.Label(edit_frame, text="New Language:", **label_style).grid(row=2, column=0)
edit_language_entry = tk.Entry(edit_frame, width=40)
edit_language_entry.grid(row=2, column=1)

edit_button = tk.Button(edit_frame, text="Edit Snippet", command=edit_snippet)
edit_button.grid(row=3, column=0, columnspan=2, pady=5)

# Delete a snippet
delete_frame = tk.Frame(root)
delete_frame.pack(pady=10)

tk.Label(delete_frame, text="Title to Delete:").grid(row=0, column=0, padx=5)
delete_title_entry = tk.Entry(delete_frame)
delete_title_entry.grid(row=0, column=1, padx=5)

delete_button = tk.Button(delete_frame, text="Delete Snippet", command=delete_snippet)
delete_button.grid(row=1, column=0, columnspan=2, pady=5)

root.mainloop()
