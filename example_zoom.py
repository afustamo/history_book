import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np

def display_map():
    map_window = tk.Toplevel(root)
    map_window.title("Historical Characters Map")

    # Create a Matplotlib figure
    fig, ax = plt.subplots()
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    ax.plot(x, y)

    # Create Matplotlib canvas
    canvas = FigureCanvasTkAgg(fig, master=map_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Add Matplotlib navigation toolbar
    toolbar = NavigationToolbar2Tk(canvas, map_window)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Create the main Tkinter window
root = tk.Tk()
root.title("Historical Characters Game")

# Add a button to trigger the display_map function
btn_show_map = tk.Button(root, text="Show Map", command=display_map)
btn_show_map.pack()

# Run the Tkinter main loop
root.mainloop()
