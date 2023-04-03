# - *- coding: utf- 8 - *-
import sqlite3
import math
import random

from tgbot.data.config import path_database as path_db
from tgbot.utils.utils_functions import get_unix, get_date


# Преобразование полученного списка в словарь
def dict_factory(cursor, row):
    save_dict = {}

    for idx, col in enumerate(cursor.description):
        save_dict[col[0]] = row[idx]

    return save_dict


# Форматирование запроса без аргументов
def query(sql, parameters: dict):
    if "XXX" not in sql: sql += " XXX "
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)

    return sql, list(parameters.values())


# Форматирование запроса с аргументами
def query_args(sql, parameters: dict):
    sql = f"{sql} WHERE "

    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])

    return sql, list(parameters.values())


################################################################################################
##################################           Юзеры            ##################################
################################################################################################

# Регистрация пользователя в БД
def register_user(id, user_name, first_name):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO users("
                    "id, is_ban, user_name, first_name, balance, count_refills, reg_date, reg_date_unix) "
                    "VALUES (?,?,?,?,?,?,?, ?)", [id, "False", user_name, first_name, 0, 0, get_date(), get_unix()])
        con.commit()

# Получение пользователя из БД
def get_user(**kwargs):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        queryy = "SELECT * FROM users"
        queryy, params = query_args(queryy, kwargs)
        return con.execute(queryy, params).fetchone()

# Редактирование пользователя
def update_user(id, **kwargs):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        queryy = f"UPDATE users SET"
        queryy, params = query(queryy, kwargs)
        params.append(id)
        con.execute(queryy + "WHERE id = ?", params)
        con.commit()

# Удаление пользователя из БД
def delete_user(id):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        con.execute("DELETE FROM users WHERE id = ?", id)
        con.commit()

# Получение всех пользователей из БД
def all_users():
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        return con.execute("SELECT * FROM users").fetchall()


#############################################################################################
###############################            Покупки            ###############################
#############################################################################################

# Добавление покупки
def add_purchase(user_id, first_name, user_name, receipt, count, price,
                position_id, position_name, item, date, date_unix):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO purchases "
                    "(user_id, user_full_name, user_name, receipt, count, price, position_id, "
                    "position_name, item, date, unix) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [user_id, first_name, user_name, receipt, count, price, position_id, position_name, item, date, date_unix])
        con.commit()

# Получение покупки
def get_purchase(receipt):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        return con.execute("SELECT * FROM purchases WHERE receipt = ?", (receipt,)).fetchone()

# Получение всех покупок
def all_purchases():
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM purchases"
        return con.execute(sql).fetchall()

# Последние N покупок
def last_purchases(user_id, count):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM purchases WHERE user_id = ? ORDER BY increment DESC LIMIT {count}"
        return con.execute(sql, [user_id]).fetchall()


###############################################################################################
###############################            Настройки            ###############################
###############################################################################################

# Получение настроек
def get_settings():
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory

        return con.execute("SELECT * FROM settings").fetchone()

# Изменение настроек
def update_settings(**kwargs):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        queryy = "UPDATE settings SET"
        queryy, parameters = query(queryy, kwargs)
        con.execute(queryy, parameters)
        con.commit()


##############################################################################################
###############################            Платежки            ###############################
##############################################################################################

# Изменение платежек
def update_payments(**kwargs):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        queryy = "UPDATE payments SET"
        queryy, parameters = query(queryy, kwargs)
        con.execute(queryy, parameters)
        con.commit()

# Получение платежек
def get_payments():
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        return con.execute("SELECT * FROM payments").fetchone()


###############################################################################################
#############################            Пополнения            ################################
###############################################################################################

# Добавление пополнения
def add_refill(amount, way, user_id, user_name, first_name, comment):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO refills("
                    "user_id, user_name, user_full_name, comment, amount, receipt, way, date, date_unix) "
                    "VALUES (?,?,?,?,?,?,?,?,?)", [user_id, user_name, first_name, comment, amount, comment, way, get_date(), get_unix()])
        con.commit()

# Получение пополнения
def get_refill(receipt):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        return con.execute("SELECT * FROM refills WHERE receipt = ?", (receipt,)).fetchone()

# Получение всех пополнений
def all_refills():
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM refills"
        return con.execute(sql).fetchall()


##############################################################################################
#############################            Промокоды            ################################
##############################################################################################

# Получение промокода
def get_coupon_search(**kwargs):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM coupons"
        sql, parameters = query_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Получение активироного промокода
def get_activate_coupon(**kwargs):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM activ_coupons"
        sql, parameters = query_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Активировать промокод
