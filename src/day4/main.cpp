#include <iostream>
#include <vector>
#include <iterator>
#include <fstream>

// const std::string FILEPATH = "../../input_files/day_4_example.txt";
const std::string FILEPATH = "../../input_files/day_4.txt";

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

    for(std::size_t i = 0; i < fileInput.size(); ++i) {
        bool canLookUp = (i > 0);
        bool canLookDown = (i < (fileInput.size() - 1));

        for(std::size_t x = 0; x < fileInput[i].size(); x++) {
            if (fileInput[i][x] != ROLL) {
                continue;
            }

            int adjacentRolls = 0;

            bool canLookLeft = (x > 0);
            bool canLookRight = (x < (fileInput[i].size() - 1));

            if (canLookUp && fileInput[i-1][x] == ROLL) {
                adjacentRolls++;
            }
            if (canLookDown && fileInput[i+1][x] == ROLL) {
                adjacentRolls++;
            }
            if (canLookRight && fileInput[i][x+1] == ROLL) {
                adjacentRolls++;
            }
            if (canLookLeft && fileInput[i][x-1] == ROLL) {
                adjacentRolls++;
            }
            if (canLookUp && canLookRight && fileInput[i-1][x+1] == ROLL) {
                adjacentRolls++;
            }
            if (canLookUp && canLookLeft && fileInput[i-1][x-1] == ROLL) {
                adjacentRolls++;
            }
            if (canLookDown && canLookRight && fileInput[i+1][x+1] == ROLL) {
                adjacentRolls++;
            }
            if (canLookDown && canLookLeft && fileInput[i+1][x-1] == ROLL) {
                adjacentRolls++;
            }

            if (adjacentRolls <= MAX_ADJACENT) {
                totalAccessible += 1;
            }
        }
        std::cout << fileInput[i] << "\n";

    }

    std::cout << "PROCESSING COMPLETE!!!!!" << "\n";
    std::cout << totalAccessible << "\n";
}