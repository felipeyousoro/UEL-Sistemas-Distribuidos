all: fraquejada compila

fraquejada:
	rpcgen -C addsub.x

compila:
	gcc server.c addsub_svc.c addsub_xdr.c -o server -lnsl
	gcc client.c addsub_clnt.c addsub_xdr.c -o client -lnsl

clean:
	rm -f *.o