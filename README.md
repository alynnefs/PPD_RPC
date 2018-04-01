# PPD_RPC

## Como executar

1. Executar o Servidor de Nomes:

```pyro4-ns```
 
2. Executar o servidor, informando IP. Exemplo:

```python s.py 127.0.0.1```

3. Executar o cliente, informando IP e ID (que deve ser 1 ou 2). Os IDs devem ser diferentes para funcionar de forma correta. Exemplo:

```python c.py 127.0.0.1 1``` e ```python c.py 127.0.0.1 2```

## Dependências

pygame

Pyro4
