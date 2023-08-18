#define PROGRAM_NUMBER 1111111
#define VERSION_NUMBER 1

struct person_data {
    char name[128];
    char street[128];
    char phone[128];
};

program NOTEBOOK_PROG
        {
                version NOTEBOOK_VERS
        {
            person_data INSERT (person_data) = 1;
        }
        = VERSION_NUMBER;
        }
= PROGRAM_NUMBER;


