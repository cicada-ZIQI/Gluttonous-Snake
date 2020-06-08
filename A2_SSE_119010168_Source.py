import turtle
import random
import time

#put the position of x-axis and y-axis of 9 foods inside food_x and food_y respectively
food_x,food_y=[],[]
#put the 9 numbers as turtles inside the food_list
food_list=[]
#put the position of 9 numbers inside the food_position_list
food_position_list=[]
#put the position of every stamp of the snake existiong right now into the snake_pos
snake_pos=[]
#put the id of every stamp existing right now into stamp_id
stamp_id=[]
# contact represents the contact times of the snake and monster
contact=0
s=turtle.Screen()
#set up the screen size
s.setup(500,500) 
s.tracer(0)
t=turtle.Turtle()
m=turtle.Turtle()
#direction represents the direction of the snake head. When direction==360, the snake won't move
direction=540
#at the beginning of the game, the length of the snake should be 5
length_should_be=5
#time1 represent the start time of the game
time1=0
#put all the positions that the snake once pause on into this list
pause_pos=[(1,1)]
#put all the directions the snake once moved to into this list
direction_list=[]
#in case of the user occasionally click the mouse
start_times=0
 
#randomly produce the position of 9 numbers
def produce_numbers():
    global food_x, food_y
    x=random.uniform(-240,240)
    y=random.uniform(-240,240)
    food_x.append(x)
    food_y.append(y)
    return (x,y)

#creante 9 turtles and let then write 9 numbers
def food_turtle_write_numbers():
    global food_list, food_position_list
    for i in range(1,10):
        y=i
        i=turtle.Turtle()
        i.hideturtle()
        i.up()
        position=produce_numbers()
        i.goto(position)
        i.write(y)
        food_list.append(i)
        food_position_list.append(position)

#write the introduction of the game. Put the monster and the snake at the right place. Write a title.     
def open_text():
    s.title("snake:   contact:   " + str(contact) + "   time:   " + str(0))
    t.hideturtle()
    t.up()
    t.goto(-200,110)
    t.color("black")
    t.write("Welcome to the Gluttonous Snake.",font=("Arial",10,"normal"))
    t.goto(-200,90)
    t.write("You are going to use 4 arrow keys to move the snake around the screen",font=("Arial",10,"normal"))
    t.goto(-200,70)
    t.write("trying to consume all the food itemsbefore the monster catch you.",font=("Arial",10,"normal"))
    t.goto(-200,50)
    t.write("Click anywhere to start the game.",font=("Arial",10,"normal"))
    t.goto(0,0)
    t.color("red")
    t.shape("square")  
    t.showturtle()
    m.up()
    m.goto(-210,-210)
    m.shape("square")
    m.color("purple")
    m.showturtle()
    s.update()
 
#After the user clicking anywhere, the introduction will disapear and 9 numbers will appear
def start(x,y):
    global stamp_id, snake_pos, time1, direction, start_times
    if start_times == 0:
        direction=360
        start_times = 1
        time1=time.time()
        t.clear()
        t.up()
        t.color("blue","black")
        id=t.stamp()
        stamp_id.append(id)
        snake_pos.append((t.xcor(),t.ycor()))
        t.color("red")
        food_turtle_write_numbers()
        s.update()
 
def right():
    global direction, direction_list
    direction=0
    direction_list.append(0)

def up():
    global direction, direction_list
    direction=90
    direction_list.append(90)

def left():
    global direction, direction_list
    direction=180
    direction_list.append(180)

def down():
    global direction, direction_list
    direction=270
    direction_list.append(270)

#if the user click the space button, the game will be paused
def pause():
    global direction, pause_pos
    if (t.xcor(),t.ycor()) != pause_pos[-1]:
        direction=360
        pause_pos.append((t.xcor(),t.ycor()))
    else:
        direction=direction_list[-1]

# the snake will extend 1 unit
def extend():
    global stamp_id, snake_pos
    t.color("blue","black")
    t.setheading(direction)
    t.forward(20)
    id=t.stamp()
    t.color("red")
    stamp_id.append(id)
    snake_pos.append((t.xcor(),t.ycor()))
    s.update()

#check whether the snake eat the food or not
def check_eat():
    global food_x,food_y, food_position_list
    snake_x=t.xcor()
    snake_y=t.ycor()
    for x in food_x:
        if abs(snake_x -x) <= 10:
            x_index=food_x.index(x)
            food_number=x_index + 1
            if abs(food_y[x_index] - snake_y) <= 10:
                for i in food_list:
                    if food_list.index(i) == x_index:
                        i.clear()
                        i.hideturtle()
                        food_position_list[x_index]=""
                        food_y[x_index]=10000
                        food_x[x_index]=10000
                return True, food_number
    else:
        return False, 0

#check whether the snake is in the screen or not
def check_in_screen():
    if int(t.xcor()) in range(-230,230) and int(t.ycor()) in range(-230,230):
        return True
    else:
        return False

