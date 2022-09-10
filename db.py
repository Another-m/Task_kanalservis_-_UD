from datetime import datetime, date

from sqlalchemy import create_engine, Column, Integer, String, DateTime, FLOAT, Date
from sqlalchemy.orm import sessionmaker, declarative_base

from settings import PG_CONFIG, SYNCH_DATA

engine = create_engine(PG_CONFIG, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, comment='№')
    order_id = Column(Integer, index=True, unique=True, nullable=False, comment='заказ №')
    price_usd = Column(FLOAT, comment='стоимость,$')
    price_rub = Column(FLOAT, comment='стоимость, руб')
    delivery_time = Column(Date, comment='срок поставки')


Base.metadata.create_all(engine)


def check_data(data):
    if SYNCH_DATA:
        delete_all()
        for line in data:
            add_data(line)
    else:
        for line in data:
            result = add_data(line)
            if result == 0:
                update_data(line)


def add_data(line):
    with Session() as session:
        try:
            data = Orders(id=line['№'],
                          order_id=line['заказ №'],
                          price_usd=line['стоимость,$'],
                          price_rub=line['стоимость, руб'],
                          delivery_time=datetime.strptime(line['срок поставки'], "%d.%m.%Y")
                          )
        except:
            print('Строка {} не была добавлена в бд из-за ошибки заполнения'.format({line['заказ №']}))
            return 1
        try:
            session.add(data)
            session.commit()
            return 1
        except:
            return 0


def update_data(line):
    with Session() as session:
        data = session.query(Orders).filter(Orders.id == line['№']).one()
        data.id = line['№'],
        data.order_id = line['заказ №'],
        data.price_usd = line['стоимость,$'],
        data.price_rub = line['стоимость, руб'],
        data.delivery_time = datetime.strptime(line['срок поставки'], "%d.%m.%Y")
        session.add(data)
        session.commit()


def delete_all():
    with Session() as session:
        session.query(Orders).delete(synchronize_session='fetch')
        session.commit()


def get_data():
    with Session() as session:
        data = session.query(Orders).all()
        return data


if __name__ == '__main__':
    print(i.price_usd for i in get_data())