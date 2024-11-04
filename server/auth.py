from flask import request, jsonify, render_template, session
from flask_session import Session
from models import User
from app import db
from app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
server_session = Session(app)


@app.route('/@me')
def get_current_user():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = User.query.filter_by(id = user_id).first()
    return jsonify(user.to_dict()), 200


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    data = request.form
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    existing_user = User.query.filter_by(username=new_user.username, email=new_user.email).first() is not None
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'username': new_user.username,
            'email': new_user.email
        }
    }), 201


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    data = request.form
    user = User.query.filter_by(username=data['username'] or data['email']).first()
    if user is None:
        return jsonify({'error': 'Invalid username or email'}), 401
    
    if not user.check_password(data['password']):
        return jsonify({'error': 'Invalid password'}), 401
    
    session['user_id'] = user.id
    return jsonify({
        'message': 'Login successful',
        'user': {
            'username': user.username,
            'email': user.email
        }
    }), 200

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return render_template('logout.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)