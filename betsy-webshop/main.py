__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import models
from models import User, Tag, Product, Purchase, UserProduct, ProductTag
from peewee import fn, SqliteDatabase


def search(term):
    products = (Product.select()
        .where(
            fn.Lower(Product.name.contains(fn.Lower(term))) |
            fn.Lower(Product.description.contains(fn.Lower(term)))
        ))
    if len(products) > 0:
        print("In stock:")
        for product in products:
            return f"Product name: {product.name}, price per unit: €{product.price}, available quantity: {product.quantity}"
    else:
        return f"No {term} available"

def list_user_products(user_id):
    products_query = (UserProduct.select(Product)
                    .join(Product,
                        on=(UserProduct.product_id == Product.id))
                    .join(User,
                        on=(UserProduct.user_id == User.id))
                    .where(UserProduct.user_id == user_id)
                    )
    return [item for item in products_query.dicts()]


def list_products_per_tag(tag_id):
    query = (ProductTag.select(models.Tag.name.alias("tag_name"),
                            Product.name.alias("name"))
            .join(models.Tag,
                on=(models.Tag.id == ProductTag.tag_id))
            .join(Product,
                on=Product.id == ProductTag.product_id)
            .where(ProductTag.tag_id == tag_id))

    return [item for item in query.dicts()]


def add_product_to_catalog(user_id, product):
    Product.create(
        name=product[0],
        description=product[1],
        price=product[2],
        quantity=product[3],
        tag=user_id),
    
    return f"{product[3]} units of {product[0]} were added to the database"


def update_stock(product_id, new_quantity):
    try:
        (Product
            .update(quantity=new_quantity)
            .where(Product.id == product_id)
            .execute())
        return "Stock is updated"
    except Exception:
        return "Unfortunately this product is not available"


def purchase_product(product_id, user_id, quantity):
    try:
        product = Product.get_by_id(product_id)
        old_quantity = product.quantity

        if quantity <= old_quantity:
            (Purchase.insert(user_id=user_id,
                                product_id=product_id,
                                quantity=quantity)
                                .execute())

            new_quantity = (old_quantity - quantity)
            update_stock(product_id, new_quantity)
            return f"You are buying {quantity} x {product.name} for €{product.price} per unit"
        else:
            return f"There are {old_quantity} units of {product.name} available, please adjust the quantity"
    except Exception:
        return "Unfortunately this product is not available"


def remove_product(product_id):
    try:
        (UserProduct.delete()
              .where(UserProduct.product_id == product_id)
              .execute())
        return f"Product is removed"

    except Exception:
        return "No product available with this id"



def create_tables():
    db = SqliteDatabase(":memory:", pragmas={"foreign_keys": 1})
    with db:
        db.create_tables([models.User,
                          models.Product,
                          models.Address,
                          models.Tag,
                          models.ProductTag,
                          models.UserProduct,
                          models.Purchase,
                          ])


def data():
    user_data = [
        ["Jelle", "Jootje", 1, 1],
        ["Dorini", "Festini", 2, 1],
        ["Showmas", "Koopman", 3, 1],
    ]

    address_data = [
        ["Eerste Oosterparkstraat", 1, "1091hh", "Amsterdam", "Nederland"],
        ["Tweede Constantijn Huygensstraat", 2, "1054ct", "Amsterdam", "Nederland"],
        ["Derde Kostverlorenkade", 3, "1054tn", "Amsterdam", "Nederland"]
    ]

    product_data = [
        ["Candlestick", "Candle holder", 12, 10],
        ["Birdhouse", "Nesting and feeding site for birds", 6.5, 10],
        ["Bath mat", "Bathroom decoration", 10, 15],
    ]

    tag_data = [
        ["tag 1"],
        ["tag 2"],
        ["tag 3"]
    ]

    user_product_data = [
        [1, 1],
        [1, 2],
        [2, 2]
    ]

    transaction_data = [
        [1, 1, 5],
        [1, 2, 6],
        [2, 3, 4]
    ]

    product_tag_data = [
        [1, 1],
        [2, 1],
        [3, 3]
    ]

    for item in address_data:
        models.Address.create(
            street=item[0],
            house_number=item[1],
            postal_code=item[2],
            city=item[3],
            country=item[4]
        )

    for item in user_data:
        models.User.create(
            first_name=item[0],
            last_name=item[1],
            address=item[2],
            billing_address=item[3]
        )

    for item in product_data:
        Product.create(
            name=item[0],
            description=item[1],
            price=item[2],
            quantity=item[3]
        )

    for item in tag_data:
        models.Tag.create(
            name=item[0]
        )

    for item in transaction_data:
        models.Purchase.create(
            user_id=item[0],
            product_id=item[1],
            quantity=item[2]
        )

    for item in user_product_data:
        models.UserProduct.create(
            user_id=item[0],
            product_id=item[1]
        )

    for item in product_tag_data:
        models.ProductTag.create(
            product_id=item[0],
            tag_id=item[1]
        )


if __name__ == "__main__":    
    create_tables()
    data()
    print(search("candlestick"))
    print(add_product_to_catalog(15, ["Table cloth", "Table decoration", 22, 8]))
    print(list_user_products(2))
    print(purchase_product(3, 2, 1))