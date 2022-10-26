import datetime

from flask import request, render_template, redirect, url_for, flash

from . import app, db
from .models import Item, Purchase
from .forms import ItemForm, PurchaseForm


def item_view():
    title = 'список товаров'
    items = Item.query.all()
    return render_template('items.html', items=items, title=title)


def item_create():
    title = 'добавление товара'
    form = ItemForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            item = Item()
            form.populate_obj(item)
            db.session.add(item)
            db.session.commit()
            flash(f'товар под №{item.id} успешно добавлен', 'success')
            return redirect(url_for('item'))
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    flash(f'ошибка в поле "{field}", текст ошибки: {error}', 'danger')

    return render_template('item_form.html', form=form, title=title)

def purchase_view():
    title = 'список покупателей'
    purchases = Purchase.query.all()
    return render_template('purchases.html', purchases=purchases, title=title)

def purchase_create():
    title = 'добавление покупателя товара'
    form = PurchaseForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            purchase = Purchase()
            form.populate_obj(purchase)
            db.session.add(purchase)
            db.session.commit()
            flash(f'покупка №{purchase.id} успешно добавлена', 'success')
            return redirect(url_for('purchase'))
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    flash(f'ошибка в поле "{field}", текст ошибки: {error}', 'danger')

    return render_template('purchase_form.html', form=form, title=title)

def get_single_item(item_id):
    item = Item.query.filter_by(id=item_id).first()
    return render_template('single_item.html', item=item)


def update_single_item(item_id):
    item = Item.query.filter_by(id=item_id).first()
    form = ItemForm(request.form, obj=item)

    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(item)
            db.session.commit()
            flash(f'товар №"{item.id}" успешно обновлен', 'success')
            return redirect(url_for('single_item', item_id=item.id))
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    flash(f'ошибка в поле "{field}", текст ошибки: {error}', 'danger')
    return render_template('item_form.html', form=form, item=item)


def delete_single_item(item_id):
    item = Item.query.filter_by(id=item_id).first()
    if request.method == 'GET':
        return render_template('delete_item.html', item=item)
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('item'))


########################################################################################################################

def get_single_purchase(purchase_id):
    purchase = Purchase.query.filter_by(id=purchase_id).first()
    return render_template('single_purchase.html', purchase=purchase)


def update_single_purchase(purchase_id):
    purchase = Purchase.query.filter_by(id=purchase_id).first()
    form = PurchaseForm(request.form, obj=purchase)

    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(purchase)
            db.session.commit()
            flash(f'покупка №{purchase.id} успешно обновлена', 'success')
            return redirect(url_for('single_purchase', purchase_id=purchase_id))
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    flash(f'ошибка в поле "{field}", текст ошибки: {error}', 'danger')
    return render_template('purchase_form.html', form=form, purchase=purchase)


def delete_single_purchase(purchase_id):
    purchase = Purchase.query.filter_by(id=purchase_id).first()
    if request.method == 'GET':
        return render_template('delete_purchase.html', purchase=purchase)
    if request.method == 'POST':
        db.session.delete(purchase)
        db.session.commit()
        flash(f'Данные о продажах под номером {purchase.id} успешно удалены', 'success')
        return redirect(url_for('purchase'))
