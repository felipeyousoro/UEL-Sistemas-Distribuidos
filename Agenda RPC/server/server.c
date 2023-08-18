#include <stdio.h>

#include "../notebook.h"
#include "../lista/lista.h"

person_data *insert_1_svc(person_data *argps, struct svc_req *rqstp) {
    printf("CHEGOU");

    static int result = 666;

    person_data *data = malloc(sizeof(struct person_data));

    strcpy(data->name, argps->name);
    strcpy(data->street, argps->street);
    strcpy(data->phone, argps->phone);

    return data;
}
