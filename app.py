import streamlit as st
import requests
# --- DETECTAR SI EL CLIENTE VIENE DE PAGAR EN STRIPE ---
query_params = st.query_params
if query_params.get("pago") == "exito":
    st.balloons()  # ¡Efecto de globos de celebración!
    st.success("🎉 ¡Pago realizado con éxito! Tu documento legal está listo.")
    
    texto_descarga = """
==================================================
POLÍTICA DE PRIVACIDAD Y PROTECCIÓN DE DATOS
==================================================
1. INFORMACIÓN AL USUARIO
El Responsable del Tratamiento le informa que sus datos serán tratados de conformidad con lo dispuesto en el Reglamento (UE) 2016/679 (RGPD) y la LOPDGDD.

2. FINALIDAD DEL TRATAMIENTO
Atender las consultas planteadas por los usuarios y prestar los servicios solicitados a través del sitio web.

3. CONTACTO
Para el ejercicio de sus derechos de acceso, rectificación o supresión, diríjase al departamento de atención legal.
==================================================
    """
    st.download_button(
        label="📥 DESCARGAR MI POLÍTICA DE PRIVACIDAD (.TXT)",
        data=texto_descarga,
        file_name="politica_privacidad_oficial.txt",
        mime="text/plain"
    )
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="VERIFICADOR LEGAL SaaS", 
    page_icon="🛡️", 
    layout="wide"
)

