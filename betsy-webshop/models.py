from peewee import *

db = SqliteDatabase(":memory:", pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db

class Address(BaseModel):
    street = CharField()
    house_number = IntegerField()
    postal_code = CharField()
    city = CharField()
    country = CharField()

    class Meta:
        database = db

class User(BaseModel):
    first_name = CharField()
    last_name = CharField()
    address = ForeignKeyField(Address)
    billing_address = ForeignKeyField(Address)

class Tag(BaseModel):
    name = CharField(unique=True)


class Product(BaseModel):
    name = CharField(index=True)
    description = CharField(index=True)
    price = DecimalField(max_digits=10, decimal_places=2,
                                auto_round=True)
    quantity = IntegerField(constraints=[Check('quantity >= 0')])
    tags = ManyToManyField(Tag)


class UserProduct(BaseModel):
    user_id = ForeignKeyField(User)
    product_id = ForeignKeyField(Product)


class Purchase(BaseModel):
    user_id = ForeignKeyField(User)
    product_id = ForeignKeyField(Product)
    quantity = IntegerField(constraints=[Check('quantity >= 0')])


ProductTag = Product.tags.get_through_model()


if __name__ == "__main__":
    pass