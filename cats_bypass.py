import requests
import time
import random

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

disciplines = {
    "AGK": {"docid": 475, "version": 77, "endPage": 378, "subject": 142},
    "PoF": {"docid": 476, "version": 80, "endPage": 398, "subject": 148},
    "OP": {"docid": 464, "version": 66, "endPage": 66, "subject": 147},
    "NAV": {"docid": 477, "version": 81, "endPage": 327, "subject": 146},
    "MET": {"docid": 466, "version": 68, "endPage": 249, "subject": 145},
    "HPL": {"docid": 463, "version": 96, "endPage": 143, "subject": 144},
    "FPP": {"docid": 479, "version": 83, "endPage": 168, "subject": 143},
    "AL": {"docid": 467, "version": 69, "endPage": 307, "subject": 141},
    "COM": {"docid": 461, "version": 62, "endPage": 99, "subject": 149},
}

def send_request(auth_token, cookies, subject):
    url = "https://wbt.catsaviation.com/3/includes/log_activity"
    headers = {"X-Requested-With": "XMLHttpRequest"}
    cookies["X-AUTH-TOKEN"] = auth_token
    data = {"sitearea": "guides", "subject": str(subject)}
    try:
        response = requests.post(url, headers=headers, cookies=cookies, data=data, verify=False)
        if "X-AUTH-TOKEN" in response.cookies:
            return response.cookies["X-AUTH-TOKEN"]
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
    return auth_token

def send_get_docs_request(auth_token, cookies, docid, page, version, endPage):
    url = "https://wbt.catsaviation.com/3/docs/get"
    headers = {"X-Requested-With": "XMLHttpRequest"}
    cookies["X-AUTH-TOKEN"] = auth_token
    data = {"type": "sg", "doc": docid, "version": version, "page": page, "startPage": "0", "endPage": endPage}
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
auth_token = input("Digite o token inicial (X-AUTH-TOKEN): ")

# Menu de escolha de disciplina
print("Escolha uma disciplina:")
for key in disciplines:
    print(f"{key}")
discipline_choice = input("Digite o código da disciplina: ").strip().upper()

if discipline_choice not in disciplines:
    print("Disciplina inválida!")
    exit()

discipline_data = disciplines[discipline_choice]
docid = discipline_data["docid"]
version = discipline_data["version"]
endPage = discipline_data["endPage"]
subject = discipline_data["subject"]

page = int(input("Digite a página inicial: "))
time_alive = int(input("Digite o tempo de execução em minutos: ")) * 60
start_time = time.time()

while time.time() - start_time < time_alive:
    auth_token = send_request(auth_token, cookies, subject)
    send_get_docs_request(auth_token, cookies, docid, page, version, endPage)
    send_check_pagesubject_request(auth_token, cookies, docid, page)
    page += 1
    remaining_time = time_alive - (time.time() - start_time)
    delay = random.randint(45, 300)
    print(f"Aguardando {delay} segundos para o próximo request...")
    time.sleep(delay)

print("Tempo de execução finalizado.")
