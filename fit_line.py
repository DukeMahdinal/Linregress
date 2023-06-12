import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy import stats
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import webbrowser
from tkinter import messagebox

# sample data
x = np.array([])
y = np.array([])

# linear regression
if len(x) > 0 and len(y) > 0:
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
else:
    slope = intercept = r_value = p_value = std_err = 0

fig, ax = plt.subplots()
ax.scatter(x,y)
fig.subplots_adjust(bottom=0.2)

# extend fit line beyond given data points
x_fit = np.linspace(min(x)-1,max(x)+1) if len(x)>0 else np.array([])
line, = ax.plot([],[], color='red')

# display formula for fit line
if len(x) > 0 and len(y) > 0:
    fit_text = plt.text(0.5, -0.3,'y = {:.2f}x + {:.2f}'.format(slope,intercept), ha='center', va='top', transform=plt.gca().transAxes)
else:
    fit_text = plt.text(0.5, -0.2,'', ha='center', va='center', transform=plt.gca().transAxes)


def import_data():
    global x,y,slope,x_fit,line, fit_text, text_artist
    # open file dialog to select excel file
    filename = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    # check if filename is not empty
    if not filename:
        return
    # read data from excel file
    try:
        data = pd.read_excel(filename)
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {filename}")
        return
    # get x and y values from data
    x_vals = data['x'].values
    y_vals = data['y'].values
    # check if there are already data points with the same x-values on the canvas
    mask = np.isin(x_vals, x)
    # discard values from excel file that are already on the canvas
    x_vals = x_vals[~mask]
    y_vals = y_vals[~mask]
    # add new data points to chart
    ax.scatter(x_vals,y_vals,color='green')
    for i in range(len(x_vals)):
        ax.text(x_vals[i], y_vals[i], f'({x_vals[i]:.{min(4, len(str(x_vals[i]).split(".")[1]))}f},{y_vals[i]:.{min(4, len(str(y_vals[i]).split(".")[1]))}f})')
    # add new data points to data arrays
    x = np.append(x,x_vals)
    y = np.append(y,y_vals)
    # enable analyze button if there is more than one data point
    if len(x) > 1:
        analyze_button.config(state=tk.NORMAL)
    canvas.draw()

def validate_input():
    try:
        x_val = float(x_entry.get())
        y_val = float(y_entry.get())
        if x_val in x:
            add_button.config(state=tk.DISABLED)
        else:
            add_button.config(state=tk.NORMAL)
    except ValueError:
        add_button.config(state=tk.DISABLED)

def animate(i):
    # Update the data of the fit line to create the animation
    line.set_data(x_fit[:i], slope*x_fit[:i] + intercept)
    return line,

# Create the animation for the fit line appearing
if len(x_fit) > 0:
    ani = FuncAnimation(fig, animate, frames=len(x_fit), interval=50, blit=True, repeat = False)
    
def add_point():
    global x,y,slope,x_fit,line, fit_text, text_artist
    # get entered x and y values for new data point
    x_val = float(x_entry.get())
    y_val = float(y_entry.get())

    # add new data point to chart
    for coll in ax.collections:
        if coll.get_facecolor()[0][1] == 1: # check if collection is green
            coll.remove()
    ax.scatter(x_val,y_val,color='green')
    # display coordinates above dot with full precision
    ax.text(x_val,y_val,f'({x_val:.{min(4, len(str(x_val).split(".")[1]))}f},{y_val:.{min(4, len(str(y_val).split(".")[1]))}f})', fontsize=8)
    # add new data point to data arrays
    x = np.append(x,x_val)
    y = np.append(y,y_val)

    # clear input fields
    x_entry.delete(0,'end')
    y_entry.delete(0,'end')
    # enable analyze button if there is more than one data point
    if len(x) > 1:
        analyze_button.config(state=tk.NORMAL)
    canvas.draw()

