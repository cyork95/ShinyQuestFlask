from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, User, Pokemon, Hunt

hunts_bp = Blueprint('hunts', __name__, url_prefix='/hunts')

@hunts_bp.route('/')
def hunts():
    if 'user_id' not in session:
        flash('Please log in to access your hunts.', 'error')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    hunts = Hunt.query.filter_by(user_id=user.id).all()
    return render_template('hunts.html', hunts=hunts)

@hunts_bp.route('/add', methods=['GET', 'POST'])
def add_hunt():
    if 'user_id' not in session:
        flash('Please log in to add a hunt.', 'error')
        return redirect(url_for('login'))
    if request.method == 'POST':
        pokemon_name = request.form['pokemon_name']
        method = request.form['method']
        pokemon = Pokemon.query.filter_by(name=pokemon_name).first()
        if not pokemon:
            pokemon = Pokemon(name=pokemon_name)
            db.session.add(pokemon)
            db.session.commit()
        new_hunt = Hunt(user_id=session['user_id'], pokemon_id=pokemon.id, method=method)
        db.session.add(new_hunt)
        db.session.commit()
        flash('Hunt added successfully!', 'success')
        return redirect(url_for('hunts.hunts'))
    return render_template('add_hunt.html')

@hunts_bp.route('/update/<int:hunt_id>', methods=['POST'])
def update_hunt(hunt_id):
    if 'user_id' not in session:
        flash('Please log in to update a hunt.', 'error')
        return redirect(url_for('login'))
    hunt = Hunt.query.get_or_404(hunt_id)
    if hunt.user_id != session['user_id']:
        flash('You are not authorized to update this hunt.', 'error')
        return redirect(url_for('hunts.hunts'))
    action = request.form.get('action')
    if action == 'increment':
        hunt.encounters += 1
    elif action == 'decrement' and hunt.encounters > 0:
        hunt.encounters -= 1
    elif action == 'complete':
        hunt.status = 'Completed'
    db.session.commit()
    flash('Hunt updated successfully!', 'success')
    return redirect(url_for('hunts.hunts'))