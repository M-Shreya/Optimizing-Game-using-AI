#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void generate_reference_string(int reference[], int n, int num_pages) 
{
    for (int i = 0; i < n; i++) {
        reference[i] = rand() % num_pages;
    }
}

void print_reference_string(int reference[], int n) 
{
    printf("Generated Reference String: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", reference[i]);
    }
    printf("\n");
}

void fifo(int reference[], int n, int frames_count) 
{
    int frames[frames_count];
    for (int i = 0; i < frames_count; i++) frames[i] = -1;

    int page_faults = 0;
    int idx = 0;

    for (int i = 0; i < n; i++) {
        int page = reference[i];
        int found = 0;

        for (int j = 0; j < frames_count; j++) {
            if (frames[j] == page) {
                found = 1;
                break;
            }
        }

        if (!found) {
            frames[idx] = page;
            idx = (idx + 1) % frames_count;
            page_faults++;
        }

        printf("Page: %d -> ", page);
        for (int j = 0; j < frames_count; j++) {
            printf("%d ", frames[j]);
        }
        printf("\n");
    }

    printf("Total page faults: %d\n", page_faults);
}

int main() {
    srand(time(0));  // Seed for random number generation

    int frames_count, reference_length;
    printf("Enter number of frames: ");
    scanf("%d", &frames_count);

    printf("Enter the length of reference string: ");
    scanf("%d", &reference_length);

    // Generate reference string (with pages from 0 to 9)
    int reference[reference_length];
    generate_reference_string(reference, reference_length, 10);  // Assuming 10 possible pages (0-9)

    print_reference_string(reference, reference_length);

    // Call FIFO page replacement algorithm
    fifo(reference, reference_length, frames_count);

    return 0;
}
