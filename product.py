from database import Database


class Product:
    def __init__(self, name, quantity, price, product_id):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.product_id = product_id

    def __str__(self):
        return f"{str(self.product_id).center(10)}" \
               f"{self.name.center(10)}" \
               f"{str(self.price).center(10)}" \
               f"{str(self.quantity).center(10)}"

    @staticmethod
    def create_table_of_products():
        with Database() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS products "
                           "(id integer primary key, name text, quantity integer, "
                           "price real)")

    @staticmethod
    def add_new_product_to_db(product_name, product_quantity, product_price):
        with Database() as cursor:
            cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
                           (product_name, product_quantity, product_price))

        # product = Product(product_name, description, quantity, price, category)
        # with Database as cursor:
        #     cursor.execute("INSERT INTO products (name, description, quantity, price, category) VALUES (?, ?, ?, "
        #                    "?, ?)", (product.name, product.description, product.quantity, product.price,
        #                              product.category))

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
    def update_products_from_db():
        with Database() as cursor:
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            return products



    # def __init__(self, name, description, quantity, price, category, product_id=None):
    #     self.product_id = product_id
    #     self.name = name
    #     self.description = description
    #     self.quantity = quantity
    #     self.price = price
    #     self.category = category



