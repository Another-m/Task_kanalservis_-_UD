from flask import Flask, render_template
from celery import Celery

import json
import pandas as pd
import plotly
import plotly.graph_objs as go

from db import get_data
from app import gs
from settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

app = Flask(__name__)
celery = Celery(app.name, broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery.conf.update(app.config)

# Запускаем в фоне приложение(проверки данных в таблице)
@celery.task()
def start_app():
    gs.request_of_indicator()


def main():
    print('Запуск фоновых процессов...')
    start_app.delay()
    print('Синхронизация таблицы и бд запущена')

# Функция построения графика
def create_plot(df):
    data = [
        go.Bar(
            x=df['срок поставки'],
            y=df['стоимость,$']
        )]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route("/")
@app.route("/index")
def index():
    data = get_data()
    data_dict = [{'№': i.id, 'заказ №': i.order_id, 'стоимость,$': i.price_usd, 'стоимость,руб': i.price_rub, 'срок поставки': i.delivery_time} for i in data]
    print(data_dict)
    df = pd.DataFrame(data_dict)
    sum_df = int(df.sum()['стоимость,$'])
    table = [df.sort_values(by='№').to_html(classes='table', index=False)]
    plot = create_plot(df)
    return render_template('index.html', title="Главная страница", table=table, sum=sum_df, plot=plot)


if __name__ == "__main__":
    main()
    app.run(debug=True)