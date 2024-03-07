import requests
from bs4 import BeautifulSoup

# URL da página da web que você deseja analisar
url = 'https://my.babbel.com/pt/tutoring/ITA'
url = 'https://globoesporte.globo.com/futebol/times/vasco/'
div_class = 'feed-post-link'
tipo = 'a'

# Faça a solicitação HTTP para obter o conteúdo da página
response = requests.get(url)

# Verifique se a solicitação foi bem-sucedida (status code 200)
if response.status_code == 200:
    # Obtenha o conteúdo HTML da página
    html_content = response.text

    # Crie um objeto BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    #print(soup)

    # Encontre a div usando sua classe (ou qualquer outro seletor)
    div = soup.find_all(tipo, class_=div_class)
    #print(div)

    # Extraia as informações desejadas da div
    if div:
        titulo = div.find('href').text.strip()
        paragrafo = div.find('h3').text.strip()

        print("Título da Div:", titulo)
        print("Parágrafo:", paragrafo)
    else:
        print(f"A div com a classe {div_class} não foi encontrada na página.")
else:
    print("Falha ao acessar a página. Status code:", response.status_code)