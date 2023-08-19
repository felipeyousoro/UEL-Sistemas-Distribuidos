#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>

#include "../notebook/notebook.h"
#include "../lista/lista.h"
#include "../person/person.h"

void insert(person_data *data, CLIENT *clnt) {
    insert_1(data, clnt);
}

void initialize(char *data, CLIENT *clnt) {
    reset_1(NULL, clnt);

    FILE *fdata = fopen(data, "r");
    Lista persons = person_data_read(fdata);
    fclose(fdata);

    foreach_list(persons, person_node) {
        insert(get_data(person_node), clnt);
    }
}

void build_and_insert(CLIENT *clnt) {
    char name[NAME_SIZE], address[ADDRESS_SIZE], phone[PHONE_SIZE];

    fprintf(stdout, "Type the name: ");
    fflush(stdout);
    fgets(name, NAME_SIZE, stdin);
    name[strlen(name) - 1] = '\0';

    fprintf(stdout, "Type the address: ");
    fflush(stdout);
    fgets(address, ADDRESS_SIZE, stdin);
    address[strlen(address) - 1] = '\0';

    fprintf(stdout, "Type the phone: ");
    fflush(stdout);
    fgets(phone, PHONE_SIZE, stdin);
    phone[strlen(phone) - 1] = '\0';

    person_data *p = person_data_create(name, address, phone);

    insert(p, clnt);

    free(p);
}

void lookup(CLIENT *clnt) {
    fprintf(stdout, "Type the name you want to search: ");
    fflush(stdout);

    char name[NAME_SIZE];
    fgets(name, NAME_SIZE, stdin);
    name[strlen(name) - 1] = '\0';

    static person_data p;
    strcpy(p.name, name);

    person_data *result = lookup_1(&p, clnt);
    print_person_data(result);
}


int main(int argc, char *argv[]) {
    CLIENT *clnt;
    clnt = clnt_create ("127.0.0.1", NOTEBOOK_PROG, NOTEBOOK_VERS, "udp");
    if (clnt == (CLIENT *) NULL)
    {
        clnt_pcreateerror ("Mamão");
        exit(1);
    }

    int key;
    char key_str[8]; char *data = "data.txt";
    while(1) {
        fprintf(stdout, "1 - Initialize\n");
        fprintf(stdout, "2 - Insert\n");
        fprintf(stdout, "3 - Lookup\n");

        fprintf(stdout, "Type the option: ");
        fflush(stdout);

        // Fazendo essa macacada pq essa MERDA
        // de linguagem tem problema com stdin :D
        fgets(key_str, 8, stdin);
        key = atoi(key_str);

        switch(key) {
            case(1):
                initialize(data, clnt);
                break;
            case(2):
                build_and_insert(clnt);
                break;
            case(3):
                lookup(clnt);
                break;
            default:
                break;
        }

        fprintf(stdout, "\n");
        fflush(stdout);
    }

    return 0;
}