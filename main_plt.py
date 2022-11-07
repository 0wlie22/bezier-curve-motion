import numpy as np
import matplotlib.pyplot as plt
import platform  # get the os on current device
import pyautogui  # get the size of the screen
from scipy.special import factorial  # for factorials

# oper_syst = platform.system()
# WIDTH, HEIGHT = pyautogui.size()
# if oper_syst == 'Darwin':
#     HEIGHT -= 117
# if oper_syst == 'Windows':
#     HEIGHT -= 60

img = np.ones((600, 600, 3))

koord_list = [100, 100, 100, 500, 300, 500, 400, 400, 550, 100]

koord_list_edited = koord_list.copy()
koord_list_edited[len(koord_list_edited) - 2] -= koord_list_edited[0]
koord_list_edited[len(koord_list_edited) - 1] -= koord_list_edited[1]


def polinom(koordinates, step):
    n = int(len(koordinates) / 2)

    while step <= 1:
        x_index = 0
        y_index = 1
        x = koordinates[0]
        y = koordinates[1]

        for i in range(1, n + 1):
            res = (factorial(n, exact=True)) / ((factorial(i, exact=True)) * factorial((n - i), exact=True))
            res = res * (1 - step) ** (n - i) * (step ** i)
            x += int(koordinates[x_index] * res)
            y += int(koordinates[y_index] * res)
            x_index += 2
            y_index += 2
        img[y, x] = (1, 0, 0)
        step += 0.001


polinom(koord_list_edited, 0)

plt.figure(figsize=(10, 8), dpi=100, facecolor='grey')
plt.grid(True, which='both', alpha=0.2, color='#222222', linestyle='--')
plt.imshow(img)
for k in range(0, len(koord_list) - 1, 2):
    if k != 0 and k != len(koord_list) - 2:
        dot_color = "c"
    else:
        dot_color = "b"
    plt.plot(koord_list[k], koord_list[k + 1], marker="o", color=dot_color)
    
plt.show()
