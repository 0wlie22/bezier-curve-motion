import pygame as pg
import platform  # get the os on current device
import pyautogui  # get the size of the screen
from scipy.special import binom  # for Bernstein polynomial

# get size of current screen and adapt to it's size
oper_syst = platform.system()
WIDTH, HEIGHT = pyautogui.size()
if oper_syst == 'Darwin':
    HEIGHT -= 117
if oper_syst == 'Windows':
    HEIGHT -= 60

WIN = pg.display.set_mode((WIDTH, HEIGHT))
# clock = pg.time.Clock()

koord_list = [100, 100, 400, 400, 900, 700, 1300, 100]
border: int = 100
line_koord_x = []
line_koord_y = []

colors: dict = {
    "fill": "#212122",
    "area": "#282828",
    "grid_main_line": "#8a8996",
    "grid_sub_line": "#4e4e59",
    "main_dot": "#b3667b",
    "middle_dot": "#dd95b4",
    "start_button": "#2e601c",
    "pause_button": "#2f560d",
    "moving_dot": "#fb4943",
    "line": "#f6e2c5",
    "text": "#000000"
}

# split coordinate list into separate x and y coordinate lists
for i in range(0, len(koord_list)):
    koord_list[i] += border
koord_x: list = koord_list[::2]
koord_y: list = koord_list[1::2]


def grid(indent: int):  # draw grid only
    WIN.fill(colors["fill"])
    pg.draw.rect(WIN, colors["area"], (100, 100, 1400, 900))

    draw_numbers()

    for j in range(100, 1001, 50):
        if j % 100 == 0:
            color = colors["grid_main_line"]
        else:
            color = colors["grid_sub_line"]
        pg.draw.line(WIN, color, (indent, j), (indent * 15, j))

    for k in range(100, 1501, 50):
        if k % 100 == 0:
            color = colors["grid_main_line"]
        else:
            color = colors["grid_sub_line"]
        pg.draw.line(WIN, color, (k, indent), (k, indent * 10))


def dots():  # draw dots on inputted coordinates
    for k in range(0, len(koord_list) - 1, 2):
        if k == 0 or k == len(koord_list) - 2:
            color = colors["main_dot"]
        else:
            color = colors["middle_dot"]
        pg.draw.circle(WIN, color, (koord_list[k], koord_list[k + 1]), 10)


def button(label: str, color: str):  # draw button
    pg.draw.rect(WIN, color, (1500 + (WIDTH - 1500 - 300) / 2, 100, 300, 100), 50, 15)
    blit_text(label, 1500 + (WIDTH - 1500 - 300) / 2 + 150, 150, 3, True, "xy")


def polynom(k_x: list, k_y: list, t: float) -> tuple[int, int]:  # count x and y coordinates
    n = int(len(k_x))
    x = y = 0

    for j in range(0, n):
        polynomial = binom(n - 1, j) * (1 - t) ** (n - 1 - j) * (t ** j)
        x += k_x[j] * polynomial
        y += k_y[j] * polynomial

    line_koord_x.append(x)
    line_koord_y.append(y)

    return x, y


def draw_line(list_x, list_y):  # draw the Bezier curve
    for index in range(0, len(list_x)):
        x = list_x[index]
        y = list_y[index]
        pg.draw.circle(WIN, colors["line"], (x, y), 1)


def draw_numbers():  # draw numbers on axes of a plot
    for step in range(100, 1600, 100):
        blit_text(str(step - 100), step, 95, 2, True, "x")
    for step in range(200, 1100, 100):
        blit_text(str(step - 100), 90, step, 2, True, "y")


def blit_text(string: str, x: int, y: int, size, change=False, change_coord=""):
    font1 = pg.font.SysFont("Arial", 20, bold=True)
    font2 = pg.font.SysFont("Arial", 15)
    font3 = pg.font.SysFont("Arial", 60, bold=True)

    font = font1 if size == 1 else (font2 if size == 2 else font3)
    text = font.render(string, True, colors["line"])

    if change:
        x -= text.get_width()
        y -= text.get_height()
        if "x" in change_coord:
            x += text.get_width()/2
        if "y" in change_coord:
            y += text.get_height()/2

    WIN.blit(text, (x, y))


def redraw_window(time: float, move_point: bool):
    grid(border)

    draw_line(line_koord_x, line_koord_y)

    if not move_point:
        text = "START"
        color = colors["start_button"]
    else:
        text = "PAUSE"
        color = colors["pause_button"]
    button(text, color)

    x, y = polynom(koord_x, koord_y, time)
    pg.draw.circle(WIN, colors["moving_dot"], (x, y), 10)

    blit_text("Press SPACE to start/pause", 1500 + (WIDTH - 1800) / 2, 240, 1)
    blit_text("Press ESC to quit", 1500 + (WIDTH - 1800) / 2, 270, 1)
    blit_text(str("x: " + str(int(x - 100))), 100, 1020, 2)
    blit_text("y: " + str(int(y - 100)), 100, 1040, 2)

    dots()


def main():
    run: bool = True
    move_point: bool = False
    time: float = 0
    t = 0

    # fill the list with line coordinate values
    while t <= 1.0:
        polynom(koord_x, koord_y, t)
        t += 0.0001

    pg.init()
    pg.display.set_caption("Bézier curve")

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    move_point = not move_point
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pos()
                if 1550 <= mouse[0] <= 1850 and 100 <= mouse[1] <= 200:
                    move_point = not move_point

        if time <= 1.0:
            redraw_window(time, move_point)
        else:
            move_point = False
            time = 0

        if move_point:
            time += 0.01

        pg.display.update()
        # clock.tick(1000)
    pg.quit()
    quit()


main()
