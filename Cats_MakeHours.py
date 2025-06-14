import requests
import time
import random


#47horas
#55horas -> frist run 18/04 
#60horas -> run 19/04
#65horas -> run 30/04 
#70horas -> run1/05
#72horas -> run 11/05
#76HORAS -> RUN 04/06
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

disciplines = [
    {"name": "AGK", "docid": 475, "version": 77, "endPage": 378, "subject": 142},
    {"name": "PoF", "docid": 476, "version": 80, "endPage": 398, "subject": 148},
    {"name": "OP", "docid": 464, "version": 66, "endPage": 66, "subject": 147},
    {"name": "NAV", "docid": 477, "version": 81, "endPage": 327, "subject": 146},
    {"name": "MET", "docid": 466, "version": 68, "endPage": 249, "subject": 145},
    {"name": "HPL", "docid": 463, "version": 96, "endPage": 143, "subject": 144},
    {"name": "FPP", "docid": 479, "version": 83, "endPage": 168, "subject": 143},
    {"name": "AL", "docid": 467, "version": 69, "endPage": 307, "subject": 141},
    {"name": "COM", "docid": 461, "version": 62, "endPage": 99, "subject": 149},
]

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

# Obter cookies e token inicial
cookies = get_initial_cookies()
auth_token = input("Digite o token inicial (X-AUTH-TOKEN): ")

# Menu de disciplinas
print("Escolha uma disciplina para começar:")
for index, discipline in enumerate(disciplines, start=1):
    print(f"{index} - {discipline['name']}")

discipline_choice = input("Digite o número da disciplina escolhida: ").strip()
if not discipline_choice.isdigit() or int(discipline_choice) not in range(1, len(disciplines)+1):
    print("Opção inválida!")
    exit()

current_index = int(discipline_choice) - 1
time_alive = int(input("Adicione o tempo de estudo em minutos: ")) * 60
start_time = time.time()
page = 2

while time.time() - start_time < time_alive:
    discipline_data = disciplines[current_index]
    docid = discipline_data["docid"]
    version = discipline_data["version"]
    endPage = discipline_data["endPage"]
    subject = discipline_data["subject"]

    # Verifica se já passou do fim do manual
    if page > endPage:
        print(f"Fim do manual de {discipline_data['name']}! Mudando para a próxima disciplina...")
        current_index = (current_index + 1) % len(disciplines)
        page = 2
        continue

    # Executa requests
    auth_token = send_request(auth_token, cookies, subject)
    send_get_docs_request(auth_token, cookies, docid, page, version, endPage)
    send_check_pagesubject_request(auth_token, cookies, docid, page)
    
    print(f"[{discipline_data['name']}] Página {page} enviada com sucesso.")
    page += 1

    remaining_time = time_alive - (time.time() - start_time)
    #delay = random.randint(45, 300)
    delay = random.randint(30, 210)
    print(f"A aguardar {delay} segundos para o próximo request... ({int(remaining_time // 60)}m restantes)")
    time.sleep(delay)

print("Tempo de estudo finalizado.")
