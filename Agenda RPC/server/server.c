#include <stdio.h>
#include <assert.h>

#include "../notebook/notebook.h"
#include "../person/person.h"

char *DATABASE_NAME = "database/database-name.txt";
char *DATABASE_ADDRESS = "database/database-phone.txt";
char *DATABASE_PHONE = "database/database-address.txt";

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

Lista load_database_in_memory() {
    FILE *fname = fopen(DATABASE_NAME, "r");
    FILE *faddress = fopen(DATABASE_ADDRESS, "r");
    FILE *fphone = fopen(DATABASE_PHONE, "r");

    Lista lista = create_list();

    while (1) {
        char name[NAME_SIZE], address[ADDRESS_SIZE], phone[PHONE_SIZE];
        fgets(name, NAME_SIZE, fname);
        fgets(address, ADDRESS_SIZE, faddress);
        fgets(phone, PHONE_SIZE, fphone);
        if (feof(fname) || feof(faddress) || feof(fphone)) break;

        name[strlen(name) - 1] = '\0';
        address[strlen(address) - 1] = '\0';
        phone[strlen(phone) - 1] = '\0';

        person_data *data = person_data_create(name, address, phone);
        insert_list(lista, data);
    }

    fclose(fname);
    fclose(faddress);
    fclose(fphone);

    return lista;
}

void *insert_1_svc(person_data *p, struct svc_req *rqstp) {
    FILE *fname = fopen(DATABASE_NAME, "a");
    FILE *faddress = fopen(DATABASE_ADDRESS, "a");
    FILE *fphone = fopen(DATABASE_PHONE, "a");

    fprintf(fname, "%s\n", p->name);
    fprintf(faddress, "%s\n", p->address);
    fprintf(fphone, "%s\n", p->phone);
    fflush(stdout);

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

person_data* lookup_1_svc(person_data *p, struct svc_req *rqstp) {
    static person_data result = {"NOT FOUND", "NOT FOUND", "NOT FOUND"};

    Lista db = load_database_in_memory();

    foreach_list(db, db_node) {
        person_data *data = get_data(db_node);

        if(strcmp(data->name, p->name) == 0) {
            strcpy(result.name, data->name);
            strcpy(result.address, data->address);
            strcpy(result.phone, data->phone);
            break;
        }
    }

    return &result;
}

void *delete_1_svc(person_data *p, struct svc_req *rqstp) {
    Lista db = load_database_in_memory();

    foreach_list(db, db_node) {
        person_data *data = get_data(db_node);

        if(strcmp(data->name, p->name) == 0) {
            remove_node(db, db_node);
            break;
        }
    }

    reset_1_svc(NULL, NULL);

    foreach_list(db, db_node) {
        person_data *data = get_data(db_node);
        insert_1_svc(data, NULL);
    }

    static int result = 1;
    return (void *) &result;
}

void *update_1_svc(person_data *p, struct svc_req *rqstp) {
    Lista db = load_database_in_memory();

    foreach_list(db, db_node) {
        person_data *data = get_data(db_node);

        if(strcmp(data->name, p->name) == 0) {
            strcpy(data->address, p->address);
            strcpy(data->phone, p->phone);
            break;
        }
    }

    reset_1_svc(NULL, NULL);

    foreach_list(db, db_node) {
        person_data *data = get_data(db_node);
        insert_1_svc(data, NULL);
    }

    static int result = 1;
    return (void *) &result;
}
