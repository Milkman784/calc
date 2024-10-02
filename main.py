import math
import operator
import threading
from time import *

import pygame

pygame.init()
pygame.display.set_caption("Calculator!")
icon = pygame.image.load("icon_calc.png")
pygame.display.set_icon(icon)
pygame.font.init()
screen = pygame.display.set_mode((670, 670))
running = True
font1 = pygame.font.SysFont("Comic Sans MS", 30)
calc = []
current_ans = None

cooldowns = {
    "Ans": False,
    "Del": False,
    "Clear": False,
    "Sin": False,
    "Cos": False,
    "Tan": False,
    "(": False,
    ")": False,
    "Pi": False,
    "Sqrt": False,
    "^": False,
    "-": False,
    "7": False,
    "8": False,
    "9": False,
    "4": False,
    "5": False,
    "6": False,
    "3": False,
    "2": False,
    "1": False,
    ".": False,
    "0": False,
    "=": False,
    "+": False,
    "/": False,
    "*": False,
}

def start_cooldown(button_name):
    cooldowns[button_name] = True
    threading.Thread(target=cooldown_reset, args=(button_name,)).start()

def cooldown_reset(button_name):
    sleep(0.5)
    cooldowns[button_name] = False

def button_press(button_name, rect):
    global calc
    if pygame.mouse.get_pressed()[0] and rect.collidepoint(pygame.mouse.get_pos()) and not cooldowns[button_name]:
        if len(calc) != 0 and button_name in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."} and (calc[-1].isdigit() or "." in calc[-1]):
            calc[-1] = calc[-1] + button_name
        elif button_name in {"+", "-", "*", "/"} and len(calc) == 0:
            if current_ans is not None:
                calc.append(current_ans)
                calc.append(button_name)
        elif button_name in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".",}:
            calc.append(button_name)
        elif button_name in {"+", "-", "*", "/"} and calc[-1] not in {"+", "-", "*", "/", "."}:
            calc.append(button_name)
        elif button_name == "=" and calc[-1] not in {"+", "-", "*", "/", "."}:
            to_float()
        elif button_name == "Clear":
            while len(calc) != 0:
                calc.pop()
        elif button_name == "Ans":
            if current_ans is not None and try_float(current_ans):
                calc.append(current_ans)
        elif button_name == "Del":
            if len(calc) != 0:
                if len(calc[-1]) > 1:
                    temp_del1 = calc[-1]
                    temp_del2 = temp_del1[:-1]
                    calc[-1] = temp_del2
                elif len(calc[-1]) == 1:
                    calc.pop()
        elif button_name == "Pi":
            calc.append("π")
        start_cooldown(button_name)

def to_float():
    i = 0
    while i < len(calc):
        if try_float(calc[i]):
            calc[i] = float(calc[i])
        i = i + 1
    operate()


def operate():
    global current_ans
    i = 0
    while i < len(calc):
        if calc[i] == "π":
            calc[i] = math.pi
        i += 1

    i = 0

    if calc[0] == 999.0:
        calc[0] = "TestError"



    while i < len(calc):
        if calc[i] == "*" or calc[i] == "/":
            if calc[i] == "*":
                calc[i - 1] = operator.mul(calc[i - 1], calc[i + 1])
                calc.pop(i + 1)
                calc.pop(i)
                i -= 1
            elif calc[i] == "/":
                calc[i - 1] = operator.truediv(calc[i - 1], calc[i + 1])
                calc.pop(i + 1)
                calc.pop(i)
                i -= 1
        else:
            i += 1

    i = 0

    while i < len(calc):
        if calc[i] == "+" or calc[i] == "-":
            if calc[i] == "+":
                calc[i - 1] = operator.add(calc[i - 1], calc[i + 1])
                calc.pop(i + 1)
                calc.pop(i)
                i -= 1
            elif calc[i] == "-":
                calc[i - 1] = operator.sub(calc[i - 1], calc[i + 1])
                calc.pop(i + 1)
                calc.pop(i)
                i -= 1
        else:
            i = i + 1


    if len(calc) != 0 and try_float(*calc):
        current_ans = str(round(*calc, 9))
    elif len(calc) != 0:
        current_ans = str(*calc)

    while len(calc) != 0:
        calc.pop()

def try_float(to_check):
    try:
        float(to_check)
        return True
    except ValueError:
        return False

def draw_equation():
    screen.blit(font1.render(str(calc), False, (0, 0, 0)), (35, 35))
    screen.blit(font1.render(current_ans, False, (0, 0, 0)), (35, 135))

