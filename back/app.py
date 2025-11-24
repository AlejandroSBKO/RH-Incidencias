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
# 5️⃣  OBTENER EL TOTAL DE INCIDENCIAS
# --------------------------------------------------------- 
@app.route("/incidencias/total", methods=["GET"])
def obtener_total_incidencias():
    try:
        response = supabase.table("incidencia").select("*", count="exact").execute()
        total = response.count
        return jsonify({"total": total}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------------
# 6️⃣  OBTENER CONTEO POR TIPO DE INCIDENCIA
# ---------------------------------------------------------
@app.route("/incidencias/por-tipo", methods=["GET"])
def obtener_incidencias_por_tipo():
    try:
        # Primero obtenemos todos los registros para procesarlos
        response = supabase.table("incidencia").select("tipo_incidencia").execute()
        
        # Creamos un diccionario para contar las ocurrencias
        conteo = {}
        for incidencia in response.data:
            tipo = incidencia['tipo_incidencia']
            if tipo in conteo:
                conteo[tipo] += 1
            else:
                conteo[tipo] = 1
        
        # Convertimos el diccionario a una lista de objetos
        resultado = [{"tipo_incidencia": tipo, "count": cantidad} 
                    for tipo, cantidad in conteo.items()]
        
        return jsonify(resultado), 200
    except Exception as e:
        print(f"Error: {str(e)}")  # Para debugging
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


# ---------------------------------------------------------
# 5️⃣  OBTENER DATOS DEL EMPLEADO POR ID
# ---------------------------------------------------------
@app.route("/empleados/<int:id_empleado>", methods=["GET"])
def obtener_datos_empleado(id_empleado):
    try:
        # 🔸 Cambiamos los nombres a minúsculas
        empleado = supabase.table("empleados_c") \
            .select("id_empleado, p_nombre, s_nombre, apellido_p, apellido_m, id_puesto_actual") \
            .eq("id_empleado", id_empleado) \
            .single() \
            .execute()

        if not empleado.data:
            return jsonify({"error": f"Empleado con ID {id_empleado} no encontrado."}), 404

        empleado_data = empleado.data

        # 🔹 Obtener el área
        area_nombre = "No asignada"
        if empleado_data.get("id_puesto_actual"):
            puesto = supabase.table("puestosa") \
                .select("id_area") \
                .eq("id_puesto", empleado_data["id_puesto_actual"]) \
                .single() \
                .execute()

            if puesto.data:
                id_area = puesto.data["id_area"]
                area = supabase.table("areasa") \
                    .select("nombre_area") \
                    .eq("id_area", id_area) \
                    .single() \
                    .execute()

                if area.data:
                    area_nombre = area.data["nombre_area"]

        # 🔹 Nombre completo
        nombre_completo = f"{empleado_data['p_nombre']} {empleado_data.get('s_nombre', '')} {empleado_data.get('apellido_p', '')} {empleado_data.get('apellido_m', '')}".replace("  ", " ").strip()

        return jsonify({
            "nombre_completo": nombre_completo,
            "area": area_nombre
        }), 200

    except Exception as e:
        print("Error al obtener empleado:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
