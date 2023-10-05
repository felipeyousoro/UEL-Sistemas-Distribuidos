Você deve informar o IP de sua máquina no arquivo
'__main__.py', na linha 9 seguindo exemplo:

IP = 'SEU IP AQUI'

--------------------------------------------------------------

Ainda, informe no arquivo 'peers.txt' o nome e o IP de cada
máquina que deseja conectar, seguindo o exemplo:

nome1 191.111.11.11
nome2 192.222.22.22

--------------------------------------------------------------

Para executar o programa, basta executar no terminal:
python3 __main__.py

--------------------------------------------------------------

O tempo padrão de espera para um heartbeat ou ACK é de 2 segundos,
    o intervalo entre heartbeats é de 2 segundos e não há delay
    pré-definido na aplicação. Todos os valores podem ser alterados
    durante a execução do programa.

O tempo total de espera para um heartbeat ou ACK é calculado conforme
    combinado em aula. Isto é, 2 * delta T, onde delta T é um tempo "base"
    (intervalo dos heartbeats) somado com o tempo padrão de espera. Este
    valor é atualizado automaticamente conforme mensagens e ACKs são recebidos.