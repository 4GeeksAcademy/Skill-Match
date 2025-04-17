from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, DateTime, Enum, func, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date, time

import enum
from typing import List

db = SQLAlchemy()

class RoleEnum (enum.Enum):
    admin = "admin"
    employer = "employer"
    freelancer = "freelancer"

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    # created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())  // OPCIONAL
    # updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())  // OPCIONAL

     # Perfiles
    employer_profile: Mapped["Employer"] = relationship("Employer", back_populates="user", uselist=False)
    freelancer_profile: Mapped["Freelancer"] = relationship("Freelancer", back_populates="user", uselist=False)

    # Reseñas
    authored_reviews: Mapped[List["Review"]] = relationship("Review", back_populates="author", foreign_keys="[Review.author_user_id]")
    received_reviews: Mapped[List["Review"]] = relationship("Review", back_populates="target", foreign_keys="[Review.target_user_id]")

    # Reportes
    authored_reports: Mapped[List["Report"]] = relationship("Report", back_populates="reporter", foreign_keys="[Report.reporter_user_id]")
    received_reports: Mapped[List["Report"]] = relationship("Report", back_populates="target", foreign_keys="[Report.target_user_id]")
    reviewed_reports: Mapped[List["Report"]] = relationship("Report", back_populates="reviewed_by_admin", foreign_keys="[Report.reviewed_by_admin_id]")


    def __repr__(self) -> str:
        return f"<User {self.id} ({self.email}) - {self.role}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email, 
            "role": self.role,
            "authored_reviews": [review.serialize() for review in self.authored_reviews],  # Reseñas que el usuario ha escrito
            "received_reviews": [review.serialize() for review in self.received_reviews],  # Reseñas que el usuario ha recibido

        }

    




class Review(db.Model):
    __tablename__ = "reviews"  # Corregir de _tablename_ a __tablename__

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    appointment_id: Mapped[int] = mapped_column(ForeignKey("appointments.id"), nullable=False)
    author_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    target_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)  # Puntaje de 1 a 5
    comment: Mapped[str] = mapped_column(String(300), nullable=True)  # Comentario opcional
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)  # Usamos func.now()

    # Relaciones inversas con User
    author: Mapped["User"] = relationship("User", back_populates="authored_reviews", foreign_keys=[author_user_id])
    target: Mapped["User"] = relationship("User", back_populates="received_reviews", foreign_keys=[target_user_id])

    # Relaciones con Appointment (suponiendo que tienes este modelo)
    appointment: Mapped["Appointment"] = relationship("Appointment", back_populates="reviews")
    
    def __repr__(self):
        return f"<Review {self.id} by User {self.author_user_id} for User {self.target_user_id}>"

    def serialize(self):
        return {
            "id": self.id,
            "appointment_id": self.appointment_id,
            "author_user_id": self.author_user_id,
            "target_user_id": self.target_user_id,
            "score": self.score,
            "comment": self.comment,
            "created_at": self.created_at.isoformat(),  # Fecha en formato ISO 8601
            "author": self.author.serialize() if self.author else None,  # Serializar el autor si existe
            "target": self.target.serialize() if self.target else None,  # Serializar el objetivo (target) si existe
            "appointment": self.appointment.serialize() if self.appointment else None,  # Serializar la cita si existe
        }





class Report(db.Model):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    reporter_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    target_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    reviewed_by_admin_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)

    reason: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(300), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relaciones inversas
    reporter: Mapped["User"] = relationship("User", back_populates="authored_reports", foreign_keys=[reporter_user_id])
    target: Mapped["User"] = relationship("User", back_populates="received_reports", foreign_keys=[target_user_id])
    reviewed_by_admin: Mapped["User"] = relationship("User", back_populates="reviewed_reports", foreign_keys=[reviewed_by_admin_id])


    def __repr__(self):
        return f"<Report {self.id} by User {self.reporter_user_id} for User {self.target_user_id}>"
    

    def serialize(self):
        return {
            "id": self.id,
            "reporter_user_id": self.reporter_user_id,
            "target_user_id": self.target_user_id,
            "reviewed_by_admin_id": self.reviewed_by_admin_id,
            "reason": self.reason,
            "description": self.description,
            "created_at": self.created_at.isoformat(),  # Fecha en formato ISO 8601
            "reporter": self.reporter.serialize() if self.reporter else None,  # Serializar el autor (reporter)
            "target": self.target.serialize() if self.target else None,  # Serializar el objetivo (target)
            "reviewed_by_admin": self.reviewed_by_admin.serialize() if self.reviewed_by_admin else None,  # Serializar el admin si existe
        }






class Freelancer(db.Model):
    __tablename__ = "freelancers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    bio: Mapped[str] = mapped_column(String(300), nullable=True)
    experience: Mapped[str] = mapped_column(String(300), nullable=True)
    skills: Mapped[str] = mapped_column(String(300), nullable=True)
    profile_picture: Mapped[str] = mapped_column(String(200), nullable=True)
    availability: Mapped[str] = mapped_column(String(50), nullable=True)  # Ej: "Disponible"

    # Relación con User
    user: Mapped["User"] = relationship(back_populates="freelancer_profile")

    def __repr__(self):
        return f"<Freelancer user_id={self.user_id}>"


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "bio": self.bio,
            "experience": self.experience,
            "skills": self.skills,
            "profile_picture": self.profile_picture,
            "availability": self.availability,
            "user": self.user.serialize() if self.user else None
        }
    

    
    

class Employer(db.Model):
    __tablename__ = "employers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    company_name: Mapped[str] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(String(300), nullable=True)

    # Relación con User
    user: Mapped["User"] = relationship(back_populates="employer_profile")

    def __repr__(self):
        return f"<Employer user_id={self.user_id} company={self.company_name}>"

    # Método de serialización
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "company_name": self.company_name,
            "description": self.description,
            "user": self.user.serialize() if self.user else None,  # Serializar el usuario asociado
        }




class Appointment(db.Model):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    employer_id: Mapped[int] = mapped_column(ForeignKey("employers.id"), nullable=False)
    freelancer_id: Mapped[int] = mapped_column(ForeignKey("freelancers.id"), nullable=False)

    job_offer_id: Mapped[int] = mapped_column(ForeignKey("job_offers.id"), nullable=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=True)

    date: Mapped['date'] = mapped_column(nullable=False)
    time: Mapped['time'] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)

    payment_id: Mapped[int] = mapped_column(ForeignKey("payments.id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relaciones opcionales para navegación
    employer: Mapped["Employer"] = relationship(back_populates="appointments_as_employer", foreign_keys=[employer_id])
    freelancer: Mapped["Freelancer"] = relationship(back_populates="appointments_as_freelancer", foreign_keys=[freelancer_id])

    def __repr__(self):
        return f"<Appointment {self.id} (Employer {self.employer_id}, Freelancer {self.freelancer_id})>"

    # Método de serialización
    def serialize(self):
        return {
            "id": self.id,
            "employer_id": self.employer_id,
            "freelancer_id": self.freelancer_id,
            "job_offer_id": self.job_offer_id,
            "service_id": self.service_id,
            "date": self.date.isoformat() if self.date else None,  # Convertir la fecha a formato ISO 8601
            "time": self.time.isoformat() if self.time else None,  # Convertir el tiempo a formato ISO 8601
            "status": self.status,
            "payment_id": self.payment_id,
            "created_at": self.created_at.isoformat(),  # Convertir created_at a formato ISO 8601
            "employer": self.employer.serialize() if self.employer else None,  # Serializar employer si existe
            "freelancer": self.freelancer.serialize() if self.freelancer else None,  # Serializar freelancer si existe
        }