#check the user win the game or not
def check_win():
    global direction
    if food_x == [10000]*9:
        direction=540
        return True
    else:
        return False
#check whether the snake contacks the monster or not
def check_contact():
    for pos in snake_pos:
        if abs(pos[0] - m.xcor()) < 20 and abs(pos[1] - m.ycor()) < 20:
            return 1
    else:
        return 0

#if the snake only moves 20 units
def snake_move_part():
    global length_should_be, snake_pos
    extend()
    length_now=len(stamp_id) - 1
    length_should_be += check_eat()[1]
    #if length_should_be > length_now, the snake only need to extend, no need to clear one of the stamp
    if length_should_be > length_now:
        s.ontimer(snake_move,400)
    #if length_should_be == length_now, the snake need to extend and also need to clear the first stamp
    else:
        t.clearstamp(stamp_id[0])
        s.update()
        stamp_id.pop(0)
        snake_pos.pop(0)
        s.ontimer(snake_move,200)

#control the move of the snake
def snake_move():
    #if the snake is in the screen and the game isn't paused
    if direction != 360 and direction != 540 and check_in_screen():
        snake_move_part()
    #if the snake is out of the range, only in the following cases can it turns back to the screen
    elif int(t.xcor()) not in range(-230,230) and int(t.ycor()) not in range(-230,230):
        if t.xcor() > 230 and t.ycor() < -230:
            if direction == 0 or direction == 270:
                s.ontimer(snake_move,200)
            else:
                snake_move_part()
        if t.xcor() < -230 and t.ycor() < -230:
            if direction == 180 or direction == 270:
                s.ontimer(snake_move,200)
            else:
                snake_move_part()
        if t.xcor() < -230 and t.ycor() > 230:
            if direction == 90 or direction == 180:
                s.ontimer(snake_move,200)
            else:
                snake_move_part()
        if t.xcor() > 230 and t.ycor() > 230:
            if direction == 0 or direction == 90:
                s.ontimer(snake_move,200)
            else:
                snake_move_part()
    elif (direction == 0 or direction == 90 or direction == 270) and t.xcor() < -230:
        snake_move_part()
    elif (direction == 0 or direction == 90 or direction == 180) and t.ycor() < -230:
        snake_move_part()
    elif (direction == 90 or direction == 180 or direction == 270) and t.xcor() > 230:
        snake_move_part()
    elif (direction == 0 or direction == 180 or direction == 270) and t.ycor() > 230:
        snake_move_part()
    #if the game is pause, just need to update the situation right now
    else:
        s.ontimer(snake_move,200)
 
#control the move of the monster
def monster_move():
    global direction, contact
    time2=time.time()
    #spend_time is the time between the user click anyshere to start the game and the time right now
    spend_time = time2 - time1
    diff_x=int(t.xcor()) - int(m.xcor())
    diff_y=int(t.ycor()) - int(m.ycor())
    #if the user doesn't pause the game
    if direction != 540:
        s.title("snake:  contact:  " + str(contact) + "   time:   " + str(spend_time))
        #if fail
        if t.distance(m) < 20:
            contact += 1
            m.stamp()
            m.hideturtle()
            m.goto(-60,0)
            m.color("red")
            m.write("Game over!",font=("Arial",18,"normal"))
            s.title("snake:  contact:  " + str(contact) + "   time:   " + str(spend_time))
            direction=360
            s.update()
            return
        #if win
        if check_win():
            m.stamp()
            m.hideturtle()
            m.goto(-60,0)
            m.color("red")
            m.write("Congratuations!!!",font=("Arial",18,"normal"))
            direction=360
            s.update()
            return
        #Through comparing the distance of the monster and the snake in y and x axis, the monster can move to a rational direction
        if abs(diff_y) >= abs(diff_x) and diff_y > 0:
            contact += check_contact()
            m.setheading(90)
            m.forward(20)
        elif abs(diff_y) >= abs(diff_x) and diff_y < 0:
            contact += check_contact()
            m.setheading(270)
            m.forward(20)
        elif abs(diff_y) < abs(diff_x) and diff_x > 0:
            contact += check_contact()
            m.setheading(0)
            m.forward(20)
        elif abs(diff_y) < abs(diff_x) and diff_x < 0:
            contact += check_contact()
            m.setheading(180)
            m.forward(20)
    s.update()
    #the monster will move in a variable speed
    speed=int(random.uniform(300,350))
    s.ontimer(monster_move,speed)
 
def bind():
    s.onkey(up,"Up")
    s.onkey(down,"Down")
    s.onkey(left,"Left")
    s.onkey(right,"Right")
    s.onkey(pause,"space")
    s.onclick(start)
    s.listen()
 
def main():
    open_text()
    snake_move()
    monster_move()
    bind()
    turtle.done()

main()