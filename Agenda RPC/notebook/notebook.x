#define PROGRAM_NUMBER 69420
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
            void INSERT(person_data) = 1;
            person_data LOOKUP(person_data) = 2;
        }
        = VERSION_NUMBER;
        }
= PROGRAM_NUMBER;


