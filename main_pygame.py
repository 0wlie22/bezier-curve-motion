import pygame as pg
import platform  # get the os on current device
import pyautogui  # get the size of the screen
from scipy.special import factorial  # for factorials

pg.init()

oper_syst = platform.system()
WIDTH, HEIGHT = pyautogui.size()
if oper_syst == 'Darwin':
    HEIGHT -= 117
if oper_syst == 'Windows':
    HEIGHT -= 60

WIN = pg.display.set_mode((WIDTH, HEIGHT))

input_koord = [100, 100, 300, 500, 500, 100]
time = 0
for i in range(0, (len(input_koord) - 1)):
    input_koord[i] += 100
# input_koord[len(input_koord) - 1] -= 100
input_koord[len(input_koord) - 2] -= input_koord[0]
x = input_koord[0]
y = input_koord[1]


def grid():
    for j in range(100, 1001, 100):
        pg.draw.line(WIN, "#AAAAAA", (100, j), (1500, j))
    for i in range(100, 1501, 100):
        pg.draw.line(WIN, "#AAAAAA", (i, 100), (i, 1000))
    for k in range(0, len(input_koord) - 1, 2):
        pg.draw.ellipse(WIN, "#77C3EC", (input_koord[k] - 5, input_koord[k + 1] - 5, 10, 10))


def polinom(input_koord, t, x, y):
    n = int(len(input_koord) / 2)
    x_index = 0
    y_index = 1

    for i in range(1, n + 1):
        res = (factorial(n)) / ((factorial(i)) * factorial(n - i)) * (1 - t) ** (n - i) * t ** i
        x += input_koord[x_index] * res
        y += input_koord[y_index] * res
        x_index += 2
        y_index += 2
    pg.draw.ellipse(WIN, "#FFFFFF", (x, y, 2, 2))


def main(t, x, y):
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        WIN.fill("#222222")
        grid()

        while t <= 1.001:
            polinom(input_koord, t, x, y)
            t += 0.001
            pg.display.update()
    pg.quit()


main(time, x, y)
