import random
import math


N = 4 
MAX_TEMP = 1000 




def initial_state():
    return [random.randint(0, N - 1) for i in range(N)]


def child_state(state):
    new_state = state.copy()
    row = random.randint(0, N - 1)
    new_state[row] = (new_state[row] + random.choice([-1, 1])) % N
    return new_state


def metric(state):
    count = 0
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                count += 1
    
    return count


def accept_probability(delta_e, temp):
    return math.exp(-delta_e / temp)




def hill_climbing_with_simulated_annealing():
    current_state = initial_state()
    print("Initial state is:",current_state)
    print("Initial attack:",metric(current_state))
    current_temp = MAX_TEMP
    

    while current_temp > 0 and metric(current_state) > 0:
        new_state = child_state(current_state)
        current_metric = metric(current_state)
        new_metric = metric(new_state)

        if new_metric <= current_metric:
            current_state = new_state
        else:
            prob = accept_probability(new_metric - current_metric, current_temp)
            if random.random() < prob:
                current_state = new_state

        current_temp = current_temp-1

    return current_state


result = hill_climbing_with_simulated_annealing()

print("Final state is",result)
if(metric(result)==0):
    print("There have no attack")