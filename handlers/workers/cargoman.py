import sqlite3

from collections import namedtuple
from decimal import Decimal
from data.config import NAME_DB, USER_DB, PASSWORD_DB

import psycopg2


class FormingCargonist:
    def __init__(self):
        self.conn = psycopg2.connect(dbname=NAME_DB, user=USER_DB,
                                     password=PASSWORD_DB, host='db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS cargo(      
                   name VARCHAR(40)  PRIMARY KEY NOT NULL,
                   quantity_poddons INTEGER,
                   quantity_box INTEGER
                   );
                """)
        self.conn.commit()

    async def add_cargo(self, name, quantyti):
        with psycopg2.connect(dbname=NAME_DB, user=USER_DB,
                              password=PASSWORD_DB, host='db') as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT quantity_kor FROM prod WHERE name=%s', (str(name),))
                quantity_box = int(cur.fetchone()[0]) * int(quantyti)
                self.cur.execute("INSERT INTO cargo VALUES (%s, %s, %s)", (name, quantyti, quantity_box))
                self.conn.commit()
                return True

    async def all_cargo(self):
        with psycopg2.connect(dbname=NAME_DB, user=USER_DB,
                              password=PASSWORD_DB, host='db') as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM cargo")
                return cur.fetchall()

    async def del_cargo(self):
        with psycopg2.connect(dbname=NAME_DB, user=USER_DB,
                              password=PASSWORD_DB, host='db') as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM cargo;', )
                conn.commit()

    async def edit_box_cargo(self, name, new_quantity):
        with psycopg2.connect(dbname=NAME_DB, user=USER_DB,
                              password=PASSWORD_DB, host='db') as conn:
            with conn.cursor() as cur:
                cur.execute(f'UPDATE cargo SET quantity_box = %s WHERE name = %s', (new_quantity, name))
                conn.commit()


class Cargonist:
    def __init__(self):
        with psycopg2.connect(dbname=NAME_DB, user=USER_DB,
                              password=PASSWORD_DB, host='db') as conn:
            with conn.cursor() as cursor:
                cursor.execute("""CREATE TABLE IF NOT EXISTS prod(    
                   name VARCHAR(40) PRIMARY KEY NOT NULL,
                   quantity_kor INTEGER, 
                   quantity_kg_or_ed INTEGER,
                   price NUMERIC(10, 2),
                   weight NUMERIC(10, 2));
                """)
                conn.commit()

    async def add_product(self, name: str, boxs: int, quantity_item: int, price: float, weight: float):
        with psycopg2.connect(dbname=NAME_DB, user=USER_DB,
                              password=PASSWORD_DB, host='db') as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(f"INSERT INTO prod VALUES ('{name}', {boxs}, {quantity_item}, {price}, {weight})")
                    conn.commit()
                    return True
                except Exception:
                    return False

    async def get_all_product(self):
        with psycopg2.connect(dbname=NAME_DB, user=USER_DB,
                              password=PASSWORD_DB, host='db') as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT name FROM prod")
                return cursor.fetchall()

    async def delete_product(self, name):
        with psycopg2.connect(dbname=NAME_DB, user=USER_DB,
                              password=PASSWORD_DB, host='db') as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"DELETE FROM prod WHERE name='{name}'")
                conn.commit()

    async def get_by_name(self, name):
        with psycopg2.connect(dbname=NAME_DB, user=USER_DB,
                              password=PASSWORD_DB, host='db') as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(f"SELECT * FROM prod WHERE name = '{name}';")
                    Product = namedtuple('Product', ['name', 'boxs', 'quantity', 'price', 'weight'])
                    data = cursor.fetchone()
                    p = Product(
                        name=data[0],
                        boxs=data[1],
                        quantity=data[2],
                        price=data[3],
                        weight=data[4]
                    )
                    return p
                except Exception as er:
                    print(f'Ошибка !!! в методе get_by_name\n {er}')
                    return False

    async def edit_price(self, product_name, new_price):
        with psycopg2.connect(dbname=NAME_DB, user=USER_DB,
                              password=PASSWORD_DB, host='db') as conn:
            with conn.cursor() as cursor:
                cursor.execute('UPDATE prod SET price = %s WHERE name = %s;', (new_price, product_name))
                conn.commit()


class Manager:
    async def get_data_cargo(self):

        with psycopg2.connect(dbname=NAME_DB, user=USER_DB,
                              password=PASSWORD_DB, host='db') as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM cargo;")
                cargo_list = cursor.fetchall()
                return cargo_list

    async def get_data_product(self, name):
        with psycopg2.connect(dbname=NAME_DB, user=USER_DB,
                              password=PASSWORD_DB, host='db') as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM prod WHERE name = '{name}';")
                cargo_list = cursor.fetchone()
                return cargo_list

    async def tr(self):
        res = {}
        cargo = await self.get_data_cargo()
        for item in cargo:
            data = await self.get_data_product(item[0])

            res.update(
                {item[0]: {
                    'count': item[1],
                    'boxs': item[2],
                    'quantyti': data[2],
                    'price': data[3],
                    'weight': data[4]
                }}
            )

        return res

    # {'Маргарин(33100)': {'name': 'Маргарин(33100)', 'count': 12, 'boxs': 45, 'quantyti': 20, 'price': 89.5,
    #                      'weight': 1},
    #  'Россиянка 1.7л': {'name': 'Россиянка 1.7л', 'count': 12, 'boxs': 112, 'quantyti': 6, 'price': 136,
    #                     'weight': 1.564}}
    async def forming_text(self):
        text_money = ''
        text_weight = ''
        data = await self.tr()
        o_weight = Decimal('0.00')
        o_money = Decimal('0.00')
        for item, element in data.items():

            # текст вес
            coutn_box = str(int(element['boxs']))
            count_bottle = str(int(element['boxs'] * int(element['quantyti'])))
            _weight = str(float(count_bottle) * float(element['weight']))
            number = Decimal(_weight)
            weight = number.quantize(Decimal("1.00"))

            o_weight += weight

            _money = str(float(count_bottle) * float(element['price']))
            number = Decimal(_money)
            price = number.quantize(Decimal("1.00"))
            o_money += price
            if item.capitalize().startswith('Майонез'):
                text_weight += f'{item} {coutn_box}вед. * {element["weight"]}кг. = {weight}кг.\n'
                text_money += f"{item} {count_bottle}вед. * {element['price']}руб. = {price}руб.\n"
            elif item.capitalize().startswith('Маргарин') or item.capitalize().startswith('Пальм'):
                text_weight += f'{item} {coutn_box}кор. * {element["quantyti"]}кг. = {weight}кг.\n'
                text_money += f"{item} {count_bottle}кг. * {element['price']}руб. = {price}руб.\n"
            else:
                text_money += f"{item} {count_bottle}бут. * {element['price']}руб. = {price}руб.\n"
                text_weight += (
                        item + f" {coutn_box}кор. * {element['quantyti']}бут. = {count_bottle}бут. * {element['weight']}кг. = {weight}кг.\n")

        text_money += f'Итого: {o_money}руб.'
        text_weight += f'Итого: {o_weight}кг.'
        result = f"{text_weight}\n\n{text_money}"

        return result


if __name__ == '__main__':
    c = Manager()
    c.forming_text()
