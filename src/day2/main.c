#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef unsigned long long int BigNumber;

// const char relativePath[] = "../../input_files/day_2_example.txt";
const char relativePath[] = "../../input_files/day_2.txt";

const char pairSeparator = '-';
const char setSeparator =  ',';

void raiseError(const char *message){
    perror(message);
    exit(1);
}

int numPlaces (const BigNumber n) {
    if (n < 10) return 1;
    return 1 + numPlaces (n / 10);
}

BigNumber  getDigit(const BigNumber  number, const int digit){
    return number / (BigNumber) pow(10, digit) % 10;
}

BigNumber extractNumber(const BigNumber id, const int digitCount) {
    // Extracts digitCount digits from id. Retrieves from least significant -> most significant
    BigNumber result = 0;
    for (int x = 1; x <= digitCount; x++) {
        result = result * 10 + getDigit(id, digitCount - x);
    }
    if (numPlaces(result) != digitCount) return 0; // in this case, there was a leading zero, don't match on this
    return result;
}

BigNumber fillNumber(const BigNumber value, const int targetDigitCount) {
    // Creates a repeating pattern out of value of targetDigitCount length
    if (value == 0 || targetDigitCount % numPlaces(value) != 0) return 0;

    BigNumber mostSignificantMultiplier = (BigNumber) pow(10, targetDigitCount - numPlaces(value));
    BigNumber filledNumber = value;

    while (mostSignificantMultiplier > 1) {
        filledNumber += value * mostSignificantMultiplier;
        mostSignificantMultiplier = mostSignificantMultiplier / (BigNumber) pow(10, numPlaces(value));
    }
    return filledNumber;
}

BigNumber parseBigNum(char* number) {
    char *eptr;
    const BigNumber result = strtoll(number, &eptr, 10);
    if (eptr == number) {
        const char* errorTemplate = "Invalid input: %s";
        char errorMessage[strlen(errorTemplate) + strlen(number) + 1];
        snprintf(errorMessage, strlen(errorTemplate) + strlen(number), errorTemplate, number);
        raiseError(errorMessage);
    }
    return result;
}

void processInput(char *buffer[2], BigNumber results[2]) {
    const BigNumber startNumber = parseBigNum(buffer[0]);
    const BigNumber endNumber = parseBigNum(buffer[1]);

    for (BigNumber i = startNumber; i <= endNumber; i++) {
        const int digitCount = numPlaces(i);

        for (int x = digitCount/2; x >= 1; x--) {
            const BigNumber extractedNumber = extractNumber(i, x);

            if (i == fillNumber(extractedNumber, digitCount)) {
                if (x == digitCount/2 && digitCount % 2 == 0) {
                    // Part one requires match to be of one number repeated twice
                    // This also means an even number of digits (integer division rounds down)
                    results[0]+=i;
                }
                // Part 2 is any match
                results[1]+=i;
                break;
            }
        }
    }
}

char *getFileContents(const char* filepath) {
    FILE* file = fopen(filepath, "r");
    if (file == NULL) {
        raiseError("File not found");
    }
    // get file size to create a buffer of the right size
    fseek(file, 0, SEEK_END);
    const long fileSize = ftell(file);

    // reset to start of file
    rewind(file);

    // initialise buffer of correct size and read data into file
    char *fileContents = (char *)malloc(fileSize * sizeof(char));
    BigNumber x = fread(fileContents, sizeof(char), fileSize, file);
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
    char *pair_buffer[2];
    // results = [day1, day2]
    BigNumber results[] = {0,0};

    while (numberPairs != NULL) {
        pair_buffer[0] = strtok_r(numberPairs, &pairSeparator, &state2);
        pair_buffer[1] = strtok_r(NULL, &pairSeparator, &state2);
        printf("Checking: %s - %s\n", pair_buffer[0], pair_buffer[1]);
        processInput(pair_buffer, results);
        printf("----------------\n");

        numberPairs = strtok_r(NULL, &setSeparator, &state1);
    }

    printf("Day One: %llu\n", results[0]);
    printf("Day Two: %llu\n", results[1]);
    printf("----------------\n");

    free(fileContents);
    return 0;
}