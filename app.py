from datetime import datetime, date
import time
from pprint import pprint
import xmltodict
import requests
import pandas as pd
import gspread

from Send_to_telegramm import send_to_tg, send_error
from db import check_data
from settings import PATH_TO_SECRET_KEY, G_TABLE, TIME_REQUEST


class G_Sheet:
    # Программа запросов и обработки данных из таблицы гугл диска

    def __init__(self, indicator_of_changes):
        self.indicator_of_changes = indicator_of_changes
        self.gc = gspread.service_account(filename=PATH_TO_SECRET_KEY)
        self.sh = self.gc.open_by_url(G_TABLE)

    # Проверка изменеий докумена
    def request_of_indicator(self):
        while True:
            new_indicator = self.sh.worksheet('indicator').get('A1')[0][0]
            # print(new_indicator)
            if new_indicator != self.indicator_of_changes:
                self.indicator_of_changes = new_indicator
                self.ad_price_rub()
            print('...scanning the table...')
            time.sleep(TIME_REQUEST)

    # Запрос всех данных таблицы
    def request_sheets(self):
        list_of_dicts = self.sh.get_worksheet(0).get_all_records()
        return list_of_dicts

    # Обработка данных, подготовка к записи в БД
    def ad_price_rub(self):
        data_sheets = self.request_sheets()
        today = date.today().strftime('%d/%m/20%y')
        URL = 'http://www.cbr.ru/scripts/XML_daily.asp'
        PARAMS = {'date_req': today, }
        response = requests.get(url=URL, params=PARAMS)
        course_cb_dict = xmltodict.parse(response.text)
        course_usd = [i['Value'] for i in course_cb_dict['ValCurs']['Valute'] if i['Name'] == 'Доллар США']
        float_course = float(course_usd[0].replace(',', '.'))
        deadline_list = list()
        for item in data_sheets:
            deadline = self.check_delivery_time(item)
            if deadline:
                deadline_list.append(deadline)
            try:
                item['стоимость, руб'] = format(item['стоимость,$'] * float_course, '.2f')
            except:
                item['стоимость, руб'] = None
        check_data(data_sheets)
        self.send_message(deadline_list)
        return data_sheets

    # Проверка дат на наличие просрочки
    def check_delivery_time(self, line):
        try:
            if datetime.strptime(line['срок поставки'], "%d.%m.%Y").date() <= date.today():
                return line
        except:
            self.send_message(None)

    # Подготовка данных для отправки в телеграм
    def send_message(self, deadline_data):
        if deadline_data is None:
            tx = "Обратите внимание, что таблица заполнена с ошибками. " \
                 "В таблице есть пропущенные строки либо не заполнены обязятельные поля!!! \n Необходимо внести изменения!"
            print(tx)
            send_error(tx, None)
            return
        df = pd.DataFrame(deadline_data)
        print('Обновленные данные добавлены в базу')
        if deadline_data:
            df.rename(columns={'стоимость,$': 'Цена',
                               'срок поставки': 'срок',
            }, inplace=True)
            df = df.drop('стоимость, руб', axis=1)
            send_to_tg(df, 1)
            q = len(deadline_data)
            print('просроченных поставок - {}, информация отправлена через телеграм'.format(q))
        else:
            send_to_tg(df, 0)


gs = G_Sheet(0)


if __name__ == "__main__":

    gs.request_of_indicator()