def activate_coupon(user_id, coupon):
    with sqlite3.connect(path_db) as con:
        con.execute('''UPDATE activ_coupons SET coupon_name = ? WHERE user_id = ?''', (coupon, user_id,))
        con.commit()

# Добавить id юзера который ввел промокод
def add_activ_coupon(user_id):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        con.execute(f"INSERT INTO activ_coupons(user_id) VALUES (?)", (user_id,))
        con.commit()

# Редактирование промокода
def update_coupon(coupon, **kwargs):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE coupons SET"
        sql, parameters = query(sql, kwargs)
        parameters.append(coupon)
        con.execute(sql + "WHERE coupon = ?", parameters)
        con.commit()

# Создание промокода
def create_coupon(coupon, uses, discount):
    with sqlite3.connect(path_db) as con:
        con.execute("INSERT INTO coupons "
                    "(coupon, uses, discount) "
                    "VALUES (?, ?, ?)",
                    [coupon, uses, discount])
        con.commit()

# Удаление промокода
def delete_coupon(coupon):
    with sqlite3.connect(path_db) as con:
        con.execute("DELETE FROM coupons WHERE coupon = ?", (coupon,))
        con.execute("DELETE FROM activ_coupons WHERE coupon_name = ?", (coupon,))
        con.commit()


##############################################################################################
#############################            Категории            ################################
##############################################################################################

# Создать категорию
def add_category(name):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO categories (id, name) VALUES (?, ?)", (get_unix(True), name))
        con.commit()

# Удалить все категории
def del_all_cats():
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        con.execute("DELETE FROM categories")
        con.commit()

# Получение всех категорий
def get_all_categories():
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        return con.execute("SELECT * FROM categories").fetchall()

# Получение категории
def get_category(cat_id):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        return con.execute("SELECT * FROM categories WHERE id = ?", (cat_id,)).fetchone()

# Изменение категории
def update_category(cat_id, **kwargs):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        queryy = f"UPDATE categories SET"
        queryy, params = query(queryy, kwargs)
        params.append(cat_id)
        con.execute(queryy + "WHERE id = ?", params)
        con.commit()

# Удаление категории
def del_category(cat_id):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        con.execute("DELETE FROM categories WHERE id = ?", (cat_id,))
        con.commit()


##############################################################################################
############################            Под-Категории            #############################
##############################################################################################

# Удаление всех под-категорий
def del_all_pod_cats():
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        con.execute("DELETE FROM pod_categories")
        con.commit()

# Получение под-категорий
def get_pod_categories(cat_id):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        return con.execute("SELECT * FROM pod_categories WHERE cat_id = ?", (cat_id,)).fetchall()

# Создание под-категории
def add_pod_category(name, cat_id):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO pod_categories (id, name, cat_id) VALUES (?, ?, ?)", (get_unix(True), name, cat_id))
        con.commit()

# Получение всех под-категорий
def get_all_pod_categories():
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM pod_categories"
        return con.execute(sql).fetchall()

# Получение под-категории
def get_pod_category(pod_cat_id):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        return con.execute("SELECT * FROM pod_categories WHERE id = ?", (pod_cat_id,)).fetchone()

# Изменение под-категории
def update_pod_category(pod_cat_id, **kwargs):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        queryy = f"UPDATE pod_categories SET"
        queryy, params = query(queryy, kwargs)
        params.append(pod_cat_id)
        con.execute(queryy + "WHERE id = ?", params)
        con.commit()

# Удаление под-категории
def del_pod_category(pod_cat_id):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        con.execute("DELETE FROM pod_categories WHERE id = ?", (pod_cat_id,))
        con.commit()


#######################################################################################
############################            Позиции            ############################
#######################################################################################

# Создание позиции
def add_position(name, price, desc, photo, cat_id, infinity, pos_id, pod_cat_id = None):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        sql = "INSERT INTO positions (id, name, price, description, photo, date, category_id, pod_category_id, infinity) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        con.execute(sql, (pos_id, name, price, desc, photo, get_date(), cat_id, pod_cat_id, infinity))
        con.commit()

# Получение позиции
def get_position(pos_id):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        return con.execute("SELECT * FROM positions WHERE id = ?", (pos_id,)).fetchone()

# Изменение позиции
def update_position(pos_id, **kwargs):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        queryy = f"UPDATE positions SET"
        queryy, params = query(queryy, kwargs)
        params.append(pos_id)
        con.execute(queryy + "WHERE id = ?", params)
        con.commit()

# Получение всех позиций
def get_all_positions():
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        sql1 = "SELECT * FROM positions"
        return con.execute(sql1).fetchall()

# Получение позиций
def get_positions(cat_id = None, pod_cat_id = None):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        if pod_cat_id is not None:
            return con.execute("SELECT * FROM positions WHERE pod_category_id = ?", (pod_cat_id,)).fetchall()
        else:
            return con.execute("SELECT * FROM positions WHERE category_id = ?", (cat_id,)).fetchall()

