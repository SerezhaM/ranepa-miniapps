import eel
import create_shedule as m

eel.init('web')
point = 0

if __name__ == '__main__':
    @eel.expose
    def start_py(x, y):
        kurs = x
        group = y
        if (kurs is not None) or (group is not None):
            if (kurs.isdigit()) and (int(kurs) < 7):
                try:
                    m.html_table_html = ""
                    m.create_request(kurs, group)
                    print(f'Курс: {x}\nГруппа: {y}')
                    # print(m.html_table_html)
                    eel.view_table(m.html_table_html)
                except:
                    print("<Ошибка>")

    eel.start('index.html')