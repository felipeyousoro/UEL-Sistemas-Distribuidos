#define PROGRAM_NUMBER 69420
#define VERSION_NUMBER 1

#define NAME_SIZE 128
#define ADDRESS_SIZE 128
#define PHONE_SIZE 128

struct person_data {
    char name[NAME_SIZE];
    char address[ADDRESS_SIZE];
    char phone[PHONE_SIZE];
};

program NOTEBOOK_PROG
        {
                version NOTEBOOK_VERS
        {
            void INSERT(person_data) = 1;
            person_data LOOKUP(person_data) = 2;
            void RESET() = 3;
            void DELETE(person_data) = 4;
            void UPDATE(person_data) = 5;
        }
        = VERSION_NUMBER;
        }
= PROGRAM_NUMBER;


