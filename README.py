import turtle
import time
import random

# --- Configuration ---
WIDTH = 650
HEIGHT = 650

# Nokia 3310 Colors (Hex Codes)
NOKIA_GREEN_BG = "#C4CFA1"
NOKIA_BLACK = "#43523D"

# Game Variables
delay = 0.1  # Initial speed
score = 0
level = 1
apples_collected = 0
target_apples = 10

# --- Setup Screen ---
wn = turtle.Screen()
wn.title("Snake - Nokia Style")
wn.bgcolor(NOKIA_GREEN_BG)
wn.setup(width=WIDTH, height=HEIGHT)
wn.tracer(0)  # Turns off screen updates for smoother animation

# --- Snake Head ---
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color(NOKIA_BLACK)
head.penup()
head.goto(0, 0)
head.direction = "stop"

# --- Snake Food ---
food = turtle.Turtle()
food.speed(0)
food.shape("square")
food.color(NOKIA_BLACK)
food.penup()
food.goto(0, 100)

# --- Snake Body Segments ---
segments = []

# --- Scoreboard ---
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color(NOKIA_BLACK)
pen.penup()
pen.hideturtle()
pen.goto(0, 280)  # Top of screen
pen.write(f"Score: 0  Level: 1  To Collect: 10", align="center", font=("Courier", 18, "bold"))

# --- Functions ---

def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

def update_scoreboard():
    pen.clear()
    remaining = target_apples - apples_collected
    pen.write(f"Score: {score}  Level: {level}  To Collect: {remaining}", align="center", font=("Courier", 18, "bold"))

def reset_game():
    global score, level, apples_collected, target_apples, delay, segments
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "stop"
    
    # Hide old segments
    for segment in segments:
        segment.goto(1000, 1000)
    
    segments.clear()
    
    # Reset stats
    score = 0
    level = 1
    apples_collected = 0
    target_apples = 10
    delay = 0.1
    update_scoreboard()

# --- Keyboard Bindings ---
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")
# Also allow WASD
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

# --- Main Game Loop ---
while True:
    wn.update()

    # 1. Check Collision with Border
    # (Coordinates are -325 to +325)
    if head.xcor() > 315 or head.xcor() < -315 or head.ycor() > 315 or head.ycor() < -315:
        reset_game()

    # 2. Check Collision with Food
    if head.distance(food) < 20:
        # Move food to random spot
        x = random.randint(-14, 14) * 20
        y = random.randint(-14, 14) * 20
        food.goto(x, y)

        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color(NOKIA_BLACK)
        new_segment.penup()
        segments.append(new_segment)

        # Update stats
        score += 10
        apples_collected += 1
        
        # Check for Level Up
        if apples_collected >= target_apples:
            level += 1
            apples_collected = 0
            target_apples += 10  # Add 10 more to requirement
            delay -= 0.01        # Speed up (lower delay is faster)
            if delay < 0.02:     # Cap max speed
                delay = 0.02

        update_scoreboard()

    # 3. Move the Body Segments
    # Move end segments first in reverse order
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where head was
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # 4. Check Collision with Body
    for segment in segments:
        if segment.distance(head) < 20:
            reset_game()

    time.sleep(delay)

wn.mainloop()