def analyze():
    global x,y,slope,x_fit,line,intercept,ani
    # recalculate fit line to pass through all blue dots (data points)
    if len(x) > 0 and len(y) > 0:
        slope, intercept,r_value,p_value,std_err=stats.linregress(x,y)
        x_fit=np.linspace(min(x)-1,max(x)+1)
        # Create a new animation for the updated fit line if x_fit is not empty
        if len(x_fit) > 0:
            ani = FuncAnimation(fig, animate, frames=len(x_fit), interval=50, blit=True, repeat = False)
    # update formula for fit line
    fit_text.set_text('y = {:.2f}x + {:.2f}'.format(slope,intercept))
    # recalculate yellow points based on new fit line
    for coll in ax.collections:
        if coll.get_facecolor()[0][0] == 1: # check if collection is yellow
            x_val = coll.get_offsets()[0][0]
            y_val = slope*x_val + intercept
            coll.set_offsets([x_val,y_val])
            # update coordinates above yellow dot
            for txt in ax.texts:
                try:
                    float(txt.get_text().split(',')[0][1:])
                    txt.set_position((x_val,y_val))
                    txt.set_text('({:.2f},{:.2f})'.format(x_val,y_val))
                except ValueError:
                    pass
        elif coll.get_facecolor()[0][1] == 1: # check if collection is green
            coll.remove()
    ax.scatter(x, y, color='blue')
    # remove text objects displaying coordinates of blue points
    for txt in ax.texts:
        if txt != fit_text and txt != text_artist:
            try:
                float(txt.get_text().split(',')[0][1:])
                txt.remove()
            except ValueError:
                pass
    # redraw coordinates of all data points
    for i in range(len(x)):
        ax.text(x[i], y[i], f'({x[i]:.{min(4, len(str(x[i]).split(".")[1]))}f},{y[i]:.{min(4, len(str(y[i]).split(".")[1]))}f})', fontsize=8)
    # enable calculate button
    calc_button.config(state=tk.NORMAL)
    canvas.draw()

def newton_interpolation(x_vals, y_vals):
    global x,y,slope,x_fit,line, fit_text, text_artist
    # calculate divided differences
    n = len(x_vals)
    div_diffs = np.zeros((n, n))
    div_diffs[:, 0] = y_vals
    for j in range(1, n):
        for i in range(n-j):
            div_diffs[i][j] = (div_diffs[i+1][j-1] - div_diffs[i][j-1]) / (x_vals[i+j] - x_vals[i])
    # calculate coefficients of polynomial
    coeffs = div_diffs[0]
    # define function to evaluate polynomial
    def f(x):
        result = coeffs[-1]
        for i in range(n-2, -1, -1):
            result = result * (x - x_vals[i]) + coeffs[i]
        return result
    # plot polynomial
    x_fit = np.linspace(np.min(x_vals), np.max(x_vals), 100)
    y_fit = f(x_fit)
    line.set_data(x_fit, y_fit)
    # display formula of polynomial
    formula = f'P(x) = {coeffs[0]:.4f}'
    for i in range(1, n):
        formula += f' + {coeffs[i]:.4f}'
        for j in range(i):
            formula += f'(x - {x_vals[j]:.4f})'
    fit_text.set_text(formula)
    canvas.draw()

def reset():
    global x,y,slope,x_fit,line, fit_text, text_artist
    # clear all data points from chart and reset fit line
    ax.clear()
    x=np.array([])
    y=np.array([])
    slope=intercept=r_value=p_value=std_err=0
    x_fit=np.linspace(min(x)-1,max(x)+1) if len(x)>0 else np.array([])
    line=ax.plot([],[],color='red')[0]
    # recreate fit_text and text_artist artists
    fit_text = ax.text(0.5,-0.2,'', ha='center', va='center', transform=ax.transAxes)
    text_artist = ax.text(0.5, 1.05, '', transform=ax.transAxes, ha='center')
    # clear text entry
    text_entry.delete(0, 'end')
    # disable analyze and calculate buttons
    analyze_button.config(state=tk.DISABLED)
    calc_button.config(state=tk.DISABLED)
    canvas.draw()


def submit():
    global x,y,slope,x_fit,line, intercept
    # calculate y value based on fit line
    x_val = float(calc_entry.get())
    y_val = slope*x_val + intercept
    # display yellow dot on chart at calculated location
    ax.scatter(x_val,y_val,color='yellow')
    # display coordinates above yellow dot
    ax.text(x_val,y_val,'({:.2f},{:.2f})'.format(x_val,y_val))
    # recalculate fit line to pass through all data points and calculated points
    x_all = np.append(x, x_val)
    y_all = np.append(y, y_val)
    slope, intercept,r_value,p_value,std_err=stats.linregress(x_all,y_all)
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    x_fit_range = np.linspace(x_min-1,x_max+1)
    line.set_data(x_fit_range,slope*x_fit_range+intercept)
    # update formula for fit line
    fit_text.set_text('y = {:.2f}x + {:.2f}'.format(slope,intercept))
    canvas.draw()

def save():
    # Get the filename from the input field
    filename = filename_entry.get()
    # Save the figure as an image
    fig.savefig(filename)

def update_text(*args):
    # Cancel any previous update_text calls
    if update_text.after_id is not None:
        root.after_cancel(update_text.after_id)
    # Schedule a new update_text call 1 second later
    update_text.after_id = root.after(1000, update_text_now)

