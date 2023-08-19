#include "person.h"

person_data *person_data_create(char *name, char *street, char *phone) {
    person_data *data = malloc(sizeof(struct person_data));

    strcpy(data->name, name);
    strcpy(data->street, street);
    strcpy(data->phone, phone);

    return data;
}

void print_person_data(person_data *data) {
    fprintf(stdout, "Name:\t\t%s\n", data->name);
    fprintf(stdout, "Street:\t\t%s\n", data->street);
    fprintf(stdout, "Phone:\t\t%s\n", data->phone);
}

Lista person_data_read(FILE *f) {
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

    }

    return lista;
}