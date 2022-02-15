from tkinter import *
import random

# constants

SPEED = 50
SPACE_SIZE = 20
BODY_PARTS = 3
BACKGROUND_COLOR = "WHITE"
SNAKE_COLOR = "RED"
MOUSE_COLOR = "GREEN"
GAME_HEIGHT = 800
GAME_WIDTH = 800

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Mouse:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH/SPACE_SIZE)-1) * SPACE_SIZE  # random position of the mouse
        y = random.randint(0, (GAME_HEIGHT/ SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=MOUSE_COLOR, tag="mouse")

def next_turn(snake, mouse):

    x, y = snake.coordinates[0]

    # snake movement coordinates
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == mouse.coordinates[0] and y == mouse.coordinates[1]:
        global score
        score += 1

        label.config(text="score:{}".format(score))  # score
        canvas.delete("mouse")
        mouse = Mouse()  # create new mouse to eat

    # delete the last snake body part if no mouse is eaten
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collision(snake):
        game_over()  # end game if snake collides with window edge
    else:
        window.after(SPEED, next_turn, snake, mouse)

def change_direction(new_direction):

    global direction

    # preventing the snake to turn 180 degree
    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    if new_direction == "up":
        if direction != "down:":
            direction = new_direction
    if new_direction == "down":
        if direction != "up":
            direction = new_direction

def check_collision(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:  # side collision
        return True
    elif y < 0 or y >= GAME_HEIGHT:  # up or dowm collision
        return True

    for body_part in snake.coordinates[1:]:  # anything after the head
        if x == body_part[0] and y== body_part[1]:
            print("Game over!")
            return True

def game_over():

    canvas.delete(ALL)  # delete everything on screen
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")

# create a window
window = Tk()  # tkinter
window.title("The game of Snake")
window.resizable(False, False)
score = 0
direction = 'down'

# window labels
label = Label(window, text="Score:{}".format(score), font=('consolas', 30))
label.pack()

# window canvas
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()  # creating window

# aligning the window in the center
window_width = window.winfo_width()
window_height = window.winfo_height()

screen_height = window.winfo_screenheight()
screen_width = window.winfo_screenwidth()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f'{window_width}x{window_height}+{x}+{y}')  # use 'x' instead of '*' for multiplication

# binding keys to movement
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
mouse = Mouse()

next_turn(snake, mouse)

window.mainloop()