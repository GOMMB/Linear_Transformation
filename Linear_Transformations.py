from p5 import *

from copy import deepcopy

from tkinter import *

master = Tk()

e1 = Entry(master, width=9)
e2 = Entry(master, width=9)
e3 = Entry(master, width=9)
e4 = Entry(master, width=9)
T = Text(master, height=2, width=17)
T.pack()
T.grid(row=2, column=0, columnspan=2, rowspan=2)
T.insert(END, 'Input matrix then press enter.')
T.configure(state="disabled")

e1.grid(row=0, column=0)
e2.grid(row=0, column=1)
e3.grid(row=1, column=0)
e4.grid(row=1, column=1)

def on_closing2():
    on_closing(None)

def on_closing(event):
    global transformation
    transformation = [[float(e1.get()), float(e2.get())],
                      [float(e3.get()), float(e4.get())]]
    master.destroy()

master.bind("<Return>", on_closing)
master.protocol("WM_DELETE_WINDOW", on_closing2)
master.title("Input Matrix\nThen Press Enter")

master.mainloop( )

def matmult(m1, m2):
    if len(m1[0]) != len(m2):
        return None
    newm = []
    for x in range(len(m1)):
        row = []
        for y in range(len(m2[0])):
            cell = 0
            for i in range(len(m1[0])):
                cell += (m1[x][i] * m2[i][y])
            row.append(cell)
        newm.append(row)
    return newm


def reset():
    global starting, ending, grid_ending, grid_starting

    starting = [[-1000 for _ in range(-1000, 1001, 100)]
                + [x for x in range(-1000, 1001, 100)],
                [y for y in range(-1000, 1001, 100)]
                + [1000 for _ in range(-1000, 1001, 100)]]

    grid_starting = deepcopy(starting)

    ending = [[1000 for _ in range(-1000, 1001, 100)]
              + [x for x in range(-1000, 1001, 100)],
              [y for y in range(-1000, 1001, 100)]
              + [-1000 for _ in range(-1000, 1001, 100)]]

    grid_ending = deepcopy(ending)


def startagain(transformation):
    global after_starting, after_ending, dist_starting, dist_ending

    after_starting = matmult(transformation, starting)

    after_ending = matmult(transformation, ending)

    dist_starting = [(x[1] - x[0], y[1] - y[0]) for x, y in
                     zip(zip(starting[0], after_starting[0]), zip(starting[1], after_starting[1]))]

    dist_ending = [(x[1] - x[0], y[1] - y[0]) for x, y in
                   zip(zip(ending[0], after_ending[0]), zip(ending[1], after_ending[1]))]


def move(before, after, dist_):
    for i in range(len(before[0])):
        x1, y1, x2, y2 = before[0][i], before[1][i], after[0][i], after[1][i]
        X, Y = dist_[i]
        if dist((x1, y1), (x2, y2)) < dist((X, Y), (0, 0)) / 100:
            before[0][i] = x2
            before[1][i] = y2
            continue
        if x1 == x2 and y1 == y2: continue

        before[0][i] += X / 100

        before[1][i] += Y / 100


reset()

startagain(transformation)


def setup():
    global canvas
    size(1000, 1000)
    title('Matrix Trnsformations')


def draw():
    background(0)
    translate(width/2, height/2)
    scale(1, -1)

    move(starting, after_starting, dist_starting)
    move(ending, after_ending, dist_ending)

    stroke(0,255,255)
    for a, b in zip(zip(grid_starting[0], grid_ending[0]), zip(grid_starting[1], grid_ending[1])):
        line((a[0], b[0]), (a[1], b[1]))

    stroke(0,255,0)
    line((-width / 2, 0), (width / 2, 0))
    line((0, height / 2), (0, -height / 2))

    stroke(255)
    for x, y in zip(zip(starting[0], ending[0]), zip(starting[1], ending[1])):
        line((x[0], y[0]), (x[1], y[1]))


def mouse_pressed():
    if mouse_button == 'LEFT':
        startagain(transformation)
    elif mouse_button == 'RIGHT':
        reset()
        startagain(transformation)

run()
