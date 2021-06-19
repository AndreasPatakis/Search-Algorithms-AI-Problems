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

def visited(state):
    visited = []
    state = state.previous_state
    while state != None:
        pos = [state.x,state.y]
        visited.append(pos)
        state = state.previous_state
    return visited

def order_states(states):
    for i in range(len(states)):
        winner = states[i]
        curr_states = []
        #Find the minimum cost out of all our state objects
        min_cost = min(states[k].cost for k in range(i,len(states)))
        #Find all the states that share the minimum cost
        #input(min_cost)
        for index in range(i,len(states)):
            if states[index].cost == min_cost:
                curr_states.append([states[index],index])
                winner = [states[i],index]
        #print("curr:",len(curr_states))
        #If more than one states share the same cost, order by minimum x
        if len(curr_states) > 1:
            min_x = min(curr_states[j][0].x for j in range(len(curr_states)))
            same_x = []
            for curr_state in curr_states:
                if curr_state[0].x == min_x:
                    same_x.append(curr_state)
                    winner = curr_state
            #if more than one states share the same x, order by minimum y
            if len(same_x) > 1:
                min_y = min(same_x[j][0].y for j in range(len(same_x)))
                for element in same_x:
                    if element[0].y == min_y:
                        winner = element
        tmp = states[i]
        #input(winner[1])
        states[i] = states[winner[1]]
        states[winner[1]] = tmp
    return states

def bfs(curr_state,cost_grid):
    next_states = expand_state(curr_state,cost_grid)
    ordered_next_states = order_states(next_states)
    return ordered_next_states

def expand_state(curr_state,cost_grid):
    already_visited = visited(curr_state)
    valid_positions = valid_pos(curr_state,cost_grid)
    states = []
    for pos in valid_positions:
        x = pos[0]
        y = pos[1]
        cost = cost_grid[x][y]
        if [x,y] not in already_visited:
            state = State(x,y,cost,curr_state)
            states.append(state)
    return states

def calc_cost(state):
    cost = 0
    while state.previous_state != None:
        cost += state.cost
        state = state.previous_state
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
        if curr_state_cost <= prev_solution_cost:
            return True
    else:
        return True
    return False

def find_solution(states,final_state,cost_grid):
    best_solutions = []
    best_solution = None
    while len(states) > 0:
        curr_state = states.pop(0)
        if is_solution(curr_state,final_state):
            if is_better_solution(curr_state,best_solution,final_state):
                best_solutions.append(curr_state)
                best_solution = curr_state
        else:
            next_states = bfs(curr_state,cost_grid)
            for state in next_states:
                states.append(state)
    return best_solutions

def print_solution(state):
    cost = calc_cost(state)
    positions = []
    while state != None:
        positions.append(state)
        state = state.previous_state
    positions.reverse()
    print("-"*50)
    print("-"*50)
    for i,pos in enumerate(positions[:-1]):
        if i == 0:
            print("Starting point: [",pos.x+1," ",pos.y+1,"]")
        else:
            print("Next point: [",pos.x+1," ",pos.y+1,"]")
    print("Final point: [",positions[-1].x+1," ",positions[-1].y+1,"]")
    print("\nThis solution has a cost of: ",cost)
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

    solutions = find_solution(queue,final_state,cost_grid)

    print("-"*30,"BEST SOLUTIONS FOUND\n","-"*30)

    print("FOUND ",len(solutions)," SOLUTIONS WITH THE SAME COST.")
    for i,solution in enumerate(solutions):
        print("\nSOLUTION: ",i+1)
        print_solution(solution)
        input("Press any key to see the next one")
