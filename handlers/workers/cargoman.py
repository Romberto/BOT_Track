import sqlite3

from collections import namedtuple
from decimal import Decimal


class FormingCargonist:
    def __init__(self):
        self.conn = sqlite3.connect(r'products.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS cargo(      
                   name VARCHAR(40)  PRIMARY KEY NOT NULL,
                   quantity_goddons INTEGER,
                   FOREIGN KEY(name) REFERENCES prod(name));
                """)
        self.conn.commit()

    async def close(self):
        self.conn.close()

    async def add_cargo(self, name, quantyti):
        self.cur.execute(f"INSERT INTO cargo VALUES ('{name}', {quantyti})")
        self.conn.commit()

    async def all_cargo(self):
        res = self.cur.execute("SELECT * FROM cargo")
        return res.fetchall()

    async def del_cargo(self):
        self.cur.execute('DELETE FROM cargo;', )
        self.conn.commit()


class Cargonist:
    def __init__(self):
        self.conn = sqlite3.connect(r'products.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS prod(
           
           name VARCHAR(40) PRIMARY KEY NOT NULL,
           quantity_kor INTEGER, 
           quantity_kg_or_ed INTEGER,
           price INTEGER,
           weight INTEGER);
        """)
        self.conn.commit()

    async def close(self):
        self.conn.close()

    async def add_product(self, name: str, boxs: int, quantity_item: int, price: float, weight: float):
        try:
            self.cur.execute(f"INSERT INTO prod VALUES ('{name}', {boxs}, {quantity_item}, {price}, {weight})")
            self.conn.commit()

            return True
        except sqlite3.IntegrityError as err:
            print('продукт с таким наименованием уже существует')
            print(err)
            return False

    async def get_all_product(self):
        res = self.cur.execute("SELECT name FROM prod")
        return res.fetchall()

    async def delete_product(self, name):
        res = self.cur.execute("DELETE FROM prod WHERE name=?", (name,))
        self.conn.commit()

    async def get_by_name(self, name):
        try:
            res = self.cur.execute(f"SELECT * FROM prod WHERE name = ?", (name,))
            Product = namedtuple('Product', ['name', 'boxs', 'quantity', 'price', 'weight'])
            data = res.fetchone()
            p = Product(
                name=data[0],
                boxs=data[1],
                quantity=data[2],
                price=data[3],
                weight=data[4]
            )
            return p
        except Exception:
            print('Ошибка !!! в методе get_by_name')
            return False

    async def edit_price(self, product_name, new_price):
        self.cur.execute('''UPDATE prod SET price = ? WHERE name = ?''', (new_price, product_name))
        self.conn.commit()


class Manager:
    async def get_data_cargo(self):
        with sqlite3.connect(r'products.db') as conn:
            cur = conn.cursor()
            query = cur.execute("SELECT * FROM cargo;")
            cargo_list = query.fetchall()
        return cargo_list

    async def get_data_product(self, name):
        with sqlite3.connect(r'products.db') as conn:
            cur = conn.cursor()
            query = cur.execute("SELECT * FROM prod WHERE name = ?;", (name,))
            cargo_list = query.fetchone()
            return cargo_list

    async def tr(self):
        res = {}
        cargo = await self.get_data_cargo()
        for item in cargo:
            data = await self.get_data_product(item[0])
            res.update(
                {item[0]: {
                    'count': item[1],
                    'boxs': data[1],
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
            coutn_box = str(int(element['count']) * int(element['boxs']))
            count_bottle = str(int(element['count']) * int(element['boxs'] * int(element['quantyti'])))
            _weight = str(float(count_bottle) * float(element['weight']))
            number = Decimal(_weight)
            weight = number.quantize(Decimal("1.00"))
            text_weight += (
                        item + f" {coutn_box}кор. * {element['quantyti']}бут. = {count_bottle}бут. * {element['weight']}кг. = {weight}кг.\n")
            o_weight += weight
            # текст деньги
            _money = str(float(count_bottle) * float(element['price']))
            number = Decimal(_money)
            price = number.quantize(Decimal("1.00"))
            text_money += f"{item} {count_bottle}бут. * {element['price']}руб. = {price}руб.\n"
            o_money += price

        text_money += f'Итого: {o_money}руб.'
        text_weight += f'Итого: {o_weight}кг.'
        result = f"{text_weight}\n\n{text_money}"

        return result


if __name__ == '__main__':
    c = Manager()
    c.forming_text()
