from app import app, db
from flask import render_template, request, redirect, url_for
from flask_login import login_required


import models as models


@app.route('/service')
@login_required
def service_page():
    services = models.Service.query.all()
    return render_template('mdService.html', services=services)


@app.route('/add-service', methods=['GET', 'POST'])
@login_required
def add_service():
    if request.method == 'POST':
        service = models.Service()
        service.name = request.form['name']
        service.description = request.form['description']
        service.price = request.form['price']
        
        db.session.add(service)
        db.session.commit()
        
        return redirect(url_for('service_page'))
    
    return render_template('add-service.html')


@app.route('/edit-service/<int:service_id>', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    service = models.Service.query.get(service_id)
    
    if request.method == 'POST':
        service.name = request.form['name']
        service.description = request.form['description']
        service.price = request.form['price']
        
        db.session.commit()
        
        return redirect(url_for('service_page'))
    
    return render_template('edit-service.html', service=service)


@app.route('/delete-service/<int:service_id>', methods=['GET', 'POST'])
@login_required
def delete_service(service_id):
    service = models.Service.query.get(service_id)
    db.session.delete(service)
    db.session.commit()
    
    return redirect(url_for('service_page'))