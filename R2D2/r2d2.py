import numpy as np

class State:
    def __init__(self,x,y,cost,prev_state):
        self.x = x
        self.y = y
        self.cost = cost
        self.previous_state = prev_state

def valid_pos(state,grid):
    grid_x = len(grid)
    grid_y = len(grid[0])
    positions = []
    if state.x - 1 >= 0:
        positions.append([state.x -1,state.y])
    if state.x + 1 < grid_x:
        positions.append([state.x + 1,state.y])
    if state.y -1 >= 0:
        positions.append([state.x, state.y - 1])
    if state.y + 1 < grid_y:
        positions.append([state.x, state.y + 1])
    return positions

def order_states(states):
    for i in range(len(states)):
        winner = states[i]
        curr_states = []
        #Find the minimum cost out of all our state objects
        min_cost = min(states[k].cost for k in range(i,len(states)))
        #Find all the states that share the minimum cost
        for index in range(i,len(states)):
            if states[index].cost == min_cost:
                curr_states.append([states[index],index])
                winner = states[i]
        #If more than one states share the same cost, order by minimum x
        if len(curr_states) > 1:
            min_x = min(curr_states[j][0].cost for j in range(len(curr_states)))
            same_x = []
            for curr_state in curr_states:
                if curr_state[0].x == min_x:
                    same_x.append(curr_state)
                    winner = curr_state
            #if more than one states share the same x, order by minimum y
            if len(same_x) > 1:
                min_y = min(same_x[j][0].cost for j in range(len(same_x)))
                for element in same_x:
                    if element[0].y == min_y:
                        winner = element
        tmp = states[i]
        states[i] = states[winner[1]]
        states[winner[1]] = tmp
    return states

def bfs(curr_state,cost_grid):
    next_states = expand_state(curr_state,cost_grid)
    ordered_next_states = order_states(next_states)
    return ordered_next_states

def expand_state(curr_state,cost_grid):
    valid_positions = valid_pos(curr_state,cost_grid)
    states = []
    for pos in valid_positions:
        x = pos[0]
        y = pos[1]
        cost = cost_grid[x][y]
        state = State(x,y,cost,curr_state)
        states.append(state)
    return states

def calc_cost(state):
    cost = 0
    while state.previous != None:
        cost += state.cost
        state = state.prev_state
    return cost

def is_solution(curr_state,final_state):
    if curr_state.x == final_state.x and curr_state.y == final_state.y:
        return True
    else:
        return False

def is_better_solution(curr_state,prev_solution,final_state):
    if prev_solution != None:
        curr_state_cost = calc_cost(curr_state)
        prev_solution_cost = calc_cost(prev_solution)
        if curr_state_cost < solution_found_cost:
            return True
    else:
        return True

def find_solution(states,final_state,cost_grid):
    best_solution = None
    while len(states) > 0:
        curr_state = states.pop(0)
        if is_solution(curr_state,final_state):
            if is_better_solution(curr_state,best_solution,final_state):
                best_solution = curr_state
                print_solution(best_solution)
        else:
            next_states = bfs(curr_state,cost_grid)
            for state in next_states:
                states.append(state)
    return best_solution

def print_solution(state):
    positions = []
    for pos in state:
        positions.append(pos)
    positions.reverse()
    print("-"*50)
    print("-"*50)
    for i,pos in enumerate(positions[:-1]):
        if i == 0:
            print("Starting point: [",pos[0]," ",pos[1],"]")
        else:
            print("Next point: [",pos[0]," ",pos[1],"]")
    print("Final point: [",pos[0]," ",pos[1],"]")
    print("-"*50)
    print("-"*50)

if __name__ == '__main__':
    cost_grid = [[1,1,1,1,2],[1,2,2,2,2],[3,3,4,4,3],[1,1,4,3,3],[4,1,1,1,1]]
    queue = []
    #Starting at position (1,4)
    init_x = 1
    init_y = 4
    cost = cost_grid[init_x-1][init_y-1]
    init_state = State(init_x-1,init_y-1,cost,None)

    #Final point at (5,5)
    final_x = 5
    final_y = 5
    cost = cost_grid[final_x-1][final_y-1]
    final_state = State(final_x-1,final_y-1,cost,None)

    queue.append(init_state)

    solution = find_solution(queue,final_state,cost_grid)

    print("BEST SOLUTION FOUND: \n")
    print_solution(solution)
