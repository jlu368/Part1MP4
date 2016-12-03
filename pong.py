import random


def main():
    paddle_height = .2
    init_state = cur_state = (.5, .5, .03, .01, .5 - paddle_height/2)


def step(state):
    new_xvelo = state[2]
    new_yvelo = state[3]

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

    if new_xpos == 1 and (state[4] >= new_ypos >= state[4] - .2):
        new_xpos = 2 - new_xpos
        u = random.uniform(-.015, .015)
        v = random.uniform(-.03, .03)
        new_xvelo += u
        if 0 < new_xvelo < .03:
            new_xvelo = .03
        elif -.03 < new_xvelo <= 0:
            new_xvelo = -.03
        new_yvelo += v

    return (new_xpos, new_ypos, new_xvelo, new_yvelo, state[4])