from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Profile, Skill, FreelancerSkill, Project, Proposal
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

routes = Blueprint('routes', __name__)
api = Blueprint('api', __name__)

bcrypt = Bcrypt()

# --- AUTENTICACIÓN ---


@routes.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not email or not password or role not in ['freelancer', 'employer']:
        return jsonify({"msg": "Rellena todos los campos"}), 400

    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({'msg': 'este email ya esta registrado'}), 400

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(email=email, password=password_hash, role=role)

    db.session.add(new_user)
    db.session.commit()

    user_id = new_user.id
    access_token = create_access_token(identity=str(user_id))

    return jsonify({**new_user.serialize(), "access_token": access_token}), 201


@routes.route('/login', methods=['POST'])
def login():

    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'msg': 'error en email o password'}), 400

    current_user = User.query.filter_by(email=email).first()

    if not current_user:
        return jsonify({'msg': 'usuario no existe'}), 404

    pass_db = current_user.password
    true_or_false = bcrypt.check_password_hash(pass_db, password)

    if true_or_false:

        user_id = current_user.id
        access_token = create_access_token(
            identity=str(user_id))

        return jsonify({
            "msg": "Sesion iniciada",
            "access_token": access_token,
            "email": email
        }), 200

    else:
        return jsonify({"msg": "Usuario o contraseña invalido."}), 401


@api.route('/private', methods=["GET"])
@jwt_required()
def home():

    current_user_id = get_jwt_identity()

    if current_user_id:
        users = User.query.all()
        user_list = []
        for user in users:
            user_act = {
                "id": user.id,
                "email": user.email,
                "is_active": user.is_active
            }
            user_list.append(user_act)

        return jsonify({"users": user_list}), 200

    else:
        return jsonify({"Error": "Error al iniciar sesion"}), 401

 # generar route para obtener el usuario todos los usuarios


# --- USUARIO ACTUAL ---

@routes.route('/users/me', methods=['GET'])
def get_current_user():
    user_id = request.args.get('user_id')

    if user_id:
        user = User.query.get(user_id)
    else:
        user = User.query.first()
        if not user:
            user = User(email="dev@example.com",
                        password=generate_password_hash("dev123"), role="admin")
            db.session.add(user)
            db.session.commit()

    return jsonify(user.serialize())


# --- PERFIL FREELANCER ---

@routes.route('/freelancer/profile', methods=['GET'])
def get_profile():
    user_id = request.args.get('user_id')

    if user_id:
        profile = Profile.query.filter_by(user_id=user_id).first()
    else:
        user = User.query.filter_by(role='freelancer').first()
        if not user:
            user = User(email="freelancer@example.com",
                        password=generate_password_hash("dev123"), role="freelancer")
            db.session.add(user)
            db.session.commit()

        profile = Profile.query.filter_by(user_id=user.id).first()

    if not profile and user:
        profile = Profile(
            user_id=user.id,
            bio="Perfil de desarrollo para pruebas",
            profile_picture="https://via.placeholder.com/150",
            hourly_rate=25.0,
            rating=4.5
        )
        db.session.add(profile)
        db.session.commit()

    if not profile:
        return jsonify({"msg": "Perfil no encontrado"}), 404

    return jsonify(profile.serialize())


@routes.route('/freelancer/profile', methods=['POST'])
def create_profile():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        user = User.query.filter_by(role='freelancer').first()
        if not user:
            user = User(email="freelancer@example.com",
                        password=generate_password_hash("dev123"), role="freelancer")
            db.session.add(user)
            db.session.commit()
        user_id = user.id

    profile = Profile.query.filter_by(user_id=user_id).first()
    if profile:
        profile.bio = data.get('bio', profile.bio)
        profile.profile_picture = data.get(
            'profile_picture', profile.profile_picture)
        profile.hourly_rate = data.get('hourly_rate', profile.hourly_rate)
        profile.rating = data.get('rating', profile.rating)
    else:
        profile = Profile(
            user_id=user_id,
            bio=data.get('bio'),
            profile_picture=data.get('profile_picture'),
            hourly_rate=data.get('hourly_rate'),
            rating=data.get('rating', 0)
        )
        db.session.add(profile)

    db.session.commit()
    return jsonify(profile.serialize()), 201


@routes.route('/freelancer/profile', methods=['PATCH'])
def update_profile():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        user = User.query.filter_by(role='freelancer').first()
        if not user:
            return jsonify({"msg": "No hay usuarios freelancer"}), 404
        user_id = user.id

    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({"msg": "Perfil no encontrado"}), 404

    profile.bio = data.get('bio', profile.bio)
    profile.hourly_rate = data.get('hourly_rate', profile.hourly_rate)
    profile.profile_picture = data.get(
        'profile_picture', profile.profile_picture)
    db.session.commit()
    return jsonify(profile.serialize())


# --- SKILLS ---

@routes.route('/skills', methods=['GET'])
def list_skills():
    skills = Skill.query.all()

    if not skills:
        default_skills = [
            "JavaScript", "Python", "React", "Node.js",
            "Angular", "Vue.js", "Django", "Flask",
            "SQL", "MongoDB", "AWS", "Docker"
        ]
        for skill_name in default_skills:
            skill = Skill(name=skill_name)
            db.session.add(skill)
        db.session.commit()
        skills = Skill.query.all()

    return jsonify([skill.serialize() for skill in skills])


@routes.route('/skills', methods=['POST'])
def create_skill():
    data = request.json
    skill = Skill(name=data.get('name'))
    db.session.add(skill)
    db.session.commit()
    return jsonify(skill.serialize()), 201


