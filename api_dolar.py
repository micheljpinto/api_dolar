# Importando todas as bibliotecas necessárias para fazer o Script Rodar

import pandas as pd
import numpy as np
from datetime import date, datetime,timedelta
import requests, json, io 


dtAtual= datetime.now()
dtPassada= dtAtual - timedelta(days=1500) # a ser utilizado no caso de querer quantificar dias anteriores ao dia atual
#dtPassada= '01-01-2017' #'01-01-2019'
dtAtual= dtAtual.strftime('%m-%d-%Y')
dtPassada= dtPassada.strftime('%m-%d-%Y')

#stringGetAPI= "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial='{}'&@dataFinalCotacao='{}'&$top=2000&$format=json&$select=cotacaoVenda,dataHoraCotacao"

stringGetAPI= "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial='{}'&@dataFinalCotacao='{}'&$top=2000&$format=json&$select=cotacaoCompra,dataHoraCotacao".format(dtPassada, dtAtual)

try:
    r = requests.get(url = stringGetAPI)
    testCon=True
    print(r.ok)
except:
    testCon=False
    print('sem conexao')

file = 'cotacaoDolar.csv'

#REMOVENDO HORA DA LISTA e CRIANDO DUAS LISTAS COM DATA E COTACAO

payload=json.loads(r.text)
temp=payload['value']
tempData=list() 
tempCot=list()

ar="Data,dolar\n"
for k in temp:
    tempData.append(k['dataHoraCotacao'][:10]) #removendo hora da variável, depois verificar se é mesmo necessario
    tempCot.append(k['cotacaoCompra'])

for k in range(0,len(tempData)): 
    ar+=str(tempData[k])+','+ str(tempCot[k])+'\n' 

sar= io.StringIO(ar)

df=pd.read_csv(sar, parse_dates = ['Data'], index_col ='Data', sep=',', encoding='latin-1') 
#Ao ser adicionada acrescenta horário novamente
df.to_csv(file) #salva o material lido na pasta local!!!!!
#cotando_dolar90 = pd.DataFrame({'Data':tempData, 'dolar':tempCot}) # a mesma de df porém sem horário



