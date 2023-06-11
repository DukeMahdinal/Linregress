import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import TextBox

# sample data
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 3.5, 4.2, 5.1, 6])

# linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
ax.scatter(x,y)

# extend fit line beyond given data points
x_fit = np.linspace(min(x)-1,max(x)+1)
line, = ax.plot(x_fit, slope*x_fit + intercept, color='red')

def update(num):
    if num < len(x):
        line.set_data(x[:num], (slope*x + intercept)[:num])
    else:
        line.set_data(x_fit, slope*x_fit + intercept)
    return line,

ani = FuncAnimation(fig, update, frames=range(len(x)+2), interval=500, repeat= False)

# display formula for fit line
fit_text = plt.text(0.5, 0.1,'y = {:.2f}x + {:.2f}'.format(slope,intercept), ha='center', va='center', transform=plt.gca().transAxes)

# create input field for entering x value
axbox = plt.axes([0.1, 0.05, 0.8, 0.075])
text_box = TextBox(axbox, 'Enter x value: ')

def submit(text):
    global x,y,slope,intercept,x_fit
    # calculate y value based on fit line
    x_val = float(text)
    y_val = slope*x_val + intercept
    # display yellow dot on chart at calculated location
    ax.scatter(x_val,y_val,color='yellow')
    # display coordinates above yellow dot
    ax.text(x_val,y_val,'({:.2f},{:.2f})'.format(x_val,y_val))
    # recalculate fit line to pass through all yellow dots
    x = np.append(x,x_val)
    y = np.append(y,y_val)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    x_fit = np.linspace(min(x)-1,max(x)+1)
    line.set_data(x_fit,slope*x_fit+intercept)
    # update formula for fit line
    fit_text.set_text('y = {:.2f}x + {:.2f}'.format(slope,intercept))
    plt.draw()

text_box.on_submit(submit)

plt.show()