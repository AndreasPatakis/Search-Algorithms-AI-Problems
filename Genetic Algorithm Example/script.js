const MARKED = 'marked'
const population = 100
//Πίνακας με τις θέσεις οι οποίες αποτελούν την λύση μας, σχηματίζουν το γράμμα Π στο grid
const solution_arr = [71, 64, 57, 50, 43, 36, 29, 22, 15, 8, 9, 10, 11, 12, 19, 26, 33, 40, 47, 54, 61, 68, 75]
var cellElements = document.querySelectorAll('[data-cell]')

//Η συνάρτηση η οποία εκτελείται οταν ο χρήστης πατάει το κουμπί start
//Είναι η βασική μας συνάρτηση, καλεί τα πάντα.
async function startClicked(){
    btn = document.getElementById("startBtn").disabled = true;
    var e = document.getElementById("elitism");
    var elitism_rate = e.value*0.01;
    e = document.getElementById("mutation");
    var mutation_rate = e.value*0.01;
    cleanGrid()
    var gen = initial_generation(population)
    var ranked_gen = top_N_chromosomes(gen,population)
    var gen_num = 0
    let chromo_length = ranked_gen[0][1].length
    while(!check_solution(ranked_gen[0][1],solution_arr)){
        gen_num+=1       
        updateView(gen_num,avg_fitness(ranked_gen,chromo_length))
        ranked_gen = top_N_chromosomes(gen,50).slice()
        gen = mating_pool(ranked_gen.slice(0,50),elitism_rate,mutation_rate).slice()
        cleanGrid()
        printChromosome(ranked_gen[0][1])  
        await sleep(20)
    }
    ranked_gen = top_N_chromosomes(gen,10)
    cleanGrid()
    printChromosome(ranked_gen[0][1])
    updateView(gen_num,avg_fitness(ranked_gen,chromo_length))
    btn = document.getElementById("startBtn").disabled = false;
}

//Συνάρτηση sleep προκειμένου να φαίνεται η ανανέωση των λύσεων όσο προχωρούν οι γενιές
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

//Καθαρίζει, δηλαδή κάνει το grid μας κενό
function cleanGrid(){
    cellElements.forEach(cell => {
        cell.classList.remove(MARKED)
    });
}

//Ενημερώνει τις μεταβλητές Total Generation και Best fitness score στην οθόνη του χρήστη
function updateView(gen,accuracy){
    document.getElementById("gen_num").innerHTML = "Total generations: "+gen.toString()
    document.getElementById("accuracy").innerHTML = "Average fitness score: "+accuracy.toString()+"%"
}

//Τυπώνει ενα χρωμόσωμα(μια λύση) στο grid μας
function printChromosome(chromosome){
    chromosome.forEach(cell => {
        cellElements[cell].classList.add(MARKED)
    });
}

function manhattan_distance(curr_block, target){
    //Calculationg height distance
    target_floor = Math.floor(target/7) + 1
    curr_block_floor = Math.floor(curr_block/7) + 1
    h_dist = Math.abs(target_floor-curr_block_floor) // Height distance between target block and current block
    //If the target block is above our current block
    if(target_floor < curr_block_floor){
        next_block = curr_block-(h_dist*7) //New block with the same width but with new height(height of our target block)
    }
    //If the target black is below our current block
    else if(target_floor > curr_block_floor){
        h_dist = Math.abs(target_floor-curr_block_floor)// Height distance between target block and current block
        next_block = curr_block+(h_dist*7) //New block with the same width but with new height(height of our target block)
    }
    //If both current block and target block are on the same floor
    else{
        h_dist = 0
        next_block = curr_block 
    }
    //Calculating width distance
    w_dist = Math.abs(target-next_block)
    //Final distance
    let manhattan_dist = h_dist + w_dist
    return manhattan_dist
}

//Διαστάυρωση ενός σημείου. Δέχεται δύο χρωμοσώματα, επιλέγεται τυχαία θέση ως ο ασσος στην μάσκα
//και στην συνέχεια γίνεται η διασταύρωση. Παράγονται 2 χρωμοσώματα
function crossover(chromosome1,chromosome2){
    let crossover_mask_pos = Math.floor(Math.random() * chromosome1.length)
    let new_chromosome1 = chromosome1.slice()
    let new_chromosome2 = chromosome2.slice()
    new_chromosome1[crossover_mask_pos] = chromosome2[crossover_mask_pos]
    new_chromosome2[crossover_mask_pos] = chromosome1[crossover_mask_pos]

    let new_chromos = [new_chromosome1,new_chromosome2]
    return new_chromos
}

//Μετάλλαξη ενός σημείου ενας χρωμοσώματος. Η θέση η οποία θα μεταλαχτεί καθώς και η θέση η οποία
//θα μεταλαχτεί επιλέγονται με τυχαίο τρόπο
function mutation(chromosome){
    let pos = Math.floor(Math.random() *chromosome.length)
    let value = Math.floor(Math.random() * cellElements.length)
    chromosome[pos] = value

    return chromosome
}

