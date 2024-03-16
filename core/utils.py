import random
import string
import random

import settings
from config import wsgi
import json

from core.pos.models import Product, Category, Customer


# print(f'PR{random.randint(100, 999)}{random.choice(string.ascii_letters)}')


def insert_product():
    ruta = f'{settings.BASE_DIR}/deploy/json/categories.json'
    try:
        with open(ruta, encoding='utf8') as product_file:
            products = json.load(product_file)
            for i in range(0, 12):
                for p in products:
                    product = Product()
                    product.category = Category.objects.get_or_create(names=p['names'])[0]
                    product.names = p['names']
                    product.code = random.randint(1, 200)
                    product.pvp = round(random.randint(1, 100) * random.random(), 2)
                    product.save()
    except Exception as e:
        print(e)


insert_product()

'''
def insert_customer():
    ruta = f'{settings.BASE_DIR}/deploy/json/customers.json'
    try:
        with open(ruta, encoding='utf8') as customer_file:
            customers = json.load(customer_file)
            for c in customers:
                customer = Customer()
                customer.first_names = c['first']
                customer.last_names = c['last']
                customer.date_birthday = c['date']
                customer.gender = bool(c['gender'])
                customer.dni = c['dni']
                customer.address = c['address']
                customer.phone = c['phone']
                customer.save()
    except Exception as e:
        print(e)

insert_customer()
'''

'''
def insert_categories():
    ruta = f'{settings.BASE_DIR}/deploy/json/generated.json'
    try:
        with open(ruta, encoding='utf8') as category_file:
            categories = json.load(category_file)
            for c in categories:
                category = Category()
                category.names = c['company']
                category.save()
    except Exception as e:
        print(e)
insert_categories()
'''
