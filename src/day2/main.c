#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// #include <regex.h> - not supported in windows :'( IF ONLY!
// regex expression would be "(\d+)(\1)"

const char relativePath[] = "../../input_files/day_2_example.txt";
// const char relativePath[] = "../../input_files/day_2.txt";

const char pairSeparator = '-';
const char setSeparator =  ',';

#define MAX_STRING_LEN 1024

int getPairFromFile(FILE* file, char *buffer[2]) {
    char ch;

    char extractedNumber[MAX_STRING_LEN] = "\0";
    int index = 0;

    while ((ch = fgetc(file)) != EOF) {
        if (ch == pairSeparator) {
            index = 0;
            buffer[0] = strdup(extractedNumber);
            extractedNumber[0] = '\0';

        }else if (ch == setSeparator) {
            // two numbers retrieved
            buffer[1] = strdup(extractedNumber);
            return 0;
        }else if (ch != '\n') {
            extractedNumber[index] = ch;
            index++;
        }
    }

    if (ch == EOF) {
        return 1;
    }
    return 0;
}

void resetBuffer(char *buffer[2]) {
    buffer[0] = (char *)malloc(MAX_STRING_LEN * sizeof(char));
    buffer[1] = (char *)malloc(MAX_STRING_LEN * sizeof(char));
}

void raiseError(char *message){
    perror(message);
    exit(1);
}

int getInvalidIdCount(char *buffer[2]) {
    int startNumber = atoi(buffer[0]);
    int endNumber = atoi(buffer[1]);

    int invalidIdCount = 0;

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

            if (strcmp(firstHalf, secondHalf) == 0) {
                printf("InvalidId: %s\n", id);
                invalidIdCount+= atoi(id);
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

    // Buffer to store each line of the file.
    char *pair_buffer[2];
    resetBuffer(pair_buffer);
    int result;
    int invalidIdCount = 0;

    while ((result = getPairFromFile(file, pair_buffer)) == 0) {
        printf("----------------\n");
        invalidIdCount += getInvalidIdCount(pair_buffer);
        printf("%s - %s\n", pair_buffer[0], pair_buffer[1]);
        printf("InvalidIdCount: %d\n", invalidIdCount);
        resetBuffer(pair_buffer);
    }

    return 0;
}