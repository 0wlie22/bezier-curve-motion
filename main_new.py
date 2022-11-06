# import pygame as pg
import numpy as np
import matplotlib.pyplot as plt
import platform         #get the os on current device
import pyautogui        #get the size of the screen
import math             #for factorials

# pg.init()

oper_syst = platform.system()
WIDTH, HEIGHT = pyautogui.size()
if oper_syst == 'Darwin':
    HEIGHT -= 117
if oper_syst == 'Windows':
    HEIGHT -= 60

img = np.ones((1000, 1000, 3))
ax = plt.subplots()

input_koord = [100, 100, 500, 200, 500, 400, 500, 500, 500, 600, 100, 700]
input_koord[len(input_koord) - 2] -= input_koord[0]
input_koord[len(input_koord) - 1] -= input_koord[1]
time = 0
for k in range(0, len(input_koord) - 1, 2):
    circle = plt.Circle((input_koord[k] - 5, input_koord[k + 1] - 5, 10, 10), 5, color="#77C3EC")

def polinom(input_koord, t):
    n = int(len(input_koord)/2)
    
    
    while t <= 1.0:
        x_index = 0
        y_index = 1
        x = input_koord[0]
        y = input_koord[1]
        
        for i in range (1, n + 1):
            res = (math.factorial(n))/((math.factorial(i)) * math.factorial(n - i)) * ((1 - t) ** (n - i)) * (t ** i)
            x += int(input_koord[x_index] * res)
            y += int(input_koord[y_index] * res)
            x_index += 2
            y_index += 2
        img[y, x] = (1, 0, 0)
        t += 0.001

def main(t, x, y):
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
               run = False
        WIN.fill("#222222")
        
        while t <= 1: 
            t += 0.001
            pg.display.update()  
    pg.quit()

polinom(input_koord, time)

plt.figure(figsize=(10,8), dpi = 100, facecolor='grey')
plt.imshow(img)
plt.grid(True, which='both', alpha=0.2, color='#222222', linestyle = '--')
ax.add_patch(circle)
plt.show()