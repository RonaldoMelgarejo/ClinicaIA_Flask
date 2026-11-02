from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from .models import (Especialidad, Medico, Paciente, Examen, Diagnostico, PrediccionIA)

class EspecialidadView(ModelView):
    datamodel = SQLAInterface(Especialidad)
    list_columns = ["id", "nombre", "descripcion"]
    add_columns = ["nombre", "descripcion"]
    edit_columns = ["nombre", "descripcion"]
    search_columns = ["nombre"]
    label_columns = {"nombre": "Nombre", "descripcion": "Descripción"}

class MedicoView(ModelView):
    datamodel = SQLAInterface(Medico)
    list_columns = ["id", "nombre", "cedula_profesional", "especialidad", "email"]
    add_columns = ["nombre", "cedula_profesional", "email", "telefono", "especialidad"]
    edit_columns = add_columns
    search_columns = ["nombre", "cedula_profesional", "especialidad"]
    label_columns = {
        "nombre": "Nombre", "cedula_profesional": "Cédula",
        "especialidad": "Especialidad", "email": "Email", "telefono": "Teléfono"
    }
    related_views = [] 
    
class PrediccionIAView(ModelView):
    datamodel = SQLAInterface(PrediccionIA)
    list_columns = ["id", "paciente", "nivel_riesgo", "probabilidad", "fecha_prediccion"]
    add_columns = ["paciente", "nivel_riesgo", "probabilidad", "texto_generado"]
    edit_columns = add_columns
    search_columns = ["paciente", "nivel_riesgo"]
    label_columns = {
        "paciente": "Paciente", "nivel_riesgo": "Nivel de riesgo",
        "probabilidad": "Probabilidad", "texto_generado": "Texto generado por IA",
        "fecha_prediccion": "Fecha de predicción"
    }
    
class PacienteView(ModelView):
    datamodel = SQLAInterface(Paciente)
    list_columns = ["id", "nombre", "fecha_nacimiento", "sexo", "fumador", "fecha_registro"]
    add_columns = [
        "nombre", "fecha_nacimiento", "sexo", "telefono", "email",
        "fumador", "anios_fumador", "tos_cronica", "dificultad_respirar"
    ]
    edit_columns = add_columns
    search_columns = ["nombre", "sexo", "fumador"]
    label_columns = {
        "nombre": "Nombre", "fecha_nacimiento": "Fecha de nacimiento",
        "sexo": "Sexo", "fumador": "Fumador",
        "anios_fumador": "Años fumando", "tos_cronica": "Tos crónica",
        "dificultad_respirar": "Dificultad al respirar",
        "fecha_registro": "Fecha de registro"
    }
    related_views = [PrediccionIAView]

class ExamenView(ModelView):
    datamodel = SQLAInterface(Examen)
    list_columns = ["id", "paciente", "medico", "tipo_examen", "fecha_examen", "estado"]
    add_columns = ["paciente", "medico", "tipo_examen", "fecha_examen", "resultado", "estado"]
    edit_columns = add_columns
    search_columns = ["paciente", "medico", "tipo_examen", "estado"]
    label_columns = {
        "paciente": "Paciente", "medico": "Médico",
        "tipo_examen": "Tipo de examen", "fecha_examen": "Fecha",
        "resultado": "Resultado", "estado": "Estado"
    }

class DiagnosticoView(ModelView):
    datamodel = SQLAInterface(Diagnostico)
    list_columns = ["id", "paciente", "medico", "tipo_diagnostico", "fecha_diagnostico"]
    add_columns = ["paciente", "medico", "examen", "descripcion", "tipo_diagnostico", "fecha_diagnostico"]
    edit_columns = add_columns
    search_columns = ["paciente", "medico", "tipo_diagnostico"]
    label_columns = {
        "paciente": "Paciente", "medico": "Médico", "examen": "Examen",
        "descripcion": "Descripción", "tipo_diagnostico": "Tipo de diagnóstico",
        "fecha_diagnostico": "Fecha"
    }
