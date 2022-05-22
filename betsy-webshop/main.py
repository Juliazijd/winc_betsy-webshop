__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import models
from models import User, Tag, Product, UserProduct, ProductTag
from peewee import fn, SqliteDatabase


def search(term):
    return (Product.select()
        .where(
            fn.Lower(Product.name.contains(fn.Lower(term))) |
            fn.Lower(Product.description.contains(fn.Lower(term)))
        ))


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
    query = (ProductTag.select(models.Tag.name.alias('tag_name'),
                            Product.name.alias('name'))
            .join(models.Tag,
                on=(models.Tag.id == ProductTag.tag_id))
            .join(Product,
                on=Product.id == ProductTag.product_id)
            .where(ProductTag.tag_id == tag_id))

    return [item for item in query.dicts()]


def add_product_to_catalog(user_id, product):
    new_product = Product.create(name=product['name'],
                            description=product['description'],
                            price=product['price'],
                            quantity=product['quantity'],
                            )

    tags_to_add = []
    for tag in product['tags']:
        new_tag, _ = Tag.get_or_create(name=tag)
        tags_to_add.append(new_tag)
        
    new_product.tags.add(tags_to_add)
    
    UserProduct.create(user_id=user_id, product_id=new_product)
    
    return new_product.id



def update_stock(product_id, new_quantity):
    return (Product.update(quantity=new_quantity)
            .where(Product.id == product_id)
            .execute())


def purchase_product(product_id, buyer_id, quantity):
    return (models.Purchase.insert(product_id=product_id,
                                user_id=buyer_id,
                                quantity=quantity)
                                .execute())


def remove_product(product_id):
    return (UserProduct.delete()
              .where(UserProduct.product_id == product_id)
              .execute())


def create_tables():
    db = SqliteDatabase(":memory:", pragmas={'foreign_keys': 1})
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
        ["Kandelaar", "Kaarsenhouder", 12, 10],
        ["Vogelhuisje", "Voederplaats voor vogels", 6.5, 10],
        ["Badmat", "Ter decoratie van badkamer", 10, 15],
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
