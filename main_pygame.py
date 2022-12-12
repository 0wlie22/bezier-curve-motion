import pygame as pg
from pygame import FULLSCREEN

import pyautogui  # get the size of the screen
from scipy.special import binom  # for Bernstein polynomial

# 1366x768 -> 1920x1200
WIDTH, HEIGHT = pyautogui.size()
WIN = pg.display.set_mode((WIDTH, HEIGHT), FULLSCREEN)
K: float = WIDTH / 1920

# clock = pg.time.Clock()

koord_list = [100, 100, 800, 300, 700, 600, 500, 800]
BLOCK: int = int((100 * K) - (100 * K) % 2)

line_koord_x: list[int] = []
line_koord_y: list[int] = []

# split coordinate list into separate x and y coordinate lists
koord_x: list = koord_list[::2]
koord_y: list = koord_list[1::2]

colors: dict = {
    "fill": "#212122",
    "rect": "#3F3D43",
    "header": "#151515",
    "area": "#282828",
    "grid_main_line": "#8a8996",
    "grid_sub_line": "#4e4e59",
    "main_dot": "#3e702c",
    "middle_dot": "#6f964d",
    "start_button": "#2e601c",
    "pause_button": "#2f560d",
    "moving_dot": "#fb4943",
    "line": "#f6e2c5",
    "text": "#000000",
    "error": "#FF0000"
}


def grid():
    WIN.fill(colors["fill"])

    end_x = 15 * BLOCK
    end_y = 10 * BLOCK

    pg.draw.rect(WIN, colors["area"], (BLOCK, BLOCK, end_x - BLOCK, end_y - BLOCK))

    draw_numbers()
    count_x = 0
    count_y = 0

    for j in range(BLOCK, 10 * BLOCK + 1, int(BLOCK / 2)):  # horizontal lines
        if count_x % 2 == 0:
            color = colors["grid_main_line"]
        else:
            color = colors["grid_sub_line"]
        pg.draw.line(WIN, color, (BLOCK, j), (end_x, j))
        count_x += 1

    for m in range(BLOCK, 15 * BLOCK + 1, int(BLOCK / 2)):  # vertical lines
        if count_y % 2 == 0:
            color = colors["grid_main_line"]
        else:
            color = colors["grid_sub_line"]
        pg.draw.line(WIN, color, (m, BLOCK), (m, end_y))
        count_y += 1


def dots():  # draw dots on inputted coordinates
    for k in range(0, len(koord_list) - 1, 2):
        if k == 0 or k == len(koord_list) - 2:
            color = colors["main_dot"]
        else:
            color = colors["middle_dot"]
        pg.draw.circle(WIN, color, (koord_list[k] / 100 * BLOCK + BLOCK, koord_list[k + 1] / 100 * BLOCK + BLOCK),
                       10 * K)


def draw_line(list_x, list_y):  # draw the Bezier curve
    for index in range(0, len(list_x)):
        x = list_x[index] / 100 * BLOCK + BLOCK
        y = list_y[index] / 100 * BLOCK + BLOCK
        pg.draw.circle(WIN, colors["line"], (x, y), 1)


def button(label: str, color: str, x: int, y: int, width, height, size):  # draw button
    pg.draw.rect(WIN, color, (x, y, width, height), int(height / 2), 10)
    blit_text(label, x + int(width / 2), y + int(height / 2), size, True, True, "xy")


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


def draw_numbers():  # draw numbers on axes of a plot
    count = 0
    for step in range(BLOCK, 16 * BLOCK, BLOCK):
        blit_text(str(count), step, BLOCK - int(5 * K), 15, False, True, "x")
        count += 100
    count = 100
    for step in range(2 * BLOCK, 11 * BLOCK, BLOCK):
        blit_text(str(count), BLOCK - int(10 * K), step, 15, False, True, "y")
        count += 100


def blit_text(string: str, x: int, y: int, size: int, bold=False, change=False, change_coord="", text_color=""):
    font = pg.font.SysFont("Arial", int(size * K), bold=True) if bold else pg.font.SysFont("Arial", int(size * K))
    if text_color == "red":
        color = colors["error"]
    else:
        color = colors["line"]

    text = font.render(string, True, color)

    if change:
        x -= text.get_width()
        y -= text.get_height()
        if "x" in change_coord:
            x += text.get_width() / 2
        if "y" in change_coord:
            y += text.get_height() / 2

    WIN.blit(text, (x, y))


