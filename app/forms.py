from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, \
    SubmitField, SelectField, DateField, validators, ValidationError

from .models import Item, Purchase


class ItemForm(FlaskForm):
    name = StringField(label="Наименование товара", validators=[validators.DataRequired()])
    price = IntegerField(label="стоимость", validators=[validators.DataRequired()])
    submit = SubmitField(label="сохранить товар")

    def validate_price(self, price):
        if price.data < 100:
            raise ValidationError('товар не может стоить менее 100 ед.')



class PurchaseForm(FlaskForm):
    name = StringField(label="ФиО клиента")
    age = IntegerField(label='возраст клиента')
    item_id = SelectField("id товара")
    date_purchase = DateField('date:')
    submit = SubmitField(label="save")



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        result = []
        for item in Item.query.all():
            result.append((item.id, item.name))
        self.item_id.choices = result

    def validate_age(self, age):
        if age.data < 18:
            raise ValidationError('возраст должен быть не менее 18 лет')
