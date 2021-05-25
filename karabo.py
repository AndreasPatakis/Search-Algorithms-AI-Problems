import random
import time
import copy


#the letter "K" for Karampoikis
END_GRID = [0,6,0,5,0,4,0,3,0,2,0,1,0,2,0,3,0,4,0,5,0,6]

POPULATION = 100

#Το Ν (0-1) του πληθυσμού θα μεταφερθεί απευθείας στην επόμενη γενιά
ELITISM_RATE = 0.3

#Ποσοστό μετάλλαξης σε κάθε γενιά. Π.χ αν έχουμε 100 πληθυσμό, με 0.3 MUTATION_RATE
#θα γίνει μια αλλαγή σε ένα σημείο(θα αλλάξει ενας ασσος τυχαία) σε 0.3*100 = 30 grid απο τα 100
#που έχει η γενιά
MUTATION_RATE = 0.1

#evaluation function
def eval_fun(end_grid, current_grid):
    correct = 0
    #11 λιστες, απο 2 ασσους η κάθε μια
    total_ones = len(end_grid)
    for i in range(total_ones):
        if(end_grid[i] == current_grid[i]):
            correct += 1
    return correct/total_ones

def sort_desc(gen):
    l = len(gen)
    for i in range(0, l):
        for j in range(0, l-i-1):
            if (gen[j][1] < gen[j + 1][1]):
                tempo = gen[j]
                gen[j]= gen[j + 1]
                gen[j + 1]= tempo
    return gen

def score_generation(end_grid,generation):
    for i,grid in enumerate(generation):
        score_grid = eval_fun(end_grid,grid[0])
        generation[i][1] = score_grid
    sorted_gen = sort_desc(generation)
    return sorted_gen

#Θες μονο δύο άσσους σε καθε γραμμή του grid
def generate_grid():
    grid = []
    for i in range(22):
        grid.append(random.randint(0,6))
    return grid

#geneating random genetic pool
def generate_gen(population):
    gen = []
    for g in range(population):
        grid = generate_grid()
        #[grid,βαθμολογία grid]
        gen.append([grid, 0])
    return gen

#Για κάθε ενα απο τα σκορ υπολογίζει μια πιθανότητα εμφάνισης, δίνοντας μεγαλύτερη πιθανότητα
#επιλογής στα υψηλότερα score
def set_odds(gen):
    #Καθε σκορ επιλέγεται μια φορά
    distinct_scores = []
    for score in gen:
        if(score[1] not in distinct_scores):
            distinct_scores.append(score[1])

    total_scores = 0
    for score in distinct_scores:
        total_scores += int(score*100)

    odds_by_score = []
    for grid in gen:
        exists = False
        odd = (int(grid[1]*100)/total_scores)*100
        for score in odds_by_score:
            if score[0] == grid[1]:
                exists = True
        if not exists:
            odds_by_score.append([grid[1],0,odd])

    for i in range(1,len(odds_by_score)):
        odds_by_score[i] = [odds_by_score[i][0],odds_by_score[i-1][2],odds_by_score[i-1][2]+odds_by_score[i][2]]
    for i in range(0,len(odds_by_score)):
        odds_by_score[i][1] = int(odds_by_score[i][1])
        odds_by_score[i][2] = int(odds_by_score[i][2])
    return odds_by_score

def pick_grid(gen,odds):
    max_num = odds[-1][2]
    number = random.randint(0,max_num-1)
    for odd in odds:
        if number >= odd[1] and number < odd[2]:
            score_selected = odd[0]
            break
    candidates = []
    for grid in gen:
        if grid[1] == score_selected:
            candidates.append(grid)
        elif grid[1] < score_selected:
            break
    grid_pos = random.randint(0,len(candidates)-1)
    return gen[grid_pos]

