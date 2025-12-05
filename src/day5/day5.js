const fs = require('fs').promises;

// const filepath = "../../input_files/day_5_example.txt";
const filepath = "../../input_files/day_5.txt";

let ranges = [];

let lowestLower = 0;
let largestUpper = 0;

let ingredientIds = [];
let freshIngredientCount = 0;

function loadRanges(rangesString){
    console.log("RANGES");
    rangesString.trim().split('\r\n').forEach(range => {
        let [lower, upper] = range.trim().split('-');
        lower = parseInt(lower);
        upper = parseInt(upper);
        ranges.push([lower, upper]);
        if (lowestLower > lower || lowestLower == 0) lowestLower = lower;
        if (largestUpper < upper || lowestLower == 0) largestUpper = upper;
    });
}

async function loadFile(filepath){
    try {
        const data = await fs.readFile(filepath, 'utf8');

        let [rangesString, numbers] = data.split(/\n\s+\n/);

        loadRanges(rangesString);
        ranges = merge(ranges);

        ingredientIds = numbers.trim().split('\r\n').map(number => parseInt(number));
    } catch (err) {
        console.error('Error reading file:', err);
    }
}

function checkInBounds(ingredientId, lowerBound, upperBound){
    return lowerBound <= ingredientId && ingredientId <= upperBound;
}

function getAvailableIdCount(lowerBound, upperBound){
    return upperBound - lowerBound + 1;
}

function merge (intervals) {
    // sort first to ensure array is ascending based on lower bound
    intervals.sort((a, b) => a[0] - b[0]);

    let previous = intervals[0];
    let result = [previous];

    for (let i = 1; i < intervals.length; i++) {
        let current = intervals[i];
        if (previous[1] >= current[0]) {
            // Upper bound of previous extends past beginning of current
            // Use max to pick the largest possible upper bound
            previous[1] = Math.max(previous[1], current[1]);
        } else {
            // Ranges don't overlap
            result.push(current);
            previous = current;
        }
    }
    return result;
}

function partTwo(){
    /* Loops over the ranges and totals the available ids in each range
       NOTE: overlapping ranges must be merged to prevent double counting
     */

    console.log('------------------------');
    let freshIdCount = 0;
    ranges.forEach(range =>{
        freshIdCount += getAvailableIdCount(range[0], range[1])
    });
    console.log(`(Part 2) Total fresh IDs: ${freshIdCount}`);
}

function partOne(){
    ingredientIds.forEach(ingredientId => {
        console.log('------------------------');
        console.log(`Processing ID ${ingredientId}`);
        if(!checkInBounds(ingredientId, lowestLower, largestUpper)){
            // Prevents excessive looping if the number is out of scope of all ranges
            console.log(`ID ${ingredientId} is not in bounds ${lowestLower} - ${largestUpper}`);
            return;
        }

        for(const range of ranges){
            if(checkInBounds(ingredientId, range[0], range[1])){
                console.log(`ID ${ingredientId} is in bounds ${range[0]} - ${range[1]}`);
                freshIngredientCount++;
                return
            }
        }

        console.log(`ID ${ingredientId} is rotten`);
    })

    console.log('------------------------');
    console.log(`(Part 1) Fresh ingredient count: ${freshIngredientCount}`);
}

loadFile(filepath).then(result =>{
    partOne();
    partTwo();
});





