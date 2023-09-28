import requests
import json
import pandas as pd
import openai
import os

openai.api_key = 'insert key here'
sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

#Função que obtem as informações dos usuários da API fornecida. Retorna os dados caso a conexão seja bem sucedida
def get_user(id):
    response = requests.get(f'{sdw2023_api_url}/users/{id}')

    return response.json() if response.status_code == 200 else None

#Função que se comunica com o ChatGPT para gerar uma mensagem personalizada para cada usuário com base em seus dados
def generate_ai_news(user): 
    
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system", 
            "content": "Você é um psicologo especialista em comportamento humano e também possui formação em finanças."
        },
        {
            "role": "user", 
            "content": f"Crie uma mensagem personalizada para {user['name']}, com base no seu saldo da conta de {user['account']['balance']}, sugerindo possíveis investimentos que sejam importantes para uma vida segura e confortável (máximo de 100 caracteres)"
        }
    ]
    )
    return completion.choices[0].message.content.strip('\"')

#Função que atualiza as mensagens na API com as informações obtidas no CHATGPT
def update_user(user):
    response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False

#Leitura de um .csv contendo os IDs dos usuários que queremos gerar novas mensagens
df = pd.read_csv('c:/Users/Daniel/Desktop/Curso Python/Desafio ETL ChatGPT/1. Extração/ClientesBanco.csv')
user_ids = df['UserID'].tolist()

#Carregamento dos dados dos usuários da API. Verifica se os dados existem antes de carregá-los
users = [user for id in user_ids if (user := get_user(id)) is not None]

#Para cada usuário é gerada uma mensagem personalizada e adicionado novas infos no json  
for user in users:
    news = generate_ai_news(user)
    print(news)
    user['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/transfer.svg",
        "description": news
    })

#Cada usuário é atualizado na API e gerada uma mensagem de sucesso caso o carregamento seja positivo
for user in users:
    success = update_user(user)
    print(f"User {user['name']} updated? {success}!")