#Εδώ θα γίνουν οι απαραίτητες διαδικασίες για την παραγωγή της επόμενης γενιάς
#Θα έχουμε ενα ποσοστό μερικής ανανέωσης (elitism_rate) και ενα ποσοστό μετάλλαξης(mutation_rate)
def mating_pool(current_gen,elitism_rate,mutation_rate):
    population = len(current_gen)
    next_gen = []
    population_to_copy = int(elitism_rate*population)
    for i in range(population_to_copy):
        next_gen.append([current_gen[i][0],0])
    gen_odds = set_odds(current_gen)

    #Εδώ γίνεται η διασταύρωση
    while(len(next_gen) < population):
        grid1 = pick_grid(current_gen,gen_odds)
        grid2 = pick_grid(current_gen,gen_odds)
        # while(grid1[0] == grid2[0]):
        #     grid1 = pick_grid(current_gen,gen_odds)
        #     grid2 = pick_grid(current_gen,gen_odds)
        children = crossover(grid1[0],grid2[0])
        for child in children:
            next_gen.append([child,0])

    #Εδώ γίνονται οι μεταλλάξεις
    mutations = int(mutation_rate*population)
    for i in range(mutations):
        grid_pos = random.randint(0,21)
        next_gen[grid_pos] = mutation(next_gen[grid_pos][0])
    return next_gen

def crossover(grid1,grid2):
    crossover_mask_pos = random.randint(0,len(grid1)-1)
    new_grid1 = grid1.copy()
    new_grid2 = grid2.copy()

    new_grid1[crossover_mask_pos] = grid2[crossover_mask_pos]
    new_grid2[crossover_mask_pos] = grid1[crossover_mask_pos]

    return [new_grid1,new_grid2]

def mutation(grid):
    grid_mask_pos = random.randint(0,21)
    grid_value = random.randint(0,6)
    grid[grid_mask_pos] = grid_value

    return [grid,0]

def nice_print(grid):
    print('-'*40)
    for i in range(0,len(grid)-1,2):
        for j in range(7):
            if grid[i] == j or grid[i+1] == j:
                print("#",end=" ")
            else:
                print("-",end=" ")
        print("\n")

def is_solution(grid):
    if(grid[1] == 1.0):
        return True
    else:
        return False




#STARTING PROGRAMM

if __name__ == '__main__':


    # init_gen = generate_gen(POPULATION)
    # init_gen_scored = score_generation(END_GRID,init_gen)
    # next_gen = mating_pool(init_gen_scored,ELITISM_RATE,MUTATION_RATE)
    # next_gen_scored = score_generation(END_GRID,next_gen)

    gen = generate_gen(POPULATION)
    gen_scored = score_generation(END_GRID,gen)
    gen_num = 1
    print("\nFIRST GENERATION.\n")
    nice_print(gen_scored[0][0])
    while(not is_solution(gen_scored[0])):
        gen_num += 1
        gen = mating_pool(gen_scored,ELITISM_RATE,MUTATION_RATE)
        gen_scored = score_generation(END_GRID,gen)
        print("Generation = ",gen_num," Accuracy: ",gen_scored[0][1])
        if gen_num%7 == 0:
            nice_print(gen_scored[0][0])
    print("\n")
    print("-"*40)
    print("\n SOLUTION FOUND IN ",gen_num," GENERATIONS.\n")
    nice_print(gen_scored[0][0])







    # init_gen = generate_gen(POPULATION)
    # init_gen_scored = score_generation(END_GRID,init_gen)
    # print(init_gen_scored[0][1])
    #
    # next_gen = mating_pool(init_gen_scored,ELITISM_RATE,MUTATION_RATE)
    # next_gen_scored = score_generation(END_GRID,next_gen)
    # print(next_gen_scored[0][1])


    # random.seed(a = None, version = 2)
    # pool = generate_gen(POPULATION)
    # i = 0
    # to_change = int(POPULATION / 5)
    # while(True):
    #     tmp = []
    #     roulette_generator(END_GRID, pool)
    #     for j in range(0, int(POPULATION/2)):
    #         pair = chooseParents(END_GRID, pool)
    #         children = mateParents(pair)
    #         tmp.append(children[0])
    #         tmp.append(children[1])
    #     pool = tmp.copy()
    #     i += 1
    #     roulette_generator(END_GRID, pool)
    #     if(i % 10 == 0):
    #         for j in range(0, to_change):
    #             g = generate_grid()
    #             pool[POPULATION -j -1][0] = g.copy()
    #     e = eval_fun(END_GRID, pool[0][0])
    #     print(e)
    #     if( e >= 0.7 ):
    #         nice_print()
    #         break
    #     else:
    #         for i in range(POPULATION):
    #             nice_print(pool[0])
