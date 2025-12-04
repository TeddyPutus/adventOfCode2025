#include <iostream>
#include <vector>
#include <iterator>
#include <fstream>

const std::string FILEPATH = "../../input_files/day_4_example.txt";
// const std::string FILEPATH = "../../input_files/day_4.txt";

constexpr char ROLL = '@';
constexpr char MARKED = 'X';
constexpr int MAX_ADJACENT = 3;

enum MODE {ONCE, FOREVER};
constexpr MODE RUN_MODE = ONCE; // part 1
// constexpr MODE RUN_MODE = FOREVER; // part 2


std::vector<std::string> fileInput;

bool whileCondition(const int loopCount, const MODE runMode) {
    if (runMode == FOREVER) {
        return true;
    }
    return loopCount < 1;
}

void loadFile() {
    std::ifstream inputFile(FILEPATH);
    std::string line;

    while (getline(inputFile, line)) {
        fileInput.push_back(line);
    }
}

int main() {
    int totalAccessible = 0;
    int loopCount = 0;

    loadFile();

    while (whileCondition(loopCount, RUN_MODE)) {
        int numberRemoved = 0;
        for(std::size_t i = 0; i < fileInput.size(); ++i) {
            const bool canLookUp = i > 0;
            const bool canLookDown = i < fileInput.size() - 1;

                for(std::size_t x = 0; x < fileInput[i].size(); x++) {
                    if (fileInput[i][x] != ROLL) {
                        continue;
                    }

                    const bool canLookLeft = x > 0;
                    const bool canLookRight = x < fileInput[i].size() - 1;

                    const int adjacentRolls = (canLookUp && fileInput[i-1][x] == ROLL) +
                        (canLookDown && fileInput[i+1][x] == ROLL) +
                        (canLookRight && fileInput[i][x+1] == ROLL) +
                        (canLookLeft && fileInput[i][x-1] == ROLL) +
                        (canLookUp && canLookRight && fileInput[i-1][x+1] == ROLL) +
                        (canLookUp && canLookLeft && fileInput[i-1][x-1] == ROLL) +
                        (canLookDown && canLookRight && fileInput[i+1][x+1] == ROLL) +
                        (canLookDown && canLookLeft && fileInput[i+1][x-1] == ROLL);


                    if (adjacentRolls <= MAX_ADJACENT) {
                        if (RUN_MODE == FOREVER) {
                            fileInput[i][x] = MARKED;
                        }

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
        loopCount++;
    }

    std::cout << "PROCESSING COMPLETE!!!!!" << "\n";
    std::cout << totalAccessible << "\n";
}