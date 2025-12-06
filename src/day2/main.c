#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
// #include <regex.h> - not supported in windows :'( IF ONLY!
// regex expression would be "(\d+)(\1)"

typedef unsigned long long int BigNumber;

// const char relativePath[] = "../../input_files/day_2_example.txt";
const char relativePath[] = "../../input_files/day_2.txt";

const char pairSeparator = '-';
const char setSeparator =  ',';

#define MAX_STRING_LEN 1024

void raiseError(char *message){
    perror(message);
    exit(1);
}

int numPlaces (const BigNumber n) {
    if (n < 10) return 1;
    return 1 + numPlaces (n / 10);
}

BigNumber  getDigit(BigNumber  number, int digit){
    return number / (BigNumber) pow(10, digit) % 10;
}

BigNumber extractNumber(BigNumber id, int digitCount) {
    BigNumber result = 0;
    for (int x = 1; x <= digitCount; x++) {
        result = result * 10 + getDigit(id, digitCount - x);
    }
    return result;
}

BigNumber rebuildNumber(BigNumber value, int digitCount) {
    for (int x = 1; x <= digitCount; x++) {
        value = value * 10;
    }
    return value;
}

BigNumber getInvalidIdCount(char *buffer[2]) {
    BigNumber startNumber = atoll(buffer[0]);
    BigNumber endNumber = atoll(buffer[1]);

    BigNumber invalidIdCount = 0;

    for (BigNumber i = startNumber; i <= endNumber; i++) {
        int digitCount = numPlaces(i);
        if (digitCount % 2 != 0) continue;

        BigNumber extractedNumber = extractNumber(i, digitCount/2);
        BigNumber rebuiltNumber = rebuildNumber(extractedNumber, digitCount/2);
        BigNumber combinedNumber = rebuiltNumber + extractedNumber;

        if (i == combinedNumber) invalidIdCount+=i;
    }
    return invalidIdCount;
}

BigNumber fillNumber(BigNumber value, int targetDigitCount) {
    if (value == 0) return 0;
    BigNumber mostSignificantMultiplier = pow(10, targetDigitCount - numPlaces(value));
    BigNumber filledNumber = value;

    while (mostSignificantMultiplier > 1) {
        filledNumber += value * mostSignificantMultiplier;
        mostSignificantMultiplier = mostSignificantMultiplier / pow(10, numPlaces(value));
    }
    return filledNumber;
}

BigNumber dayTwo(char *buffer[2]) {
    BigNumber startNumber = atoll(buffer[0]);
    BigNumber endNumber = atoll(buffer[1]);

    BigNumber invalidIdCount = 0;

    for (BigNumber i = startNumber; i <= endNumber; i++) {
        int digitCount = numPlaces(i);

        for (int x = 1; x <= digitCount/2; x++) {
            BigNumber extractedNumber = extractNumber(i, x);
            BigNumber filledNumber = fillNumber(extractedNumber, digitCount);

            if (i == filledNumber) {
                invalidIdCount+=i;
                break;
            }
        }


    }
    return invalidIdCount;
}

char *getFileContents(char* relativePath) {
    FILE* file = fopen(relativePath, "r");
    if (file == NULL) {
        raiseError("File not found");
    }
    // get file size to create a buffer of the right size
    fseek(file, 0, SEEK_END);
    int fileSize = ftell(file);

    // reset to start of file
    rewind(file);

    // initialise buffer of correct size and read data into file
    char *fileContents = (char *)malloc(fileSize * sizeof(char));
    int x = fread(fileContents, sizeof(char), fileSize, file);
    // buffer must be null terminated!
    fileContents[x] = '\0';

    return fileContents;
}

int main() {
    char *fileContents = getFileContents(relativePath);

    // strtok uses an internal state to track how it's split a string
    // as it's being used to split two strings, we need to use strtok_r and provide our own state variable for each
    char *state1, *state2;
    char* numberPairs = strtok_r(fileContents, &setSeparator, &state1);

    // Buffer to store each line of the file.
    BigNumber dayOneCount = 0;
    BigNumber dayTwoCount = 0;
    char *pair_buffer[2];

    while (numberPairs != NULL) {
        pair_buffer[0] = strtok_r(numberPairs, &pairSeparator, &state2);
        pair_buffer[1] = strtok_r(NULL, &pairSeparator, &state2);
        dayOneCount += getInvalidIdCount(pair_buffer);
        dayTwoCount += dayTwo(pair_buffer);
        printf("Checking: %s - %s\n", pair_buffer[0], pair_buffer[1]);
        printf("----------------\n");

        numberPairs = strtok_r(NULL, &setSeparator, &state1);
    }

    printf("Day One: %llu\n", dayOneCount);
    printf("Day Two: %llu\n", dayTwoCount);
    printf("----------------\n");
    return 0;
}