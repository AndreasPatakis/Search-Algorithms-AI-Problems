const MARKED = 'marked'
const population = 100
//Οι 42 θεσεις για να δημιουργηθει το γραμμα Π (δυαδες αριθμων)
const solution = '7164575043362922150809101112192633404754616875'
const solution_arr = chromosomeToArray(solution)
var cellElements = document.querySelectorAll('[data-cell]')


async function startClicked(){
    cleanGrid()
    var gen = initial_generation(population)
    var best = top_N_chromosomes(gen,50)
    var gen_num = 0
    let chromo_length = best[0][1].length

    while(!check_solution(best[0][1],solution_arr)){
        gen_num+=1       
        var score = ((chromo_length-best[0][0])/chromo_length)*100
        updateView(gen_num,Math.floor(score))
        best = top_N_chromosomes(gen,50).slice()
        gen = mating_pool(best).slice()
        cleanGrid()
        printChromosome(best[0][1])  
        await sleep(20)
    }
    best = top_N_chromosomes(gen,10)
    cleanGrid()
    printChromosome(best[0][1])
    score = ((chromo_length-best[0][0])/chromo_length)*100
    console.log(score)
    updateView(gen_num,score)
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
function cleanGrid(){
    cellElements.forEach(cell => {
        cell.classList.remove(MARKED)
    });
}

function updateView(gen,accuracy){
    document.getElementById("gen_num").innerHTML = gen
    document.getElementById("accuracy").innerHTML = accuracy.toString()+"%"
}

function printChromosome(chromosome){
    chromosome.forEach(cell => {
        cellElements[cell].classList.add(MARKED)
    });
}

function chromosomeToArray(str){
    let res = str.match(/.{1,2}/g)
    for(let i=0; i<res.length;i++) res[i] = parseInt(res[i],10)
    return res
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

function crossover(chromosome1,chromosome2){
    let crossover_mask_pos = Math.floor(Math.random() * chromosome1.length)
    let new_chromosome1 = chromosome1.slice()
    let new_chromosome2 = chromosome2.slice()
    new_chromosome1[crossover_mask_pos] = chromosome2[crossover_mask_pos]
    new_chromosome2[crossover_mask_pos] = chromosome1[crossover_mask_pos]

    let new_chromos = [new_chromosome1,new_chromosome2]
    return new_chromos
}

function mutation(chromosome){
    let pos = Math.floor(Math.random() *chromosome.length)
    let value = Math.floor(Math.random() * cellElements.length)
    chromosome[pos] = value

    return chromosome
}
//Αποκλιση κάθε θέσης απο την πραγματική
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

function top_N_chromosomes(generation,N){
    gen_n_scores = []
    generation.forEach(chromosome =>{
        let score = fitness_score(chromosome,solution_arr)
        gen_n_scores.push([score,chromosome])
    })
    return sort2d(gen_n_scores).slice(0,N)
}

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

function mating_pool(top_genes){
    let next_gen = []
    //10% μεταλλάξεις σε κάθε γενία
    let num_of_mutations =  Math.floor(0.30 * top_genes.length)
    //20% ελιτισμός σε κάθε γενία
    let elitism_num = Math.floor(top_genes.length * 0.40)
    for(let i = 0; i < elitism_num; i++){
        next_gen.push(top_genes[i][1])
    }
    //Το μισό του πληθυσμού που πέρασε στην επόμενη γενία ωσ μερική ανανέωση
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

