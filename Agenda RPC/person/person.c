#include "person.h"

person_data *person_data_create(char *name, char *address, char *phone) {
    person_data *data = malloc(sizeof(struct person_data));

    strcpy(data->name, name);
    strcpy(data->address, address);
    strcpy(data->phone, phone);

    return data;
}

void print_person_data(person_data *data) {
    fprintf(stdout, "-------------------------\n");
    fprintf(stdout, "Name:\t\t%s\n", data->name);
    fprintf(stdout, "Street:\t\t%s\n", data->address);
    fprintf(stdout, "Phone:\t\t%s\n", data->phone);
    fprintf(stdout, "-------------------------\n");
    fflush(stdout);
}

Lista person_data_read(FILE *f) {
    Lista lista = create_list();

    while (!feof(f)) {
        char name[NAME_SIZE], address[ADDRESS_SIZE], phone[PHONE_SIZE];
        fgets(name, NAME_SIZE, f);
        fgets(address, ADDRESS_SIZE, f);
        fgets(phone, PHONE_SIZE, f);

        name[strlen(name) - 1] = '\0';
        address[strlen(address) - 1] = '\0';
        phone[strlen(phone) - 1] = '\0';

        person_data *data = person_data_create(name, address, phone);
        insert_list(lista, data);

    }

    return lista;
}