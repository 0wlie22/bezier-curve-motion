import pygame as pg
import platform  # get the os on current device
import pyautogui  # get the size of the screen
from pygame import RESIZABLE
from scipy.special import binom  # for brezenghem polynomial
import sys

pg.init()

stop = False
clock = pg.time.Clock()
mouse = pg.mouse.get_pos()

# get size of current screen and adapt to it's size
oper_syst = platform.system()
WIDTH, HEIGHT = pyautogui.size()
if oper_syst == 'Darwin':
    HEIGHT -= 117
if oper_syst == 'Windows':
    HEIGHT -= 60

# set window size
WIN = pg.display.set_mode((WIDTH, HEIGHT), RESIZABLE)

koord_list = [100, 100, 600, 300, 600, 600, 100, 800]
border: int = 100

for i in range(0, len(koord_list)):
    koord_list[i] += border
koord_x = koord_list[::2]
koord_y = koord_list[1::2]


def grid(indent):
    WIN.fill("#222222")
    for j in range(100, 1001, 100):
        pg.draw.line(WIN, "#AAAAAA", (indent, j), (indent * 15, j))
    for k in range(100, 1501, 100):
        pg.draw.line(WIN, "#AAAAAA", (k, indent), (k, indent * 10))


def dots():
    for k in range(0, len(koord_list) - 1, 2):
        if k != 0 and k != len(koord_list) - 2:
            color = "light blue"
        else:
            color = "light green"
        pg.draw.ellipse(WIN, color, (koord_list[k] - 8, koord_list[k + 1] - 8, 16, 16))


def button(text_color, button_color):
    font = pg.font.SysFont("Georgia", 50)
    text = font.render("START", True, text_color)

    pg.draw.rect(WIN, button_color, [1550, 100, 300, 100])
    WIN.blit(text, (1550 + text.get_width()/2, 100 + text.get_height()/2))


def polinom(k_x, k_y, t):
    n = int(len(k_x))
    x = y = 0

    for j in range(0, n):
        #     res = (factorial(n, exact=True)) / ((factorial(i, exact=True)) * factorial((n - i), exact=True))
        bern_polinom = binom(n - 1, j) * (1 - t) ** (n - 1 - j) * (t ** j)
        x += k_x[j] * bern_polinom
        y += k_y[j] * bern_polinom
    pg.draw.rect(WIN, "white", (x, y, 2, 2))
    dots()


def redraw_window(k_x, k_y):
    global stop
    t = 0
    grid(border)

    pg.draw.rect(WIN, "white", (k_x[0], k_y[0], 2, 2))

    while t <= 1.0:
        pg.display.update()
        polinom(koord_x, koord_y, t)
        t += 0.001
        clock.tick(1000)


def main():
    global stop
    run = True
    stop = False
    while run:
        grid(border)
        button("black", "grey")
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            # if event.type == pg.MOUSEBUTTONDOWN:
        if 1550 <= mouse[0] <= 1850 and 100 <= mouse[1] <= 200:
            print("true")
            redraw_window(koord_x, koord_y)
    pg.quit()
    quit()


main()
