import requests
import pandas as pd
import math

url = "https://api.casadosdados.com.br/v2/public/cnpj/search"

headers = {
    "Content-Type": "application/json",
    "User-Agent": "insomnia/2023.5.8"
}

dados = []

mes = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
ano = [str(ano) for ano in range(2000, 2026)]
i = 0
j = 0
pag = 8

while j < len(ano) and int(ano[j]) < 2024:

    page_num = 1
    tot_pag = pag

    k = i + 1
    l = j

    if i >= 11:
        k = 11
        i = 0
        j += 1

    while page_num <= tot_pag:
        params = {
            "query": {
                "termo": [],
                "atividade_principal": [],
                "natureza_juridica": [],
                "uf": [],
                "municipio": [],
                "bairro": [],
                "situacao_cadastral": "ATIVA",
                "cep": [],
                "ddd": []
            },
            "range_query": {
                "data_abertura": {
                    "lte": ano[l] + "-" + mes[k] + "-01",
                    "gte": ano[j] + "-" + mes[i] + "-01"
                },
                "capital_social": {
                  "lte": None,
                  "gte": None
                }
            },
            "extras": {
                "somente_mei": False,
                "excluir_mei": False,
                "com_email": False,
                "incluir_atividade_secundaria": False,
                "com_contato_telefonico": False,
                "somente_fixo": False,
                "somente_celular": False,
                "somente_matriz": False,
                "somente_filial": False
            },
            "page": page_num
            }

        response = requests.post(url, json=params, headers=headers)

        if response.status_code == 200:
            if response.json()["data"].get("cnpj"):
                data = response.json()["data"]["cnpj"]
                dados.extend(data)

                pag = int(math.ceil(response.json()["data"]["count"] / 20))

                print(f"Dados coletados com sucesso. Página {page_num} ")

        else:
            print(f"Erro na requisição da página {page_num}. Código de status:", response.status_code)

        page_num += 1

    df = pd.DataFrame(dados)

    df.to_excel(f"planilhas/casadosdados {mes[i]}-{ano[j]} até {mes[k]}-{ano[l]}.xlsx", index=False)

    if l != j:
        i = 0
    else:
        i += 1



print("Todos dados salvos com sucesso!")