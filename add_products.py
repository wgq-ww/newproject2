from unwrap import db, app
from unwrap.user.models import Products

# 添加应用上下文
with app.app_context():
    # 添加三种规格的清洁套装
    products = [
        Products(
            name='Personal Care and Cleaning Set (Small)',
            description='Perfect for individuals or small households. Contains essential cleaning and personal care products.',
            price=40.00
        ),
        Products(
            name='Personal Care and Cleaning Set (Medium)',
            description='Ideal for small families. More products for comprehensive home care.',
            price=66.00
        ),
        Products(
            name='Personal Care and Cleaning Set (Large)',
            description='Best for large families. Complete set of cleaning and personal care products.',
            price=99.00
        )
    ]

    # 添加商品到数据库
    for product in products:
        # 检查是否已存在相同名称的产品
        existing_product = Products.query.filter_by(name=product.name).first()
        if not existing_product:
            db.session.add(product)

    db.session.commit() 