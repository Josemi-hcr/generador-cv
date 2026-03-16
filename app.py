import streamlit as st
from fpdf import FPDF
import io

st.set_page_config(page_title="Generador de CV Pro", layout="wide")

# --- INTERFAZ ---
st.title("📄 Mi Generador de CV Profesional")
st.info("Rellena los datos a la izquierda. Usa ';' para separar puntos en la experiencia.")

with st.sidebar:
    st.header("1. DATOS PERSONALES")
    nombre = st.text_input("Nombre Completo", "ROSA GÓMEZ GARCÍA")
    cargo = st.text_input("Subtítulo / Cargo", "Senior Asset Manager")
    contacto = st.text_input("Contacto", "Tel: 637 485 439 | email: maria@gmail.com")
    
    st.header("2. PERFIL")
    perfil = st.text_area("Extracto profesional", height=150)

    st.header("3. EXPERIENCIA")
    num_exp = st.number_input("Nº de empresas", 1, 10, 1)
    experiencias = []
    for i in range(int(num_exp)):
        with st.expander(f"Empresa {i+1}", expanded=True):
            e = {
                "puesto": st.text_input(f"Puesto {i+1}"),
                "empresa": st.text_input(f"Empresa {i+1}"),
                "fecha": st.text_input(f"Fechas {i+1}"),
                "func": st.text_area(f"Funciones (separar por ;) {i+1}")
            }
            experiencias.append(e)

# --- MOTOR DE GENERACIÓN PDF ---
def crear_pdf(nombre, cargo, contacto, perfil, experiencias):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Cabecera
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 10, nombre.upper(), ln=True, align="C")
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 10, cargo, ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100)
    pdf.cell(0, 5, contacto, ln=True, align="C")
    pdf.ln(10)
    
    # Perfil
    pdf.set_text_color(0)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "PERFIL PROFESIONAL", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, perfil, align="J")
    pdf.ln(5)
    
    # Experiencia
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "EXPERIENCIA PROFESIONAL", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    
    for exp in experiencias:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 6, exp['puesto'], ln=True)
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(100)
        pdf.cell(0, 6, f"{exp['empresa']} | {exp['fecha']}", ln=True)
        pdf.set_text_color(0)
        pdf.set_font("Helvetica", "", 10)
        
        funciones = exp['func'].split(';')
        for f in funciones:
            if f.strip():
                pdf.cell(5) 
                pdf.cell(0, 6, f"- {f.strip()}", ln=True)
        pdf.ln(3)
        
    # Retornar el PDF como bytes de forma segura
    return pdf.output()

# --- ACCIÓN ---
if st.button("🚀 GENERAR PDF"):
    try:
        pdf_data = crear_pdf(nombre, cargo, contacto, perfil, experiencias)
        
        st.success("¡PDF creado con éxito!")
        st.download_button(
            label="📥 Descargar Currículum",
            data=bytes(pdf_data), # Convertimos explícitamente a bytes
            file_name=f"CV_{nombre.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Hubo un error al generar el archivo: {e}")
