from datetime import date, datetime

dataInf = "2024-09-15"
data_formatada = datetime.strptime(dataInf, "%Y-%m-%d").date()
data_formatada = data_formatada.strftime("%d/%m/%Y")
data = date.today()
data_atual = data.strftime("%d/%m/%Y")


print(data_atual+ " " + data_formatada)

if data_formatada < data_atual:
    print("Data Informada Menor")
elif data_formatada == data_atual:
    print("As datas são iguais")
else:
    print("Tudo certo")
