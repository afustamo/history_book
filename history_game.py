import tkinter as tk
from tkinter import simpledialog, StringVar
from tkinter import scrolledtext
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil import parser
import wikipediaapi
import os
import re
import numpy as np
import matplotlib.backends.backend_pdf
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import matplotlib

# Create a Tkinter window
root = tk.Tk()
root.title("Historical Characters Game")
root.geometry("800x600")  # Set the size as needed

def create_new_window(title):
    new_window = tk.Toplevel(root)
    new_window.title(title)
    return new_window

# Define a StringVar to update the message label text
message_var = StringVar()

# Add a Label to the GUI to display messages
message_label = tk.Label(root, textvariable=message_var)
message_label.pack()

# Function for generic input
def input_dialog(title, label, callback, message_var):
    input_window = tk.Toplevel()
    input_window.title(title)

    tk.Label(input_window, text=label).grid(row=0, column=0)
    entry = tk.Entry(input_window)
    entry.grid(row=0, column=1)

    # Callback function for the "OK" button
    def ok_button_callback():
        value = entry.get()
        callback(value)
        input_window.destroy()

    # "OK" button
    ok_button = tk.Button(input_window, text="OK", command=ok_button_callback)
    ok_button.grid(row=1, column=0, columnspan=2)

    # Callback function for the "Cancel" button
    def cancel_button_callback():
        input_window.destroy()

    # "Cancel" button
    cancel_button = tk.Button(input_window, text="Cancel", command=cancel_button_callback)
    cancel_button.grid(row=2, column=0, columnspan=2)

    # Message widget
    message_label = tk.Label(input_window, textvariable=message_var)
    message_label.grid(row=3, column=0, columnspan=2)
    
def set_message(message):
    message_var.set(message)
    message_label.config(text=message_var.get())

# Get the current working directory
current_directory = os.getcwd()
print(f"Current Working Directory: {current_directory}")

# Change the working directory
new_directory = "/Users/alessandrofusta/Library/Mobile Documents/com~apple~CloudDocs/MyP/h"
os.chdir(new_directory)

# Verify the change
updated_directory = os.getcwd()
print(f"Updated Working Directory: {updated_directory}")

def read_characters():
    file_path = 'characters.csv'
    print(f"Checking file existence: {os.path.isfile(file_path)}")
    try:
        df = pd.read_csv(file_path, sep=',', parse_dates=['date_of_birth', 'date_of_death'])
        return df.to_dict('records') if not df.empty else []
    except FileNotFoundError:
        return []

# Initialize characters from the CSV file
characters = read_characters()

def write_characters(characters):
    df = pd.DataFrame(characters)
    df.to_csv('characters.csv', index=False)

# Example usage for add_character
def add_character():
    title = "Add Character"
    label = "Search and select a character:"
    callback = lambda name: handle_add_character(name)
    message_var = tk.StringVar()
    input_dialog(title, label, callback, message_var)

# Wikipedia API client
wiki_wiki = wikipediaapi.Wikipedia("history_book (alessandro.fusta@outlook.it)","en")

def fetch_character_details(name):
    wiki_wiki = wikipediaapi.Wikipedia("history_book (alessandro.fusta@outlook.it)","en")
    page_py = wiki_wiki.page(name)

    if not page_py.exists():
        print(f"Error: Wikipedia page for {name} not found.")
        return None

    # Extract birth and death information from categories
    birth_date = None
    death_date = None

    for category in page_py.categories.values():
        category_name = category.title
        # Use regular expressions to match patterns in categories
        birth_match = re.match(r'Category:(\d{4}) births', category_name)
        death_match = re.match(r'Category:(\d{4}) deaths', category_name)

        if birth_match:
            birth_date = birth_match.group(1)
        elif death_match:
            death_date = death_match.group(1)

    # Create a dictionary with character details
    character_details = {
        'name': name,
        'date_of_birth': birth_date if birth_date else "Not available",
        'date_of_death': death_date if death_date else "Not available",
    }

    return character_details

