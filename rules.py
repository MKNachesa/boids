from utils import *

MIN_DIST = 20
COHESION_SCALER = 100
VELOCITY_SCALER = 8


def separation_rule(t_id, turtles_list):
    t_pos = np.array([turtles_list[t_id].pos()], dtype=float)
    separation_velocity = np.array([0, 0], dtype=float)
    for i in range(len(turtles_list)):
        if i != t_id:
            other_t_pos = np.array([turtles_list[i].pos()])
            dist = calc_dist(t_pos, other_t_pos)
            if dist <= MIN_DIST:
                diff = (other_t_pos - t_pos).flatten()
                separation_velocity -= diff

    separation_velocity = separation_velocity.flatten()

    return separation_velocity


def cohesion_rule(t_id, turtles_list, max_neighbor_dist=MIN_DIST+30):
    new_pos = np.array([0, 0], dtype=float).flatten()
    t_pos = np.array([turtles_list[t_id].pos()], dtype=float)
    num_neighbors = 0
    for i, t in enumerate(turtles_list):
        if i != t_id:
            other_t_pos = np.array([turtles_list[i].pos()])
            dist = calc_dist(t_pos, other_t_pos)
            if max_neighbor_dist is None or dist <= max_neighbor_dist:
                new_pos += np.array([t.pos()], dtype=float).flatten()
                num_neighbors += 1

    new_pos = new_pos / num_neighbors if num_neighbors > 0 else new_pos
    cohesion_velocity = ((new_pos - t_pos) / COHESION_SCALER).flatten()

    return cohesion_velocity


def alignment_rule(t_id, turtles_list, max_neighbor_dist=75):
    common_velocity = np.array([0, 0], dtype=float)
    t_velocity = get_velocity_vector(t_id, turtles_list)
    t = turtles_list[t_id]
    t_pos = np.array([t.pos()], dtype=float).flatten()
    num_neighbors = 0
    for i, t in enumerate(turtles_list):
        if i != t_id:
            other_t_pos = np.array([turtles_list[i].pos()])
            dist = calc_dist(t_pos, other_t_pos)
            if dist <= max_neighbor_dist:
                other_t_velocity = get_velocity_vector(i, turtles_list)
                common_velocity += other_t_velocity
                num_neighbors += 1

    common_velocity = common_velocity / num_neighbors if num_neighbors > 0 else common_velocity
    common_velocity = (common_velocity - t_velocity) / VELOCITY_SCALER

    common_velocity = common_velocity.flatten()

    return common_velocity


def bound_position_rule(t_id, turtles_list):
    x_min = -300
    x_max = 300
    y_min = -300
    y_max = 300

    bounding_vector = np.array([0, 0], dtype=float).flatten()
    t_pos = turtles_list[t_id].pos()
    if t_pos[0] < x_min:
        bounding_vector[0] = 10
    elif t_pos[0] > x_max:
        bounding_vector[0] = -10

    if t_pos[1] < y_min:
        bounding_vector[1] = 10
    elif t_pos[1] > y_max:
        bounding_vector[1] = -10

    return bounding_vector


def direction_change_rule(t_id, turtles_list):
    t_velocity = get_velocity_vector(t_id, turtles_list)
    max_angle_change = 90
    t_heading = velocity_to_heading(t_velocity)
    heading_change = np.random.rand() * max_angle_change - max_angle_change * 2
    t_heading = t_heading + heading_change
    heading_change_velocity = heading_to_vector(t_heading)
    heading_change_speed = 1 - abs(heading_change) / (max_angle_change / 2)
    heading_change_velocity = heading_change_velocity * heading_change_speed

    return heading_change_velocity


def speed_restriction_rule(t_velocity, minim_speed=10, maxim_speed=20):
    t_speed = np.linalg.norm(t_velocity)
    if t_speed < minim_speed:
        t_velocity = t_velocity / t_speed * minim_speed
    elif t_speed > maxim_speed:
        t_velocity = t_velocity / t_speed * maxim_speed
    return t_velocity