def draw_widgets():

    pygame.draw.rect(screen, (200, 255, 255), pygame.Rect(10, 10, 650, 100))

    pygame.draw.rect(screen, (200, 255, 255), pygame.Rect(10, 120, 320, 100))

    ans_rect = pygame.Rect(10, 230, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), ans_rect)
    screen.blit(font1.render("Ans", False, (0, 0, 0)), (35, 265))
    button_press("Ans", ans_rect)

    del_rect = pygame.Rect(120, 230, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), del_rect)
    screen.blit(font1.render("Del", False, (0, 0, 0)), (145, 265))
    button_press("Del", del_rect)

    clear_rect = pygame.Rect(230, 230, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), clear_rect)
    screen.blit(font1.render("Clear", False, (0, 0, 0)), (250, 265))
    button_press("Clear", clear_rect)

    sin_rect = pygame.Rect(10, 340, 100, 100)
    pygame.draw.rect(screen, (255, 100, 100), sin_rect)
    screen.blit(font1.render("Sin", False, (0, 0, 0)), (35, 375))
    button_press("Sin", sin_rect)

    cos_rect = pygame.Rect(120, 340, 100, 100)
    pygame.draw.rect(screen, (255, 100, 100), cos_rect)
    screen.blit(font1.render("Cos", False, (0, 0, 0)), (145, 375))
    button_press("Cos", cos_rect)

    tan_rect = pygame.Rect(230, 340, 100, 100)
    pygame.draw.rect(screen, (255, 100, 100), tan_rect)
    screen.blit(font1.render("Tan", False, (0, 0, 0)), (255, 375))
    button_press("Tan", tan_rect)

    left_parentheses_rect = pygame.Rect(10, 450, 100, 100)
    pygame.draw.rect(screen, (255, 100, 100), left_parentheses_rect)
    screen.blit(font1.render("(", False, (0, 0, 0)), (45, 485))
    button_press("(", left_parentheses_rect)

    right_parentheses_rect = pygame.Rect(120, 450, 100, 100)
    pygame.draw.rect(screen, (255, 100, 100), right_parentheses_rect)
    screen.blit(font1.render(")", False, (0, 0, 0)), (155, 485))
    button_press(")", right_parentheses_rect)

    pi_rect = pygame.Rect(230, 450, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), pi_rect)
    screen.blit(font1.render("Pi", False, (0, 0, 0)), (255, 485))
    button_press("Pi", pi_rect)

    sqrt_rect = pygame.Rect(10, 560, 100, 100)
    pygame.draw.rect(screen, (255, 100, 100), sqrt_rect)
    screen.blit(font1.render("Sqrt", False, (0, 0, 0)), (25, 595))
    button_press("Sqrt", sqrt_rect)

    pow_rect = pygame.Rect(120, 560, 100, 100)
    pygame.draw.rect(screen, (255, 100, 100), pow_rect)
    screen.blit(font1.render("^", False, (0, 0, 0)), (155, 595))
    button_press("^", pow_rect)

    minus_rect = pygame.Rect(230, 560, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), minus_rect)
    screen.blit(font1.render("-", False, (0, 0, 0)), (265, 595))
    button_press("-", minus_rect)

    seven_rect = pygame.Rect(340, 120, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), seven_rect)
    screen.blit(font1.render("7", False, (0, 0, 0)), (375, 155))
    button_press("7", seven_rect)

    eight_rect = pygame.Rect(450, 120, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), eight_rect)
    screen.blit(font1.render("8", False, (0, 0, 0)), (485, 155))
    button_press("8", eight_rect)

    nine_rect = pygame.Rect(560, 120, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), nine_rect)
    screen.blit(font1.render("9", False, (0, 0, 0)), (595, 155))
    button_press("9", nine_rect)

    four_rect = pygame.Rect(340, 230, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), four_rect)
    screen.blit(font1.render("4", False, (0, 0, 0)), (375, 265))
    button_press("4", four_rect)

    five_rect = pygame.Rect(450, 230, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), five_rect)
    screen.blit(font1.render("5", False, (0, 0, 0)), (485, 265))
    button_press("5", five_rect)

    six_rect = pygame.Rect(560, 230, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), six_rect)
    screen.blit(font1.render("6", False, (0, 0, 0)), (595, 265))
    button_press("6", six_rect)

    three_rect = pygame.Rect(340, 340, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), three_rect)
    screen.blit(font1.render("3", False, (0, 0, 0)), (375, 375))
    button_press("3", three_rect)

    two_rect = pygame.Rect(450, 340, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), two_rect)
    screen.blit(font1.render("2", False, (0, 0, 0)), (485, 375))
    button_press("2", two_rect)

    one_rect = pygame.Rect(560, 340, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), one_rect)
    screen.blit(font1.render("1", False, (0, 0, 0)), (595, 375))
    button_press("1", one_rect)

    dot_rect = pygame.Rect(340, 450, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), dot_rect)
    screen.blit(font1.render(".", False, (0, 0, 0)), (375, 485))
    button_press(".", dot_rect)

    zero_rect = pygame.Rect(450, 450, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), zero_rect)
    screen.blit(font1.render("0", False, (0, 0, 0)), (485, 485))
    button_press("0", zero_rect)

    equal_rect = pygame.Rect(560, 450, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), equal_rect)
    screen.blit(font1.render("=", False, (0, 0, 0)), (595, 485))
    button_press("=", equal_rect)

    plus_rect = pygame.Rect(340, 560, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), plus_rect)
    screen.blit(font1.render("+", False, (0, 0, 0)), (375, 595))
    button_press("+", plus_rect)

    divide_rect = pygame.Rect(450, 560, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), divide_rect)
    screen.blit(font1.render("/", False, (0, 0, 0)), (485, 595))
    button_press("/", divide_rect)

    multiply_rect = pygame.Rect(560, 560, 100, 100)
    pygame.draw.rect(screen, (255, 255, 100), multiply_rect)
    screen.blit(font1.render("*", False, (0, 0, 0)), (595, 595))
    button_press("*", multiply_rect)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    draw_widgets()

    draw_equation()

    pygame.display.flip()

pygame.quit()
