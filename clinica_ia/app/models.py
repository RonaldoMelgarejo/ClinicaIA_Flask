from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, Enum, Boolean, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime 

class Especialidad(Model):
    __tablename__ = "especialidades"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text)

    medicos = relationship("Medico", back_populates="especialidad")

    def __repr__(self):
        return self.nombre


class Medico(Model):
    __tablename__ = "medicos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    cedula_profesional = Column(String(50), nullable=False, unique=True)
    email = Column(String(120))
    telefono = Column(String(20))
    especialidad_id = Column(Integer, ForeignKey("especialidades.id"), nullable=False)

    especialidad = relationship("Especialidad", back_populates="medicos")
    examenes = relationship("Examen", back_populates="medico")
    diagnosticos = relationship("Diagnostico", back_populates="medico")

    def __repr__(self):
        return self.nombre

class Paciente(Model):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    sexo = Column(Enum("M", "F", "Otro"), nullable=False)
    telefono = Column(String(20))
    email = Column(String(120))
    fumador = Column(Boolean, default=False, nullable=False)
    anios_fumador = Column(Integer, default=0)
    tos_cronica = Column(Boolean, default=False, nullable=False)
    dificultad_respirar = Column(Boolean, default=False, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    examenes = relationship("Examen", back_populates="paciente")
    diagnosticos = relationship("Diagnostico", back_populates="paciente")
    predicciones = relationship("PrediccionIA", back_populates="paciente")

    def __repr__(self):
        return self.nombre


class Examen(Model):
    __tablename__ = "examenes"
    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("medicos.id"), nullable=False)
    tipo_examen = Column(String(100), nullable=False)
    fecha_examen = Column(Date, nullable=False)
    resultado = Column(Text)
    estado = Column(Enum("Pendiente", "Realizado", "Cancelado"),
                    nullable=False, default="Pendiente")

    paciente = relationship("Paciente", back_populates="examenes")
    medico = relationship("Medico", back_populates="examenes")
    diagnosticos = relationship("Diagnostico", back_populates="examen")

    def __repr__(self):
        return f"{self.tipo_examen} - {self.fecha_examen}"

class Diagnostico(Model):
    __tablename__ = "diagnosticos"
    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("medicos.id"), nullable=False)
    examen_id = Column(Integer, ForeignKey("examenes.id"), nullable=True)
    descripcion = Column(Text, nullable=False)
    tipo_diagnostico = Column(String(100), nullable=False)
    fecha_diagnostico = Column(Date, nullable=False)

    paciente = relationship("Paciente", back_populates="diagnosticos")
    medico = relationship("Medico", back_populates="diagnosticos")
    examen = relationship("Examen", back_populates="diagnosticos")

    def __repr__(self):
        return f"{self.tipo_diagnostico} - {self.fecha_diagnostico}"


class PrediccionIA(Model):
    __tablename__ = "predicciones_ia"
    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    nivel_riesgo = Column(Enum("Bajo", "Medio", "Alto"), nullable=False)
    probabilidad = Column(DECIMAL(5, 4), nullable=True)
    texto_generado = Column(Text)
    fecha_prediccion = Column(DateTime, default=datetime.utcnow)
    modelo_version = Column(String(50), default="medgemma-4b-it")

    paciente = relationship("Paciente", back_populates="predicciones")

    def __repr__(self):
        return f"{self.nivel_riesgo} - {self.fecha_prediccion}"

