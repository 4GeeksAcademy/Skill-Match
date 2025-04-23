from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey, DateTime, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing import List, Optional
from datetime import datetime

db = SQLAlchemy()

# --- MODELOS BASE ---


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    first_name: Mapped[str] = mapped_column(String(80), nullable=True)
    last_name: Mapped[str] = mapped_column(String(80), nullable=True)
    # 'freelancer', 'employer', 'admin'
    role: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    # Relaciones
    profile: Mapped[Optional["Profile"]] = relationship(
        "Profile", back_populates="user", uselist=False)
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="employer")
    proposals: Mapped[List["Proposal"]] = relationship(
        "Proposal", back_populates="freelancer")

    def __repr__(self):
        return f"<User {self.email} - {self.role}>"

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# --- PERFIL DEL FREELANCER ---

class Profile(db.Model):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), unique=True, nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(Text)
    profile_picture: Mapped[Optional[str]] = mapped_column(String(255))
    hourly_rate: Mapped[Optional[float]] = mapped_column(Float)
    rating: Mapped[Optional[float]] = mapped_column(Float)

    # Relaciones
    user: Mapped["User"] = relationship("User", back_populates="profile")
    skills: Mapped[List["FreelancerSkill"]] = relationship(
        "FreelancerSkill", back_populates="profile", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Profile UserID={self.user_id}>"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "bio": self.bio,
            "profile_picture": self.profile_picture,
            "hourly_rate": self.hourly_rate,
            "rating": self.rating,
            "skills": [fs.skill.serialize() for fs in self.skills]
        }


# --- SKILLS Y RELACIÓN MANY-TO-MANY ---


class Skill(db.Model):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    freelancers: Mapped[List["FreelancerSkill"]] = relationship(
        "FreelancerSkill", back_populates="skill")

    def __repr__(self):
        return f"<Skill {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class FreelancerSkill(db.Model):
    __tablename__ = "freelancer_skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"))
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))

    profile: Mapped["Profile"] = relationship(
        "Profile", back_populates="skills")
    skill: Mapped["Skill"] = relationship(
        "Skill", back_populates="freelancers")

    def serialize(self):
        return {
            "id": self.id,
            "profile_id": self.profile_id,
            "skill": self.skill.serialize()
        }


# --- PROYECTOS Y PROPUESTAS ---


class Project(db.Model):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    employer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(100))
    budget: Mapped[Optional[float]] = mapped_column(Float)
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime)
    # open, in_progress, completed, cancelled
    status: Mapped[str] = mapped_column(String(20), default="open")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    employer: Mapped["User"] = relationship("User", back_populates="projects")
    proposals: Mapped[List["Proposal"]] = relationship(
        "Proposal", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project {self.title}>"

    def serialize(self):
        return {
            "id": self.id,
            "employer_id": self.employer_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "budget": self.budget,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "proposals": [p.serialize_basic() for p in self.proposals]
        }


class Proposal(db.Model):
    __tablename__ = "proposals"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    freelancer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    message: Mapped[str] = mapped_column(Text, nullable=False)
    proposed_budget: Mapped[Optional[float]] = mapped_column(Float)
    status: Mapped[str] = mapped_column(
        String(20), default="pending")  # pending, accepted, rejected
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    project: Mapped["Project"] = relationship(
        "Project", back_populates="proposals")
    freelancer: Mapped["User"] = relationship(
        "User", back_populates="proposals")

    def __repr__(self):
        return f"<Proposal ProjectID={self.project_id} FreelancerID={self.freelancer_id}>"

    def serialize(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "freelancer_id": self.freelancer_id,
            "message": self.message,
            "proposed_budget": self.proposed_budget,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "freelancer": self.freelancer.serialize()
        }

    def serialize_basic(self):
        return {
            "id": self.id,
            "freelancer_id": self.freelancer_id,
            "status": self.status,
            "proposed_budget": self.proposed_budget
        }
