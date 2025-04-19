from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from .models import db, User, Profile, Skill, FreelancerSkill, Project, Proposal

routes = Blueprint('routes', __name__)

# --- AUTENTICACIÓN ---

@routes.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not email or not password or role not in ['freelancer', 'employer']:
        return jsonify({"msg": "Datos inválidos"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Correo ya registrado"}), 409

    hashed_pw = generate_password_hash(password)
    user = User(email=email, password=hashed_pw, role=role)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201

@routes.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Credenciales inválidas"}), 401

    access_token = create_access_token(identity={
        "id": user.id,
        "email": user.email,
        "role": user.role
    })

    return jsonify(access_token=access_token, user=user.serialize())


# --- USUARIO ACTUAL ---

@routes.route('/users/me', methods=['GET'])
@jwt_required()
def get_current_user():
    identity = get_jwt_identity()
    user = User.query.get(identity['id'])
    return jsonify(user.serialize())


# --- PERFIL FREELANCER ---

@routes.route('/freelancer/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()['id']
    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({"msg": "Perfil no encontrado"}), 404
    return jsonify(profile.serialize())

@routes.route('/freelancer/profile', methods=['POST'])
@jwt_required()
def create_profile():
    user_id = get_jwt_identity()['id']
    if Profile.query.filter_by(user_id=user_id).first():
        return jsonify({"msg": "Perfil ya existe"}), 400

    data = request.json
    profile = Profile(
        user_id=user_id,
        bio=data.get('bio'),
        profile_picture=data.get('profile_picture'),
        hourly_rate=data.get('hourly_rate'),
        rating=data.get('rating')
    )
    db.session.add(profile)
    db.session.commit()
    return jsonify(profile.serialize()), 201

@routes.route('/freelancer/profile', methods=['PATCH'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()['id']
    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({"msg": "Perfil no encontrado"}), 404

    data = request.json
    profile.bio = data.get('bio', profile.bio)
    profile.hourly_rate = data.get('hourly_rate', profile.hourly_rate)
    profile.profile_picture = data.get('profile_picture', profile.profile_picture)
    db.session.commit()

    return jsonify(profile.serialize())


# --- SKILLS ---

@routes.route('/skills', methods=['GET'])
def list_skills():
    skills = Skill.query.all()
    return jsonify([skill.serialize() for skill in skills])

@routes.route('/skills', methods=['POST'])
@jwt_required()
def create_skill():
    identity = get_jwt_identity()
    if identity["role"] != "admin":
        return jsonify({"msg": "Solo admin puede crear skills"}), 403

    data = request.json
    skill = Skill(name=data.get('name'))
    db.session.add(skill)
    db.session.commit()
    return jsonify(skill.serialize()), 201

@routes.route('/freelancer/skills', methods=['POST'])
@jwt_required()
def add_freelancer_skills():
    user_id = get_jwt_identity()['id']
    profile = Profile.query.filter_by(user_id=user_id).first()
    skill_ids = request.json.get('skill_ids', [])

    for skill_id in skill_ids:
        fs = FreelancerSkill(profile_id=profile.id, skill_id=skill_id)
        db.session.add(fs)

    db.session.commit()
    return jsonify({"msg": "Skills agregadas"}), 201

@routes.route('/freelancer/skills/<int:skill_id>', methods=['DELETE'])
@jwt_required()
def remove_freelancer_skill(skill_id):
    user_id = get_jwt_identity()['id']
    profile = Profile.query.filter_by(user_id=user_id).first()
    fs = FreelancerSkill.query.filter_by(profile_id=profile.id, skill_id=skill_id).first()
    if fs:
        db.session.delete(fs)
        db.session.commit()
        return jsonify({"msg": "Skill eliminada"}), 200
    return jsonify({"msg": "Skill no encontrada"}), 404


# --- PROJECTS ---

@routes.route('/projects', methods=['GET'])
def get_all_projects():
    projects = Project.query.filter(Project.status != 'cancelled').all()
    return jsonify([p.serialize() for p in projects])

@routes.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    identity = get_jwt_identity()
    if identity['role'] != 'employer':
        return jsonify({"msg": "Solo empleadores pueden crear proyectos"}), 403

    data = request.json
    project = Project(
        employer_id=identity['id'],
        title=data.get('title'),
        description=data.get('description'),
        category=data.get('category'),
        budget=data.get('budget'),
        deadline=data.get('deadline'),
        status="open"
    )
    db.session.add(project)
    db.session.commit()
    return jsonify(project.serialize()), 201

@routes.route('/projects/<int:id>', methods=['GET'])
def get_project(id):
    project = Project.query.get(id)
    if not project:
        return jsonify({"msg": "Proyecto no encontrado"}), 404
    return jsonify(project.serialize())


# --- PROPOSALS ---

@routes.route('/projects/<int:project_id>/proposals', methods=['POST'])
@jwt_required()
def submit_proposal(project_id):
    identity = get_jwt_identity()
    if identity['role'] != 'freelancer':
        return jsonify({"msg": "Solo freelancers pueden postularse"}), 403

    data = request.json
    proposal = Proposal(
        project_id=project_id,
        freelancer_id=identity['id'],
        message=data.get('message'),
        proposed_budget=data.get('proposed_budget')
    )
    db.session.add(proposal)
    db.session.commit()
    return jsonify(proposal.serialize()), 201

@routes.route('/projects/<int:project_id>/proposals', methods=['GET'])
@jwt_required()
def list_proposals_for_project(project_id):
    identity = get_jwt_identity()
    project = Project.query.get(project_id)

    if not project or project.employer_id != identity['id']:
        return jsonify({"msg": "No autorizado"}), 403

    return jsonify([p.serialize() for p in project.proposals])

@routes.route('/freelancer/proposals', methods=['GET'])
@jwt_required()
def get_my_proposals():
    user_id = get_jwt_identity()['id']
    proposals = Proposal.query.filter_by(freelancer_id=user_id).all()
    return jsonify([p.serialize() for p in proposals])


# --- ADMIN ---

@routes.route('/admin/users', methods=['GET'])
@jwt_required()
def list_users():
    identity = get_jwt_identity()
    if identity["role"] != "admin":
        return jsonify({"msg": "Acceso denegado"}), 403

    users = User.query.all()
    return jsonify([u.serialize() for u in users])
