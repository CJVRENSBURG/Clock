import pygame
import math
from datetime import datetime

Black = (0,0,0)
White = (255,255,255)
Red = (255,0,0)

Digital_H = 100
Width = 700
Height = Width + Digital_H
Clock_W = Width
Clock_H = 700
Margin_H = Margin_W = 5
Clock_R = (Width-Margin_W) / 2
Hour_R = Clock_R / 2
Minute_R = Clock_R * 7 / 10
Second_R = Clock_R * 8 / 10
Text_R = Clock_R * 9 / 10
Tick_R = 2
Tick_Length = 5
Hour_Stroke = 5
Minute_Stroke = 2
Second_Stroke = 2
Clock_Stroke = 2
Center_W = 10
Center_H = 10
Hours_in_Clock = 12
Minutes_in_Hour = 60
Seconds_in_Minute = 60
Size = (Width, Height)

def circlePoint(center, radius, theta):
    """
    Calculates the location of a point of a circle given the circle's
    center and radius as well as the point's angle from the xx' axis.
    """
    return (center[0] + radius * math.cos(theta),
            center[1] + radius * math.sin(theta))

def lineAtAngle(screen, center, radius, theta, color, width):
    """
    Draws a line from center towards an angle.
    The angle is give in radius.
    """
    point = circlePoint(center, radius, theta)
    pygame.draw.line(screen, color, center, point, width)

def GetAngle(unit, total):
    """
    Calculates the angle, in radius, corresponding to a portion of the clock
    counting using the given units up to a given total and starting from 12
    o'clock and moving clock wise.
    """
    return 2 * math.pi * unit / total - math.pi / 2

pygame.init()
screen = pygame.display.set_mode(Size)
pygame.display.set_caption("Clock")
Hour_font = pygame.font.SysFont("comicsans", 25, True, False)
digital_font = pygame.font.SysFont("comicsans", 32, True, False)

clock = pygame.time.Clock()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(White)

    now = datetime.now()

    c_x, c_y = Center_W / 2, Clock_H / 2
    center = (c_x, c_y)

    # draw the Clock
    pygame.draw.circle(screen, Black, center, Clock_W / 2 - Margin_W / 2, Clock_Stroke)

    # draw clock mounts
    pygame.draw.circle(screen, Black, center, Clock_W / 2 - Margin_W / 2, Clock_Stroke)

    # draw hands
    hour_theta = GetAngle(now.hour + 1.0 * now.minute / Minutes_in_Hour, Hours_in_Clock)
    minute_theta = GetAngle(now.minute, Minutes_in_Hour)
    second_theta = GetAngle(now.second, Seconds_in_Minute)

    for (radius, theta, color, stroke) in ((Hour_R, hour_theta, Black, Hour_Stroke), (Minute_R, minute_theta, Black, Minute_Stroke), (Second_R, second_theta, Red, Second_Stroke)):
        lineAtAngle(screen, center, radius, theta, color, stroke)

    # draw hour markings (text)
    for hour in range(1, Hours_in_Clock + 1):
        theta = GetAngle(hour, Hours_in_Clock)
        text = Hour_font.render(str(hour), True, Black)
        screen.blit(text, circlePoint(center, Text_R, theta))

    # draw minute markings (lines)
    for minute in range(0, Minutes_in_Hour):
        theta = GetAngle(minute, Minutes_in_Hour)
        p1 = circlePoint(center, Clock_R - Tick_Length, theta)
        p2 = circlePoint(center, Clock_R, theta)
        pygame.draw.line(screen, Black, p1, p2, Tick_R)

    # draw digital clock
    digital_text = now.strftime("%H:%M:%S")
    text = digital_font.render(digital_text, True, Black)
    screen.blit(text, [Width / 2 - digital_font.size(digital_text)[0] / 2, Height - Digital_H / 2 - digital_font.size(digital_text)[1] / 2])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()