#!/usr/bin/env python3

from tkinter import Tk, Canvas, mainloop
from math import cos, sin, pi, sqrt

from numpy import dot
# dot = lambda X, Y: [[sum(a*b for a, b in zip(X_row, Y_col)) for Y_col in zip(*Y)] for X_row in X]

master = Tk()

# constants
dimensions = {'width': 400, 'height': 400}
center = {k: v // 2 for k, v in dimensions.items()}

delta_alpha = - pi / 2**10
delta_beta = - pi / 2**8

# globals
alpha = 0
beta = 0

canvas = Canvas(master, **dimensions)
canvas.pack()


def transform(x, y, z, alpha, beta):
    transformation = [
        [cos(beta), 0, -sin(beta)],
        [-sin(alpha) * sin(beta), cos(alpha), -sin(alpha) * cos(beta)],
        [0, 0, 0]
    ]
    res = dot(transformation, [[x], [y], [z]])
    return res[0][0], res[1][0]


def draw2Dline(x, y, color):
    canvas.create_line(center['width'], center['height'], center['width'] + x, center['height'] - y, fill=color)


def draw3Dline(x, y, z, color='black'):
    x, y = transform(x, y, z, alpha, beta)
    draw2Dline(x, y, color)


def draw3Dpolygon(points, color='grey'):
    points = map(lambda p: transform(p[0], p[1], p[2], alpha, beta), points)  # transform points
    points = list(map(lambda p: (center['width'] + p[0], center['height'] - p[1]), points))  # center points
    canvas.create_polygon(points, outline=color, fill='')


def update_canvas():
    # update transformation
    global alpha, beta
    alpha += delta_alpha
    beta += delta_beta

    canvas.delete('all')

    size = 200

    draw3Dline(size, 0, 0, 'blue')  # x
    draw3Dline(0, size, 0, 'green')  # y
    draw3Dline(0, 0, size, 'red')  # z

    draw3Dline(-size, 0, 0, 'blue')  # -x
    draw3Dline(0, -size, 0, 'green')  # -y
    draw3Dline(0, 0, -size, 'red')  # -z

    A = (-size / 2, 0, size / 4)
    B = (size / 2, 0, size / 4)
    C = (0, 0, -size * sqrt(3) / 4)
    D = (0, size / 2, 0)
    draw3Dpolygon([A, B, C])
    draw3Dpolygon([A, B, D])
    draw3Dpolygon([B, C, D])
    draw3Dpolygon([A, C, D])

    master.after(20, update_canvas)


update_canvas()
mainloop()
