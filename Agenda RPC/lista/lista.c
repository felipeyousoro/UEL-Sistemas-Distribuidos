#include <stdio.h>
#include <stdlib.h>
#include "lista.h"

typedef struct dynamic_list_node {
    void *data;
    struct dynamic_list_node *next;
    struct dynamic_list_node *prev;
} dynamic_list_node;

typedef struct dynamic_list {
    dynamic_list_node *head;
    dynamic_list_node *tail;
    int size;
} dynamic_list;

dynamic_list_node *create_node(void *data) {
    dynamic_list_node *node = (dynamic_list_node *) malloc(sizeof(dynamic_list_node));
    node->data = data;
    node->next = NULL;
    node->prev = NULL;

    return node;
}

Lista create_list() {
    dynamic_list *list = (dynamic_list *) malloc(sizeof(dynamic_list));
    list->head = NULL;
    list->tail = NULL;
    list->size = 0;

    return list;
}

void insert_list(Lista list, void *data) {
    dynamic_list *dlist = (dynamic_list *) list;
    dynamic_list_node *node = create_node(data);

    if (dlist->head == NULL) {
        dlist->head = node;
        dlist->tail = node;
    } else {
        dlist->tail->next = node;
        node->prev = dlist->tail;
        dlist->tail = node;
    }

    dlist->size++;
}

Lista concat_lists(Lista list1, Lista list2) {
    dynamic_list *super_list = create_list();
    dynamic_list *dlist1 = (dynamic_list *) list1;
    dynamic_list *dlist2 = (dynamic_list *) list2;

    dynamic_list_node *node = dlist1->head;

    while (node != NULL) {
        insert_list(super_list, node->data);
        node = node->next;
    }

    node = dlist2->head;

    while (node != NULL) {
        insert_list(super_list, node->data);
        node = node->next;
    }

    return super_list;
}

Lista concat_lists_no_dup(Lista list1, Lista list2) {
    dynamic_list *super_list = create_list();
    dynamic_list *dlist1 = (dynamic_list *) list1;
    dynamic_list *dlist2 = (dynamic_list *) list2;

    dynamic_list_node *node = dlist1->head;

    while (node != NULL) {
        insert_list(super_list, node->data);
        node = node->next;
    }

    node = dlist2->head;

    while (node != NULL) {
        if (index_of_element(super_list, node->data) == -1) {
            insert_list(super_list, node->data);
        }

        node = node->next;
    }

    return super_list;
}

int index_of_node(Lista list, list_node node) {
    dynamic_list *dlist = (dynamic_list *) list;
    dynamic_list_node *aux = dlist->head;

    int i = 0;

    while (aux != NULL && aux != node) {
        aux = aux->next;
        i++;
    }

    if (aux == NULL) {
        return -1;
    }

    return i;
}

int index_of_element(Lista list, void *data) {
    dynamic_list *dlist = (dynamic_list *) list;
    dynamic_list_node *node = dlist->head;

    int i = 0;

    while (node != NULL && node->data != data) {
        node = node->next;
        i++;
    }

    if (node == NULL) {
        return -1;
    }

    return i;
}

int get_size(Lista list) {
    dynamic_list *dlist = (dynamic_list *) list;

    return dlist->size;
}

void* search_element(Lista list, void *param, int (*cmp)(void*, void*)) {
    dynamic_list *dlist = (dynamic_list *) list;
    dynamic_list_node *node = dlist->head;

    while (node != NULL && cmp(node->data, param) != 0) {
        node = node->next;
    }

    if (node == NULL) {
        return NULL;
    }

    return node->data;
}

Lista search_elements(Lista list, void *param, int (*cmp)(void*, void*)) {
    dynamic_list *dlist = (dynamic_list *) list;
    dynamic_list_node *node = dlist->head;
    Lista result = create_list();

    while (node != NULL) {
        if (cmp(node->data, param) == 0) {
            insert_list(result, node->data);
        }

        node = node->next;
    }

    return result;
}

list_node get_index(Lista list, int index) {
    dynamic_list *dlist = (dynamic_list *) list;
    dynamic_list_node *node = dlist->head;
    int i = 0;

    while (node != NULL && i < index) {
        node = node->next;
        i++;
    }

    return node;
}

list_node get_head(Lista list) {
    dynamic_list *dlist = (dynamic_list *) list;

    return dlist->head;
}

list_node get_tail(Lista list) {
    dynamic_list *dlist = (dynamic_list *) list;

    return dlist->tail;
}


list_node get_next(list_node node) {
    dynamic_list_node *aux = node;
    return aux->next;
}

list_node get_prev(list_node node) {
    dynamic_list_node *aux = node;

    return aux->prev;
}

void *get_data(list_node node) {
    dynamic_list_node *aux = node;

    return aux->data;
}

void set_data(list_node node, void *data) {
    dynamic_list_node *aux = node;

    aux->data = data;
}

void* remove_node(Lista list, list_node node) {
    dynamic_list *dlist = (dynamic_list *) list;
    dynamic_list_node *aux = node;

    if (aux == dlist->head) {
        dlist->head = aux->next;
    }

    if (aux == dlist->tail) {
        dlist->tail = aux->prev;
    }

    if (aux->prev != NULL) {
        aux->prev->next = aux->next;
    }

    if (aux->next != NULL) {
        aux->next->prev = aux->prev;
    }

    void* info = aux->data;
    free(aux);

    dlist->size--;

    return info;
}

int remove_data(Lista list, void *data) {
    dynamic_list *dlist = (dynamic_list *) list;
    dynamic_list_node *aux = dlist->head;

    while (aux != NULL && aux->data != data) {
        aux = aux->next;
    }

    if (aux == NULL) {
        return 0;
    }

    remove_node(list, aux);

    return 1;
}

void destroy_list(Lista list) {
    dynamic_list *dlist = (dynamic_list *) list;
    dynamic_list_node *aux = dlist->head;

    while (aux != NULL) {
        dlist->head = aux->next;
        free(aux);
        aux = dlist->head;
    }

    dlist->size = 0;
}