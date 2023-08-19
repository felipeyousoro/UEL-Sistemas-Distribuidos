LISTA = lista/lista.c
PERSON = person/person.c

CLIENT_PATH = client/client.c
SERVER_PATH = server/server.c

CLIENT_OBJS = $(LISTA:.c=.o) $(PERSON:.c=.o)
SERVER_OBJS = $(LISTA:.c=.o) $(PERSON:.c=.o)

all: comp_rpc comp_client comp_server

comp_rpc:
	cd notebook && rpcgen -C notebook.x

comp_client: $(CLIENT_OBJS)
	gcc -o run_client $(CLIENT_PATH) $(CLIENT_OBJS) notebook/notebook_clnt.c notebook/notebook_xdr.c -lnsl

comp_server:
	gcc -o run_server $(SERVER_PATH) $(SERVER_OBJS) notebook/notebook_svc.c notebook/notebook_xdr.c -lnsl

%.o: %.c
	gcc -c $< -o $@

clean:
	#rm -f *.o