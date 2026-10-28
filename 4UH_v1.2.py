import os
import sys
import webview

# resolucion de rutas para desarrollo y empaquetado con pyinstaller
def ruta_recurso(ruta_relativa):
    try:
        ruta_base = sys._MEIPASS
    except AttributeError:
        ruta_base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(ruta_base, ruta_relativa)

# selector de perfil: "personal" o "generico"
PERFIL_ACTIVO = "generico"

CONFIGURACIONES = {
    "generico": {
        "titulo_ventana": "Conversor de Escalas y Unidades v1.2",
        "saludo": "Herramienta de Medición Técnica",
        "tab_escalas": "Escalas de Planos",
        "tab_unidades": "Conversor de Unidades",
        "lbl_medida": "Medida a convertir (cm):",
        "lbl_esc_ant": "Escala actual (ej. 250 o 1:250):",
        "lbl_esc_nue": "Escala destino (ej. 75 o 1:75):",
        "btn_escala": "Calcular Escala",
        "lbl_valor": "Valor a transformar:",
        "btn_unidad": "Convertir Unidades",
        "img_inicial": "../assets/icono_tecnico.png",
        "img_exito": "../assets/icono_tecnico.png",
        "img_espera": "../assets/icono_tecnico.png"
    },
    "personal": {
        "titulo_ventana": "4UH - Especial v1.2",
        "saludo": "Calculadora de escalas ૮ ˶ᵔ ᵕ ᵔ˶ ა",
        "tab_escalas": "Tus Escalas 📐",
        "tab_unidades": "Tus Unidades 📏",
        "lbl_medida": "Medida a cambiar (cm):",
        "lbl_esc_ant": "Escala que tienes (ej. 1:250 o 250):",
        "lbl_esc_nue": "Escala a la que pasas (ej. 1:75 o 75):",
        "btn_escala": "Calcular medida ✨",
        "lbl_valor": "Medida a transformar :3 :",
        "btn_unidad": "Convertir unidades muak ^3^",
        "img_inicial": "../assets/personaje_pensando.png",
        "img_exito": "../assets/personaje_feliz.png",
        "img_espera": "../assets/personaje_pensando.png"
    }
}

FACTORES_METRO = {
    "Milímetros (mm)": 0.001,
    "Centímetros (cm)": 0.01,
    "Metros (m)": 1.0,
    "Kilómetros (km)": 1000.0,
    "Pulgadas (in)": 0.0254,
    "Pies (ft)": 0.3048,
    "Yardas (yd)": 0.9144,
    "Millas (mi)": 1609.344,
}

# clase puente expuesta a javascript dentro del html
class ApiCalculadora:
    def obtener_configuracion(self):
        # envia textos segun el perfil activo al cargar la pagina
        return {
            "perfil": PERFIL_ACTIVO,
            "textos": CONFIGURACIONES[PERFIL_ACTIVO],
            "unidades": list(FACTORES_METRO.keys())
        }

    def calcular_escala(self, medida_str, esc_ant_str, esc_nue_str):
        try:
            medida = float(medida_str)
            ant = float(esc_ant_str.strip().lower().replace("1:", "").replace("1/", ""))
            nue = float(esc_nue_str.strip().lower().replace("1:", "").replace("1/", ""))

            if ant <= 0 or nue <= 0:
                return {"ok": False, "msg": "Las escalas deben ser mayores a cero."}
            if ant == nue:
                return {"ok": False, "msg": "Las escalas ingresadas son identicas."}

            res = round(medida * (ant / nue), 3)
            f_ant = int(ant) if ant.is_integer() else ant
            f_nue = int(nue) if nue.is_integer() else nue

            if PERFIL_ACTIVO == "personal":
                msg = f"Listo mi amor: {medida} cm en 1:{f_ant} equivale a {res} cm en 1:{f_nue} ૮ ˶ᵔ ᵕ ᵔ˶ ა"
            else:
                msg = f"{medida} cm en 1:{f_ant} equivale a {res} cm en 1:{f_nue}"

            return {"ok": True, "resultado": msg}
        except ValueError:
            msg = "Solo numeros miamorcita bella (⸝⸝๑﹏๑⸝⸝)" if PERFIL_ACTIVO == "personal" else "Ingrese valores numericos validos."
            return {"ok": False, "msg": msg}

    def convertir_unidades(self, valor_str, u_origen, u_destino):
        try:
            valor = float(valor_str)
            if u_origen not in FACTORES_METRO or u_destino not in FACTORES_METRO:
                return {"ok": False, "msg": "Seleccione unidades validas."}

            en_metros = valor * FACTORES_METRO[u_origen]
            res = round(en_metros / FACTORES_METRO[u_destino], 4)

            u1 = u_origen.split()[0]
            u2 = u_destino.split()[0]

            if PERFIL_ACTIVO == "personal":
                msg = f"Ahi tienes mi vida: {valor} {u1} = {res} {u2} ദ്ദി(˵ •̀ ᴗ - ˵ )"
            else:
                msg = f"{valor} {u1} = {res} {u2}"

            return {"ok": True, "resultado": msg}
        except ValueError:
            msg = "Solo numeros miamorcita bella (⸝⸝๑﹏๑⸝⸝)" if PERFIL_ACTIVO == "personal" else "Ingrese un valor numerico valido."
            return {"ok": False, "msg": msg}

if __name__ == "__main__":
    api = ApiCalculadora()
    archivo_html = ruta_recurso(os.path.join("gui", "index.html"))

    # creacion de la ventana de escritorio con frontend web
    ventana = webview.create_window(
        title=CONFIGURACIONES[PERFIL_ACTIVO]["titulo_ventana"],
        url=archivo_html,
        js_api=api,
        width=480,
        height=620,
        resizable=False
    )
    webview.start()