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

void initialize(CLIENT *clnt) {
    reset_1(NULL, clnt);

}

void lookup(char *name, CLIENT *clnt) {
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

    int key; char key_str[8];
    char name[128];
    while(1) {
        fprintf(stdout, "1 - Initialize\n");
        fprintf(stdout, "2 - Lookup\n");

        fprintf(stdout, "Type the option: ");
        fflush(stdout);

        // Fazendo essa macacada pq essa MERDA
        // de linguagem tem problema com stdin :D
        fgets(key_str, 8, stdin);
        key = atoi(key_str);

        switch(key) {
            case(1):
//                FILE *f = fopen("data.txt", "r");
//                assert(f != NULL);
//
//                read_info_t info;
//                person_data_read(f, &info);

                break;

            case(2):
                fprintf(stdout, "Type the name you want to search: ");
                fflush(stdout);

                fgets(name, 128, stdin);
                name[strlen(name) - 1] = '\0';

                lookup(name, clnt);
                break;
            case(3):

                break;
            default:
                break;
        }

        fprintf(stdout, "\n");
        fflush(stdout);
    }

    return 0;
}