# Удаление всех позиций
def del_all_positions():
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        con.execute("DELETE FROM positions")
        con.commit()

# Удаление позиции
def del_position(pos_id):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        con.execute("DELETE FROM positions WHERE id = ?", (pos_id,))
        con.commit()


######################################################################################
############################            Товары            ############################
######################################################################################

# Получение товаров
def get_items(**kwargs):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM items"
        sql, parameters = query_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Получение всех товаров
def get_all_items():
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM items"
        return con.execute(sql).fetchall()

# Очистка товаров
def del_all_items():
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM items"
        con.execute(sql)
        con.commit()

# Удаление товаров
def remove_item(**kwargs):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM items"
        sql, parameters = query_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()

# Покупка товаров
def buy_item(get_items, get_count, infinity):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory
        split_len, send_count, save_items = 0, 0, []
        if infinity == "-":
            for select_send_item in get_items:
                if send_count != get_count:
                    send_count += 1
                    if get_count >= 2:
                        select_data = f"{send_count}. {select_send_item['data']}"
                    else:
                        select_data = select_send_item['data']

                    save_items.append(select_data)
                    sql, parameters = query_args("DELETE FROM items",
                                                    {"id": select_send_item['id']})
                    con.execute(sql, parameters)

                    if len(select_data) >= split_len: split_len = len(select_data)
                else:
                    break
            con.commit()

            split_len += 1
            get_len = math.ceil(3500 / split_len)
        else:
            for select_send_item in get_items:
                if send_count != get_count:
                    send_count += 1
                    if get_count >= 2:
                        select_data = f"{send_count}. {select_send_item['data']}"
                    else:
                        select_data = select_send_item['data']

                    save_items.append(select_data)

                    if len(select_data) >= split_len: split_len = len(select_data)
                else:
                    break

            split_len += 1
            get_len = math.ceil(3500 / split_len)

    return save_items, send_count, get_len

# Добавление товара
def add_item(category_id, position_id, get_all_items):
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory

        for item_data in get_all_items:
            if not item_data.isspace() and item_data != "":
                con.execute("INSERT INTO items "
                            "(id, data, position_id, category_id, date) "
                            "VALUES (?, ?, ?, ?, ?)",
                            [random.randint(1000000000, 9999999999), item_data.strip(), position_id,
                            category_id, get_date()])
        con.commit()

#######################################################################################
############################            Создание            ###########################
############################           Базы Данных          ###########################
#######################################################################################

