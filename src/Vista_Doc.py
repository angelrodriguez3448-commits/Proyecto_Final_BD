import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import Conectar_DB as connect  # para volver al login
from datetime import datetime

# Para generar PDF
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
except Exception:
    # No romper la importación; avisaremos al crear la consulta si faltara
    ImageReader = None
    canvas = None
    A4 = None

titulo = "ND: La salud lo es todo"

def directorio_img(elemento):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    IMG_DIR = os.path.join(BASE_DIR, "img")
    return os.path.join(IMG_DIR, elemento)

icon_path = directorio_img("ND_icono.ico")
fondo_path = directorio_img("fondo_interfaz.jpg")


# -------------------------
# FUNCIÓN PARA CONSULTAR CITAS DEL DOCTOR
# -------------------------
def consultar_citas_doctor(codigo_doctor):
    conn = connect.conectar()
    if not conn:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT c.codigo, p.nombre, c.fecha, c.hora
            FROM hospital.cita c
            JOIN hospital.paciente p ON c.cod_paciente = p.codigo
            WHERE c.cod_doctor = %s
            ORDER BY c.fecha, c.hora;
        """, (codigo_doctor,))

        registros = cur.fetchall()
        cur.close()
        conn.close()

        ventana = tk.Toplevel()
        ventana.title("Mis Citas")
        ventana.geometry("700x400")

        columnas = ("Código Cita", "Paciente", "Fecha", "Hora")
        tree = ttk.Treeview(ventana, columns=columnas, show="headings")

        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        tree.pack(fill="both", expand=True)

        for fila in registros:
            cod, pac, fecha, hora = fila

            try:
                fecha = fecha.strftime("%Y-%m-%d")
            except:
                fecha = str(fecha)

            hora = hora.strftime("%H:%M") if hasattr(hora, "strftime") else str(hora)

            tree.insert("", "end", values=(cod, pac, fecha, hora))

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener las citas:\n{e}")


# ---------------------------------------------------
# FUNCIÓN: ver_pacientes -> pacientes que tienen cita con el doctor (UNIQUE)
# ---------------------------------------------------
def ver_pacientes(codigo_doctor):
    conn = connect.conectar()
    if not conn:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT DISTINCT 
                p.codigo,
                p.nombre,
                p.direccion,
                p.telefono,
                p.fecha_nac,
                p.sexo,
                p.edad,
                p.estatura
            FROM hospital.paciente p
            INNER JOIN hospital.cita c 
                ON p.codigo = c.cod_paciente
            WHERE c.cod_doctor = %s
            ORDER BY p.nombre;
        """, (codigo_doctor,))

        pacientes = cur.fetchall()
        cur.close()
        conn.close()

        ventana = tk.Toplevel()
        ventana.title("Pacientes Asignados")
        ventana.geometry("900x400")

        columnas = ("ID", "Nombre", "Dirección", "Teléfono", "Fecha Nac", "Sexo", "Edad", "Estatura")
        tree = ttk.Treeview(ventana, columns=columnas, show="headings")

        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        tree.pack(fill="both", expand=True)

        for p in pacientes:
            # formatear fecha si es objeto date
            fila = list(p)
            try:
                if hasattr(fila[4], "strftime"):
                    fila[4] = fila[4].strftime("%Y-%m-%d")
            except Exception:
                fila[4] = str(fila[4])
            tree.insert("", "end", values=tuple(fila))

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener los pacientes:\n{e}")


# ---------------------------------------------------
# FUNCIONES PARA CREAR CONSULTA Y GENERAR PDF
# ---------------------------------------------------
def generar_pdf_consulta(datos_consulta, logo_path):
    """
    datos_consulta: dict con keys:
      codigo, cod_cita, diagnostico, cod_medicamento, fecha_creacion (datetime), doctor_nombre
    logo_path: ruta a imagen (puede ser fondo/logo)
    """
    if canvas is None or ImageReader is None:
        raise RuntimeError("La librería reportlab no está instalada. Instale con: pip install reportlab")

    # Nombre del archivo
    filename = f"consulta_{datos_consulta['codigo']}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    w, h = A4

    # Dibujar logo arriba a la izquierda si existe
    try:
        if logo_path and os.path.exists(icon_path):
            img = ImageReader(icon_path)
            # ajustar tamaño conservando aspecto (máx ancho 120)
            c.drawImage(img, 40, h - 190, width=120, preserveAspectRatio=True, mask='auto')
    except Exception:
        pass

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(180, h - 60, "Nucleo de Diagnostico: La salud lo es todo")
    c.drawString(180, h - 80, "Consulta Médica")

    # Info de la consulta
    c.setFont("Helvetica", 11)
    y = h - 120
    salto = 18

    c.drawString(40, y, f"Código Consulta: {datos_consulta['codigo']}")
    y -= salto
    c.drawString(40, y, f"Código Cita: {datos_consulta['cod_cita']}")
    y -= salto
    c.drawString(40, y, f"Doctor: {datos_consulta.get('doctor_nombre','')}")
    y -= salto
    c.drawString(40, y, f"Medicamento: {datos_consulta['cod_medicamento']} - {datos_consulta['nombre_medicamento']}")
    y -= salto
    c.drawString(40, y, f"Fecha de creación: {datos_consulta['fecha_creacion'].strftime('%Y-%m-%d %H:%M:%S')}")
    y -= salto * 1.5

    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Diagnóstico:")
    y -= salto

    c.setFont("Helvetica", 11)
    # wrap texto de diagnóstico (max ancho ~ 500)
    texto = datos_consulta['diagnostico']
    max_chars_line = 90
    lines = []
    while texto:
        lines.append(texto[:max_chars_line])
        texto = texto[max_chars_line:]
    for line in lines:
        c.drawString(40, y, line)
        y -= salto
        if y < 100:
            c.showPage()
            y = h - 80

    c.showPage()
    c.save()

    return filename


