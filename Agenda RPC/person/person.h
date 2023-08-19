#ifndef PERSON_H
#define PERSON_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../lista/lista.h"
#include "../notebook/notebook.h"

#define NAME_SIZE 128
#define STREET_SIZE 128
#define PHONE_SIZE 128

person_data *person_data_create(char *name, char *street, char *phone);
void print_person_data(person_data *data);
Lista person_data_read(FILE *f);

#endif
