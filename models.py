from datetime import datetime

from sqlalchemy.orm import backref
from unwrap import db, login_manager,app
from flask_login import UserMixin
from flask import flash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20),unique=False, nullable=False)
    lastname = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    cart= db.relationship('Cart',backref='buyer',lazy=True)
    orders = db.relationship('Order', backref='buyer', lazy=True)

    def add_to_cart(self,product_id):
        row_to_add=Cart(product_id=product_id,user_id=self.id)
        db.session.add(row_to_add)
        db.session.commit()
        flash("Your item has been added","success")

    def create_order(self, delivery_info):
        """
        从购物车创建订单
        delivery_info: 包含配送信息的字典
        """
        # 计算总价
        cart_items = Cart.query.filter_by(buyer=self).all()
        if not cart_items:
            return None
            
        total_price = sum(
            item.quantity * Products.query.get(item.product_id).price 
            for item in cart_items
        )
        
        # 创建订单
        order = Order(
            order_number=Order.generate_order_number(),
            user_id=self.id,
            total_price=total_price,
            email=delivery_info['email'],
            delivery_area=delivery_info['delivery_area'],
            phone=delivery_info['phone'],
            address=delivery_info['address'],
            notes=delivery_info.get('notes', '')
        )
        
        # 添加订单项
        for cart_item in cart_items:
            product = Products.query.get(cart_item.product_id)
            order_item = OrderItem(
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=product.price
            )
            order.items.append(order_item)
        
        # 保存订单
        try:
            db.session.add(order)
            # 清空购物车
            for item in cart_items:
                db.session.delete(item)
            db.session.commit()
            return order
        except Exception as e:
            db.session.rollback()
            raise e

    def __repr__(self):
        return (f"User>'{self.firstname}',"f"'{self.lastname}','{self.email}'<")


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    #size = db.Column(db.String(20))

    def __repr__(self):
        return (f"Product('{self.name}',"
                f"'{self.price}')")


class Cart(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    product_id=db.Column(db.Integer, db.ForeignKey('products.id'),nullable=False)
    quantity=db.Column(db.Integer, nullable=False,default=1)

    def __repr__(self):
        return (f"Cart('Product id:{self.product_id}',"
                f"'User id{self.user_id}')")


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    delivery_area = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default='pending')
    is_subscription = db.Column(db.Boolean, default=False)
    subscription_duration = db.Column(db.Integer)
    
    # 订单项关系保持不变
    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f"Order('{self.order_number}', '{self.order_date}')"

    @staticmethod
    def generate_order_number():
        prefix = datetime.utcnow().strftime('%Y%m%d')
        count = Order.query.filter(
            Order.order_date >= datetime.utcnow().date()
        ).count()
        return f"{prefix}{str(count + 1).zfill(4)}"


class OrderItem(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    # 关联商品
    product = db.relationship('Products')

    def __repr__(self):
        return f"OrderItem('{self.product_id}', '{self.quantity}')"


if __name__ == '__main__':
    pass