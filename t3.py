import pyodbc

connection_string = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=localhost;"
    r"DATABASE=ATV3;"
    r"UID=sa;"
    r"PWD=1234"
)

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

menu = '1 - Consultar saldo \n' \
       '2 - Realizar uma transferência\n' \
       'O que você deseja realizar? '
print(menu)
escolha = int(input())

if escolha == 1:
    idOrigem = int(input("Digite o ID da conta: "))
    query = 'SELECT saldo FROM Contas WHERE idConta = ?'
    cursor.execute(query, (idOrigem,))
    result = cursor.fetchone()
    if result:
        saldo = result[0]
        print(f'Saldo da conta {idOrigem}: R${float(saldo):.2f}')
    else:
        print("Conta não encontrada!")
        

elif escolha == 2:
    idOrigem = int(input("Digite o ID da conta de origem: "))
    idDestino = int(input("Digite o ID da conta de destino: "))
    valor = float(input("Digite o valor da transferência: "))

    query = """
    DECLARE @mensagem VARCHAR(100);
    EXEC sp_RealizarTransferencia ?, ?, ?, @mensagem OUTPUT;
    SELECT @mensagem AS msg;
    """
    cursor.execute(query, (idOrigem, idDestino, valor))
    mensagem = cursor.fetchone()[0]
    print(mensagem)
    conn.commit()

else:
    print("Escolha inválida")

cursor.close()
conn.close()
