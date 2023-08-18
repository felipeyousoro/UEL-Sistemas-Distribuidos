#ifndef LISTA_H
#define LISTA_H

#include <stdio.h>
#include <stdlib.h>

typedef void *Lista;
typedef void *list_node;

/* Criar e inserir na lista */

Lista create_list();

void insert_list(Lista list, void *data);

/* União de listas */

Lista concat_lists(Lista list1, Lista list2);

Lista concat_lists_no_dup(Lista list1, Lista list2);

/* Operaçoes de busca ou utilitários da lista */

int index_of_node(Lista list, list_node node);

int index_of_element(Lista list, void *data);

int get_size(Lista list);

void *search_element(Lista list, void *param, int (*cmp)(void *, void *));

Lista search_elements(Lista list, void *param, int (*cmp)(void *, void *));

/* Operações de para iterar */

// Index starts at 0
list_node get_index(Lista list, int index);

list_node get_head(Lista list);

list_node get_tail(Lista list);

list_node get_next(list_node node);

list_node get_prev(list_node node);

/* Set e get de dados */

void *get_data(list_node node);

void set_data(list_node node, void *data);

/* Remoção de elementos */

void *remove_node(Lista list, list_node node);

int remove_data(Lista list, void *data);

void destroy_list(Lista list);

#define foreach_list(list, node) \
    for (list_node node = get_head(list); node != NULL; node = get_next(node))

//void remove_node_free_data(Lista list, list_node node);
//void destroy_list_free_data(Lista list);

#endif