#include <stdio.h>
#include <assert.h>

#include "../notebook/notebook.h"
#include "../lista/lista.h"

char *DATABASE_NAME = "database/database-name.txt";
char *DATABASE_ADDRESS = "database/database-phone.txt";
char *DATABASE_PHONE = "database/database-address.txt";

void *insert_1_svc(person_data *p, struct svc_req *rqstp) {
    FILE *fname = fopen(DATABASE_NAME, "a");
    FILE *faddress = fopen(DATABASE_ADDRESS, "a");
    FILE *fphone = fopen(DATABASE_PHONE, "a");

    fprintf(fname, "%s\n", p->name);
    fprintf(faddress, "%s\n", p->street);
    fprintf(fphone, "%s\n", p->phone);

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
        char buffer[128];
        fgets(buffer, 128, fname);
        if(feof(fname)) break;

        buffer[strlen(buffer) - 1] = '\0';

        if (strcmp(buffer, name) == 0) {
            found = 1;
            break;
        }

        index++;
    }
    fclose(fname);

    return (found == 1) ? index : -1;
}

void build_person_data(person_data *p, long index) {
    FILE *fname = fopen(DATABASE_NAME, "r");
    FILE *faddress = fopen(DATABASE_ADDRESS, "r");
    FILE *fphone = fopen(DATABASE_PHONE, "r");

    int i = 0;
    while (1) {
        char name[128], address[128], phone[128];
        fgets(name, 128, fname);
        fgets(address, 128, faddress);
        fgets(phone, 128, fphone);
        if (feof(fname) || feof(faddress) || feof(fphone)) break;

        if (i == index) {
            name[strlen(name) - 1] = '\0';
            address[strlen(address) - 1] = '\0';
            phone[strlen(phone) - 1] = '\0';

            strcpy(p->name, name);
            strcpy(p->street, address);
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

    if(get_name_index(p->name) != -1) {
        build_person_data(&result, get_name_index(p->name));
        return &result;
    }

    return NULL;
}