# Callback function for add_character
def handle_add_character(name):
    # Fetch character details from Wikipedia
    character_details = fetch_character_details(name)

    if character_details:
        characters.append(character_details)
        write_characters(characters)  # Update the CSV file
        print("Character added successfully!\n")
    else:
        print("Character not found on Wikipedia.\n")

# Function to modify an existing character
def modify_character():
    char_name = simpledialog.askstring("Input", "Enter the name of the character to modify:")

    # Check if the character exists
    character = next((char for char in characters if char["name"] == char_name), None)
    if character:
        new_name = simpledialog.askstring("Input", "Enter New Name:")
        birth_date = simpledialog.askstring("Input", "Enter New Date of Birth (YYYY/MM/DD):")
        death_date = simpledialog.askstring("Input", "Enter New Date of Death (Leave blank if alive):")

        # Update the character in the list
        character["name"] = new_name
        character["date_of_birth"] = birth_date
        character["date_of_death"] = death_date
        write_characters(characters)  # Update the CSV file
        set_message("Character modified successfully!\n")  # Update the message label
    else:
        set_message("Character not found.\n")  # Update the message label

# Function to remove a character
def remove_character():
    char_name = simpledialog.askstring("Input", "Enter the name of the character to remove:")

    # Check if the character exists
    character_index = next((index for index, char in enumerate(characters) if char["name"] == char_name), None)

    if character_index is not None:
        del characters[character_index]
        write_characters(characters)  # Update the CSV file
        set_message("Character removed successfully!\n")  # Update the message label
    else:
        set_message("Character not found.\n")  # Update the message label

def display_character_list():
    if not characters:
        set_message("No characters in the list.\n")  # Update the message label in the main window
    else:
        message = "List of Characters:\n"
        for char in characters:
            message += f"Name: {char['name']}, Date of Birth: {char['date_of_birth']}, Date of Death: {char['date_of_death']}\n"

        # Create a new Toplevel window for displaying the list with a scrollbar
        list_window = create_new_window("Character List")

        # Create a scrolled text widget
        scroll_text = scrolledtext.ScrolledText(list_window, wrap=tk.WORD, width=40, height=20)
        scroll_text.pack(expand=True, fill='both')

        # Insert the character list into the scrolled text widget
        scroll_text.insert(tk.END, message)

# Remove the following line from the display_character_list function
# set_message(message)  # Update the message label in the main window

# Function to display character information
def display_character_info():
    char_name = simpledialog.askstring("Input", "Enter the name of the character to display information:")

    # Check if the character exists
    character = next((char for char in characters if char["name"] == char_name), None)
    if character:
        message = f"Character Information:\n{pd.DataFrame([character])}\n"
        set_message(message)  # Update the message label
    else:
        set_message("Character not found.\n")  # Update the message label

# Function to save and display the map
def save_to_pdf(fig, filename):
    pdf_pages = matplotlib.backends.backend_pdf.PdfPages(filename)
    pdf_pages.savefig(fig, bbox_inches='tight', dpi=300)
    pdf_pages.close()


