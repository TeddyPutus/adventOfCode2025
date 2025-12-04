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

enum HORIZONTAL {LEFT=-1, H_CENTRE=0, RIGHT=1};
enum VERTICAL {UP=-1, V_CENTRE=0, DOWN=1};

std::vector<std::string> fileInput;

bool checkChar(const int column, const int row, const VERTICAL vertical, const HORIZONTAL horizontal) {
    const bool canHorizontal = 0 <= column + horizontal && column + horizontal <= fileInput[0].size();
    const bool canVertical = 0 <= row + vertical && row + vertical <= fileInput.size()-1;

    return canHorizontal && canVertical && fileInput[row+vertical][column+horizontal] == ROLL;
}

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

int getAdjacentRolls(const int column, const int row) {
    return  checkChar(column, row, UP, H_CENTRE) +
            checkChar(column, row, DOWN, H_CENTRE) +
            checkChar(column, row, V_CENTRE, RIGHT) +
            checkChar(column, row, V_CENTRE, LEFT) +
            checkChar(column, row, UP, RIGHT) +
            checkChar(column, row, UP, LEFT) +
            checkChar(column, row, DOWN, RIGHT) +
            checkChar(column, row, DOWN, LEFT);
}

void markSpot(const MODE runMode, const int row, const int column) {
    if (runMode == FOREVER) {
        fileInput[row][column] = MARKED;
    }
}

int main() {
    int totalAccessible = 0;
    int loopCount = 0;

    loadFile();

    while (whileCondition(loopCount, RUN_MODE)) {
        int numberRemoved = 0;
        for(std::size_t row = 0; row < fileInput.size(); ++row) {

                for(std::size_t column = 0; column < fileInput[row].size(); column++) {
                    if (fileInput[row][column] != ROLL) {
                        continue;
                    }

                    if (const int adjacentRolls = getAdjacentRolls(column, row); adjacentRolls <= MAX_ADJACENT) {
                        markSpot(RUN_MODE, row, column);
                        totalAccessible += 1;
                        numberRemoved += 1;
                    }
                }
                std::cout << fileInput[row] << "\n";
        }
        std::cout << "Number removed: " << numberRemoved << "\n";
        if (numberRemoved == 0) {
            // Nothing left to remove (specific to part 2)
            break;
        }
        loopCount++;
    }

    std::cout << "PROCESSING COMPLETE!!!!!" << "\n";
    std::cout << totalAccessible << "\n";
}