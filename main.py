# Η συγκεκριμένη κλάση περιέχει όλες τις χρήσιμες πληροφορίες για τις καταστάσεις οι οποίες μπορούν να προκύψουν στο παιχνίδι.
# Κάθε αντικείμενο της κλάσης αυτής είναι δηλαδή μια κατάσταση του παιχνιδιού
class State:
    def __init__(self,left_bank,right_bank,side,previous_move,previous_state,depth):
        self.left_bank = left_bank
        self.right_bank = right_bank
        self.side = side
        self.previous_move = previous_move
        self.previous_state = previous_state
        self.depth = depth


#Επιστρέφει τις επιτρεπτές μεταθέσεις τις οποίες μπορεί να κάνει η βάρκα
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

#Ελέγχει οτι καθόλη την διάρκεια των μετακινήσεων, οι Κανίβαλοι και οι Ιεροπόστολοι παραμένουν πάντα 3 και 3
def permissible(mis,can):
    mis_allowed = False
    can_allowed = False
    if( (mis[0] >= 0 and mis[0] <= 3) and (mis[1] >= 0 and mis[1] <= 3) ):
        mis_allowed = True
    if( (can[0] >= 0 and can[0] <= 3) and (can[1] >= 0 and can[1] <= 3) ):
        can_allowed = True
    return mis_allowed and can_allowed

#Υλοποιεί μια μεταφορά και επιστρέφει το αποτέλεσμα της
#Δηλαδή πόσοι Κανίβαλοι,Ιεροπόστολοι ειναι αριστερά και δεξία και σε ποίο σημείο βρίσκεται η βάρκα
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

#Δημιουργεί όλες τις καταστάσεις που μπορούν να προκύψουν απο την τρέχουσα κατάσταση (βάση των κινήσεων οι οποίες επιτρέπεται να γίνουν)
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

#Τυπώνει την όλες τις κινήσεις οι οποίες έγιναν για να οδηγηθούμε στην λύση(ή σε κάποια αλλη κατάσταση)
def print_journey(state_obj):
    states = []
    state = state_obj
    print("\nSOLUTION FOUND IN TREE DEPTH: ",state.depth)
    print("\nOur Journey:\n")
    while(state != None):
        states.append(state)
        state = state.previous_state
    states.reverse()
    for pos in range(1,len(states)):
        if((pos-1) % 2 == 0):
            print(states[pos-1].left_bank," --> Transfer:",states[pos].previous_move," --> ",states[pos-1].right_bank)
        else:
            print(states[pos-1].left_bank," <-- Transfer:",states[pos].previous_move," <-- ",states[pos-1].right_bank)
        print(states[pos].left_bank," -- Current State -- ",states[pos].right_bank)
    if(states[-1].left_bank == [0,0] and states[-1].right_bank == [3,3]):
        print("[0, 0] -- FINAL STATE PROBLEM SOLVED! -- [3, 3]")

#Δέχεται καταστάσεις και επιστρέφει εκείνες οι οποίες αποτελούν λύση(αν υπάρχουν)
def winning_state(states):
    solutions = []
    for state_obj in states:
        if(state_obj.right_bank == [3,3]):
            solutions.append(state_obj)
    return solutions

#Ελέγχει αν ο τύπος δεδομένου ο οποίος δόθηκε αντιστοιχεί σε ακέραιο αριθμό
def is_int(num):
    try:
        value = int(num)
        return True
    except ValueError:
        print("Input must be an integer.")
        return False

#Ελέγχει αν το περιεομενο της απάντησης είναι το αποδεκτό
def continue_searching():
    ans = input("\nDo you want me to look for another solution?[Y/n]: ")
    while(ans != "y" and ans != "yes" and ans != "n" and ans != "no"):
        ans = input("Please type yes or no: ")
    if(ans == "yes" or ans == "y"):
        return True
    else:
        print("\nByee!")
        return False


# Η υλοποίηση του αλγορίθμου Αναζήτηση Πρώτα σε Πλάτος(Breadth-First Search)
def bfs(states):
    next_states = []
    while(len(states) != 0):
        state_obj = states[0]
        if (winning_state([state_obj])):
            print_journey(state_obj)
            if(continue_searching() == False):
                return state_obj
        moves = legalMoves(state_obj,possible_moves)
        new_states = createStates(state_obj,moves)
        #next_states += new_states
        states += new_states
        states.pop(0)
    return next_states

# Η υλοποίηση του αλγορίθμου Επαναληπτικής Εκβάθυνσης(Iterative Deepening)
def iterative_deepening(states,depth):
    while (len(states) != 0):
        #print("DEPTH: ",states[0].depth)
        state_obj = states[0]
        if (winning_state([state_obj])):
            print_journey(state_obj)
            if(continue_searching() == False):
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
                    if(continue_searching() == False):
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


#Εμφανίζει τα αρχικά μηνύματα στον χρήστη και εκτελεί τον αλγόριθμο αναζήτης τον οποίο θα επιλέξει
def options_and_exec(states):
    print("\nHELLO!\nWelcome to Missionaries and Cannibals game solver.\n"+
    "\nTo find a solution using Breadth-First Search algorithm type 1."+
    "\nTo find a solution using Iterative Deepening algorithm type 2.")
    algo = input("\nChoose algorithm: ")
    while(is_int(algo) == False):
        algo = input("Choose algorithm: ")
    algo = int(algo)
    while(algo != 1 and algo != 2):
        print("Please choose one of the options 1 and 2\n")
        algo = int(input("Choose algorithm: "))
    if(algo == 1):
        print("\n---Breadth-First Search---\n")
        bfs(states)
    else:
        print("\n---Iterative Deepening---\n")
        iterative_deepening(states,3)



if __name__ == '__main__':

    # Κάθε μετακίνηση που μπορεί να κάνει η βάρκα απο την μία όχθη στην άλλη
    # Κάθε πίνακας είναι της μορφής [Ιεροπόστολοι, Κανίβαλοι]
    possible_moves = [[0, 2], [0, 1], [1, 1], [1, 0], [2, 0]]

    # Η κατάσταση κατα την οποία ξεκινάμε (όλοι βρίσκονται στην αριστερά όχθη)
    initial_state = State([3,3],[0,0],"left",[],None,0)

    # Η τελική κατάσταση (όλοι βρίσκονται στην δεξία όχθη)
    #goal_state = State([0,0],[3,3],"right")

    states = [initial_state]
    options_and_exec(states)
