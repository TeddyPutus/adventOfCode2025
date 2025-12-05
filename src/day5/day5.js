const fs = require('fs').promises;

// const filepath = "../../input_files/day_5_example.txt";
const filepath = "../../input_files/day_5.txt";

let ranges = [];
let lowerBoundaries = [];
let upperBoundaries = [];
let boundaryMap = {};

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


        // not sure what shape i want yet
        ranges.push([lower, upper]);
        // possibly order these??
        lowerBoundaries.push(lower);
        upperBoundaries.push(upper);
        boundaryMap[lower] = upper;

        if (lowestLower > lower || lowestLower == 0) lowestLower = lower;
        if (largestUpper < upper || lowestLower == 0) largestUpper = upper;
    });

    console.log(ranges);
    console.log(lowerBoundaries);
    console.log(upperBoundaries);
    console.log(boundaryMap);
    console.log(lowestLower);
    console.log(largestUpper);
}

async function loadFile(filepath){

    try {
        const data = await fs.readFile(filepath, 'utf8');

        let [ranges, numbers] = data.split(/\n\s+\n/);

        loadRanges(ranges);

        ingredientIds = numbers.trim().split('\r\n').map(number => parseInt(number));
    } catch (err) {
        console.error('Error reading file:', err);
    }
}

function checkInBounds(ingredientId, lowerBound, upperBound){
    return lowerBound <= ingredientId && ingredientId <= upperBound;
}


loadFile(filepath).then(result =>{
    console.log(ingredientIds)
    ingredientIds.forEach(ingredientId => {
        console.log('------------------------');
        console.log(`Processing ID ${ingredientId}`);
        if(!checkInBounds(ingredientId, lowestLower, largestUpper)){
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
    console.log(`Fresh ingredient count: ${freshIngredientCount}`);
});





