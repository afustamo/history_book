#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 17:43:39 2023

@author: alessandrofusta
"""

import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog
import matplotlib.dates as mdates
from dateutil import parser
from datetime import datetime
import os

# Set the working directory
new_directory = "/Users/alessandrofusta/Library/Mobile Documents/com~apple~CloudDocs/MyP/h"
os.chdir(new_directory)

# Function to read characters from CSV file
def read_characters():
    file_path = 'characters.csv'
    if os.path.isfile(file_path):
        return pd.read_csv(file_path,sep=",")
    return []

# Initialize characters from the CSV file
characters = read_characters()

# Function to write characters to a CSV file
def write_characters(characters):
    pd.DataFrame(characters).to_csv('characters.csv', index=False)

# Function for generic input
def input_dialog(title, labels, callback, message_var):
    input_window = tk.Toplevel()
    input_window.title(title)

    entries = [tk.Entry(input_window) for _ in labels]
    for row, (label, entry) in enumerate(zip(labels, entries)):
        tk.Label(input_window, text=label).grid(row=row, column=0)
        entry.grid(row=row, column=1)

    def ok_button_callback():
        values = [entry.get() for entry in entries]
        callback(*values)
        input_window.destroy()

    ok_button = tk.Button(input_window, text="OK", command=ok_button_callback)
    ok_button.grid(row=len(labels), column=0, columnspan=2)

    cancel_button = tk.Button(input_window, text="Cancel", command=input_window.destroy)
    cancel_button.grid(row=len(labels) + 1, column=0, columnspan=2)

    tk.Label(input_window, textvariable=message_var).grid(row=len(labels) + 2, column=0, columnspan=2)

# Function to add a character
def add_character():
    title = "Add Character"
    labels = ["Name:", "Date of Birth (YYYY/MM/DD):", "Date of Death (Leave blank if alive):"]
    callback = lambda name, birth_date, death_date: handle_add_character(name, birth_date, death_date)
    message_var = tk.StringVar()
    input_dialog(title, labels, callback, message_var)

# Callback function for add_character
def handle_add_character(name, birth_date, death_date):
    new_character = {
        "name": name,
        "date_of_birth": birth_date,
        "date_of_death": death_date if death_date else None
    }
    characters.append(new_character)
    write_characters(characters)

# Function to display the map
def display_map():
    df = pd.DataFrame(characters)
    df["date_of_birth"] = pd.to_datetime(df["date_of_birth"], errors='coerce')
    df["date_of_death"] = pd.to_datetime(df["date_of_death"], errors='coerce')

    df = df.sort_values(by="date_of_birth")
    today_date = datetime.today().date()
    formatted_date = today_date.strftime("%Y-%m-%d")
    df["date_of_death"] = df["date_of_death"].fillna(formatted_date)

    fig, ax = plt.subplots(figsize=(10, 6))

    for _, char in df.iterrows():
        birth_date_dt = char["date_of_birth"] or datetime(1500, 1, 1)
        death_date_dt = char["date_of_death"] or datetime.now()

        timedelta = (death_date_dt - birth_date_dt) / 2
        midpoint = birth_date_dt + timedelta

        ax.plot(
            [mdates.date2num(birth_date_dt), mdates.date2num(death_date_dt)],
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

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.xaxis.set_major_locator(mdates.YearLocator(100))
    ax.set_xlim(mdates.date2num(df["date_of_birth"].min()), mdates.date2num(df["date_of_death"].max()))
    ax.set_yticklabels([])

    plt.title("Historical Characters Map")
    plt.show()

# Other functions...

# Function to modify an existing character
def modify_character():
    char_name = simpledialog.askstring("Input", "Enter the name of the character to modify:")
    character = next((char for char in characters if char["name"] == char_name), None)
    
    if character:
        birth_date = simpledialog.askstring("Input", "Enter New Date of Birth (YYYY/MM/DD):")
        death_date = simpledialog.askstring("Input", "Enter New Date of Death (Leave blank if alive):")

        character["date_of_birth"] = birth_date
        character["date_of_death"] = death_date
        write_characters(characters)
        print("Character modified successfully!\n")
    else:
        print("Character not found.\n")

# Function to display character information
def display_character_info():
    char_name = simpledialog.askstring("Input", "Enter the name of the character to display information:")

    # Check if the character exists
    character = next((char for char in characters if char["name"] == char_name), None)
    if character:
        print("Character Information:")
        print(pd.DataFrame([character]))
    else:
        print("Character not found.\n")

# Function to remove a character
def remove_character():
    char_name = simpledialog.askstring("Input", "Enter the name of the character to remove:")

    # Check if the character exists
    character_index = next((index for index, char in enumerate(characters) if char["name"] == char_name), None)

    if character_index is not None:
        del characters[character_index]
        write_characters(characters)  # Update the CSV file
        print("Character removed successfully!\n")
    else:
        print("Character not found.\n")

# Function to display the list of characters
def display_character_list():
    if not characters:
        print("No characters in the list.\n")
    else:
        print("List of Characters:")
        for char in characters:
            print(f"Name: {char['name']}, Date of Birth: {char['date_of_birth']}, Date of Death: {char['date_of_death']}")
        print()



# Function to handle GUI
def gui():
    root = tk.Tk()
    root.title("Historical Characters Game")

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
            print("Closing the game. Goodbye!\n")
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