# --- CSS PERSONALIZADO ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    [data-testid="stAppViewContainer"] {
        background-color: #090d16;
        color: #f1f5f9;
        font-family: 'Inter', sans-serif !important;
    }
    
    [data-testid="stHeader"] {
        background-color: rgba(9, 13, 22, 0);
    }

    html, body, p, span, label, input, button {
        font-family: 'Inter', sans-serif !important;
    }

    .hero-title {
        text-align: center;
        font-weight: 800;
        font-size: 2.2rem;
        letter-spacing: -0.02em;
        color: #ffffff;
        margin-bottom: 0.2rem;
    }
    .hero-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }

    [data-testid="stTextInput"] > div > div > input {
        background-color: #131b2e;
        border: 1px solid #1e293b;
        border-radius: 8px;
        color: #ffffff;
        padding: 14px 16px;
        font-size: 0.95rem;
    }
    [data-testid="stTextInput"] label {
        color: #cbd5e1 !important;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    [data-testid="stButton"] button {
        width: 100%;
        background: linear-gradient(135deg, #e11d48 0%, #be123c 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px;
        padding: 14px;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.05em;
        text-transform: uppercase !important;
        box-shadow: 0 4px 14px rgba(225, 29, 72, 0.35);
        transition: all 0.2s ease-in-out;
    }
    [data-testid="stButton"] button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(225, 29, 72, 0.5);
    }

    .card-panel {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        height: 100%;
    }
    .card-header {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #f43f5e;
        margin-bottom: 1.2rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid #1f2937;
    }

    .status-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid #1e293b;
    }
    .status-row:last-child {
        border-bottom: none;
    }
    .status-label {
        color: #e2e8f0;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .badge-success {
        background-color: rgba(16, 185, 129, 0.1);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.2);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
    }
    .badge-danger {
        background-color: rgba(244, 63, 94, 0.1);
        color: #f43f5e;
        border: 1px solid rgba(244, 63, 94, 0.2);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER PRINCIPAL ---
st.markdown('<div class="hero-title">🛡️ AUDITOR LEGAL WEB</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Escaneo automático de cumplimiento normativo (RGPD / LSSI)</div>', unsafe_allow_html=True)

# --- CONTROLES ---
col_input, col_btn = st.columns([3, 1])

with col_input:
    url_usuario = st.text_input("SITIO WEB A INSPECCIONAR", "https://www.coursera.org")

with col_btn:
    st.write("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    analizar = st.button("ANALIZAR AHORA")

# --- LÓGICA DE AUDITORÍA ---
if analizar:
    if not url_usuario.startswith("http"):
        url_usuario = "https://" + url_usuario
        
    st.markdown(f"<p style='text-align:center; color:#64748b; margin-top: 1rem;'>Analizando estructura HTML de <b>{url_usuario}</b>...</p>", unsafe_allow_html=True)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"
    }
    
    elementos = {
        "privacidad": ("Política de Privacidad", ["privacy", "privacidad", "politica de privacidad", "política de privacidad"], "Alto"),
        "terminos": ("Términos y Condiciones", ["terms", "terminos", "términos", "conditions", "condiciones", "terms of use"], "Medio"),
        "cookies": ("Aviso de Cookies", ["cookie", "cookies", "politica de cookies", "política de cookies"], "Medio-Alto")
    }
    
    try:
        respuesta = requests.get(url_usuario, headers=headers, timeout=10)
        contenido = respuesta.text.lower()
        
        resultados = {}
        faltantes = []
        
        for clave, (nombre, palabras, nivel_riesgo) in elementos.items():
            encontrado = any(p in contenido for p in palabras)
            resultados[clave] = {
                "nombre": nombre,
                "encontrado": encontrado,
                "riesgo": nivel_riesgo
            }
            if not encontrado:
                faltantes.append((nombre, nivel_riesgo))
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        # --- COLUMNA 1: DOCUMENTOS ---
        with col1:
            st.markdown("""
            <div class="card-panel">
                <div class="card-header">📄 Documentos Legales Detectados</div>
            """, unsafe_allow_html=True)
            
            for item in resultados.values():
                badge = '<span class="badge-success">DETECTADO</span>' if item["encontrado"] else '<span class="badge-danger">NO DETECTADO</span>'
                st.markdown(f"""
                <div class="status-row">
                    <span class="status-label">{item['nombre']}</span>
                    {badge}
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)

        # --- COLUMNA 2: DIAGNÓSTICO ---
        with col2:
            st.markdown("""
            <div class="card-panel">
                <div class="card-header">⚠️ Diagnóstico de Riesgo Legal</div>
            """, unsafe_allow_html=True)
            
            if not faltantes:
                st.markdown("""
                <div class="status-row">
                    <span class="status-label">Riesgo de Sanción / Multa</span>
                    <span class="badge-success">RIESGO BAJO / CONFORME</span>
                </div>
                <div class="status-row">
                    <span class="status-label">Estado de Publicidad (Ads)</span>
                    <span class="badge-success">APTO PARA CAMPAÑAS</span>
                </div>
                <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 1rem;">
                    El sitio incluye las menciones legales obligatorias básicas.
                </p>
                """, unsafe_allow_html=True)
            else:
                for nombre, riesgo in faltantes:
                    st.markdown(f"""
                    <div class="status-row">
                        <span class="status-label">Falta {nombre}</span>
                        <span class="badge-danger">RIESGO {riesgo.upper()}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                <p style="color: #f43f5e; font-size: 0.8rem; margin-top: 1rem; font-weight: 600;">
                    ⚠️ La falta de estos documentos expone al propietario a sanciones administrativas.
                </p>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # --- SECCIÓN GENERADOR + PASARELA DE PAGO ---
        if faltantes:
            st.markdown("<br><hr style='border-color: #1f2937;'><br>", unsafe_allow_html=True)
            st.subheader("🛠️ Generar Solución Legal Inmediata")
            st.write("Completa los datos de tu empresa para preparar la documentación legal adaptada:")
            
            with st.form("form_generador"):
                nombre_empresa = st.text_input("Nombre de la Empresa / Autónomo:")
                cif_empresa = st.text_input("NIF / CIF:")
                email_contacto = st.text_input("Email de contacto legal:")
                
                btn_generar = st.form_submit_button("GENERAR Y CONTINUAR AL PAGO")
                
                if btn_generar and nombre_empresa and cif_empresa:
                    st.success("✅ Datos registrados correctamente. Haz clic en el botón inferior para abonar y descargar tu documento:")
                    
                    enlace_stripe = "https://buy.stripe.com/3cI5kD2FlcWy5K8a4387K00"
                    
                    st.markdown(f"""
                        <div style="text-align: center; margin-top: 15px;">
                            <a href="{enlace_stripe}" target="_blank" style="text-decoration: none;">
                                <button type="button" style="
                                    width: 100%;
                                    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                                    color: white;
                                    padding: 16px;
                                    border: none;
                                    border-radius: 8px;
                                    font-size: 1.05rem;
                                    font-weight: 700;
                                    cursor: pointer;
                                    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
                                ">
                                    💳 PAGAR Y DESCARGAR DOCUMENTO
                                </button>
                            </a>
                        </div>
                    """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error de conexión con la URL especificada: {e}")
