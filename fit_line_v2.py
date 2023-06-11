import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
    canvas.draw()

def analyze():
    global x,y,slope,x_fit,line
    # recalculate fit line to pass through all blue dots (data points)
    if len(x) > 0 and len(y) > 0:
        slope, intercept,r_value,p_value,std_err=stats.linregress(x,y)
        x_fit=np.linspace(min(x)-1,max(x)+1)
        line.set_data(x_fit,slope*x_fit+intercept)
        # update formula for fit line
        fit_text.set_text('y={:.2f}x+{:.2f}'.format(slope,intercept))
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
 canvas.draw()

def submit():
 global x,y,slope,intercept,x_fit
 # calculate y value based on fit line
 x_val = float(calc_entry.get())
 y_val = slope*x_val + intercept
 # display yellow dot on chart at calculated location
 ax.scatter(x_val,y_val,color='yellow')
 # display coordinates above yellow dot
 ax.text(x_val,y_val,'({:.2f},{:.2f})'.format(x_val,y_val))
 canvas.draw()

root = tk.Tk()
root.wm_title("Linear Regression")

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=0,column=0,columnspan=4)

new_data_label = tk.Label(root,text="New Data Point")
new_data_label.grid(row=1,column=0,columnspan=2)

x_label = tk.Label(root,text="x:")
x_label.grid(row=2,column=0)
x_entry = tk.Entry(root)
x_entry.grid(row=2,column=1)

y_label = tk.Label(root,text="y:")
y_label.grid(row=3,column=0)
y_entry = tk.Entry(root)
y_entry.grid(row=3,column=1)

add_button = tk.Button(master=root,text="ADD",command=add_point)
add_button.grid(row=4,column=0,columnspan=2)

analyze_button=tk.Button(master=root,text="Analyze",command=analyze)
analyze_button.grid(row=5,column=0,columnspan=2)

reset_button=tk.Button(master=root,text="Reset",command=reset)
reset_button.grid(row=6,column=0,columnspan=2)

calc_label=tk.Label(root,text="Calculate based on fit line:")
calc_label.grid(row=1,column=2,columnspan=2)

calc_entry=tk.Entry(root)
calc_entry.grid(row=2,column=2,columnspan=2)

calc_button=tk.Button(master=root,text="Calculate",command=submit)
calc_button.grid(row=3,column=2,columnspan=2)

tk.mainloop()