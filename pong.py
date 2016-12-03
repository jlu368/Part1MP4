import random, itertools
import numpy as np

class state:
    def __init__(self, ball, paddle, x_vel, y_vel):
        self.ball_loc = ball
        self.paddle_loc = paddle
        self.x_vel = x_vel
        self.y_vel = y_vel

def main():
    paddle_height = .2
    init_state = cur_state = (.5, .5, .03, .01, .5 - paddle_height/2)
    decisions = []
    states ={}

    for x in range(12):discrete = discretize(state)
        discrete_states[state]
        for y in range(12):
            for paddle in range(12):
                for xvel in [-1,1]:
                    for yvel in [-1,0,1]:
                        new_state = state((x,y), paddle, xvel, yvel)
                        states[new_state] = (0,0,0)

    while True:
        cur_decision = step(cur_state, states, decisions)
        cur_state = cur_decision[0]
        discrete = discretize(cur_state)
        decisions.append((discrete, cur_decision[1]))
        if cur_state[0] > 1:
            cur_state = init_state
            for decision in decisions:
                score = states[decision[0]]
                if decision > 0:
                    states[decision[0]] = (score[0], score[1]-1, score[2])
                elif decision < 0:
                    states[decision[0]] = (score[0]-1, score[1], score[2])
                else:
                    states[decision[0]] = (score[0], score[1], score[2]-1)
            decisions = []



def step(state, discrete_states, decisions):
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
        for decision in decisions:
            score = discrete_states[decision[0]]
            if decision > 0:
                discrete_states[decision[0]] = (score[0], score[1]+3, score[2])
            elif decision < 0:
                discrete_states[decision[0]] = (score[0]+3, score[1], score[2])
            else:
                discrete_states[decision[0]] = (score[0], score[1], score[2]+3)
        new_xpos = 2 - new_xpos
        u = random.uniform(-.015, .015)
        v = random.uniform(-.03, .03)
        new_xvelo += u
        if 0 < new_xvelo < .03:
            new_xvelo = .03
        elif -.03 < new_xvelo <= 0:
            new_xvelo = -.03
        new_yvelo += v

    new_state = (new_xpos, new_ypos, new_xvelo, new_yvelo, state[4])
    discrete = discretize(new_state)
    scores = discrete_states[discrete]
    change = 0
    if scores[0] < scores[1] > scores[2]:
        change = .04
        new_state += .04
    elif scores[1] < scores[0] > scores[2]:
        change = -.04
        new_state[4] -= .04


    return (new_state, change)

def discretize(state):
    twelve = np.linspace(0,1,12)
    
