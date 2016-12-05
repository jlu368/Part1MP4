import random, itertools, json
import numpy as np

class State:
    def __init__(self, ball, paddle, x_vel, y_vel):
        self.ball_loc = ball
        self.paddle_loc = paddle
        self.x_vel = x_vel
        self.y_vel = y_vel

    def __hash__(self):
        return hash((self.ball_loc, self.x_vel, self.y_vel, self.paddle_loc))

    def __eq__(self, other):
        if self.ball_loc == other.ball_loc and self.paddle_loc == other.paddle_loc \
            and self.x_vel == other.x_vel and self.y_vel == other.y_vel:
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str((self.ball_loc, self.x_vel, self.y_vel, self.paddle_loc))

    def fail(self):
        if self == State((-1,-1), 0, 0, 0):
            return True
        return False

def random_state():
    ball_x = random.uniform(0,1)
    ball_y = random.uniform(0,1)
    x_vel = .03 * random.choice([-1,1])
    y_vel = .03 * random.choice([-1,0,1])
    paddle = random.uniform(0,1)

    return (ball_x, ball_y, x_vel, y_vel, paddle)

def main():
    gamma = .9
    paddle_height = .2
    init_state = (.5, .5, .03, .01, .5 - paddle_height/2)
    cur_state = random_state()
    states = {}
    hit = 0
    games = 0
    alpha = 1

    for x in range(25):
        for y in range(25):
            for paddle in range(25):
                for xvel in [-1,1]:
                    for yvel in [-1,0,1]:
                        new_state = State((x,y), paddle, xvel, yvel)
                        states[new_state] = (0,0,0)
    states[State((-1,-1), 0, 0, 0)] = (-1,-1,-1)

    while True:
        cur_state, states, hit = step(cur_state, states, hit, alpha, gamma)
        discrete = discretize(cur_state)
        if cur_state[0] > 1:
            # exit()
            # if hit > 0:
            #     print(hit)
            games += 1
            alpha = 1000/(1000 + games)
            # print(games)
            if games % 10000 == 0:
                hit = final_q(init_state, states, 0, 0)
                # import IPython
                # IPython.embed()
                print(hit)
            cur_state = random_state()
            # cur_state = init_state
            hit = 0


def final_q(cur_state, states, hit, step):
    disc = discretize(cur_state)
    print_board(disc)
    # if 20 > step >= 16:
    #     import IPython
    #     IPython.embed()
        # exit()
    if disc.fail():
        # import IPython
        # IPython.embed()
        return hit

    val = states[disc]
    if val[1] < val[0] > val[2]:
        new_state, _, n_hit = next_state(cur_state, 0, hit)
    elif val[0] < val[1] < val[2]:
        new_state, _, n_hit = next_state(cur_state, 2, hit)
    else:
        new_state, _, n_hit = next_state(cur_state, 1, hit)

    n_hit = final_q(new_state, states, n_hit, step+1)
    return n_hit



def print_board(state):
    for x in range(25):
        for y in range(25):
            if state.ball_loc == (x,y):
                print("o", end='')
            elif x == 24 and y == state.paddle_loc:
                print('_', end='')
            else:
                print(' ', end='')
        print()


def step(state, discrete_states, hit, alpha, gamma):
    action = random.randint(0,2)
    new_state, q, hit = next_state(state, action, hit)
    q += gamma * max_q(new_state, discrete_states)
    val = discrete_states[discretize(state)]
    td_val = val[action] + alpha*(q-val[action])
    if action == 0:
        discrete_states[discretize(state)] = (td_val, val[1], val[2])
    elif action == 1:
        discrete_states[discretize(state)] = (val[0], td_val, val[2])
    else:
        discrete_states[discretize(state)] = (val[0], val[1], td_val)

    return new_state, discrete_states, hit


def max_q(state, discrete_states):
    disc = discretize(state)
    val = discrete_states[disc]
    if val[1] < val[0] > val[2]:
        return val[0]
    elif val[0] < val[1] < val[2]:
        return val[2]
    else:
        return val[1]

def next_state(state, action, hit):
    new_xvelo = state[2]
    new_yvelo = state[3]
    reward = 0

    new_xpos = state[0] + state[2]
    if new_xpos < 0:
        new_xpos = -new_xpos
        new_xvelo = -new_xvelo

    new_ypos = state[1] + state[3]
    if new_ypos < 0:
        new_ypos = -new_ypos
        new_yvelo = -new_yvelo
    elif new_ypos > 1:
        new_ypos = 2 - new_ypos
        new_yvelo = -new_yvelo

    if new_xpos >= 1 and (state[4] <= new_ypos <= state[4] + .2):
        new_xpos = 2 - new_xpos
        u = random.uniform(-.015, .015)
        v = random.uniform(-.03, .03)
        new_xvelo = -new_xvelo + u
        if 0 < new_xvelo < .03:
            new_xvelo = .03
        elif -.03 < new_xvelo <= 0:
            new_xvelo = -.03
        new_yvelo += v
        hit += 1
        reward = 1
    elif new_xpos > 1:
        reward = -1

    if action == 0:
        new_paddle = state[4]
    elif action == 1:
        new_paddle = state[4] + .04
        if new_paddle > (1 - .2):
            new_paddle = .8
    elif action == 2:
        new_paddle = state[4] - .04
        if new_paddle < 0:
            new_paddle = 0

    new_state = (new_xpos, new_ypos, new_xvelo, new_yvelo, new_paddle)
    return new_state, reward, hit

def discretize(state):
    if (state[0] >= 1 and not (state[4] <= state[1] <= state[4] + .2)) or int(state[0]*24)>24:
        return State((-1,-1), 0, 0, 0)
    coords = (int(state[0]*24), int(state[1]*24))
    paddle = int(state[4]*24)

    if state[2] > 0:
        xvel = 1
    else:
        xvel = -1

    if state[3] > 0:
        yvel = 1
    elif state[3] < 0:
        yvel = -1
    else:
        yvel = 0

    return State(coords, paddle, xvel, yvel)

main()
