#include <stdio.h>
#include <assert.h>

#include "../notebook/notebook.h"
#include "../person/person.h"

char *DATABASE_NAME = "database/database-name.txt";
char *DATABASE_ADDRESS = "database/database-phone.txt";
char *DATABASE_PHONE = "database/database-address.txt";

void *insert_1_svc(person_data *p, struct svc_req *rqstp) {
    FILE *fname = fopen(DATABASE_NAME, "a");
    FILE *faddress = fopen(DATABASE_ADDRESS, "a");
    FILE *fphone = fopen(DATABASE_PHONE, "a");

    fprintf(fname, "%s\n", p->name);
    fprintf(faddress, "%s\n", p->address);
    fprintf(fphone, "%s\n", p->phone);

    fclose(fname);
    fclose(faddress);
    fclose(fphone);

    static int result = 1;
    return (void *) &result;
}

void *reset_1_svc(void *null, struct svc_req *rqstp) {
    FILE *fname = fopen(DATABASE_NAME, "w");
    FILE *faddress = fopen(DATABASE_ADDRESS, "w");
    FILE *fphone = fopen(DATABASE_PHONE, "w");

    fclose(fname);
    fclose(faddress);
    fclose(fphone);

    static int result = 1;
    return (void *) &result;
}

static long get_name_index(char *name) {
    FILE *fname = fopen(DATABASE_NAME, "r");
    int found = 0; long index = 0;
    while (1) {
        char buffer[NAME_SIZE];
        fgets(buffer, NAME_SIZE, fname);
        if(feof(fname)) break;

        buffer[strlen(buffer) - 1] = '\0';

//        for(int i = 0; i < strlen(buffer); i++) {
//            printf("%d ", buffer[i]);
//        }
//        printf("\n");
//        for(int i = 0; i < strlen(name); i++) {
//            printf("%d ", name[i]);
//        }
//        printf("||||||||||||||||||\n");

        if (strcmp(buffer, name) == 0) {
            found = 1;
            break;
        }

        index++;
    }
    fclose(fname);

    return (found == 1) ? index : -1;
}

static void build_person_data(person_data *p, long index) {
    FILE *fname = fopen(DATABASE_NAME, "r");
    FILE *faddress = fopen(DATABASE_ADDRESS, "r");
    FILE *fphone = fopen(DATABASE_PHONE, "r");

    int i = 0;
    while (1) {
        char name[NAME_SIZE], address[ADDRESS_SIZE], phone[PHONE_SIZE];
        fgets(name, NAME_SIZE, fname);
        fgets(address, ADDRESS_SIZE, faddress);
        fgets(phone, PHONE_SIZE, fphone);
        if (feof(fname) || feof(faddress) || feof(fphone)) break;

        if (i == index) {
            name[strlen(name) - 1] = '\0';
            address[strlen(address) - 1] = '\0';
            phone[strlen(phone) - 1] = '\0';

            strcpy(p->name, name);
            strcpy(p->address, address);
            strcpy(p->phone, phone);
            break;
        }

        i++;
    }

    fclose(fname);
    fclose(faddress);
    fclose(fphone);
}

person_data* lookup_1_svc(person_data *p, struct svc_req *rqstp) {
    static person_data result;

    //printf("%li\n", get_name_index(p->name));

    if(get_name_index(p->name) != -1) {
        build_person_data(&result, get_name_index(p->name));
        return &result;
    }
    else {
        strcpy(result.name, "NOT FOUND");
        strcpy(result.address, "NOT FOUND");
        strcpy(result.phone, "NOT FOUND");
    }

    return &result;
}
