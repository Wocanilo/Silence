# This file is part of the Silence framework.
# Silence was developed by the IISSI1-TI team
# (Agustín Borrego, Daniel Ayala, Carlos Ortiz, Inma Hernández & David Ruiz)
# and it is distributed as open source software under the GNU-GPL 3.0 License.

from flask import Blueprint, jsonify, request
from bll.SubjectBLL import SubjectBLL
from bll.BLLException import BLLException

subject_api = Blueprint('subject_api', __name__)
subjectBLL = SubjectBLL()

# Methods for the subject endpoint

@subject_api.route("/subject", methods=["GET"])
def get_all():
    # Returns all subjects in the system
    subjects = subjectBLL.get_all()
    res = jsonify(subjects), 200
    return res

@subject_api.route("/subject/<int:oid>", methods=["GET"])
def get_by_oid(oid):
    # Returns one subject by OID
    res = None

    try:
        subject = subjectBLL.get_by_oid(oid)
        res = jsonify(subject), 200
    except BLLException as exc:
        error = {'error': str(exc)}
        res = jsonify(error), 400

    return res

@subject_api.route("/subject", methods=["POST"])
def insert():
    # Creates a new subject
    form = request.form

    name = form.get("name", default=None)
    acronym = form.get("acronym", default=None)
    n_credits = form.get("credits", default=None)
    course = form.get("course", default=None)
    subject_type = form.get("subject_type", default=None)
    degreeId = form.get("degreeId", default=None)

    res = None

    try:
        oid = subjectBLL.insert(name, acronym, n_credits, course, subject_type, degreeId)
        res = jsonify({'oid': oid}), 200
    except BLLException as exc:
        error = {'error': str(exc)}
        res = jsonify(error), 400

    return res

@subject_api.route("/subject/<int:oid>", methods=["PUT"])
def update(oid):
    # Updates an existing subject
    form = request.form

    name = form.get("name", default=None)
    acronym = form.get("acronym", default=None)
    n_credits = form.get("credits", default=None)
    course = form.get("course", default=None)
    subject_type = form.get("subject_type", default=None)
    degreeId = form.get("degreeId", default=None)

    res = None
    
    try:
        new_oid = subjectBLL.update(oid, name, acronym, n_credits, course, subject_type, degreeId)
        res = jsonify({'oid': new_oid}), 200
    except BLLException as exc:
        error = {'error': str(exc)}
        res = jsonify(error), 400

    return res
           
@subject_api.route("/subject/<int:oid>", methods=["DELETE"])
def delete(oid):
    # Deletes a subject by OID
    res = None

    try:
        subjectBLL.delete(oid)
        res = jsonify({'oid': oid}), 200
    except BLLException as exc:
        error = {'error': str(exc)}
        res = jsonify(error), 400

    return res
