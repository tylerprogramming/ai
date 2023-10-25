# filename: classic_pong.py

import turtle
import os

# Create screen
sc = turtle.Screen()
sc.title("Pong")
sc.bgcolor("black")
sc.setup(width=1000, height=500)

# Left paddle
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=6, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Right paddle
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=6, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(40)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 2
ball.dy = -2

# Display scores
score_a = 0
score_b = 0
score = turtle.Turtle()
score.speed(0)
score.color("white")
score.penup()
score.hideturtle()
score.goto(0, 260)
score.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

# Update the score display
def update_score():
    score.clear()
    score.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

# Moving the left paddle
def paddleaup():
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)
def paddleadown():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)

# Moving the right paddle
def paddlebup():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)
def paddlebdown():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)

# Keyboard bindings
sc.listen()
sc.onkeypress(paddleaup, "w")
sc.onkeypress(paddleadown, "s")
sc.onkeypress(paddlebup, "Up")
sc.onkeypress(paddlebdown, "Down")

# Main game loop
while True:
    sc.update()

    # Ball moving
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border checking
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
        os.system("afplay bounce.wav&")
    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
        os.system("afplay bounce.wav&")
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dy *= -1
        score_a += 1
        update_score()
        os.system("afplay fail.wav&")
    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dy *= -1
        score_b += 1
        update_score()
        os.system("afplay fail.wav&")

    # Paddle collision
    if (ball.dx > 0) and (350 > ball.xcor() > 340) and (paddle_b.ycor() + 50 > ball.ycor() > paddle_b.ycor() - 50):
        ball.color("blue")
        ball.dx *= -1
        os.system("afplay paddle.wav&")
    elif (ball.dx < 0) and (-350 < ball.xcor() < -340) and (paddle_a.ycor() + 50 > ball.ycor() > paddle_a.ycor() - 50):
        ball.color("red")
        ball.dx *= -1
        os.system("afplay paddle.wav&")

    # Limit paddle's movement
    if paddle_a.ycor() > 250:
        paddle_a.sety(250)
    if paddle_b.ycor() > 250:
        paddle_b.sety(250)
    if paddle_a.ycor() < -240:
        paddle_a.sety(-240)
    if paddle_b.ycor() < -240:
        paddle_b.sety(-240)