from app import app, db
from flask import render_template, request, redirect, url_for


import models as models


@app.route('/payment-method')
def payment_method_page():
    payment_methods = models.PaymentMethod.query.all()
    return render_template('mdPaymentMethod.html', payment_methods=payment_methods)


@app.route('/add-payment-method', methods=['GET', 'POST'])
def add_payment_method():
    payment_method = models.PaymentMethod()
    
    if request.method == 'POST':
        payment_method.name = request.form['name']
        
        db.session.add(payment_method)
        db.session.commit()
        
        return redirect(url_for('payment_method_page'))
    
    return render_template('edit-payment-method.html', payment_method=payment_method)


@app.route('/edit-payment-method/<int:payment_method_id>', methods=['GET', 'POST'])
def edit_payment_method(payment_method_id):
    payment_method = models.PaymentMethod.query.get(payment_method_id)
    
    if request.method == 'POST':
        payment_method.name = request.form['name']
        
        db.session.commit()
        
        return redirect(url_for('payment_method_page'))
    
    return render_template('edit-payment-method.html', payment_method=payment_method)


@app.route('/delete-payment-method/<int:payment_method_id>', methods=['GET', 'POST'])
def delete_payment_method(payment_method_id):
    payment_method = models.PaymentMethod.query.get(payment_method_id)
    db.session.delete(payment_method)
    db.session.commit()
    
    return redirect(url_for('payment_method_page'))