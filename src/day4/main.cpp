#include <iostream>
#include <vector>
#include <iterator>
#include <fstream>

const std::string FILEPATH = "../../input_files/day_4_example.txt";
// const std::string FILEPATH = "../../input_files/day_4.txt";

constexpr char ROLL = '@';
constexpr char MARKED = 'X';
constexpr int MAX_ADJACENT = 3;

std::vector<std::string> fileInput;

int main() {
    std::ifstream inputFile(FILEPATH);
    std::string line;
    int totalAccessible = 0;

    while (getline(inputFile, line)) {
        // std::cout << line << "\n";
        fileInput.push_back(line);
    }

    while (true) {
        int numberRemoved = 0;
        for(std::size_t i = 0; i < fileInput.size(); ++i) {
            const bool canLookUp = (i > 0);
            const bool canLookDown = (i < (fileInput.size() - 1));

                for(std::size_t x = 0; x < fileInput[i].size(); x++) {
                    if (fileInput[i][x] != ROLL) {
                        continue;
                    }

                    const bool canLookLeft = (x > 0);
                    const bool canLookRight = (x < (fileInput[i].size() - 1));

                    const int adjacentRolls = (canLookUp && fileInput[i-1][x] == ROLL) +
                        (canLookDown && fileInput[i+1][x] == ROLL) +
                        (canLookRight && fileInput[i][x+1] == ROLL) +
                        (canLookLeft && fileInput[i][x-1] == ROLL) +
                        (canLookUp && canLookRight && fileInput[i-1][x+1] == ROLL) +
                        (canLookUp && canLookLeft && fileInput[i-1][x-1] == ROLL) +
                        (canLookDown && canLookRight && fileInput[i+1][x+1] == ROLL) +
                        (canLookDown && canLookLeft && fileInput[i+1][x-1] == ROLL);


                    if (adjacentRolls <= MAX_ADJACENT) {
                        fileInput[i][x] = MARKED;
                        totalAccessible += 1;
                        numberRemoved += 1;
                    }
                }
                std::cout << fileInput[i] << "\n";
        }
        std::cout << "Number removed: " << numberRemoved << "\n";
        if (numberRemoved == 0) {
            break;
        }

    }

    std::cout << "PROCESSING COMPLETE!!!!!" << "\n";
    std::cout << totalAccessible << "\n";
}