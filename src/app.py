"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person
app = Flask(__name__)

# Inicializamos la familia Jackson
jackson_family = FamilyStructure("Jackson")

# Cargar los 3 miembros iniciales
jackson_family.add_member({
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
})

jackson_family.add_member({
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
})

jackson_family.add_member({
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
})

# Obtener todos los miembros
@app.route("/members", methods=["GET"])
def get_members():
    try:
        return jsonify(jackson_family.get_all_members()), 200
    except:
        return jsonify({"error": "Server error"}), 500

# Obtener un miembro por id
@app.route("/members/<int:member_id>", methods=["GET"])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member:
            return jsonify(member), 200
        else:
            return jsonify({"error": "Member not found"}), 404
    except:
        return jsonify({"error": "Server error"}), 500

# Agregar un nuevo miembro
@app.route("/members", methods=["POST"])
def add_member():
    try:
        member = request.get_json()
        if not member or "first_name" not in member or "age" not in member or "lucky_numbers" not in member:
            return jsonify({"error": "Bad request"}), 400

        new_member = jackson_family.add_member(member)
        return jsonify(new_member), 200
    except:
        return jsonify({"error": "Server error"}), 500

# Eliminar un miembro por id
@app.route("/members/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    try:
        deleted = jackson_family.delete_member(member_id)
        if deleted:
            return jsonify({"done": True}), 200
        else:
            return jsonify({"error": "Member not found"}), 404
    except:
        return jsonify({"error": "Server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)