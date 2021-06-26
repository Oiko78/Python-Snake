from turtle import Turtle, Screen
from random import randint

SIZE = 500
GRID_NUM = 20
GRID_SIZE = SIZE // GRID_NUM

snake = None
screen = Screen()
screen.setup(SIZE, SIZE)
screen.bgcolor('black')
screen.setworldcoordinates(10, 8, SIZE + 2, SIZE)
screen.title('Snake Game, Or is it?  - Oiko')

class Snake:
  def __init__(self):
    self.head = init_turtle()
    self.food = init_food()
    self.head.setpos((GRID_SIZE // 2 + GRID_SIZE * 9, GRID_SIZE // 2 + GRID_SIZE * 10))
    self.body = []
    self.direction = -1 # 0 = right, 1 = up, 2 = left, 3 = down
    self.speed = 25
    self.isLevelUp = False

  def levelup(self):
    self.body.insert(0, self.head.clone())
    self.head.setheading(self.direction * 90)
    self.head.forward(GRID_SIZE)
    
  def update(self):
    if len(self.body) > 0:
      self.body = self.body[-1:] + self.body[:-1] 
      self.body[0].setpos(self.head.pos())

  def checkPos(self):
    x, y = self.head.xcor(), self.head.ycor()
    if not (y >= 0 and y <= SIZE) or not (x >= 0 and x <= SIZE):
      if self.direction == 0:
        self.head.setpos(GRID_SIZE // 2, y)
      elif self.direction == 1:
        self.head.setpos(x, GRID_SIZE // 2)
      elif self.direction == 2:
        self.head.setpos(SIZE - GRID_SIZE // 2, y)
      elif self.direction == 3:
        self.head.setpos(x, SIZE - GRID_SIZE // 2)
  
  def resetSnake(self):
    while self.body:
      self.body.pop().reset()
    self.head.setpos((GRID_SIZE // 2 + GRID_SIZE * 9, GRID_SIZE // 2 + GRID_SIZE * 10))
    self.direction = -1


  def checkBodyCollision(self):
    for turtle in self.body:
      if self.body.index(turtle) < 2:
        continue
      if abs(self.head.xcor() - turtle.xcor()) < GRID_SIZE and abs(self.head.ycor() - turtle.ycor()) < GRID_SIZE:
        print('YOU LOSE WITH SCORE:', len(self.body))
        screen.title(f'Snake Game, Or is it?  - Oiko | Score: {len(self.body)}')
        self.resetSnake()
        
  def checkFoodCollision(self):
    if abs(self.head.xcor() - self.food.xcor()) < GRID_SIZE and abs(self.head.ycor() - self.food.ycor()) < GRID_SIZE:
        self.food.setpos(randomPos())
        self.levelup()


def init_turtle():
  turtle = Turtle()
  turtle.shape('square')
  turtle.shapesize(1.25)
  turtle.color('red')
  turtle.pencolor('#404040')
  turtle.speed('fastest')
  turtle.up()
  return turtle
def randomPos():
  x = GRID_SIZE // 2 + GRID_SIZE * randint(0, 19)
  y = GRID_SIZE // 2 + GRID_SIZE * randint(0, 19)
  return (x, y)
def init_food():
  turtle = Turtle()
  turtle.shape('square')
  turtle.shapesize(1.25)
  turtle.color('green')
  turtle.penup()
  turtle.setpos(randomPos())
  turtle.hideturtle()
  return turtle
def init_border():
  def border():
    turtle = init_turtle()
    for _ in range(4):
      turtle.down()
      turtle.forward(SIZE)
      turtle.left(90)
      yield(0)
    turtle.penup()
    turtle.hideturtle()

  def horizontal():
    turtle = init_turtle()
    for x in range(GRID_SIZE, SIZE, GRID_SIZE):
      turtle.goto(x, 0)
      turtle.pendown()
      turtle.goto(x, SIZE)
      turtle.penup()
      yield(0)
    turtle.hideturtle()

  def vertical():
    turtle = init_turtle()
    for y in range(GRID_SIZE, SIZE, GRID_SIZE):
      turtle.goto(0, y)
      turtle.pendown()
      turtle.goto(SIZE, y)
      turtle.penup()
      yield(0)
    turtle.hideturtle()

  generator1 = border()
  generator2 = horizontal()
  generator3 = vertical()
  while(next(generator1, 1) + next(generator2, 1) + next(generator3, 1) < 3):
    pass

def movement():
  global snake

  def right():
    if snake.direction != 2:
      snake.direction = 0
  def up():
    if snake.direction != 3:
      snake.direction = 1
  def left():
    if snake.direction != 0:
      snake.direction = 2
  def down():
    if snake.direction != 1:
      snake.direction = 3

  screen.onkeypress(left, 'Left')
  screen.onkeypress(up, 'Up')
  screen.onkeypress(right, 'Right')
  screen.onkeypress(down, 'Down')
  screen.listen()

  if(snake.direction != -1):
    snake.update()
    snake.head.setheading(snake.direction * 90)
    snake.head.forward(GRID_SIZE)
    snake.checkPos()
    snake.checkBodyCollision()
    snake.checkFoodCollision()
  if snake.isLevelUp:
    snake.levelup()
    snake.isLevelUp = False
  screen.ontimer(movement, snake.speed)
  # print('head', snake.head.pos())


def start_game():
  global snake
  snake = Snake()
  snake.food.showturtle()
  def pop():
    if len(snake.body) > 0:
      snake.body.pop().reset()
 
  def exit():
    screen.bye()
  def levelUp():
    if not snake.isLevelUp:
      snake.isLevelUp = True

  screen.onkeypress(pop, 'q')
  screen.onkeypress(exit, 'Escape')
  screen.onkeypress(levelUp, 'Return')
  screen.listen()
  movement()


init_border()
start_game()
screen.mainloop()