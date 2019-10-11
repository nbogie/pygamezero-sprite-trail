import math
import random

# Credits:
# Uses assets from "Lap Rusher Assets" by Virgate Designs
#   https://opengameart.org/content/lap-rusher-assets

treads = Actor('cartrail')
car = Actor('car')
carpark = Actor('carpark2')
lasers = []
powerups = []
collected_powerups = []

car.x = 200
car.y = 200
carpark.topleft = (0,0)

frame_count = 0
speed = 1
skid_speed = 4
accel = 0.14
turningStep = 5
treads_history = []

def update_lasers():
    if keyboard.space:
        laser = Actor('lasergreen')
        laser.x = car.x
        laser.y = car.y
        laser.angle = car.angle
        laser.speed = 8
        lasers.append(laser)

    for laser in lasers:
        move_actor_forward(laser, laser.speed)

def update_powerups():
    # maybe add a powerup
    if frame_count % 100 == 0:
        powerup_type = random.randint(0,3)
        pu = Actor("powerup%d" % powerup_type)
        pu.x = random.randint(0, 600)
        pu.y = random.randint(0, 600)
        pu.type = powerup_type
        powerups.append(pu)
    for pu in powerups:
        if pu.collidepoint(car.x, car.y):
            pu.x = 0

def update():
    global speed, frame_count

    frame_count += 1
    update_powerups()
    update_lasers()
    # handle player inputs
    turning = False

    if keyboard.right:
        turning = True
        car.angle -= turningStep
        if car.angle < 0:
            car.angle += 360

    if keyboard.left:
        turning = True
        car.angle += turningStep
        if car.angle > 359:
            car.angle -= 360

    if keyboard.down:
        speed -= accel

    if keyboard.up:
        speed += accel

    speed = speed * 0.98
    move_actor_forward(car, speed)

    # maybe add skid positions to the treads_history
    if (turning and frame_count % 2 == 0 and speed > skid_speed):
        treads_history.append((car.x, car.y, car.angle + 90))

def move_actor_forward(actor, spd):
    dx = spd * math.cos(math.radians(actor.angle))
    dy = -1 * spd * math.sin(math.radians(actor.angle))

    actor.x += dx
    actor.y += dy

def draw():
    screen.fill((200, 200, 180))
    carpark.draw()

    for (x, y, angle) in treads_history[-30:-1]:
        treads.x = x
        treads.y = y
        treads.angle = angle + 90

        treads.draw()
    for pu in powerups:
        pu.draw()

    for laser in lasers:
        laser.draw()

    car.draw()