def display_map():
    map_window = create_new_window("Historical Characters Map")
    df = pd.DataFrame(characters)
    df["date_of_death"]
    today_date = datetime.today().date()
    formatted_date = today_date.strftime("%Y-%m-%d")
    df.loc[df["date_of_death"]=="", "date_of_death"] = np.nan
    df["date_of_death"] = df["date_of_death"].fillna(formatted_date)

    df["date_of_birth"] = df["date_of_birth"].apply(lambda x: parser.parse(x) if pd.notnull(x) and x != "Not available" else None)  
    df["date_of_death"] = df["date_of_death"].apply(lambda x: parser.parse(x) if pd.notnull(x) and x != "Not available" else None)

    df = df.sort_values(by="date_of_birth")
    
    fig, ax = plt.subplots(figsize=(10, 6))

    for _, char in df.iterrows():
        birth_date_str = char["date_of_birth"].strftime("%Y-%m-%d") if pd.notnull(char["date_of_birth"]) else ""
        death_date_str = char["date_of_death"].strftime("%Y-%m-%d") if pd.notnull(char["date_of_death"]) else "today"

        if birth_date_str:
            birth_date_dt = datetime.strptime(birth_date_str, "%Y-%m-%d")
        else:
            birth_date_dt = datetime(1500, 1, 1)  # Adjusted default birth date

        if death_date_str != "today":
            death_date_dt = datetime.strptime(death_date_str, "%Y-%m-%d") if death_date_str else datetime.now()
        else:
            death_date_dt = datetime.now()

        # Calculate the midpoint between date_of_birth and date_of_death
        timedelta = (death_date_dt - birth_date_dt) / 2
        midpoint = birth_date_dt + timedelta

        ax.plot(
            [birth_date_dt, death_date_dt],
            [char["name"], char["name"]],
            label=char["name"],
            linewidth=3
        )
        ax.text(
            midpoint,
            char["name"],
            char["name"],
            ha='center',
            va='bottom',
            fontsize=8
        )

    # Set date formatter for x-axis
    date_format = mdates.DateFormatter("%Y")
    ax.xaxis.set_major_formatter(date_format)

    # Set date locator for x-axis
    ax.xaxis.set_major_locator(mdates.YearLocator(100))
    
    # Set custom x-axis limits
    min_date = df["date_of_birth"].dropna().min()
    max_date = df["date_of_death"].dropna().max()
    ax.set_xlim(min_date, max_date)
    
    # Add horizontal ticks and lines every 100 years
    years_locator = mdates.YearLocator(base=50)
    ax.xaxis.set_minor_locator(years_locator)

    # Move x-axis tick labels to the top
    ax.tick_params(axis='x', which='both', bottom=True, top=True, labelbottom=True, labeltop=True)
    
    # Ensure minor grid lines are displayed on top of tick labels
    ax.xaxis.grid(True, which='major', linestyle='--', linewidth=1, color='gray', alpha=1, zorder = 1)
    ax.xaxis.grid(True, which='minor', linestyle='--', linewidth=0.5, color='gray', alpha=0.5, zorder = 1)
    
    # Hide y-axis tick labels
    ax.set_yticklabels([])
    
    plt.title("Historical Characters Map")
    
    map_window = create_new_window("Historical Characters Map")
    
    # Display the Matplotlib plot in the existing window
    canvas = FigureCanvasTkAgg(fig, master=map_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Add a Matplotlib navigation toolbar
    toolbar = NavigationToolbar2Tk(canvas, map_window)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Enable interactive zooming
    def on_key(event):
        if event.key == 'Z':
            toolbar.zoom()
        elif event.key == 'p':
            toolbar.pan()

    canvas.mpl_connect('key_press_event', on_key)

    # Save the plot to a PDF file
    # save_to_pdf(fig, "historical_characters_map.pdf")



# GUI function
def gui():
    root.title("Historical Characters Game")

    # Set the initial size of the window
    root.geometry("800x600")  # Set the size as needed

    def button_click(choice):
        if choice == 1:
            add_character()
        elif choice == 2:
            modify_character()
        elif choice == 3:
            display_character_info()
        elif choice == 4:
            display_map()
        elif choice == 5:
            remove_character()
        elif choice == 6:
            display_character_list()
        elif choice == 0:
            print("Closing the history map. Goodbye!\n")
            root.destroy()
        else:
            print("Invalid choice. Please enter a valid option.\n")

    buttons = [
        tk.Button(root, text=f"{i}: {label}", command=lambda i=i: button_click(i))
        for i, label in enumerate(["Close","Add a character", "Modify an existing character",
                                   "Display character information", "Display the map", "Delete a character",
                                   "Display character list"])
    ]

    for button in buttons:
        button.pack()

    root.mainloop()

if __name__ == "__main__":
    gui()

