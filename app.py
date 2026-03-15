import streamlit as st
from xhtml2pdf import pisa
from io import BytesIO

st.set_page_config(page_title="Generador de CV Profesional", layout="wide")

# Estilos visuales de la interfaz
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #1a2a3a; color: white; font-weight: bold; border-radius: 5px; }
    </style>
    """, unsafe_allow_stdio=True)

st.title("📄 Generador de CV Ejecutivo")
st.write("Introduce los datos del cliente a la izquierda. Al terminar, pulsa el botón para generar el PDF.")

# --- FORMULARIO EN LA BARRA LATERAL ---
with st.sidebar:
    st.header("1. DATOS PERSONALES")
    nombre = st.text_input("Nombre Completo (20pt)", "ROSA GÓMEZ GARCÍA")
    cargo = st.text_input("Cargo / Subtítulo (15pt)", "Senior Asset Manager | Team Leader")
    contacto = st.text_input("Contacto (10pt)", "Tel: 000 000 000 | email: cliente@gmail.com")
    
    st.header("2. PERFIL")
    perfil = st.text_area("Extracto (10pt - Interlineado 1.4)", height=150)

    st.header("3. EXPERIENCIA")
    num_exp = st.number_input("¿Cuántas empresas?", 1, 10, 2)
    experiencias = []
    for i in range(int(num_exp)):
        with st.expander(f"Empresa {i+1}", expanded=True):
            e = {
                "puesto": st.text_input(f"Puesto {i+1} (11pt Negrita)"),
                "empresa": st.text_input(f"Empresa {i+1}"),
                "fecha": st.text_input(f"Fechas {i+1}"),
                "func": st.text_area(f"Funciones (separar por ;) {i+1}")
            }
            experiencias.append(e)

    st.header("4. OTROS")
    formacion = st.text_area("Formación (un título por línea)")
    idiomas = st.text_input("Idiomas", "Castellano: Nativo")
    competencias = st.text_area("Competencias (separadas por |)")

# --- MOTOR DE DISEÑO PDF ---
def generar_pdf_html(nombre, cargo, contacto, perfil, experiencias, formacion, idiomas, competencias):
    lista_formacion = formacion.split('\n')
    
    html = f"""
    <html>
    <head>
    <style>
        @page {{ size: A4; margin: 1.5cm 2cm; }}
        body {{ font-family: Helvetica, Arial, sans-serif; color: #333; line-height: 1.4; }}
        .header {{ text-align: center; margin-bottom: 25px; }}
        .nombre {{ font-size: 20pt; font-weight: bold; color: #000; text-transform: uppercase; }}
        .subtitulo {{ font-size: 15pt; font-weight: bold; color: #000; margin-top: 5px; }}
        .contacto {{ font-size: 10pt; color: #555; margin-top: 5px; }}
        .seccion {{ 
            font-size: 13pt; font-weight: bold; color: #000; text-transform: uppercase; 
            border-bottom: 1px solid #000; margin-top: 22px; margin-bottom: 12px; padding-bottom: 2px;
        }}
        .exp-bloque {{ margin-bottom: 15px; }}
        .puesto {{ font-size: 11pt; font-weight: bold; color: #000; }}
        .empresa-fecha {{ font-size: 10pt; color: #777; margin-bottom: 5px; }}
        .texto-base {{ font-size: 10pt; color: #333; text-align: justify; }}
        ul {{ margin-top: 5px; padding-left: 18px; }}
        li {{ margin-bottom: 3px; font-size: 10pt; }}
    </style>
    </head>
    <body>
        <div class="header">
            <div class="nombre">{nombre}</div>
            <div class="subtitulo">{cargo}</div>
            <div class="contacto">{contacto}</div>
        </div>
        <div class="seccion">Perfil Profesional</div>
        <div class="texto-base">{perfil}</div>
        <div class="seccion">Experiencia Profesional</div>
    """
    for exp in experiencias:
        funs = exp['func'].split(';')
        html += f"""
        <div class="exp-bloque">
            <div class="puesto">{exp['puesto']}</div>
            <div class="empresa-fecha">{exp['empresa']} | {exp['fecha']}</div>
            <ul>{"".join([f"<li>{f.strip()}</li>" for f in funs if f.strip()])}</ul>
        </div>"""
    
    html += f"""
        <div class="seccion">Formación</div>
        <ul>{"".join([f"<li>{line.strip()}</li>" for line in lista_formacion if line.strip()])}</ul>
        <div class="seccion">Idiomas y Competencias</div>
        <div class="texto-base">
            <p><b>Idiomas:</b> {idiomas}</p>
            <p><b>Competencias:</b> {competencias}</p>
        </div>
    </body></html>"""
    return html

# --- BOTÓN DE ACCIÓN ---
if st.button("🚀 GENERAR PDF PROFESIONAL"):
    if not nombre or not perfil:
        st.error("Por favor, rellena al menos el nombre y el perfil.")
    else:
        html_out = generar_pdf_html(nombre, cargo, contacto, perfil, experiencias, formacion, idiomas, competencias)
        pdf_buffer = BytesIO()
        pisa.CreatePDF(html_out, dest=pdf_buffer)
        
        st.success("✅ ¡CV generado con éxito!")
        st.download_button(
            label="⬇️ Descargar archivo PDF",
            data=pdf_buffer.getvalue(),
            file_name=f"CV_{nombre.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