# Создание Базы Данных
def create_db():
    with sqlite3.connect(path_db) as con:
        con.row_factory = dict_factory

        # Пользователи
        if len(con.execute("PRAGMA table_info(users)").fetchall()) == 16:
            print("database was found (users | 1/11)")
        else:
            con.execute("CREATE TABLE users("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "id INTEGER,"
                        "is_ban TEXT,"
                        "user_name TEXT,"
                        "first_name TEXT,"
                        "balance INTEGER,"
                        "total_refill INTEGER DEFAULT 0,"
                        "count_refills INTEGER,"
                        "reg_date TIMESTAMP,"
                        "reg_date_unix INTEGER,"
                        "ref_lvl INTEGER DEFAULT 1,"
                        "ref_id INTEGER,"
                        "ref_user_name TEXT,"
                        "ref_first_name TEXT,"
                        "ref_count INTEGER DEFAULT 0,"
                        "ref_earn INTEGER DEFAULT 0)")
            

            print("database was not found (users | 1/11), creating...")

        # Настройки
        if len(con.execute("PRAGMA table_info(settings)").fetchall()) == 18:
            print("database was found (settings | 2/11)")
        else:
            con.execute("CREATE TABLE settings("
                        "is_work TEXT,"
                        "is_refill TEXT,"
                        "is_buy TEXT,"
                        "is_ref TEXT,"
                        "is_notify TEXT,"
                        "is_sub TEXT,"
                        "faq TEXT,"
                        "chat TEXT,"
                        "news TEXT,"
                        "support TEXT,"
                        "ref_percent_1 INTEGER,"
                        "ref_percent_2 INTEGER,"
                        "ref_percent_3 INTEGER,"
                        "ref_lvl_1 INTEGER,"
                        "ref_lvl_2 INTEGER,"
                        "ref_lvl_3 INTEGER,"
                        "profit_day INTEGER,"
                        "profit_week INTEGER)")

            con.execute("INSERT INTO settings("
                        "is_work, is_refill, is_buy, is_ref, is_notify, is_sub, faq, ref_percent_1, ref_percent_2, ref_percent_3, ref_lvl_1, ref_lvl_2, ref_lvl_3, support,"
                        "profit_day, profit_week)"
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        ["True", "False", "False", "False", "True", "False", "None", 0, 0, 0, 0, 0, 0, "None", get_unix(), get_unix()])
            print("database was not found (settings | 2/11), creating...")

        # Платежные системы
        if len(con.execute("PRAGMA table_info(payments)").fetchall()) == 5:
            print("database was found (payment systems | 3/11)")
        else:
            con.execute("CREATE TABLE payments("
                        "pay_qiwi TEXT,"
                        "pay_crystal TEXT,"
                        "pay_yoomoney TEXT,"
                        "pay_lolz TEXT,"
                        "pay_lava TEXT)")

            con.execute("INSERT INTO payments("
                        "pay_qiwi, pay_crystal, pay_yoomoney, pay_lolz, pay_lava) "
                        "VALUES (?, ?, ?, ?, ?)",
                        ['False', 'False', 'False', 'False', 'False'])
            print("database was not found (payment systems| 3/11), creating...")

        # Пополнения
        if len(con.execute("PRAGMA table_info(refills)").fetchall()) == 10:
            print("database was found (Payments | 4/11)")
        else:
            con.execute("CREATE TABLE refills("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "user_id INTEGER,"
                        "user_name TEXT,"
                        "user_full_name TEXT,"
                        "comment TEXT,"
                        "amount INTEGER,"
                        "receipt TEXT,"
                        "way TEXT,"
                        "date TIMESTAMP,"
                        "date_unix INTEGER)")
            print("database was not found (Payments | 4/11), creating...")

        # Категории
        if len(con.execute("PRAGMA table_info(categories)").fetchall()) == 3:
            print("database was found (Categories | 5/11)")
        else:
            con.execute("CREATE TABLE categories("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "id INTEGER,"
                        "name TEXT)")
            print("database was not found (Categories | 5/11), creating...")

        # Под-Категории
        if len(con.execute("PRAGMA table_info(pod_categories)").fetchall()) == 4:
            print("database was found (Sub-Categories | 6/11)")
        else:
            con.execute("CREATE TABLE pod_categories("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "cat_id INTEGER,"
                        "id INTEGER,"
                        "name TEXT)")
            print("database was not found (Sub-Categories | 6/11), creating...")

        # Позиции
        if len(con.execute("PRAGMA table_info(positions)").fetchall()) == 10:
            print("database was found (Items | 7/11)")
        else:
            con.execute("CREATE TABLE positions("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "id INTEGER,"
                        "name TEXT,"
                        "price INTEGER,"
                        "description TEXT,"
                        "photo TEXT,"
                        "date TIMESTAMP,"
                        "category_id INTEGER,"
                        "pod_category_id INTEGER,"
                        "infinity TEXT)")
            print("database was not found (Items | 7/11), creating...")

        # Товары
        if len(con.execute("PRAGMA table_info(items)").fetchall()) == 6:
            print("database was found (Goods | 8/11)")
        else:
            con.execute("CREATE TABLE items("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "id INTEGER,"
                        "data TEXT,"
                        "position_id INTEGER,"
                        "category_id INTEGER,"
                        "date TIMESTAMP)")
            print("database was not found (Goods | 8/11), creating...")

        # Промокоды
        if len(con.execute("PRAGMA table_info(coupons)").fetchall()) == 3:
            print("database was found (Promocodes| 9/11)")
        else:
            con.execute('CREATE TABLE coupons('
                        'coupon TEXT,'
                        'uses INTEGER,'
                        'discount INTEGER);')
            print("database was not found (Promocodes | 9/11), creating...")

        # Активные промокоды
        if len(con.execute("PRAGMA table_info(activ_coupons)").fetchall()) == 2:
            print("database was found (Active Promocodes | 10/11)")
        else:
            con.execute('CREATE TABLE activ_coupons('
                        'coupon_name TEXT,'
                        'user_id INTEGER);')
            print("database was not found (Active Promocodes | 10/11), creating...")

        # Покупки
        if len(con.execute("PRAGMA table_info(purchases)").fetchall()) == 12:
            print("database was found (Purchaches | 11/11)")
        else:
            con.execute("CREATE TABLE purchases("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "user_id INTEGER,"
                        "user_name TEXT,"
                        "user_full_name TEXT,"
                        "receipt TEXT,"
                        "count INTEGER,"
                        "price INTEGER,"
                        "position_id INTEGER,"
                        "position_name TEXT,"
                        "item TEXT,"
                        "date TIMESTAMP,"
                        "unix INTEGER)")
            print("database was not found (Purchaches | 11/11), creating...")

            con.commit()