//Επιστρέφει σαν score ενος χρωμοσώματος την συνολική ΑΠΟΚΛΙΣΗ που είχε απο την πραγματική λύση
//Δηλαδή όσο μεγαλύτερη η τιμή η οποία θα επιστραφεί, τοσο πιο μακρία απέχει το χρωμόσωμα απο την λύση
function fitness_score(chromosome,soluton_arr){
    let total_deviation = 0
    for (let i = 0; i < chromosome.length; i++){
       /* if(!solution_arr.includes(chromosome[i])){
            total_deviation += 1
        }*/
        if(solution_arr[i] != chromosome[i]){
            total_deviation += 1
        }
    }
    return total_deviation
}

//Δέχεται τον πληθυσμό τον οποίον πρέπει να έχουν οι γενιές, και παράγει τυχαία την πρώτη γενία Ν χρωμοσωμάτων
function initial_generation(population){
    let generation = []
    for (let i = 0; i < population; i++){
        let chromosome = []
        while(chromosome.length != solution_arr.length){
            let value = Math.floor(Math.random() * cellElements.length)
            if(!chromosome.includes(value)){
                chromosome.push(value)
            }
        }
        generation.push(chromosome)
    } 
    return generation
}

//Δέχεται μια γενία και έναν αριθμό Ν και επιστρέφει τα Ν καλύτερα χρωμοσώματα της γενιάς αυτής βάση το score τους(lower is better)
function top_N_chromosomes(generation,N){
    gen_n_scores = []
    generation.forEach(chromosome =>{
        let score = fitness_score(chromosome,solution_arr)
        gen_n_scores.push([score,chromosome])
    })
    return sort2d(gen_n_scores).slice(0,N)
}

//Δέχεται μια γενία και τα score κάθε χρωμοσώματος της και επιστρέφει την ίδια γενία αλλα ταξινομημένη σε αύξουσα σειρά
//αφου όσο μικρότερο το score τόσο καλύτερη η λύση (μικρότερη απόκλιση)
function sort2d(arr){
    for(let i = 0; i < arr.length; i++){
        min_pos = i
        min_value = arr[i][0]
        for(let j = i; j < arr.length; j++){
            if(arr[j][0] <= min_value){
                min_pos = j
                min_value = arr[j][0]
            }
        }
        let temp = arr[i]
        arr[i] = arr[min_pos]
        arr[min_pos] = temp
    }
    return arr
}

//Δέχεται τα 50 καλύτερα χρωμοσώματα μιας γενίας, ενα ποσοστό ελιτισμού και ενα ενα ποσοστό μετάλλαξης
//Απο τα 50 αυτά χρωμοσώματα το ποσοτο ελιτισμού το οποίο επίλεξε ο χρήστης θα μεταφερθεί απευθείας
//στην επόμενη γενία, ενώ το μισο απο αυτο καθώς και τα υπόλοιπα χρωμοσώματα θα διασταυρωθούν για να
//παράξουν την υπόλοιπη γενία
//Απο την τελική γενία θα γίνουν μεταλλάξεις στο ποσοτό χρωμοσωμάτων το οποίο επίλεξε ο χρήστης
function mating_pool(top_genes,elitism_rate,mutation_rate){
    let next_gen = []
    //Μεταλλάξεις σε κάθε γενία
    let num_of_mutations =  Math.floor(mutation_rate * top_genes.length)
    //Ελιτισμός σε κάθε γενία
    let elitism_num = Math.floor(top_genes.length * elitism_rate)
    //Μερική ανανέωση πληθυσμού
    for(let i = 0; i < elitism_num; i++){
        next_gen.push(top_genes[i][1])
    }
    //Το μισό του πληθυσμού που πέρασε στην επόμενη γενία ως μερική ανανέωση
    //θα συμμετάσχει στην διασταύρωση
    elitism_half = Math.floor(elitism_num/2)
    for(let i = elitism_half; i < top_genes.length; i++){
        pick_chromo = Math.floor(Math.random()* top_genes.length)
        while(pick_chromo == i){
            pick_chromo = Math.floor(Math.random()* top_genes.length)
        }
        chromo = crossover(top_genes[i][1],top_genes[pick_chromo][1])
        next_gen.push(chromo[0])
        next_gen.push(chromo[1])
    }
    for(let i = 0; i < num_of_mutations; i++){
        let chromosome = Math.floor(Math.random() * next_gen.length)
        next_gen[chromosome] = mutation(next_gen[chromosome])
    }
    return next_gen
}

//Ελέγχει αν η λύση η οποία δόθηκε είναι η σωστή
function check_solution(chromosome,solution_arr){
    correct = 0
    for(let i = 0; i < chromosome.length; i++){
        if(chromosome[i] == solution_arr[i]){
            correct += 1
        }
    }
    if(correct == solution_arr.length){
        return true;
    }else{
        false;
    }
}

//Επιστρέφει το μέσο όρο καταλληλότητας κάθε γενίας
function avg_fitness(generation){
    let chromo_length = generation[0][1].length
    let avg_score = 0
    for(let i = 0; i < generation.length; i++){
        avg_score += generation[i][0]
    }
    avg_score = ((generation.length*chromo_length - avg_score)/(generation.length*chromo_length))*100
    return Math.floor(avg_score)
}
