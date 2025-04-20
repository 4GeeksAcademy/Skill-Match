from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from src.api.models import db, User, Profile, Skill, Project, Proposal, FreelancerSkill

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de JWT
app.config['JWT_SECRET_KEY'] = 'super-secret-key-for-testing'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hora

# Inicializar extensiones
db.init_app(app)
Migrate(app, db)
JWTManager(app)

# Crear todas las tablas
with app.app_context():
    db.drop_all()  # Elimina todas las tablas existentes
    db.create_all()  # Crea todas las tablas definidas en los modelos

    # Creando algunas skills de ejemplo
    skills = [
        Skill(name="JavaScript"),
        Skill(name="Python"),
        Skill(name="React"),
        Skill(name="Node.js"),
        Skill(name="Flask"),
        Skill(name="Django")
    ]

    for skill in skills:
        db.session.add(skill)

    # Creando un usuario admin
    admin = User(
        email="admin@example.com",
        password="admin123",
        role="admin"
    )
    db.session.add(admin)

    db.session.commit()

    print("Base de datos inicializada correctamente.")
    print("Tablas creadas: users, profiles, skills, freelancer_skills, projects, proposals")
    print("Usuario admin creado - Email: admin@example.com, Password: admin123")
    print("Skills ejemplo creadas: JavaScript, Python, React, Node.js, Flask, Django")
