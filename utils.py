import numpy as np

def calc_dist(pos1, pos2):
    dist = np.sqrt(((pos1 - pos2) ** 2).sum())
    return dist

def heading_to_vector(t_heading):
    t_heading = (t_heading) / 180 * np.pi # from degrees to radians
    t_heading = np.array([np.cos(t_heading), np.sin(t_heading)], dtype=float).flatten()

    return t_heading


def velocity_to_heading(t_velocity):
    heading = (np.arctan2(t_velocity[1], t_velocity[0]) / np.pi * 180) % 360

    return heading


def get_velocity_vector(t_id, turtles_list):
    t = turtles_list[t_id]
    t_speed = t.actual_speed
    t_heading = t.heading()
    t_heading = heading_to_vector(t_heading) # unit vector heading
    t_velocity = t_heading * t_speed

    return t_velocity