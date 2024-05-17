from app import app, db
from flask import render_template, request, redirect, url_for
from flask_login import login_required


import models as models


@app.route('/policy')
@login_required
def policy_page():
    policies = models.Policy.query.all()
    return render_template('mdpolicy.html', policies=policies)


@app.route('/add-policy', methods=['GET', 'POST'])
@login_required
def add_policy():
    policy = models.Policy()
    
    if request.method == 'POST':
        policy.name = request.form['name']
        policy.description = request.form['description']
        policy.value = request.form['value']
        policy.value_type = models.PolicyValueType[request.form['value_type']]

        db.session.add(policy)
        db.session.commit()
        
        return redirect(url_for('policy_page'))
    
    value_types = [value_type.name for value_type in models.PolicyValueType]

    return render_template('edit-policy.html'
                           , policy=policy
                           , value_types=value_types)


@app.route('/edit-policy/<int:policy_id>', methods=['GET', 'POST'])
@login_required
def edit_policy(policy_id):
    policy = models.Policy.query.get(policy_id)
    
    if request.method == 'POST':
        policy.name = request.form['name']
        policy.description = request.form['description']
        policy.value = request.form['value']
        policy.value_type = models.PolicyValueType[request.form['value_type']]
        
        db.session.commit()
        
        return redirect(url_for('policy_page'))
    
    value_types = [value_type.name for value_type in models.PolicyValueType]

    return render_template('edit-policy.html'
                           , policy=policy
                           , value_types=value_types)


@app.route('/delete-policy/<int:policy_id>', methods=['GET', 'POST'])
@login_required
def delete_policy(policy_id):
    policy = models.Policy.query.get(policy_id)
    db.session.delete(policy)
    db.session.commit()
    
    return redirect(url_for('policy_page'))