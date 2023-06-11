import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy import stats
import tkinter as tk

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

# extend fit line beyond given data points
x_fit = np.linspace(min(x)-1,max(x)+1) if len(x)>0 else np.array([])
line, = ax.plot([],[], color='red')

# display formula for fit line
if len(x) > 0 and len(y) > 0:
    fit_text = plt.text(0.5, 0.1,'y = {:.2f}x + {:.2f}'.format(slope,intercept), ha='center', va='center', transform=plt.gca().transAxes)
else:
    fit_text = plt.text(0.5, 0.1,'', ha='center', va='center', transform=plt.gca().transAxes)

def add_point():
    global x,y,slope,x_fit,line
    # get entered x and y values for new data point
    x_val = float(x_entry.get())
    y_val = float(y_entry.get())
    # add new data point to chart
    ax.scatter(x_val,y_val,color='blue')
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

def animate(i):
    # Update the data of the fit line to create the animation
    line.set_data(x_fit[:i], slope*x_fit[:i] + intercept)
    return line,

# Create the animation for the fit line appearing
ani = FuncAnimation(fig, animate, frames=len(x_fit), interval=50, blit=True)

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
    # enable calculate button
    calc_button.config(state=tk.NORMAL)
    canvas.draw()

def reset():
    global x,y,slope,x_fit,line
    # clear all data points from chart and reset fit line
    ax.clear()
    x=np.array([])
    y=np.array([])
    slope=intercept=r_value=p_value=std_err=0
    x_fit=np.linspace(min(x)-1,max(x)+1) if len(x)>0 else np.array([])
    line=ax.plot([],[],color='red')[0]
    # update formula for fit line
    fit_text.set_text('')
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

root = tk.Tk()
root.wm_title("Linear Regression")

canvas = FigureCanvasTkAgg(fig,master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=0,column=0,rowspan=2,columnspan=4, sticky="nsew")

new_data_label = tk.Label(root, text="New Data Point")
new_data_label.grid(row=2, column=0, columnspan=2, sticky="nsew")

x_label = tk.Label(root, text="x:")
x_label.grid(row=3, column=0, sticky="nsew")
x_entry = tk.Entry(root)
x_entry.grid(row=3, column=1, sticky="nsew")

y_label = tk.Label(root, text="y:")
y_label.grid(row=4, column=0, sticky="nsew")
y_entry = tk.Entry(root)
y_entry.grid(row=4, column=1, sticky="nsew")

add_button = tk.Button(master=root, text="ADD", command=add_point)
add_button.grid(row=5, column=0)

analyze_button = tk.Button(master=root, text="Analyze", command=analyze)
analyze_button.grid(row=5, column=1)

reset_button = tk.Button(master=root, text="Reset", command=reset)
reset_button.grid(row=5, column=2)

calc_label = tk.Label(root, text="Calculate based on fit line:")
calc_label.grid(row=2, column=3)

calc_entry = tk.Entry(root)
calc_entry.grid(row=3, column=3)

calc_button = tk.Button(master=root, text="Calculate", command=submit)
calc_button.grid(row=5, column=3)

# Create the input field for the filename
filename_label = tk.Label(root, text="Filename:")
filename_label.grid(row=6, column=0)
filename_entry = tk.Entry(root)
filename_entry.grid(row=6, column=1)

# Create the save button
save_button = tk.Button(master=root, text="SAVE", command=save)
save_button.grid(row=6, column=2)

analyze_button.config(state=tk.DISABLED)
calc_button.config(state=tk.DISABLED)

def on_closing():
    root.quit()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

tk.mainloop()