def update_text_now():
    # Get the text from the input field
    text = text_var.get()
    # Update the text above the chart
    text_artist.set_text(text)
    # Redraw the canvas
    canvas.draw()
    
guide_window_open = False

def show_guide():
    global guide_window_open
    if not guide_window_open:
        guide_window = tk.Toplevel(root)
        guide_window.protocol("WM_DELETE_WINDOW", lambda: on_guide_window_close(guide_window))
        guide_text = """Welcome to the Linear Regression app!

This app allows you to add data points to a scatter plot and perform a linear regression analysis to find the best-fit line for the data.

To add a new data point, enter the x and y coordinates in the 'New Data Point' section and click the 'ADD' button. You can also update an existing data point by entering its x coordinate and a new y coordinate, then clicking the 'UPDATE' button. To delete an existing data point, enter its x coordinate and 'x' as the y coordinate, then clicking the 'DELETE' button.

To import data from an Excel file, click the 'Import Data' button and select the file. The data should be in two columns labeled 'x' and 'y'.

Once you have added at least two data points, you can click the 'Analyze' button to perform a linear regression analysis and display the best-fit line for the data. The formula for the line will be displayed below the plot.

You can also calculate the y-value for a given x-value based on the best-fit line by entering the x-value in the 'Calculate based on fit line' section and clicking the 'Calculate' button. This will add a new point to the plot with the calculated y-value.

You can zoom in and out on the plot by scrolling up and down while hovering over it. You can also pan around the plot by clicking and dragging with the right mouse button.

To reset the plot and clear all data points, click the 'Reset' button.

You can save an image of the current plot by entering a filename in the 'Filename' field and clicking the 'SAVE' button.

Data points are color-coded to indicate their type:"""
        guide_label = tk.Label(guide_window, text=guide_text, justify=tk.LEFT)
        guide_label.pack(anchor=tk.W)
        
        # Create frame for color labels
        color_frame = tk.Frame(guide_window)
        color_frame.pack(anchor=tk.W)
        
        # Create labels with colored text for each type of data point
        green_label = tk.Label(color_frame, text="Green: ", fg="green")
        green_label.pack(side=tk.LEFT)
        green_text = tk.Label(color_frame, text="Manually added or imported data points")
        green_text.pack(side=tk.LEFT)
        
        yellow_label = tk.Label(color_frame, text="\nYellow: ", fg="orange")
        yellow_label.pack(side=tk.LEFT)
        yellow_text = tk.Label(color_frame, text="Calculated points based on best-fit line")
        yellow_text.pack(side=tk.LEFT)
        
        guide_window_open = True


def on_guide_window_close(guide_window):
    global guide_window_open
    guide_window.destroy()
    guide_window_open = False

def frame(row,column,span=1):

    frame = tk.Frame(root)
    frame.grid(row=row, column=column,columnspan=span, sticky="nsew")
    
    return frame
    

root = tk.Tk()
root.wm_title("Linear Regression")

canvas = FigureCanvasTkAgg(fig,master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=0,column=0,rowspan=10,columnspan=6, sticky="nsew")

def zoom(event):
    # Get the current x and y limits
    cur_xlim = ax.get_xlim()
    cur_ylim = ax.get_ylim()
    cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
    cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
    xdata = event.xdata # get event x location
    ydata = event.ydata # get event y location
    if event.button == 'up':
        # Zoom in
        scale_factor = 1/1.5
    elif event.button == 'down':
        # Zoom out
        scale_factor = 1.5
    else:
        # Something else
        scale_factor = 1
    # Set new limits
    new_xlim = [xdata - cur_xrange*scale_factor,
                xdata + cur_xrange*scale_factor]
    new_ylim = [ydata - cur_yrange*scale_factor,
                ydata + cur_yrange*scale_factor]
    ax.set_xlim(new_xlim)
    ax.set_ylim(new_ylim)
    
    canvas.draw()

canvas.mpl_connect('scroll_event', zoom)

def on_press(event):
    if event.button == 3:
        global press
        press = event.xdata, event.ydata

def on_release(event):
    if event.button == 3:
        global press
        press = None

def on_motion(event):
    if press is None:
        return
    if event.inaxes != ax:
        return
    xpress, ypress = press
    dx = event.xdata - xpress
    dy = event.ydata - ypress
    cur_xlim = ax.get_xlim()
    cur_ylim = ax.get_ylim()
    ax.set_xlim(cur_xlim[0]-dx, cur_xlim[1]-dx)
    ax.set_ylim(cur_ylim[0]-dy, cur_ylim[1]-dy)
    canvas.draw()

global press
press = None

