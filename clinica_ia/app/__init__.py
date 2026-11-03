from flask import Flask

#from flask_appbuilder.extensions import db
from .extensions import appbuilder, db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")
    db.init_app(app)
    with app.app_context():
        
        appbuilder.init_app(app, db.session)
        #appbuilder.init_app(app)
        #db.create_all()
        # Registering the views and APIs
        from .views import (
            EspecialidadView, MedicoView, PacienteView,
            ExamenView, DiagnosticoView, PrediccionIAView
        )
        
        appbuilder.add_view(EspecialidadView, "Especialidades", icon="fa-stethoscope", category="Catálogos")
        appbuilder.add_view(MedicoView, "Médicos", icon="fa-user-md", category="Catálogos")
        appbuilder.add_view(PacienteView, "Pacientes", icon="fa-users", category="Gestión Clínica")
        appbuilder.add_view(ExamenView, "Exámenes", icon="fa-flask", category="Gestión Clínica")
        appbuilder.add_view(DiagnosticoView, "Diagnósticos", icon="fa-notes-medical", category="Gestión Clínica")
        appbuilder.add_view(PrediccionIAView, "Predicciones IA", icon="fa-robot", category="Inteligencia Artificial")
    return app

app = create_app()