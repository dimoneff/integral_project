from database import Database
from colorama import Fore


class Product:
    def __init__(self, name, description, category, quantity, price, product_id):
        self.name = name
        self.description = description
        self.category = category
        self.quantity = quantity
        self.price = price
        self.product_id = product_id

    def __str__(self):
        if self.quantity == 0:
            qnt = f"{Fore.RED}{str(self.quantity).center(10)}"
        elif 3 >= self.quantity >= 1:
            qnt = f"{Fore.YELLOW}{str(self.quantity).center(10)}"
        else:
            qnt = f"{Fore.GREEN}{str(self.quantity).center(10)}"

        return f"{str(self.product_id).center(10)}" \
               f"{self.name.center(25)}" \
               f"{self.description.center(25)}" \
               f"{self.category.center(25)}" \
               f"{str(self.price).center(10)}" \
               f"{qnt}"

    @staticmethod
    def create_table_of_products():
        with Database() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS products "
                           "(id INTEGER PRIMARY KEY, "
                           "name TEXT NOT NULL, "
                           "description TEXT NOT NULL, "
                           "category text NOT NULL, "
                           "quantity INTEGER NOT NULL, "
                           "price REAL NOT NULL)")

    @staticmethod
    def load_initial_data():
        with Database() as cursor:
            query = "INSERT INTO products (name, description, " \
                    "category, price, quantity) " \
                    "VALUES (?, ?, ?, ?, ?)"
            values = (("steeleye stout", "12 oz bottles", "beverages", 17.99, 24),
                      ("sasquatch ale", "12 oz bottles", "beverages", 13.99, 0),
                      ("mascarpone fabioli", "200 g pkgs", "dairy products", 31.99, 20),
                      ("gula malacca", "2 kg bags", "condiments", 19.99, 3),
                      ("mozzarella di giovanni", "200 g pkgs", "dairy products", 34.99, 4),
                      ("vegie-spread", "625 g jars", "condiments", 43.99, 15),
                      ("spegesild", "450 g glasses", "seafood", 11.99, 4),
                      ("ipoh coffee", "500 g tins", "beverages", 45.99, 16),
                      ("thüringer rostbratwurst", "bags x 30 sausgs", "meat/poultry", 123.99, 50),
                      ("alice mutton", "1 kg tins", "meat/poultry", 38.99, 3))
            cursor.executemany(query, values)

    @staticmethod
    def add_new_product_to_db(product_name, product_description, product_category, product_quantity, product_price):
        with Database() as cursor:
            cursor.execute("INSERT INTO products (name, description, category, quantity, price) "
                           "VALUES (?, ?, ?, ?, ?)",
                           (product_name, product_description, product_category, product_quantity, product_price))

    @staticmethod
    def update_existing_product(product_quantity, product_name):
        with Database() as cursor:
            cursor.execute("UPDATE products SET quantity = ? WHERE name = ?",
                           (product_quantity, product_name))

    @staticmethod
    def update_price_by_id(product_price, product_id):
        with Database() as cursor:
            cursor.execute("UPDATE products SET price = ? WHERE id = ?",
                           (product_price, product_id))

    @staticmethod
    def update_price_by_name(product_price, product_name):
        with Database() as cursor:
            cursor.execute("UPDATE products SET price = ? WHERE name = ?",
                           (product_price, product_name))

    @staticmethod
    def update_product_quantity_by_id(product_qnt, product_id):
        with Database() as cursor:
            cursor.execute("UPDATE products SET quantity = ? WHERE id = ?",
                           (product_qnt, product_id))

    @staticmethod
    def update_product_quantity_by_name(product_qnt, product_name):
        with Database() as cursor:
            cursor.execute("UPDATE products SET quantity = ? WHERE name = ?",
                           (product_qnt, product_name))

    @staticmethod
    def remove_product_by_name_from_db(product_name):
        with Database() as cursor:
            cursor.execute("DELETE FROM products WHERE name = ?",
                           (product_name,))

    @staticmethod
    def remove_product_by_id_from_db(product_id):
        with Database() as cursor:
            cursor.execute("DELETE FROM products WHERE id = ?",
                           (product_id,))

    @staticmethod
    def sell_product_by_name(product_quantity, product_name):
        with Database() as cursor:
            cursor.execute("UPDATE products SET quantity = ? WHERE name = ?",
                           (product_quantity, product_name))

    @staticmethod
    def sell_product_by_id(product_quantity, product_id):
        with Database() as cursor:
            cursor.execute("UPDATE products SET quantity = ? WHERE id = ?",
                           (product_quantity, product_id))

    @staticmethod
    def load_products_from_db():
        with Database() as cursor:
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            return products
