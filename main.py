import re
from tabulate import tabulate
from PyPDF2 import PdfFileReader

from request import request_pdf

days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
main_list = []
html_table_html = ""

def Get_PDF_Content(pdf_path):
    content = ""
    count_min = 1000
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        number_of_pages = pdf.getNumPages()
        for i in range(0, number_of_pages):
            content += pdf.getPage(i).extractText() + "\n"
        content = " ".join(content.replace(u"\xa0", " ").strip().split())

        for day in days:
            count = content.find(day)
            if count < count_min:
                count_min = count

        content_clear = content[count_min:].replace(" – ", "–")
        print(content_clear)

        words = content_clear.split()
        day_week = ''
        txt = ''
        with open("values", "r+") as file:
            file.truncate(0)
            for word in words:
                if word in days: #проверка на день недели
                    if word != day_week:
                        file.write(txt + '\n')
                        txt = ""
                        if word == "Понедельник":
                            file.write('\n' + txt)
                    day_week = word
                    txt = ''.join([txt, word])
                else:
                    txt = ' '.join([txt, word])
            file.write(txt)
            file.close()

        # print(count_min)
        print("Расписание записано в текстовый файл")


def create_table():
    with open("values") as file:
        lines = [line.rstrip() for line in file]

        while '' in lines:  # удаление пустых элементов списка
            lines.remove('')

        for i in range(0, len(lines)):
            str = lines[i]
            words = str.split()

            day = ""
            date = ""
            time = ""
            lesson = ""
            teacher = ""
            classes = ""
            notes = ""

            # print("Time: ", time)
            # print("Len: ", len(words))

            for i in range(0, len(words)):
                # print("i: ", i)
                if i == 0:
                    day = words[i]
                    # print("day: ", i)

                elif i == 1:
                    date = words[i]
                    # print("date: ", i)

                elif (re.search(r"\d\/\d", words[i])) or (re.search(r"\w\/\d", words[i])) or (words[i] == "ДОТ") or (
                        words[i] == "Б/З") or (words[i] == "уточн."):
                    if classes != "":
                        classes = classes + "\n" + words[i]
                    else:
                        classes = classes + words[i]
                    # print("classes: ", i)

                elif (i < len(words) - 1) and ('/' in words[i + 1]) and (re.search(r"\w\.\w\.", words[i]) is None):
                    if classes != "":
                        classes = classes + "\n" + words[i] + "" + words[i + 1]
                    else:
                        classes = classes + words[i] + "" + words[i + 1]
                    # print("classes: ", i)

                elif ("ОТМЕНА!" in words[i]):
                    notes = words[i]
                    # print("notes: ", i)

                elif (i < len(words) - 1) and (re.search(r"\w\.\w\.", words[i + 1])):
                    if teacher != "":
                        teacher = teacher + "\n" + words[i] + " " + words[i + 1]
                    else:
                        teacher = teacher + words[i] + " " + words[i + 1]
                    # print("teacher: ", i)

                elif (i > 1) and (words[i].isalpha()):
                    if words[i][0].isupper():
                        lesson = lesson + "\n" + words[i]
                    else:
                        lesson = lesson + " " + words[i]
                    # print("lesson: ", i)

                elif (i > 1) and (words[i].split("-")[:1][0].isdigit()):
                    if time != "":
                        time = time + "\n" + words[i]
                    else:
                        time = time + words[i]
                    # print("time: ", i)

            one_line_clear = [day, date, time, lesson, teacher, classes, notes]
            main_list.append(one_line_clear)

    print_table(main_list)

            # print(main_list)


def print_table(table_of_values):
    global html_table_html

    headers = ["День недели", "Дата", "Время", "Дисциплина", "Преподаватель", "Аудитория", "Примечания"]
    shedule_table = tabulate(table_of_values, headers, tablefmt="simple_grid")
    html_table = tabulate(table_of_values, headers, tablefmt='html')
    # print(shedule_table)
    html_table_html = f"<h1 id='text_h1'>Расписание для {number_of_kurs}-курса группы №{number_of_group}</h1>{html_table}"

    # with open('web/table.html', "r+") as html_file:
    #     html_file.truncate(0)
    #     html_table_html = f"<h1>Расписание для {number_of_kurs}-курса группы №{number_of_group}</h1>{html_table}"
    #     html_file.write(html_table_html)
    #     html_file.close()



def create_request(x, y):
    global number_of_kurs, number_of_group

    number_of_kurs = x
    number_of_group = y

    path = request_pdf(number_of_kurs, number_of_group)
    Get_PDF_Content(path)
    try:
        create_table()
    except:
        print("<Error: create table>")



# if __name__ == '__main__':
#     number_of_kurs = input("Укажите номер вашего курса: ")
#     number_of_group = input("Укажите номер вашей группы: ")
#
#     path = request_pdf(number_of_kurs, number_of_group)
#
#     Get_PDF_Content(path)
#     try:
#         create_table()
#     except:
#         print("--- Error: create table ---")



