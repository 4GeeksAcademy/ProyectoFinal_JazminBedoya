from flask import Flask, jsonify, request
from backend.app import app, db
from backend.models import User


#Obtener todos los usuarios

@app.route("/users" , methods=['GET'])
def getUser():
    users = User.query.all()
    return jsonify([u.serialize () for u in users]), 200



#Obtener usuario por id
@app.route("/users/<int:id>" , methods=['GET'])
def getUser(id):
    users = User.query.get_or_404(id)
    return jsonify(user.serialize ()), 200



#Crear nuevo usuario

@app.route("/users" , methods=['POST'])
def createUser():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "faltan campos obligatorios"}),400
   
    #Verificar si email ya existe
    if User.query.filter_by(email = data['email']).first():
        return jsonify({"error": "El email ya esta registrado"}),400
    
    new_user = User(
        name= data.get('name'),
        email = data['email'],
     )
    
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()),201


@app.route("/users/<int:id>" , methods=['PUT'])
def updateUser(id): 
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)

    #Si es una nueva contraseña , se vuelve a encriptar

    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()
    return jsonify(user.serialize()),200


#Eliminar Usuario

@app.route("/users/<int:id>" , methods=['DELETE'])
def deleteUser(id): 
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado correctamente"}), 200












app.run(host='0.0.0.0')