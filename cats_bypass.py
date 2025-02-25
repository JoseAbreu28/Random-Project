import requests
import time
import random

#Obtençao das cookies de sessão
def get_initial_cookies():
    return {
        "cats_wbt_school": "aecporto",
        "cats_wbt_schoolfull": "Aero+Clube+do+Porto",
        "cats_wbt_schoolscheme": "0",
        "cats_wbt_schoolshowname": "0",
        "cats_wbt_tourtaken": "1",
        "cats_wbt_schoolcolor": "%233a5475",
        "cats_wbt_session": input("Digite o valor de cats_wbt_session: "),
    }

def send_request(auth_token, cookies):
    url = "https://wbt.catsaviation.com/3/includes/log_activity"
    headers = {"X-Requested-With": "XMLHttpRequest"}
    cookies["X-AUTH-TOKEN"] = auth_token
    data = {"sitearea": "guides", "subject": "148"}
    try:
        response = requests.post(url, headers=headers, cookies=cookies, data=data, verify=False)
        if "X-AUTH-TOKEN" in response.cookies:
            return response.cookies["X-AUTH-TOKEN"]
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
    return auth_token

def send_get_docs_request(auth_token, cookies, docid, page):
    url = "https://wbt.catsaviation.com/3/docs/get"
    headers = {"X-Requested-With": "XMLHttpRequest"}
    cookies["X-AUTH-TOKEN"] = auth_token
    data = {"type": "sg", "doc": docid, "version": "80", "page": page, "startPage": "0", "endPage": "398"}
    try:
        requests.post(url, headers=headers, cookies=cookies, data=data, verify=False)
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")

def send_check_pagesubject_request(auth_token, cookies, docid, page):
    url = "https://wbt.catsaviation.com/3/includes/cats-viewer/check_pagesubject"
    headers = {"X-Requested-With": "XMLHttpRequest"}
    cookies["X-AUTH-TOKEN"] = auth_token
    data = {"type": "sg", "docid": docid, "version": "80", "page": page}
    try:
        requests.post(url, headers=headers, cookies=cookies, data=data, verify=False)
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")

# Definir cookies ao iniciar o script
cookies = get_initial_cookies()

# Token inicial
auth_token = input("Adicione o token inicial (X-AUTH-TOKEN): ")
docid = int(input("Adicione o código da disciplina (docid POF=476, MET=466 , AGK=475 ,AL=467 ): "))
page = int(input("Adicione a página inicial (recomendado começar por um valor baixo ex:10) : "))
time_alive = int(input("Adicione o tempo de execução em minutos: ")) * 60
start_time = time.time()

while time.time() - start_time < time_alive:
    auth_token = send_request(auth_token, cookies)
    send_get_docs_request(auth_token, cookies, docid, page)
    send_check_pagesubject_request(auth_token, cookies, docid, page)
    page += 1
    remaining_time = time_alive - (time.time() - start_time)
    delay = random.randint(45, 300)
    print(f"A Aguardar {delay} segundos para o próximo request...")
    time.sleep(delay)

print("Programa terminado com sucesso")
