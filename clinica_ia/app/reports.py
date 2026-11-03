# reports.py
from flask_appbuilder import BaseView, expose
from flask_appbuilder.security.decorators import has_access
from flask import request
from sqlalchemy import text


class ReporteRiesgoView(BaseView):
    """Reporte 1: Pacientes con riesgo alto/medio en un rango de fechas."""
    default_view = "index"

    @expose("/")
    @has_access
    def index(self):
        fecha_inicio = request.args.get("fecha_inicio", "")
        fecha_fin = request.args.get("fecha_fin", "")
        nivel = request.args.get("nivel", "")

        resultados = []
        if fecha_inicio and fecha_fin:
            sql_str = """
                SELECT p.nombre, pi.nivel_riesgo, pi.probabilidad,
                       pi.fecha_prediccion, pi.texto_generado
                FROM predicciones_ia pi
                JOIN pacientes p ON pi.paciente_id = p.id
                WHERE pi.fecha_prediccion BETWEEN :inicio AND :fin
            """
            params = {"inicio": fecha_inicio, "fin": fecha_fin + " 23:59:59"}

            if nivel:
                sql_str += " AND pi.nivel_riesgo = :nivel"
                params["nivel"] = nivel

            sql_str += " ORDER BY pi.probabilidad DESC"

            resultados = self.appbuilder.session.execute(
                text(sql_str), params
            ).fetchall()

        return self.render_template(
            "reports/riesgo.html",
            resultados=resultados,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            nivel=nivel,
        )


class ReporteExamenesView(BaseView):
    """Reporte 2: Exámenes por especialidad y médico en un rango de fechas."""

    default_view = "index"
    @expose("/")
    @has_access
    def index(self):
        fecha_inicio = request.args.get("fecha_inicio", "")
        fecha_fin = request.args.get("fecha_fin", "")

        resultados = []
        if fecha_inicio and fecha_fin:
            sql_str = """
                SELECT e.nombre AS especialidad, m.nombre AS medico,
                       COUNT(*) AS total_examenes
                FROM examenes ex
                JOIN medicos m ON ex.medico_id = m.id
                JOIN especialidades e ON m.especialidad_id = e.id
                WHERE ex.fecha_examen BETWEEN :inicio AND :fin
                GROUP BY e.nombre, m.nombre
                ORDER BY total_examenes DESC
            """
            params = {"inicio": fecha_inicio, "fin": fecha_fin}
            resultados = self.appbuilder.session.execute(
                text(sql_str), params
            ).fetchall()

        return self.render_template(
            "reports/examenes.html",
            resultados=resultados,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
        )


class ReporteDiagnosticosView(BaseView):
    """Reporte 3: Distribución de diagnósticos por tipo y sexo del paciente."""

    default_view = "index"
    @expose("/")
    @has_access
    def index(self):
        fecha_inicio = request.args.get("fecha_inicio", "")
        fecha_fin = request.args.get("fecha_fin", "")

        resultados = []
        if fecha_inicio and fecha_fin:
            sql_str = """
                SELECT d.tipo_diagnostico, p.sexo, COUNT(*) AS cantidad
                FROM diagnosticos d
                JOIN pacientes p ON d.paciente_id = p.id
                WHERE d.fecha_diagnostico BETWEEN :inicio AND :fin
                GROUP BY d.tipo_diagnostico, p.sexo
                ORDER BY d.tipo_diagnostico, p.sexo
            """
            params = {"inicio": fecha_inicio, "fin": fecha_fin}
            resultados = self.appbuilder.session.execute(
                text(sql_str), params
            ).fetchall()

        return self.render_template(
            "reports/diagnosticos.html",
            resultados=resultados,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
        )