from product import Product
from colorama import Fore, init


class Application:
    def __init__(self):
        self.products = []
        init(autoreset=True)
        self.create_table_if_not_exists()
        self.run()

    @staticmethod
    def create_table_if_not_exists():
        Product.create_table_of_products()

    def run(self):
        flag = True
        while flag:
            self.show_options()
            user_choice = input(Fore.YELLOW + "Your choice here from 1 to 8: ")
            match user_choice:
                # Showing the list of products
                case "1":
                    self.show_products()
                # Adding a product to the list
                case "2":
                    self.add_product()
                # Updating a product's price
                case "3":
                    self.update_price()
                # Updating a product's quantity by its id or name
                case "4":
                    self.update_quantity()
                # Searching a product
                case "5":
                    self.search_product()
                # Selling a product
                case "6":
                    self.sell_product()
                # Deleting a product
                case "7":
                    response = input(Fore.RED + "Are you sure of deleting a product: Y/n ").strip().lower()
                    if response == "y":
                        self.remove_product()
                # Showing the products out of stock
                case "8":
                    self.low_stock_report()
                # Quitting the application
                case _:
                    answer = input(Fore.RED + "Are you sure you want to exit? Y/n ").strip().lower()
                    if answer == "y":
                        print(Fore.GREEN + "Thank you for using the app.\nGood bye!")
                        flag = False

    @staticmethod
    def show_options():
        print("""
    1. To show products
    2. To add a product
    3. To update a product price
    4. To update a product quantity
    5. To search a product 
    6. To sell a product
    7. To remove a product
    8. To generate a low stock report
    To exit press any key...
          """)

    # add a new product or update the quantity of the existing product
    def add_product(self):
        product_name = self.input_product_name()
        existing_product = self.product_exists(product_name)
        if existing_product:
            quantity = self.input_product_qnt()
            existing_product.quantity += int(quantity)
            Product.update_existing_product(quantity, product_name)
            print(f"{Fore.GREEN}The quantity of the product {product_name.capitalize()} successfully updated.")
        else:
            # description = input("Enter a product description: ")
            # quantity = self.input_product_qnt()
            # price = self.input_product_price()
            # category = input("Enter a product category: ")
            price = self.input_product_price()
            quantity = self.input_product_qnt()
            Product.add_new_product_to_db(product_name, quantity, price)
            print(f"{Fore.GREEN}New product {product_name.capitalize()} successfully added.")

    # Clears and updates the product list from the database
    def update_product_list(self):
        self.products.clear()
        products = Product.load_products_from_db()
        for product in products:
            self.products.append(Product(product[1], product[2], product[3], product[0]))

    # Prints the products in the console
    def show_products(self):
        self.update_product_list()
        if self.products:
            self.print_list_header()
            for product in self.products:
                print(f"{Fore.BLUE}{product}")
        else:
            print(f"{Fore.RED}The list is empty.")

    # Checks if a product exists by its name
    def product_exists(self, name):
        self.update_product_list()
        for product in self.products:
            if product.name == name:
                return product

    # Checks if a products exists by its id
    def product_exists_by_id(self, product_id):
        self.update_product_list()
        for product in self.products:
            if product.product_id == product_id:
                return product

    # Searches a product by its id, name, quantity, category or price"
    def search_product(self):
        print("""
    1. To search a product by id press 1
    2. To search a product by its name press 2
    3. To search a product by its quantity press 3
    4. To search a product by its the category press 4
    5. To search a product by its price press 5
    """)
        choice = input("Searching by option: ")

        match choice:
            case "1":
                self.search_by_id()
            case "2":
                self.search_by_name()
            case "3":
                self.search_by_qnt()
            case "4":
                pass
            case "5":
                self.search_by_price()

    def search_by_name(self):
        product_name = self.input_product_name()
        existing_product = self.product_exists(product_name)
        if existing_product:
            self.print_list_header()
            print(existing_product)
        else:
            print(f"{Fore.RED}Product not found.")

    def search_by_id(self):
        product_id = self.input_product_id()
        existing_product = self.product_exists_by_id(product_id)
        if existing_product:
            self.print_list_header()
            print(existing_product)
        else:
            print(f"{Fore.RED}Product not found.")

    def search_by_qnt(self):
        qnt = self.input_product_qnt()
        found_products = list(filter(lambda product: product.quantity >= qnt, self.products))
        if found_products:
            found_qnt = len(found_products)
            if found_qnt != 1:
                print(f"{Fore.GREEN}Found {len(found_products)} products with quantity greater or equal to {qnt}.")
            else:
                print(f"{Fore.GREEN}Found {len(found_products)} product with quantity greater or equal to {qnt}.")
            self.print_list_header()
            for item in found_products:
                print(item)
        else:
            print(f"{Fore.RED}Nothing found.")

    def search_by_price(self):
        price = self.input_product_price()
        found_products = list(filter(lambda product: product.price >= price, self.products))
        found_qnt = len(found_products)
        if found_products:
            if found_qnt != 1:
                print(f"{Fore.GREEN}Found {found_qnt} products with a price greater or equal to {price}.")
            else:
                print(f"{Fore.GREEN}Found {found_qnt} product with a price greater or equal to {price}.")
            self.print_list_header()
            for item in found_products:
                print(item)
        else:
            print(f"{Fore.RED}Nothing found.")

    def sell_product(self):
        print("Starting to sell...")
        product_name = self.input_product_name()
        existing_product = self.product_exists(product_name)
        if existing_product:
            qnt = self.input_product_qnt()
            if existing_product.quantity - qnt >= 0:
                print(f"{Fore.GREEN}Amount to pay: {qnt * existing_product.price} "
                      f"dollars for {qnt} units of {existing_product.name}.")
                if qnt != 1:
                    print(f"{Fore.GREEN}{qnt} units of {existing_product.name} have been sold.")
                else:
                    print(f"{Fore.GREEN}{qnt} unit of {existing_product.name} has been sold.")
                existing_product.quantity -= qnt
                Product.sell_product_by_name(existing_product.quantity, product_name)
            else:
                print(f"{Fore.RED}Not sufficient amount of product, try a lesser quantity.")
        else:
            print(f"{Fore.RED}There is no {product_name}.")

    # Removes a product by its id or name
    def remove_product(self):
        print("""
    1. To remove the product by its id press 1
    2. To remove the product by its name press 2
            """)
        choice = input("Removing by option: ")
        match choice:
            case "1":
                product_id = int(input("Input the product id: "))
                existing_product = self.product_exists_by_id(product_id)
                if existing_product:
                    Product.remove_product_by_id_from_db(existing_product.product_id)
                    print(f"{Fore.GREEN}{existing_product.name.capitalize()} successfully removed.")
                else:
                    print(f"{Fore.RED}Product not found.")

            case "2":
                product_name = self.input_product_name()
                existing_product = self.product_exists(product_name)
                if existing_product:
                    Product.remove_product_by_name_from_db(existing_product.name)
                    print(f"{Fore.GREEN}{existing_product.name.capitalize()} successfully removed.")

                else:
                    print(f"{Fore.RED}Product not found.")

            case _:
                print(f"{Fore.RED}Invalid option.")

    def update_price(self):
        print("""
        1. To update the product by id press 1
        2. To update the product by name press 2
        """)
        choice = input("Updating the product by option: ")
        match choice:
            case "1":
                product_id = int(input("Input the product id: "))
                existing_product = self.product_exists_by_id(product_id)
                if existing_product:
                    print("Updating price...")
                    price = self.input_product_price()
                    Product.update_price_by_id(price, product_id)
                    print(f"{Fore.GREEN}{existing_product.name.capitalize()} price updated.")
                else:
                    print(f"{Fore.RED}Product not found.")

            case "2":
                product_name = self.input_product_name()
                existing_product = self.product_exists(product_name)
                if existing_product:
                    print("Updating price...")
                    price = self.input_product_price()
                    print(f"{Fore.GREEN}{existing_product.name.capitalize()} price updated.")
                    Product.update_price_by_name(price, product_name)
                else:
                    print(f"{Fore.RED}Product not found.")

            case _:
                print(f"{Fore.RED}Invalid option.")

    def update_quantity(self):
        print("""
        1. To update the product by id press 1
        2. To update the product by name press 2
           """)
        choice = input("Updating the product quantity by option: ")
        match choice:
            case "1":
                product_id = self.input_product_id()
                quantity = self.input_product_qnt()
                existing_product = self.product_exists_by_id(product_id)
                if existing_product:
                    Product.update_product_quantity_by_id(quantity, existing_product.product_id)
                    print(f"{Fore.GREEN}The product quantity successfully updated.")
                else:
                    print(f"{Fore.RED}Product not found.")
            case "2":
                product_name = self.input_product_name()
                quantity = self.input_product_qnt()
                existing_product = self.product_exists(product_name)
                if existing_product:
                    Product.update_product_quantity_by_name(quantity, product_name)
                    print(f"{Fore.GREEN}The product quantity successfully updated.")
            case _:
                print(f"{Fore.RED}Invalid option.")

    def low_stock_report(self):
        self.update_product_list()
        quantity = self.input_product_qnt()
        if self.products:
            low_stock = list(filter(lambda product: product.quantity <= quantity, self.products))
            print(f"\tProducts with the quantity less or equal to {quantity}:")
            self.print_list_header()
            for item in low_stock:
                print(f"{Fore.BLUE}{item}")
        else:
            print(f"{Fore.GREEN} No product of low stock.")

    # inputs static methods
    @staticmethod
    def input_product_name():
        while True:
            name = input("Enter a product name: ").strip().lower()
            if name:
                return name
            else:
                print(f"{Fore.RED}You didn't enter a product name.")

    @staticmethod
    def input_product_price():
        while True:
            try:
                price = float(input("Enter a product price: "))
                if price > 0:
                    return price
                else:
                    raise ValueError(f"{Fore.RED}The price must be greater than 0")
            except ValueError as e:
                print(f"{Fore.RED}{e}")

    @staticmethod
    def input_product_qnt():
        while True:
            try:
                qnt = int(input("Enter a product quantity: "))
                if qnt >= 0:
                    return qnt
            except ValueError as e:
                print(f"{Fore.RED}{e}")

    @staticmethod
    def input_product_id():
        while True:
            try:
                return int(input("Enter a product id: "))
            except ValueError as e:
                print(f"{Fore.RED}{e}")

    # Prints the headline
    @staticmethod
    def print_list_header():
        print(f"{Fore.MAGENTA}{'Id'.center(10)}{'Name'.center(10)}{'Price'.center(10)}{'Quantity'.center(10)}")


if __name__ == "__main__":
    Application()
