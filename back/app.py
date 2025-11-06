from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase_conn import supabase

app = Flask(__name__, static_folder="../front", static_url_path="", template_folder="../front")
CORS(app)

@app.route("/")
def home():
    return app.send_static_file("dashboard.html")

# ---------------------------------------------------------
# 1️⃣  OBTENER TODAS LAS INCIDENCIAS
# ---------------------------------------------------------
@app.route("/incidencias", methods=["GET"])
def obtener_incidencias():
    try:
        response = supabase.table("incidencia").select("*").execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------
# 2️⃣  CREAR UNA NUEVA INCIDENCIA
# ---------------------------------------------------------
@app.route("/incidencias", methods=["POST"])
def crear_incidencia():
    try:
        data = request.json

        nueva_incidencia = {
            "id_empleado": data["id_empleado"],
            "fecha_incidencia": data.get("fecha_incidencia"),
            "tipo_incidencia": data.get("tipo_incidencia"),
            "descripcion_incidencia": data.get("descripcion_incidencia"),
            "evidencia_incidencia": data.get("evidencia_incidencia"),
            "accion_tomada": data.get("accion_tomada"),
            "estado": data.get("estado", True)
        }

        response = supabase.table("incidencia").insert(nueva_incidencia).execute()
        return jsonify(response.data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------
# 3️⃣  EDITAR (ACTUALIZAR) UNA INCIDENCIA
# ---------------------------------------------------------
@app.route("/incidencias/<int:id_incidencia>", methods=["PUT"])
def actualizar_incidencia(id_incidencia):
    try:
        data = request.json

        # Solo actualizamos los campos que llegan en el body
        response = supabase.table("incidencia") \
            .update(data) \
            .eq("id_incidencia", id_incidencia) \
            .execute()

        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------
# 4️⃣  ELIMINAR UNA INCIDENCIA
# ---------------------------------------------------------
@app.route("/incidencias/<int:id_incidencia>", methods=["DELETE"])
def eliminar_incidencia(id_incidencia):
    try:
        response = supabase.table("incidencia") \
            .delete() \
            .eq("id_incidencia", id_incidencia) \
            .execute()

        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