@routes.route('/freelancer/skills', methods=['POST'])
def add_freelancer_skills():
    data = request.json
    user_id = data.get('user_id')
    skill_ids = data.get('skill_ids', [])

    if not user_id:
        user = User.query.filter_by(role='freelancer').first()
        if not user:
            user = User(email="freelancer@example.com",
                        password=generate_password_hash("dev123"), role="freelancer")
            db.session.add(user)
            db.session.commit()
        user_id = user.id

    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile:
        profile = Profile(
            user_id=user_id,
            bio="Perfil de desarrollo para pruebas",
            profile_picture="https://via.placeholder.com/150",
            hourly_rate=25.0,
            rating=4.5
        )
        db.session.add(profile)
        db.session.commit()

    for skill_id in skill_ids:
        existing = FreelancerSkill.query.filter_by(
            profile_id=profile.id, skill_id=skill_id).first()
        if not existing:
            fs = FreelancerSkill(profile_id=profile.id, skill_id=skill_id)
            db.session.add(fs)

    db.session.commit()
    return jsonify({"msg": "Skills agregadas", "profile_id": profile.id, "skill_ids": skill_ids}), 201


@routes.route('/freelancer/skills/<int:skill_id>', methods=['DELETE'])
def remove_freelancer_skill(skill_id):
    user_id = request.args.get('user_id')

    if not user_id:
        user = User.query.filter_by(role='freelancer').first()
        if not user:
            return jsonify({"msg": "No hay usuarios freelancer"}), 404
        user_id = user.id

    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({"msg": "Perfil no encontrado"}), 404

    fs = FreelancerSkill.query.filter_by(
        profile_id=profile.id, skill_id=skill_id).first()
    if fs:
        db.session.delete(fs)
        db.session.commit()
        return jsonify({"msg": "Skill eliminada"}), 200
    return jsonify({"msg": "Skill no encontrada"}), 404


# --- PROJECTS ---

@routes.route('/projects', methods=['GET'])
def get_all_projects():
    projects = Project.query.filter(Project.status != 'cancelled').all()

    if not projects:
        employer = User.query.filter_by(role='employer').first()
        if not employer:
            employer = User(email="employer@example.com",
                            password=generate_password_hash("dev123"), role="employer")
            db.session.add(employer)
            db.session.commit()

        example_projects = [
            {
                "title": "Desarrollo de sitio web corporativo",
                "description": "Necesitamos un sitio web moderno y responsivo para nuestra empresa.",
                "category": "web-development",
                "budget": 1500.00,
                "deadline": "2025-12-31",
                "status": "open"
            },
            {
                "title": "Aplicación móvil para delivery",
                "description": "Buscamos desarrolladores para crear una app de entrega de comida.",
                "category": "mobile-app",
                "budget": 3000.00,
                "deadline": "2025-10-15",
                "status": "open"
            },
            {
                "title": "Rediseño de identidad de marca",
                "description": "Necesitamos actualizar nuestra imagen corporativa.",
                "category": "design",
                "budget": 800.00,
                "deadline": "2025-08-01",
                "status": "open"
            }
        ]

        for p_data in example_projects:
            project = Project(
                employer_id=employer.id,
                title=p_data["title"],
                description=p_data["description"],
                category=p_data["category"],
                budget=p_data["budget"],
                deadline=p_data["deadline"],
                status=p_data["status"]
            )
            db.session.add(project)

        db.session.commit()
        projects = Project.query.filter(Project.status != 'cancelled').all()

    return jsonify([p.serialize() for p in projects])


@routes.route('/projects', methods=['POST'])
def create_project():
    data = request.json
    employer_id = data.get('employer_id')

    if not employer_id:
        employer = User.query.filter_by(role='employer').first()
        if not employer:
            employer = User(email="employer@example.com",
                            password=generate_password_hash("dev123"), role="employer")
            db.session.add(employer)
            db.session.commit()
        employer_id = employer.id

    # Convertir la cadena de fecha a objeto datetime
    deadline_str = data.get('deadline')
    deadline = None
    if deadline_str:
        try:
            # Asumiendo formato YYYY-MM-DD
            from datetime import datetime
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
        except ValueError:
            return jsonify({"msg": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400

    project = Project(
        employer_id=employer_id,
        title=data.get('title'),
        description=data.get('description'),
        category=data.get('category'),
        budget=data.get('budget'),
        deadline=deadline,
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
def submit_proposal(project_id):
    data = request.json
    freelancer_id = data.get('freelancer_id')

    if not freelancer_id:
        freelancer = User.query.filter_by(role='freelancer').first()
        if not freelancer:
            freelancer = User(email="freelancer@example.com",
                              password=generate_password_hash("dev123"), role="freelancer")
            db.session.add(freelancer)
            db.session.commit()
        freelancer_id = freelancer.id

    project = Project.query.get(project_id)
    if not project:
        return jsonify({"msg": "Proyecto no encontrado"}), 404

    proposal = Proposal(
        project_id=project_id,
        freelancer_id=freelancer_id,
        message=data.get('message'),
        proposed_budget=data.get('proposed_budget')
    )
    db.session.add(proposal)
    db.session.commit()
    return jsonify(proposal.serialize()), 201


@routes.route('/projects/<int:project_id>/proposals', methods=['GET'])
def list_proposals_for_project(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({"msg": "Proyecto no encontrado"}), 404

    return jsonify([p.serialize() for p in project.proposals])


@routes.route('/freelancer/proposals', methods=['GET'])
def get_my_proposals():
    freelancer_id = request.args.get('freelancer_id')
    if not freelancer_id:
        freelancer = User.query.filter_by(role='freelancer').first()
        if not freelancer:
            return jsonify([])
        freelancer_id = freelancer.id

    proposals = Proposal.query.filter_by(freelancer_id=freelancer_id).all()
    return jsonify([p.serialize() for p in proposals])


# --- ADMIN ---

@routes.route('/admin/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users])
