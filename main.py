import numpy as np
import time
from turtle import *

from rules import *
from utils import get_velocity_vector


def initialise_turtles(N):
    tracer(n=N*5, delay=300)
    turtles_list = [Turtle("turtle") for _ in range(N)]
    coor_range = np.arange(-300, 301)
    starting_positions = np.random.choice(coor_range, (N, 2), replace=True)
    headings = np.random.choice(360, N, replace=True)
    for i, t in enumerate(turtles_list):
        t.penup()
        t.speed(0)
        t.goto(starting_positions[i, 0], starting_positions[i, 1])
        t.setheading(headings[i])
        t.speed(1)
        t.actual_speed = np.random.randint(20, 30)
    turtles_list[0].color("red")
    return turtles_list, coor_range


def update_turtle_positions(turtles_list):
    new_positions = []
    new_headings = []
    new_speeds = []
    for i, t in enumerate(turtles_list):
        velocities_list = []
        cur_pos = np.array([t.pos()], dtype=float).flatten()
        if i == -1:
            heading_change_velocity = direction_change_rule(i, turtles_list)
            velocities_list.append(heading_change_velocity)
        else:
            separation_velocity = separation_rule(i, turtles_list)
            cohesion_velocity = cohesion_rule(i, turtles_list)
            common_velocity = alignment_rule(i, turtles_list)
            velocities_list.extend([separation_velocity, cohesion_velocity, common_velocity])
        turtle_velocity = get_velocity_vector(i, turtles_list)
        bounding_velocity = bound_position_rule(i, turtles_list)

        new_velocity = sum(velocities_list) + bounding_velocity
        new_velocity = (new_velocity + turtle_velocity)
        # if i == -1:
        #     new_velocity = speed_restriction_rule(new_velocity)
        new_velocity = speed_restriction_rule(new_velocity)
        new_heading = velocity_to_heading(new_velocity)
        new_speed = np.linalg.norm(new_velocity)
        new_pos = cur_pos + new_velocity
        new_positions.append(new_pos)
        new_headings.append(new_heading)
        new_speeds.append(new_speed)

    return new_positions, new_headings, new_speeds


def draw_turtle_positions(turtles_list, new_positions, new_headings, new_speeds):
    tracer(n=len(turtles_list), delay=2000)
    for i, t in enumerate(turtles_list):
        t.setheading(new_headings[i])
        t.actual_speed = new_speeds[i]
        x, y = new_positions[i]
        t.goto(x, y)


if __name__ == "__main__":
    turtles_list, coor_range = initialise_turtles(N=50)
    for i in range(10000):
        new_positions, new_headings, new_speeds = update_turtle_positions(turtles_list)
        draw_turtle_positions(turtles_list, new_positions, new_headings, new_speeds)

    input()