import requests
import re
import os
from bs4 import BeautifulSoup

#придумать распределение файлов для многопользования

def current_path_directory():
    path = os.getcwd()
    current_path = path + "/" + "PDF_WORKER.pdf"

    return current_path

def request_pdf(number_of_kurs, number_of_group):

    url = 'https://emit.ranepa.ru/faculty-2/ai/'

    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'lxml')

    number_of_group_digital = re.findall(r'\d+', number_of_group)
    number_of_group_digital_clear = number_of_group_digital[0] + "-" + number_of_group_digital[1]

    req_text = str(number_of_kurs) + '-kurs'
    req_group = str(number_of_group_digital_clear)

    for a in soup.find_all('a', href=True):
        if (req_text in a['href']) and (req_group in a['href']):
            url_pdf = a['href']
            r = requests.get(url_pdf, verify=False)

            with open(current_path_directory(), 'wb') as f:
                f.write(r.content)
                path = os.path.abspath(current_path_directory())
                print("Картинка сохранена!")
                return path