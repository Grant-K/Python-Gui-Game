import Tkinter
import math
import random
root = Tkinter.Tk()

canvas = Tkinter.Canvas(root, width=600, height=600, background='#FFFFFF')
canvas.grid(row=0, rowspan=1, column=1)
x = random.randint(0,600)
y = 300
r = 10
rx1 = 250
ry1 = 575
rx2 = 350
ry2 = 590
speed = 3      
direction = 1
circle_item = canvas.create_oval(x-r, y-r, x+r, y+r, outline='#000000', fill='#00FFFF')
rectangle_item = canvas.create_rectangle(rx1,ry1,rx2,ry2, outline='#000000', fill='#00FFFF')

def main():
    # Get the slider data and create x- and y-components of velocity
    velocity_x = speed * math.cos(direction) # adj = hyp*cos()
    velocity_y = speed * math.sin(direction) # opp = hyp*sin()
    # Change the canvas item's coordinates
    canvas.move(circle_item, velocity_x, velocity_y)
    
    # Get the new coordinates and act accordingly if ball is at an edge
    x1, y1, x2, y2 = canvas.coords(circle_item)
    global direction
    # If crossing left or right of canvas
    if x2>canvas.winfo_width() or x1<0: 
        direction = math.pi - direction # Reverse the x-component of velocity
    # If crossing top or bottom of canvas
    if y1<0: 
        direction = -1 * direction # Reverse the y-component of velocity
    
    # Create an event in 1 msec that will be handled by animate(),
    # causing recursion      
    if circle_item in canvas.find_overlapping(rx1,ry1-10,rx2,ry2):
        direction = -1 * direction
    canvas.after(1, main)
# Call function directly to start the recursion
main()

root.mainloop()