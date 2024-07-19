import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkinter import font  # Import the font module

import mysql.connector

# Connect to MySQL database
def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="anitejmishra",
            database="anitej2"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

# Add a new entry to the database
def add_entry(conn, table):
    try:
        cursor = conn.cursor()
        query = f"DESCRIBE {table}"
        cursor.execute(query)
        columns = [col[0] for col in cursor.fetchall()]

        add_window = tk.Toplevel()
        add_window.title("Add Entry")

        entries = {}
        for i, column in enumerate(columns):
            label = tk.Label(add_window, text=column.capitalize() + ":", font=("Qatar2022-Medium", 12))  # Use custom font
            label.grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(add_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[column] = entry

        def submit_entry():
            values = ",".join([f"'{entry.get()}'" for entry in entries.values()])
            query = f"INSERT INTO {table} VALUES ({values})"
            try:
                cursor.execute(query)
                conn.commit()
                messagebox.showinfo("Success", "Entry added successfully.")
                add_window.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")

        submit_button = tk.Button(add_window, text="Add Entry", command=submit_entry, font=("Qatar2022-Medium", 12), bg="#FF9933", fg="white")  # Use custom font
        submit_button.grid(row=len(columns), columnspan=2, padx=10, pady=5)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

# View entries in a table
def view_table(conn, table):
    try:
        cursor = conn.cursor()
        query = f"SELECT * FROM {table}"
        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            messagebox.showinfo("No Entries", "No entries found.")
            return

        # Create a new window for displaying table
        view_window = tk.Toplevel()
        view_window.title(f"View Table - {table}")

        # Create treeview widget
        tree = ttk.Treeview(view_window)
        tree["columns"] = [desc[0] for desc in cursor.description]
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Insert data into treeview
        for row in rows:
            tree.insert("", "end", values=row)
        
        tree.pack(expand=True, fill="both")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

# Main window
def main():
    conn = connect_to_mysql()
    if conn:
        print("Connected to the Store Management System database.")
        root = tk.Tk()
        root.title("STORE MANAGEMENT SYSTEM")
        root.geometry("600x400")

        # Load custom fonts
        custom_font_title = font.Font(family="Qatar2022-Bold", size=24)  # Title font
        custom_font_text = font.Font(family="Qatar2022-Medium", size=12)  # Text font

        # Create a colorful banner with title and motto
        banner_frame = tk.Frame(root, bg="#FF9933")  # Saffron color
        banner_frame.pack(fill="x")

        title_label = tk.Label(banner_frame, text="STORE MANAGEMENT SYSTEM", font=custom_font_title, fg="white", bg="#007FFF")  # Use custom title font
        title_label.pack(pady=10)

        motto_label = tk.Label(banner_frame, text="Simplifying your business since 2024", font=custom_font_text, fg="white", bg="#008000")  # Use custom text font
        motto_label.pack(pady=5)

        def open_add_entry_window():
            table_name = simpledialog.askstring("Table Name", "Enter table name:")
            if table_name:
                add_entry(conn, table_name)

        def open_view_table_window():
            table_name = simpledialog.askstring("Table Name", "Enter table name:")
            if table_name:
                view_table(conn, table_name)

        add_button = tk.Button(root, text="Add Entry", command=open_add_entry_window, font=custom_font_text, bg="#008000", fg="white")  # Use custom text font
        add_button.pack(pady=10)

        view_button = tk.Button(root, text="View Table", command=open_view_table_window, font=custom_font_text, bg="#007FFF", fg="white")  # Use custom text font
        view_button.pack(pady=10)

        team_members = ["Anitej Mishra", "S Gagan", "Satvik Sharma"]
        team_label = tk.Label(root, text="Team Members:", font=("Qatar2022-Medium", 12, "bold"), fg="#FF9933")  # Use custom text font
        team_label.pack()
        for member in team_members:
            member_label = tk.Label(root, text=member, font=("Qatar2022-Medium", 12))  # Use custom text font
            member_label.pack()

        root.mainloop()
        conn.close()
        print("Disconnected from the Store Management System database.")

if __name__ == "__main__":
    main()
