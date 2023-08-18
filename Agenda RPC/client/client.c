#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>

#include "../notebook/notebook.h"
#include "../lista/lista.h"

person_data *person_data_create(char *name, char *street, char *phone) {
    person_data *data = malloc(sizeof(struct person_data));

    strcpy(data->name, name);
    strcpy(data->street, street);
    strcpy(data->phone, phone);

    return data;
}

void print_person_data(person_data *data) {
    printf("Name: %s\n", data->name);
    printf("Street: %s\n", data->street);
    printf("Phone: %s\n", data->phone);
}

typedef struct read_data {
    int size;
    person_data **data;
} read_info_t;

void person_data_read(FILE *f, read_info_t *info) {
    int i = 0;

    Lista lista = create_list();

    while (!feof(f)) {
        char name[128], street[128], phone[128];
        fgets(name, 128, f);
        fgets(street, 128, f);
        fgets(phone, 128, f);

        name[strlen(name) - 1] = '\0';
        street[strlen(street) - 1] = '\0';
        phone[strlen(phone) - 1] = '\0';

        person_data *data = person_data_create(name, street, phone);
        insert_list(lista, data);

        i++;
    }

    info->size = i;
    info->data = malloc(sizeof(person_data *) * info->size);

    i = 0;
    foreach_list(lista, list_node) {
        info->data[i] = get_data(list_node);
        i++;
    }

}

void insert(person_data *data, CLIENT *clnt) {
    insert_1(data, clnt);
}

void lookup(char *name, CLIENT *clnt) {
    static person_data p;
    strcpy(p.name, name);

    person_data *result = lookup_1(&p, clnt);
    if (!result) {
        printf("Not found\n");
    } else {
        print_person_data(result);
    }

}


int main(int argc, char *argv[]) {
    printf("/*** Client started ***\\\n");

    printf("/*** Data read successfully ***\\\n");

    CLIENT *clnt;
    clnt = clnt_create ("127.0.0.1", NOTEBOOK_PROG, NOTEBOOK_VERS, "udp");
    if (clnt == (CLIENT *) NULL)
    {
        clnt_pcreateerror ("Mamão");
        exit(1);
    }

    printf("/*** Client created ***\\\n");

    int key; char key_str[8];
    char name[128];
    while(1) {
        fprintf(stdout, "1 - Initialize\n");
        fprintf(stdout, "2 - Lookup\n");

        fprintf(stdout, "Type the option: ");

        fflush(stdout);
        fgets(key_str, 8, stdin);
        key = atoi(key_str); // Fazendo essa macacada
                        // pq essa merda de linguagem tem problema com stdin :D

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

            default:
                break;
        }
    }

    return 0;
}