import Tkinter
import math
import random
from time import sleep
#from apscheduler.schedulers.background import BackgroundScheduler
#sched = BackgroundScheduler()
root = Tkinter.Tk()
canvas = Tkinter.Canvas(root, width=600, height=600, background='#FFFFFF')
canvas.grid(row=0, rowspan=1, column=1)
x = random.randint(0,600)
y = 300
r = 10
rxs1 = 260
rys1 = 575
rxs2 = 340
rys2 = 590
speed = 5  
score = 0
started = 0
msPassed = 0
direction = random.uniform((math.pi/6),((5*math.pi)/6))
while(direction > 1.74533 and direction < 1.39626):
    direction = random.uniform((math.pi/6),((5*math.pi)/6))
circle_item = canvas.create_oval(x-r, y-r, x+r, y+r, outline='#000000', fill='#00FFFF')
rectangle_item = canvas.create_rectangle(rxs1,rys1,rxs2,rys2, outline='#000000', fill='#00FFFF')
rectangle_items = []
score_item = canvas.create_text(550, 580, text = "Score = 0")
#sched.start()
def start(event):
    global started
    if(started == 0):
        genBlocks()
        #sched.add_job(genBlocks, 'interval', seconds=2)
        main()
        started = 1
def genBlocks():
        x3 = random.randint(-30,0)
        x4 = x3+30
        y3 = 0
        y4 = 10
        global rectangle_items
        if(len(rectangle_items) > 0):
            for index in range (0, len(rectangle_items)):
                canvas.move(rectangle_items[(len(rectangle_items)-1) - index], 0, 13) 
                #sleep(.005)
            rectangle_items.append(canvas.create_rectangle(x3,y3,x4,y4, outline='#000000', fill='#00FFFF'))
            while(x4 < 600):
                xDist = random.randint(30,100)
                rect=canvas.create_rectangle(x4+3,y3,x4+xDist,y4, outline='#000000', fill='#00FFFF')
                rectangle_items.append(rect)
                x3, y3, x4, y4 = canvas.coords(rectangle_items[len(rectangle_items)-1])
        else:
            for num in range(0,4):
                rectangle_items.append(canvas.create_rectangle(x3,y3,x4,y4, outline='#000000', fill='#00FFFF'))
                x3, y3, x4, y4 = canvas.coords(rectangle_items[len(rectangle_items)-1])
                while(x4 < 600):
                    xDist = random.randint(30,100)
                    rect=canvas.create_rectangle(x4+3,y3,x4+xDist,y4, outline='#000000', fill='#00FFFF')
                    rectangle_items.append(rect)
                    x3, y3, x4, y4 = canvas.coords(rectangle_items[len(rectangle_items)-1])
                
                y3 = y4+3
                y4 = y3+10
                x3 = 0
                x4 = random.randint(30,100)
            canvas.update_idletasks()
def main():
    # Get the slider data and create x- and y-components of velocity
    global direction
    global rectangle_items
    global score
    global msPassed
    msPassed += 5
    if(msPassed%1000 == 0):
        print(msPassed)
    if((msPassed/1000) >= 2 and (msPassed%2000) == 0):
        genBlocks()
    velocity_x = speed * math.cos(direction) # adj = hyp*cos()
    velocity_y = speed * math.sin(direction) # opp = hyp*sin()
    # Change the canvas item's coordinates
    canvas.move(circle_item, velocity_x, velocity_y)
    # Get the new coordinates and act accordingly if ball is at an edge
    x1, y1, x2, y2 = canvas.coords(circle_item)
    
    # If crossing left or right of canvas
    if x2>canvas.winfo_width() or x1<0: 
        direction = math.pi - direction # Reverse the x-component of velocity
        velocity_x = speed * math.cos(direction) # adj = hyp*cos()
        velocity_y = speed * math.sin(direction) # opp = hyp*sin()
        canvas.move(circle_item, velocity_x*2, velocity_y*2)
    # If crossing top or bottom of canvas
    if y1<0: 
        velocity_x = speed * math.cos(direction) # adj = hyp*cos()
        velocity_y = speed * math.sin(direction) # opp = hyp*sin()
        canvas.move(circle_item, velocity_x*2, velocity_y*2)
        direction = -1 * direction # Reverse the y-component of velocity
    # Create an event in 1 msec that will be handled by animate(),
    # causing recursion      
    rx1, ry1, rx2, ry2 = canvas.coords(rectangle_item)
    if circle_item in canvas.find_overlapping(rx1,ry1,rx2,ry2):
        direction = direction * -1
        for n in range(1, 5):
            velocity_x = speed * math.cos(direction)
            velocity_y = speed * math.sin(direction)
            canvas.move(circle_item, velocity_x*2, velocity_y*2)
            sleep(.0075)
    pointerxpos = root.winfo_pointerx() - root.winfo_rootx()
    xdistance = math.sqrt((rx1 - canvas.canvasx(pointerxpos,gridspacing = None))**2)
    if(rx1 > canvas.canvasx(pointerxpos,gridspacing = None)):
        xdistance = xdistance * -1
    if((rx1 + (xdistance-40)) < 5):
        canvas.move(rectangle_item, 5 - rx1, 0)
    elif((rx2 + (xdistance-40)) > 600):
        canvas.move(rectangle_item, 600 - rx2, 0)
    else:
        canvas.move(rectangle_item, xdistance-40, 0)
    global rectangle_items
    if(len(rectangle_items) < 0):
            genBlocks()
    else:
        for index in range(0, (len(rectangle_items))):
            if(index < len(rectangle_items)):
                x3, y3, x4, y4 = canvas.coords(rectangle_items[index])
                if(circle_item in canvas.find_overlapping(x3, y3, x4, y4)):
                    canvas.delete(rectangle_items[index])
                    del rectangle_items[index]
                    direction = direction * -1
                    score = (int)(score + (x4 - x3))
                    canvas.itemconfig(score_item, text = "Score = " + str(score))
                    
    canvas.after(5, main)
# Call function directly to start the recursion
canvas.bind("<Button-1>", start)
root.mainloop()

#sched.shutdown()