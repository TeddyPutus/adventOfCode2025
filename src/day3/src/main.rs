use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

// const FILEPATH: &str = "../../input_files/day_3_example.txt";
const FILEPATH: &str = "../../input_files/day_3.txt";

fn main() {
    let mut result: u32 = 0;
    if let Ok(lines) = read_lines(FILEPATH) {
        for line in lines.map_while(Result::ok) {
            println!("{}", line);
            result += process_line(line);
        }
    }
    println!("Processing complete!");
    println!("Result is: {}", result);
}

fn process_line(line: String) -> u32{
    let mut largest_number: u32 = 0;
    let mut second_largest_number: u32 = 0;

    let line_length: u32 = line.chars().count().try_into().unwrap();
    let mut largest_num_index: u32 = 0;

    for (i, c) in line.chars().enumerate() {
        let current_number = c.to_digit(10).unwrap();

        if i < (line_length - 1).try_into().unwrap() {
            if current_number > largest_number {
                largest_number = current_number;
                largest_num_index = i.try_into().unwrap();
            }
        }
    }
    for (i, c) in line.chars().enumerate() {
        let current_number = c.to_digit(10).unwrap();

        if i > largest_num_index.try_into().unwrap() {
            if current_number > second_largest_number {
                second_largest_number = current_number;
            }
        }
    }

    // if current_number > largest_number && largest_number == 0{
        //     largest_number = current_number;
        // }else if current_number > second_largest_number {
        //     second_largest_number = current_number;
        // }
        //
        // if largest_number == 9 && second_largest_number == 9 {
        //     // Already found the largest possible numbers
        //     break;
        // }
    // }

    println!("Largest numbers found: {} and {}", largest_number, second_largest_number);
    println!("Returning: {}", (largest_number * 10) + second_largest_number);
    return (largest_number * 10) + second_largest_number;
}

// The output is wrapped in a Result to allow matching on errors.
// Returns an Iterator to the Reader of the lines of the file.
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