def crear_consulta_dialog(codigo_doctor, doctor_nombre):
    """
    Abre ventana para crear una consulta vinculada a una cita.
    Campos: codigo (consulta), cod_cita (FK), diagnostico (<=200 chars), cod_medicamento (FK)
    """
    win = tk.Toplevel()
    win.title("Crear Consulta")
    win.geometry("500x400")
    win.configure(bg="#e6f0ff")

    tk.Label(win, text="Crear nueva Consulta", font=("Arial", 14, "bold"), bg="#e6f0ff").pack(pady=10)

    frame = tk.Frame(win, bg="#e6f0ff")
    frame.pack(pady=5, padx=8, fill="x")

    # ---------------------------
    # CARGAR CITAS DEL DOCTOR
    # ---------------------------
    conn = connect.conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.codigo, p.nombre
        FROM hospital.cita c
        JOIN hospital.paciente p ON c.cod_paciente = p.codigo
        WHERE c.cod_doctor = %s
        ORDER BY c.codigo;
    """, (codigo_doctor,))
    citas = cur.fetchall()
    cur.close()
    conn.close()

    lista_citas = [f"{c[0]} - {c[1]}" for c in citas]
        # ---------------------------
    # CARGAR MEDICAMENTOS
    # ---------------------------
    conn = connect.conectar()
    cur = conn.cursor()
    cur.execute("SELECT codigo, nombre FROM hospital.medicamento ORDER BY codigo;")
    meds = cur.fetchall()
    cur.close()
    conn.close()

    lista_meds = [f"{m[0]} - {m[1]}" for m in meds]


    tk.Label(frame, text="Código (consulta):", bg="#e6f0ff").grid(row=0, column=0, sticky="e", pady=6)
    entry_codigo = tk.Entry(frame, width=30)
    entry_codigo.grid(row=0, column=1, pady=6)

    tk.Label(frame, text="Código Cita (FK):", bg="#e6f0ff").grid(row=1, column=0, sticky="e", pady=6)

    # ---------------------------
    # CAMBIO: COMBOBOX EN VEZ DE ENTRY
    # ---------------------------
    combo_citas = ttk.Combobox(frame, values=lista_citas, width=30, state="readonly")
    combo_citas.grid(row=1, column=1, pady=6)

    tk.Label(frame, text="Diagnóstico (<=200 chars):", bg="#e6f0ff").grid(row=2, column=0, sticky="ne", pady=6)
    txt_diagn = tk.Text(frame, width=40, height=6)
    txt_diagn.grid(row=2, column=1, pady=6)

    tk.Label(frame, text="Código Medicamento (FK):", bg="#e6f0ff").grid(row=3, column=0, sticky="e", pady=6)
    combo_meds = ttk.Combobox(frame, values=lista_meds, width=30, state="readonly")
    combo_meds.grid(row=3, column=1, pady=6)


    def on_guardar():
        # Leer valores
        cod = entry_codigo.get().strip()
        cod_cita = combo_citas.get().split(" - ")[0]   # <-- EXTRAER SOLO EL CÓDIGO
        diagnostico = txt_diagn.get("1.0", "end").strip()
        cod_med = combo_meds.get().split(" - ")[0]


        # Validaciones básicas
        if not (cod and cod_cita and diagnostico and cod_med):
            messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
            return

        # tipos
        try:
            cod_int = int(cod, 10)
            cod_cita_int = int(cod_cita, 10)
            cod_med_int = int(cod_med, 10)
        except ValueError:
            messagebox.showerror("Tipo inválido", "Los códigos deben ser números enteros.")
            return

        if len(diagnostico) > 200:
            messagebox.showerror("Longitud", "El diagnóstico no puede exceder 200 caracteres.")
            return

        conn = connect.conectar()
        if not conn:
            messagebox.showerror("DB", "No se pudo conectar a la base de datos.")
            return

        try:
            cur = conn.cursor()

            # 1) Verificar que la cita exista
            cur.execute("SELECT 1 FROM hospital.cita WHERE codigo = %s;", (cod_cita_int,))
            if cur.fetchone() is None:
                cur.close()
                conn.close()
                messagebox.showerror("Cita inválida", "La cita indicada no existe.")
                return

            # 2) Verificar que esa cita NO tenga ya una consulta
            cur.execute("SELECT 1 FROM hospital.consulta WHERE cod_cita = %s;", (cod_cita_int,))
            if cur.fetchone():
                cur.close()
                conn.close()
                messagebox.showerror("Ya existe", "Esa cita ya tiene una consulta registrada.")
                return

            # 3) Verificar medicamento
            cur.execute("SELECT 1 FROM hospital.medicamento WHERE codigo = %s;", (cod_med_int,))
            if cur.fetchone() is None:
                cur.close()
                conn.close()
                messagebox.showerror("Medicamento inválido", "El código de medicamento no existe.")
                return

            # 4) Insertar
            cur.execute("""
                INSERT INTO hospital.consulta (codigo, cod_cita, diagnostico, cod_medicamento)
                VALUES (%s, %s, %s, %s);
            """, (cod_int, cod_cita_int, diagnostico, cod_med_int))
            conn.commit()

            cur.close()
            conn.close()
            
        # Obtener nombre del medicamento
            conn2 = connect.conectar()
            cur2 = conn2.cursor()
            cur2.execute("SELECT nombre FROM hospital.medicamento WHERE codigo = %s;", (cod_med_int,))
            nombre_medicamento = cur2.fetchone()[0]
            cur2.close()
            conn2.close()


            # PDF
            datos_pdf = {
                "codigo": cod_int,
                "cod_cita": cod_cita_int,
                "diagnostico": diagnostico,
                "cod_medicamento": cod_med_int,
                "nombre_medicamento": nombre_medicamento,
                "fecha_creacion": datetime.now(),
                "doctor_nombre": doctor_nombre
            }

            logo = fondo_path
            try:
                pdf_file = generar_pdf_consulta(datos_pdf, logo)
                messagebox.showinfo("Éxito", f"Consulta creada correctamente.\nPDF generado: {pdf_file}")
            except RuntimeError as re:
                messagebox.showwarning("Sin reportlab", f"Consulta creada, pero no se pudo generar PDF:\n{re}")
            except Exception as e:
                messagebox.showwarning("PDF", f"Consulta creada, pero ocurrió un error generando el PDF:\n{e}")

            win.destroy()

        except Exception as e:
            try:
                conn.rollback()
            except:
                pass
            messagebox.showerror("Error", f"No se pudo crear la consulta:\n{e}")

    tk.Button(win, text="Guardar Consulta", bg="#0078A0", fg="white", width=20, command=on_guardar).pack(pady=12)
    tk.Button(win, text="Cancelar", bg="#828181", fg="white", width=20, command=win.destroy).pack(pady=6)

    win.mainloop()



# -------------------------
# VISTA PRINCIPAL DEL DOCTOR
# -------------------------
def vista_doctor(nombre, codigo_doctor):

    doctor = tk.Tk()
    doctor.title(f"{titulo} - Doctor {nombre}")
    doctor.geometry("400x300")
    doctor.configure(bg="#e6f0ff")

    # Ícono
    if os.path.exists(icon_path):
        doctor.iconbitmap(icon_path)

    # Fondo con imagen
    try:
        if os.path.exists(fondo_path):
            imagen = Image.open(fondo_path)
            imagen = imagen.resize((400, 300))
            imagen_tk = ImageTk.PhotoImage(imagen)
            fondo_label = tk.Label(doctor, image=imagen_tk)
            fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
            doctor.fondo_img = imagen_tk
    except:
        pass

    # Título
    tk.Label(doctor, text="Menú principal", font=("Arial", 14, "bold")).pack(pady=30)
    tk.Label(doctor, text=f"Hola: {nombre}", font=("Arial", 12)).place(relx=1.0, y=10, anchor="ne")

    # -------------------------
    # BOTÓN CONSULTAR CITAS
    # -------------------------
    tk.Button(doctor,
              text="Consultar Mis Citas",
              bg="#0078A0", fg="white",
              width=20, height=2,
              command=lambda: consultar_citas_doctor(codigo_doctor)
              ).pack(pady=10)

    # -------------------------
    # BOTÓN VER PACIENTES
    # -------------------------
    tk.Button(doctor,
              text="Ver Pacientes",
              bg="#006699", fg="white",
              width=20, height=2,
              command=lambda: ver_pacientes(codigo_doctor)
              ).pack(pady=10)

    # -------------------------
    # BOTÓN CONSULTA (NUEVO)
    # -------------------------
    tk.Button(doctor,
              text="Consulta",
              bg="#1E7E34", fg="white",
              width=20, height=2,
              command=lambda: crear_consulta_dialog(codigo_doctor, nombre)
              ).pack(pady=10)

    # -------------------------
    # BOTÓN CERRAR SESIÓN
    # -------------------------
    tk.Button(doctor, text="Cerrar Sesión",
              bg="#005563", fg="white",
              width=15, height=2,
              command=lambda: [doctor.destroy(), connect.ventana_login()]
              ).place(relx=0.40, rely=0.95, anchor="se")

    # -------------------------
    # BOTÓN SALIR
    # -------------------------
    tk.Button(doctor, text="Salir",
              bg="#828181", fg="white",
              width=15, height=2,
              command=doctor.quit
              ).place(relx=0.95, rely=0.95, anchor="se")

    doctor.mainloop()
