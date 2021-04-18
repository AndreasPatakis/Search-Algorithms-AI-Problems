class State:
    def __init__(self,left_bank,right_bank,side,prior_move,came_from_obj,depth):
        self.left_bank = left_bank
        self.right_bank = right_bank
        self.side = side
        self.prior_move = prior_move
        self.came_from_obj = came_from_obj
        self.depth = depth


#Επιστρέφει τις επιτρεπτές μεταθέσης τις οποίες μπορεί να κάνει η βάρκα
#στην συγκεκριμένη κατάσταση
def legalMoves(state_obj,possible_moves):
    moves = []
    for move in possible_moves:
        if(state_obj.side == "left"):
            left_miss = state_obj.left_bank[0] - move[0]
            left_can = state_obj.left_bank[1] - move[1]
            right_miss = state_obj.right_bank[0] + move[0]
            right_can = state_obj.right_bank[1] + move[1]
        else:
            left_miss = state_obj.left_bank[0] + move[0]
            left_can = state_obj.left_bank[1] + move[1]
            right_miss = state_obj.right_bank[0] - move[0]
            right_can = state_obj.right_bank[1] - move[1]
        if(permissible([left_miss,right_miss],[left_can,right_can])):
            if(left_miss >= left_can or left_miss == 0):
                if(right_miss >= right_can or right_miss == 0):
                    moves.append(move)
    return moves

def permissible(mis,can):
    mis_allowed = False
    can_allowed = False
    if( (mis[0] >= 0 and mis[0] <= 3) and (mis[1] >= 0 and mis[1] <= 3) ):
        mis_allowed = True
    if( (can[0] >= 0 and can[0] <= 3) and (can[1] >= 0 and can[1] <= 3) ):
        can_allowed = True
    return mis_allowed and can_allowed

def travel(state_obj,move):
    if (state_obj.side == "left"):
        left_miss = state_obj.left_bank[0] - move[0]
        left_can = state_obj.left_bank[1] - move[1]
        right_miss = state_obj.right_bank[0] + move[0]
        right_can = state_obj.right_bank[1] + move[1]
        side = "right"
    else:
        left_miss = state_obj.left_bank[0] + move[0]
        left_can = state_obj.left_bank[1] + move[1]
        right_miss = state_obj.right_bank[0] - move[0]
        right_can = state_obj.right_bank[1] - move[1]
        side = "left"

    return [[left_miss,left_can],[right_miss,right_can],side]

def createStates(state_obj,moves):
    new_states = []
    for move in moves:
        results = travel(state_obj,move)
        if(results[0] == [3,3]):
            pass
        else:
            new_state = State(results[0],results[1],results[2],move,state_obj,state_obj.depth+1)
            new_states.append(new_state)
    return new_states


def print_journey(state_obj):
    states = []
    state = state_obj
    print("\nTREE DEPTH: ",state.depth)
    print("Our Journey:")
    while(state != None):
        states.append(state)
        state = state.came_from_obj
    states.reverse()
    for pos in range(1,len(states)):
        if((pos-1) % 2 == 0):
            print(states[pos-1].left_bank," --> Transfer:",states[pos].prior_move," --> ",states[pos-1].right_bank)
        else:
            print(states[pos-1].left_bank," <-- Transfer:",states[pos].prior_move," <-- ",states[pos-1].right_bank)
        print(states[pos].left_bank," -- Current State -- ",states[pos].right_bank)
    if(states[-1].left_bank == [0,0] and states[-1].right_bank == [3,3]):
        print("[0, 0] -- FINAL STATE PROBLEM SOLVED! -- [3, 3]")

def winning_state(states):
    solutions = []
    for state_obj in states:
        if(state_obj.right_bank == [3,3]):
            solutions.append(state_obj)
    return solutions

def bfs(states):
    next_states = []
    while(len(states) != 0):
        state_obj = states[0]
        moves = legalMoves(state_obj,possible_moves)
        new_states = createStates(state_obj,moves)
        next_states += new_states
        states.pop(0)
    return next_states

def iterative_deepening(states,depth):
    while (len(states) != 0):
        #print("DEPTH: ",states[0].depth)
        state_obj = states[0]
        if (winning_state([state_obj])):
            print_journey(state_obj)
            return state_obj
        moves = legalMoves(state_obj, possible_moves)
        new_states = createStates(state_obj, moves)
        states.pop(0)
        states = new_states + states
        if(states[0].depth == depth):
            next_states = []
            while (len(states) != 0):
                state_obj = states[0]
                if(winning_state([state_obj])):
                    print_journey(state_obj)
                    return state_obj
                if(state_obj.depth == depth):
                    next_states.append(state_obj)
                    states.pop(0)
                else:
                    moves = legalMoves(state_obj, possible_moves)
                    new_states = createStates(state_obj, moves)
                    states.pop(0)
                    states = new_states + states
            depth += 3
            states = next_states









def bfs_option(states,max_depth):
    while (states[0].depth < max_depth):
        solutions_found = winning_state(states)
        for state in solutions_found:
            print_journey(state)
        if (solutions_found):
            break
        else:
            states = bfs(states)




if __name__ == '__main__':

    # Κάθε μετακίνηση που μπορεί να κάνει η βάρκα απο την μία όχθη στην άλλη
    # Κάθε πίνακας είναι της μορφής [Ιεροπόστολοι, Κανίβαλοι]
    possible_moves = [[0, 2], [0, 1], [1, 1], [1, 0], [2, 0]]

    # Η κατάσταση κατα την οποία ξεκινάμε (όλοι βρίσκονται στην αριστερά όχθη)
    initial_state = State([3,3],[0,0],"left",[],None,0)
    # Η τελική κατάσταση (όλοι βρίσκονται στην δεξία όχθη)
    #goal_state = State([0,0],[3,3],"right")

    states = [initial_state]
    max_depth = 15
    bfs_option(states,max_depth)

    iterative_deepening(states,3)






