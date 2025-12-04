use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

// const FILEPATH: &str = "../../input_files/day_3_example.txt";
const FILEPATH: &str = "../../input_files/day_3.txt";
const NUM_DIGITS: u64 = 12;

fn main() {
    let mut result: u64 = 0;
    if let Ok(lines) = read_lines(FILEPATH) {
        for line in lines.map_while(Result::ok) {
            println!("{}", line);
            result += process_line(line);
        }
    }
    println!("Processing complete!");
    println!("Result is: {}", result);
}

fn get_largest_number(line: String, line_length:u64, start_index: u64, mut first_go: bool) -> (u64,u64){
    let mut largest_number: u64 = 0;
    let mut largest_num_index: u64 = start_index;
    for (i, c) in line.chars().enumerate() {
        let current_number: u64 = c.to_digit(10).unwrap().into();

        if first_go {
            largest_number = current_number;
            largest_num_index = i.try_into().unwrap();
            first_go = false;
        }

        //we want to look at numbers in the range of: larger than start index -> start_index + (length of line - remaining digits to find)
        if (i < (line_length).try_into().unwrap()) && (i > start_index.try_into().unwrap()){
            if current_number > largest_number {
                largest_number = current_number;
                largest_num_index = i.try_into().unwrap();
            }
        }
    }
    return (largest_number, largest_num_index)
}

fn process_line(line: String) -> u64{
    let mut largest_numbers: Vec<u64> = Vec::new();

    let mut largest_number: u64 = 0;

    let line_length: u64 = line.chars().count().try_into().unwrap();
    let mut largest_num_index: u64 = 0;

    for n in 0..NUM_DIGITS {
        (largest_number, largest_num_index) = get_largest_number(line.clone(), line_length - (NUM_DIGITS - n - 1), largest_num_index, n==0);
        largest_numbers.push(largest_number);
    }

    largest_number = 0;
    for n in 0..largest_numbers.len(){
        largest_number = largest_number * 10;
        largest_number = largest_number + largest_numbers[n];
    }

    println!("Returning: {}", largest_number);
    println!("-----------------------------");
    return largest_number
}

// The output is wrapped in a Result to allow matching on errors.
// Returns an Iterator to the Reader of the lines of the file.
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