canvas.mpl_connect('button_press_event', on_press)
canvas.mpl_connect('button_release_event', on_release)
canvas.mpl_connect('motion_notify_event', on_motion)

# Create a StringVar to hold the text
text_var = tk.StringVar()

# Trace changes to the StringVar and call update_text when it changes
text_var.trace('w', update_text)

# Create the input field for the text
text_label = tk.Label(frame(10,0), text="Title:")
text_label.pack(anchor="w", padx=(20, 0) , pady=(11 ,0))
text_entry = tk.Entry(root, textvariable = text_var ,state= "normal" )
text_entry.grid(row=10, column=1)


# Create a text artist to display the text above the chart
text_artist = ax.text(0.5, 1.05, '', transform=ax.transAxes, ha='center')

# Initialize after_id to None
update_text.after_id = None

new_data_label = tk.Label(root, text="New   Data Point")
new_data_label.grid(row=0, column=6, columnspan=3, sticky="nsew")

x_entry_var = tk.StringVar()
y_entry_var = tk.StringVar()

x_label = tk.Label(root, text="x:")
x_label.grid(row=1, column=6, sticky="nsew")
x_entry = tk.Entry(frame(1,7), textvariable=x_entry_var)
x_entry.pack(anchor="w", padx=(25, 22.5) , pady=(12 ,0))

y_label = tk.Label(root, text="y:")
y_label.grid(row=2, column=6, sticky="nsew")
y_entry = tk.Entry(frame(2,7), textvariable=y_entry_var)
y_entry.pack(anchor="w", padx=(25, 22.5) , pady=(11 ,0))

add_button = tk.Button(master=frame(3,6), text="ADD", command=add_point, state=tk.DISABLED)
add_button.pack(anchor="w", padx=(30, 0) , pady=(15 ,0))

x_entry_var.trace('w', lambda *args: validate_input())
y_entry_var.trace('w', lambda *args: validate_input())

import_button = tk.Button(frame(3,7), text="Import Data", command=import_data)
import_button.pack(anchor="w", padx=(45, 0) , pady=(15 ,0))

analyze_button = tk.Button(master=frame(3,8), text="Analyze", command=analyze)
analyze_button.pack(anchor="w", padx=(0, 0) , pady=(14 ,0))

reset_button = tk.Button(master=frame(7,8), text="Reset", command=reset)
reset_button.pack(anchor="w", padx=(12.5, 0) , pady=(2.5 ,0))

calc_label = tk.Label(root, text="Calculate based on fit line:")
calc_label.grid(row=4, column=6, columnspan=3)

x_calc_label = tk.Label(root, text="x:")
x_calc_label.grid(row=5, column=6, sticky="nsew")

calc_entry = tk.Entry(frame(5, 7))
calc_entry.pack(anchor="w", padx=(25, 22.5), pady=(11,0))

calc_button = tk.Button(master=frame(7,6), text="Calculate", command=submit)
calc_button.pack(anchor="w", padx=(20, 0) , pady=(2.5 ,0))

# Create the input field for the filename
filename_label = tk.Label(root, text="Filename:")
filename_label.grid(row=10, column=2)
filename_entry = tk.Entry(root)
filename_entry.grid(row=10, column=3)

# Create the save button
save_button = tk.Button(master=frame(10,4), text="SAVE", command=save)
save_button.pack(anchor="w", padx=(10, 0) , pady=(10 ,10))

guide_button = tk.Button(root, text="Show Guide", command=show_guide)
guide_button.grid(row=10, column=5)

analyze_button.config(state=tk.DISABLED)
calc_button.config(state=tk.DISABLED)

# Create frame for developer labels
dev_frame = tk.Frame(root)
dev_frame.grid(row=10, column=7)

# Create label with "Developed By" text
dev_label = tk.Label(dev_frame, text="~~ Developed By")
dev_label.grid(row=0, column=0)

# Create label with "Duke" text and make it a clickable link
duke_label = tk.Label(dev_frame, text="Duke", fg="blue", cursor="hand2")
duke_label.grid(row=0, column=1)
duke_label.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/TheOneWhoCares0"))

# Create label with "~~" text
end_label = tk.Label(dev_frame, text=" ~~")
end_label.grid(row=0, column=2)

# Create the Newton Interpolation button
newton_button = tk.Button(master=frame(3,9), text="Newton Interpolation", command=lambda: newton_interpolation(x, y))
newton_button.pack(anchor="w", padx=(0, 0) , pady=(14 ,0))

# Make all labels bold and underlined with font size 12
for label in [dev_label, duke_label, end_label]:
    label.config(font="-weight bold -size 8")


def on_closing():
    root.quit()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

tk.mainloop()