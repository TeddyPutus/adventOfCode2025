#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// #include <regex.h> - not supported in windows :'( IF ONLY!
// regex expression would be "(\d+)(\1)"

// const char relativePath[] = "../../input_files/day_2_example.txt";
const char relativePath[] = "../../input_files/day_2.txt";

const char pairSeparator = '-';
const char setSeparator =  ',';

#define MAX_STRING_LEN 1024

void raiseError(char *message){
    perror(message);
    exit(1);
}

unsigned long long int getInvalidIdCount(char *buffer[2]) {
    int startNumber = atoi(buffer[0]);
    int endNumber = atoi(buffer[1]);

    unsigned long long int invalidIdCount = 0;

    for (int i = startNumber; i <= endNumber; i++) {
        char id[MAX_STRING_LEN];
        sprintf(id, "%d", i);

        if (strlen(id) % 2 == 0) {
            int halfLength = strlen(id) / 2;
            char firstHalf[halfLength + 1];
            char secondHalf[halfLength + 1];
            strncpy(firstHalf, id, halfLength);
            strncpy(secondHalf, id + halfLength, halfLength);
            firstHalf[halfLength] = '\0';
            secondHalf[halfLength] = '\0';

            if (atoi(firstHalf) == atoi(secondHalf)) {
                // printf("InvalidId: %s\n", id);
                invalidIdCount+= i;
            }
        }

    }
    return invalidIdCount;
}

int main() {
    FILE* file = fopen(relativePath, "r");
    if (file == NULL) {
        raiseError("File not found");
    }
    // get file size to create a buffer of the right size
    fseek(file, 0, SEEK_END);
    int fileSize = ftell(file);
    rewind(file);
    char *fileContents = (char *)malloc(fileSize * sizeof(char));
    int x = fread(fileContents, sizeof(char), fileSize, file);
    fileContents[x] = '\0';

    char *state1, *state2;
    char* numberPairs = strtok_r(fileContents, &setSeparator, &state1);

    // Buffer to store each line of the file.
    unsigned long long int invalidIdCount = 0;
    char *pair_buffer[2];

    while (numberPairs != NULL) {
        pair_buffer[0] = strtok_r(numberPairs, &pairSeparator, &state2);
        pair_buffer[1] = strtok_r(NULL, &pairSeparator, &state2);
        printf("----------------\n");
        invalidIdCount += getInvalidIdCount(pair_buffer);
        printf("%s - %s\n", pair_buffer[0], pair_buffer[1]);
        printf("InvalidIdCount: %llu\n", invalidIdCount);
        numberPairs = strtok_r(NULL, &setSeparator, &state1);
    }

    printf("----------------\n");
    invalidIdCount += getInvalidIdCount(pair_buffer);
    printf("%s - %s\n", pair_buffer[0], pair_buffer[1]);
    printf("InvalidIdCount: %llu\n", invalidIdCount);

    return 0;
}