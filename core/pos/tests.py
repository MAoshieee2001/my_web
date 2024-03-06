from config.wsgi import *
from core.pos.models import *
from core.accounts.models import *

# Create your tests here.
# category = Category.objects.first()

# product = Product(category=category, code='PR78362XA', names='Lasantes', pvp=0.00, stock=1)
# print(product.save())

# product = Product.objects.first()
# print(product.toJSON())

user = User.objects.first()
print(user.toJSON())