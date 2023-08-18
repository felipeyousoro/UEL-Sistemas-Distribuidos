#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>

#include "../notebook.h"
#include "../lista/lista.h"

struct person_data *person_data_create(char *name, char *street, char *phone) {
    person_data *data = malloc(sizeof(struct person_data));

    strcpy(data->name, name);
    strcpy(data->street, street);
    strcpy(data->phone, phone);

    return data;
}

void print_person_data(person_data *data) {
    printf("Name: %s", data->name);
    printf("Street: %s", data->street);
    printf("Phone: %s", data->phone);
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

void insert(CLIENT *clnt, person_data *data) {

    person_data *gay = insert_1(data, clnt);

    print_person_data(gay);
}

int main(int argc, char *argv[]) {
    printf("Client started\n");

    FILE *f = fopen("data.txt", "r");
    assert(f != NULL);
    read_info_t info;
    person_data_read(f, &info);

    printf("Data read successfully\n");

    CLIENT *clnt;
    clnt = clnt_create (argv[1], NOTEBOOK_PROG, NOTEBOOK_VERS, "udp");
    if (clnt == (CLIENT *) NULL)
    {
        clnt_pcreateerror ("Mamão");
        exit(1);
    }

    printf("Client created\n");

    insert(clnt, info.data[0]);

    return 0;
}