def main_menu(points):
    WIN.fill(colors["fill"])

    # title
    blit_text("Beziér algorithm", WIDTH / 2, BLOCK, 60, True, True, "x")
    blit_text("for moving 2D objects", WIDTH / 2, int(160 * K), 50, False, True, "x")

    # main rect
    pg.draw.rect(WIN, colors["rect"], (BLOCK, 2 * BLOCK, (WIDTH - BLOCK) / 5 * 3, HEIGHT - 3 * BLOCK),
                 int((WIDTH - 2 * BLOCK) / 5 * 3), 10)
    pg.draw.rect(WIN, colors["header"], (BLOCK, 2 * BLOCK, (WIDTH - BLOCK) / 5 * 3, int((HEIGHT - 4 * BLOCK) / 10)), 0,
                 0, 10, 10)

    button("START", colors["start_button"], 2 * BLOCK + (WIDTH - 2 * BLOCK) / 5 * 3 + 50, 2 * BLOCK,
           WIDTH - (WIDTH - 2 * BLOCK) / 5 * 3 - 3 * BLOCK - 100, (HEIGHT - 4 * BLOCK) / 4, 100)

    blit_text("Press ESC to quit", 2 * BLOCK + (WIDTH - 2 * BLOCK) / 5 * 3 + 50
              + (WIDTH - (WIDTH - 2 * BLOCK) / 5 * 3 - 3 * BLOCK - 100) / 2,
              2 * BLOCK + (HEIGHT - 4 * BLOCK) / 4 + int(40 * K), 20, True, True, "x")
    blit_text("Point coordinates:", int(1.2 * BLOCK), int(2.2 * BLOCK), 40)
    blit_text("+", 0.5 * BLOCK + (WIDTH - BLOCK) / 5 * 3, 2 * BLOCK, 60)

    for i in range(1, points + 1):
        pg.draw.line(WIN, colors["header"], (BLOCK ,2 * BLOCK + BLOCK * i + int((HEIGHT - 4 * BLOCK) / 10)),
                     (BLOCK + (WIDTH - BLOCK) / 5 * 3 - 1, 2 * BLOCK + BLOCK * i + int((HEIGHT - 4 * BLOCK) / 10)), 2)
        blit_text(str(i), int(1.2 * BLOCK), 2 * BLOCK + i * BLOCK, 30, bold=True)
        # pg.draw.rect(WIN, "#FFFFFF", ())


def window(time: float, move_point: bool):
    grid()

    draw_line(line_koord_x, line_koord_y)

    # start/pause button
    if not move_point:
        text = "START"
        color = colors["start_button"]
    else:
        text = "PAUSE"
        color = colors["pause_button"]
    button(text, color, 15 * BLOCK + (WIDTH - 15 * BLOCK - BLOCK * 3) / 2, BLOCK, 3 * BLOCK, BLOCK, 60)
    button("back to menu", "#0f360d", 15 * BLOCK + (WIDTH - 15 * BLOCK - BLOCK * 3) / 2,
           2 * BLOCK + int(25 * K), 3 * BLOCK, BLOCK, 40)

    dots()

    x, y = polynom(koord_x, koord_y, time)
    pg.draw.circle(WIN, colors["moving_dot"], (x / 100 * BLOCK + BLOCK, y / 100 * BLOCK + BLOCK), int(10 * K))

    # instructions
    blit_text("Press SPACE to start/pause", 15 * BLOCK + (WIDTH - 18 * BLOCK) / 2, 9 * BLOCK, 20, True)
    blit_text("Press ESC to quit", 15 * BLOCK + (WIDTH - 18 * BLOCK) / 2, 9 * BLOCK + int(30 * K), 20, True)

    # show dot coordinates
    # blit_text(str("x: " + str(int(x))), BLOCK, 10 * BLOCK + 20, 15)
    # blit_text("y: " + str(int(y)), BLOCK, 10 * BLOCK + 40, 15)


def main():
    run: bool = True
    time: float = 0
    t: float = 0
    menu: bool = True
    move_point: bool = False
    max_points: bool = False
    points: int = 2

    # fill the list with line coordinate values
    while t <= 1:
        polynom(koord_x, koord_y, t)
        t += 0.0001

    pg.init()
    pg.display.set_caption("Beziér curve")

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
                    if time > 1:
                        time = 0
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pos()
                if menu:
                    if 2 * BLOCK + (WIDTH - 2 * BLOCK) / 5 * 3 + 50 <= mouse[0] <= \
                            (2 * BLOCK + (WIDTH - 2 * BLOCK) / 5 * 3 + 50) + \
                            (WIDTH - (WIDTH - 2 * BLOCK) / 5 * 3 - 3 * BLOCK - 100) and 2 * BLOCK <= mouse[1] <= \
                            (7 * BLOCK) + (int((HEIGHT - 4 * BLOCK) / 4)):
                        menu = False
                    if BLOCK <= mouse[1] <= 2 * BLOCK + int((HEIGHT - 4 * BLOCK) / 10) and BLOCK + \
                            (WIDTH - BLOCK) / 5 * 3 - int((HEIGHT - 4 * BLOCK) / 10) <= mouse[0] <= \
                            BLOCK + (WIDTH - BLOCK) / 5 * 3:
                        if points < 7:
                            points += 1
                            max_points = False
                        else:
                            max_points = True
                else:
                    if 15 * BLOCK + (WIDTH - 15 * BLOCK - BLOCK * 3) / 2 <= mouse[0] <= \
                            (15 * BLOCK + (WIDTH - 15 * BLOCK - BLOCK * 3) / 2) + 3 * BLOCK and \
                            2 * BLOCK + int(25 * K) <= mouse[1] <= 2 * BLOCK + int(25 * K) + BLOCK:
                        menu = True
                    if int(1550 * K) <= mouse[0] <= int(1850 * K) and BLOCK <= mouse[1] <= 2 * BLOCK:
                        move_point = not move_point
                        if time > 1:
                            time = 0

        if time > 1:
            move_point = False

        if menu:
            main_menu(points)
        else:
            window(time, move_point)
        if move_point:
            time += 0.01

        if max_points:
            blit_text("maximum 7 points", int(1.2 * BLOCK), int(10.2 * BLOCK), 40, text_color="red")

        pg.display.update()
    pg.quit()
    quit()


if __name__ == "__main__":
    main()
