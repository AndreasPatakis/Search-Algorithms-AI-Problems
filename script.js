const MARKED = 'marked'
const population = 100
//Οι 42 θεσεις για να δημιουργηθει το γραμμα Π (δυαδες αριθμων)
const solution = '71386750414292215161718192633404754616875'
const solution_arr = chromosomeToArray(solution)
var cellElements = document.querySelectorAll('[data-cell]')


function startClicked(){
    gen = initial_generation(population)
    best = pick_parents(gen)
    printChromosome(best[0][1])
}

function cleanGrid(){
    cellElements.forEach(cell => {
        cell.classList.remove(MARKED)
    });
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

function addZero(str){
    if(str.length == 1){
        str = "0"+str
    }
    return str
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
function fitness_score(chromosome,solution_arr){
    let total_deviation = 0
    for (let i = 0; i < chromosome.length; i++){
        total_deviation += manhattan_distance(chromosome[i],solution_arr[i])
    }
    return total_deviation
}

function initial_generation(population){
    let generation = []
    for (let i = 0; i < 100; i++){
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

function pick_parents(generation){
    gen_n_scores = []
    generation.forEach(chromosome =>{
        let score = fitness_score(chromosome,solution_arr)
        gen_n_scores.push([score,chromosome])
    })
    return sort2d(gen_n_scores)
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


