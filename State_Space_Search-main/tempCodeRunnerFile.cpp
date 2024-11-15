#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define REFERENCE_LENGTH 20
#define NUM_PAGES 10

void generate_reference_string(int *ref_string) 
{
    for (int i = 0; i < REFERENCE_LENGTH; i++) 
    {
        ref_string[i] = rand() % NUM_PAGES;
    }

    printf("Generated string: \n");
    for (int i = 0; i < REFERENCE_LENGTH; i++) 
    {
        printf("%d ", ref_string[i]);
    }
}

int fifo(int *ref_string, int frames) 
{
    int page_faults = 0;
    int queue[frames];
    int front = 0, rear = 0, count = 0;

    for (int i = 0; i < REFERENCE_LENGTH; i++) {
        int page = ref_string[i];
        int found = 0;

        for (int j = 0; j < count; j++) {
            if (queue[j] == page) {
                found = 1;
                break;
            }
        }

        if (!found) 
        {
            if (count == frames) 
            {
                front = (front + 1) % frames;
                count--;
            }
            queue[rear] = page;
            rear = (rear + 1) % frames;
            count++;
            page_faults++;
        }
    }
    return page_faults;
}

int optimal(int *ref_string, int frames) 
{
    int page_faults = 0;
    int page_frames[frames];

    for (int i = 0; i < frames; i++) {
        page_frames[i] = -1;
    }

    for (int i = 0; i < REFERENCE_LENGTH; i++) {
        int page = ref_string[i];
        int found = 0;

        for (int j = 0; j < frames; j++) {
            if (page_frames[j] == page) {
                found = 1;
                break;
            }
        }

        if (!found) {
            if (i >= frames) {
                int farthest = -1, replace_index = 0;
                for (int j = 0; j < frames; j++) {
                    int future_index = -1;
                    for (int k = i + 1; k < REFERENCE_LENGTH; k++) {
                        if (page_frames[j] == ref_string[k]) {
                            future_index = k;
                            break;
                        }
                    }
                    if (future_index == -1 || future_index > farthest) {
                        farthest = future_index;
                        replace_index = j;
                    }
                }
                page_frames[replace_index] = page;
            } else {
                page_frames[i] = page;
            }
            page_faults++;
        }
    }
    return page_faults;
}

int lru_stack(int *reference_string, int frames) {
    int page_faults = 0;
    int stack[frames], stack_size = 0;

    for (int i = 0; i < REFERENCE_LENGTH; i++) {
        int page = reference_string[i];
        int found = 0;

        for (int j = 0; j < stack_size; j++) {
            if (stack[j] == page) {
                found = 1;
                for (int k = j; k < stack_size - 1; k++) {
                    stack[k] = stack[k + 1];
                }
                stack[stack_size - 1] = page;
                break;
            }
        }

        if (!found) {
            if (stack_size == frames) {
                for (int k = 0; k < stack_size - 1; k++) {
                    stack[k] = stack[k + 1];
                }
                stack[stack_size - 1] = page;
            } else {
                stack[stack_size++] = page;
            }
            page_faults++;
        }
    }
    return page_faults;
}

int lru_clock(int *reference_string, int frames) {
    int page_faults = 0;
    int page_frames[frames];
    int reference_bits[frames];
    int clock_pointer = 0;

    for (int i = 0; i < frames; i++) {
        page_frames[i] = -1;
        reference_bits[i] = 0;
    }

    for (int i = 0; i < REFERENCE_LENGTH; i++) {
        int page = reference_string[i];
        int found = 0;

        for (int j = 0; j < frames; j++) {
            if (page_frames[j] == page) {
                reference_bits[j] = 1;
                found = 1;
                break;
            }
        }

        if (!found) {
            while (reference_bits[clock_pointer] == 1) {
                reference_bits[clock_pointer] = 0;
                clock_pointer = (clock_pointer + 1) % frames;
            }

            page_frames[clock_pointer] = page;
            reference_bits[clock_pointer] = 1;
            clock_pointer = (clock_pointer + 1) % frames;
            page_faults++;
        }
    }
    return page_faults;
}

int second_chance(int *reference_string, int frames) {
    int page_faults = 0;
    int page_frames[frames];
    int modify_bits[REFERENCE_LENGTH];
    int reference_bits[frames];
    int clock_pointer = 0;

    for (int i = 0; i < frames; i++) {
        page_frames[i] = -1;
        reference_bits[i] = 0;
    }

    for (int i = 0; i < REFERENCE_LENGTH; i++) {
        modify_bits[i] = rand() % 2;
        int page = reference_string[i];
        int found = 0;

        for (int j = 0; j < frames; j++) {
            if (page_frames[j] == page) {
                reference_bits[j] = 1;
                found = 1;
                break;
            }
        }

        if (!found) {
            while (reference_bits[clock_pointer] == 1) {
                reference_bits[clock_pointer] = 0;
                clock_pointer = (clock_pointer + 1) % frames;
            }

            page_frames[clock_pointer] = page;
            reference_bits[clock_pointer] = modify_bits[i];
            clock_pointer = (clock_pointer + 1) % frames;
            page_faults++;
        }
    }
    return page_faults;
}

int main(int argc, char *argv[]) 
{
    
    if (argc != 2) {
        printf("Usage: %s <number_of_frames>\n", argv[0]);
        return 1;
    }

    int frames = atoi(argv[1]);
    int reference_string[REFERENCE_LENGTH];
    srand(time(NULL));
    generate_reference_string(reference_string);

    printf("Generated Reference String: ");
    for (int i = 0; i < REFERENCE_LENGTH; i++) {
        printf("%d ", reference_string[i]);
    }
    printf("\n");

    int choice;
    do 
    {
        printf("\n1. FIFO\n2. Optimal\n3. LRU (Stack)\n4. LRU (Clock)\n5. Second Chance\n6. Exit\n");
        printf("Enter choice (1-6): ");
        scanf("%d", &choice);

        int page_faults = 0;
        switch (choice) {
            case 1:
                page_faults = fifo(reference_string, frames);
                printf("FIFO Page Faults: %d\n", page_faults);
                break;
            case 2:
                page_faults = optimal(reference_string, frames);
                printf("Optimal Page Faults: %d\n", page_faults);
                break;
            case 3:
                page_faults = lru_stack(reference_string, frames);
                printf("LRU (Stack) Page Faults: %d\n", page_faults);
                break;
            case 4:
                page_faults = lru_clock(reference_string, frames);
                printf("LRU (Clock) Page Faults: %d\n", page_faults);
                break;
            case 5:
                page_faults = second_chance(reference_string, frames);
                printf("Second Chance Page Faults: %d\n", page_faults);
                break;
            case 6:
                printf("Exiting program.\n");
                break;
            default:
                printf("Invalid choice\n");
        }
    } while (choice != 6);

    return 0;
}
