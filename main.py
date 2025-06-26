import math
import re
import pygame

pygame.init()

WIDTH = 400
HEIGHT = 600
BORDER = 20

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Calculator")

running = True
clock = pygame.time.Clock()

# COLORS
BODY = (46, 53, 64)
SCREEN_COLOR = (193, 204, 212)
NUM_BUTTONS = (125, 138, 150)
BUTTON_CLEAR_DEL = (89, 96, 106)
BUTTON_OPERATIONS = (244, 186, 59)
BUTTON_EQUAL = (242, 90, 60)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Screen text
screen_text = ""

screen_rect = pygame.Rect(BORDER//2, 60, WIDTH - BORDER, 110)

buttons = [
    ['DEL','C','(',')'],
    ['√','^','e','π'],
    ['7', '8','9','/'],
    ['4','5','6','x'],
    ['1','2','3','-'],
    ['0','.','=','+']
]

w = WIDTH // 4
h = 70
top_border = 185
font_history = pygame.font.SysFont('comicsans', 20)
font = pygame.font.SysFont('comicsans', 35)
screen_font = pygame.font.SysFont('comicsans', 60)  # Font only for the screen

result_shown = False
buttons_rects = []

def draw_buttons():
    buttons_rects.clear()

    for row in range(6):
        for col in range(4):
            x = col * w + BORDER // 2
            y = row * h + top_border
            label = buttons[row][col]

            if label in {'+', '-', '/', 'x'}:
                color = BUTTON_OPERATIONS
            elif label == '=':
                color = BUTTON_EQUAL
            elif label == 'C' or label == 'DEL':
                color = BUTTON_CLEAR_DEL
            else:
                color = NUM_BUTTONS
            
            btn_rect = pygame.Rect(x, y, w - BORDER, h - BORDER)
            pygame.draw.rect(win, color, btn_rect, border_radius=20)

            text_surface = font.render(label, True, BUTTON_TEXT_COLOR)
            text_rect = text_surface.get_rect(center=btn_rect.center)
            win.blit(text_surface, text_rect)

            buttons_rects.append((btn_rect, label))

def calculate_expression(expr_str: str) -> str:
    try:
        expr = expr_str
        expr = expr.replace('x', '*')
        expr = expr.replace('^', '**')
        expr = expr.replace('π', 'math.pi')
        expr = re.sub(r'\be\b', 'math.e', expr)
        expr = re.sub(r'√\s*\(?([0-9.]+)\)?', r'math.sqrt(\1)', expr)
        result = eval(expr, {"math": math})

        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        else:
            return str(round(result, 5))
    except:
        return "Error"

# History
history = []
history_buttons = []
show_history = False

def draw_history_button(x, y, width, height):
    his_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(win, (255, 0, 0), his_rect, border_radius=20)
    text = font_history.render("HISTORY", True, (255, 255, 255))
    text_rect = text.get_rect(centery=screen_rect.centery, left=screen_rect.left + 120, top=screen_rect.top - 50)
    win.blit(text, text_rect)
    history_buttons.append(his_rect)

while running:
    clock.tick(60)

    if show_history:
        win.fill(BODY)

        title = font.render("HISTORY", True, (255, 255, 255))
        win.blit(title, (WIDTH//2 - title.get_width()//2, 30))

        current_y = 100

        for i, entry in enumerate(reversed(history[-10:])):
            line = font.render(entry, True, (255, 255, 255))
            win.blit(line, (40, current_y))
            current_y += 30

        back_text = font_history.render("Click to go back", True, (200, 200, 200))
        win.blit(back_text, (WIDTH//2 - back_text.get_width()//2, HEIGHT - 40))

        pygame.display.update()

        waiting = True
        while waiting:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                    waiting = False
                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    show_history = False
                    waiting = False
        continue

    win.fill(BODY)
    pygame.draw.rect(win, SCREEN_COLOR, screen_rect, border_radius=20)

    screen_text_surface = screen_font.render(screen_text, True, (0,0,0))
    screen_text_rect = screen_text_surface.get_rect(right=screen_rect.right - 20, centery=screen_rect.centery)
    win.blit(screen_text_surface, screen_text_rect)

    draw_history_button(BORDER//2, BORDER//2, WIDTH - BORDER, 30)
    draw_buttons()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for btn_rect, label in buttons_rects:
                if btn_rect.collidepoint(event.pos):
                    if label == 'C':
                        screen_text = ''
                    elif label == '=':
                        result_shown = True
                        try:
                            history.append(screen_text)
                            screen_text = calculate_expression(screen_text)
                            history.append(screen_text)
                            for calc in history:
                                print(calc)
                        except:
                            screen_text = "Error"
                    elif label == 'DEL':
                        if not result_shown:
                            screen_text = screen_text[:-1]
                    else:
                        if result_shown:
                            if label in {'+', '-', '/', 'x', '^'}:
                                screen_text += label
                                result_shown = False
                            else:
                                screen_text = label
                                result_shown = False
                        else:
                            screen_text += label
            for btn_his in history_buttons:
                if btn_his.collidepoint(event.pos):
                    show_history = True

pygame.quit()
