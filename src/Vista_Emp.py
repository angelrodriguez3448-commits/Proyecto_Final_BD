import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import os
from datetime import datetime, time as dtime
import Conectar_DB as connect

def directorio_img(elemento):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    IMG_DIR = os.path.join(BASE_DIR, "img")
    path = os.path.join(IMG_DIR, elemento)
    return path

icon_path = directorio_img("ND_icono.ico")

titulo = "ND: La salud lo es todo"

# ==========================
# VISTA EMPLEADO (Vista empleado)
# ==========================
def vista_empleado(nombre):
    global ventana_empleado, nom, icon_path, titulo
    nom = nombre

    ventana_empleado = tk.Tk()
    ventana_empleado.title(titulo)
    ventana_empleado.geometry("400x300")
    ventana_empleado.configure(bg="#e6f0ff")

    if os.path.exists(icon_path):
        ventana_empleado.iconbitmap(icon_path)

    imagen_path = directorio_img("fondo_interfaz.jpg")

    try:
        if os.path.exists(imagen_path):
            imagen = Image.open(imagen_path)
            imagen = imagen.resize((400, 300))
            imagen_tk = ImageTk.PhotoImage(imagen)
            # Mantener referencia para evitar que se libere de memoria
            label_fondo = tk.Label(ventana_empleado, image=imagen_tk)
            label_fondo.image = imagen_tk
            label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

    except FileNotFoundError as e:
        messagebox.showerror("Error", str(e))

    # Encabezado
    tk.Label(ventana_empleado, text="Vista Empleado", font=("Arial", 14, "bold")).pack(pady=30)
    tk.Label(ventana_empleado, text=f"Hola: {nombre}", font=("Arial", 12)).place(relx=1.0, y=10, anchor="ne")

    # Botón para pacientes
    tk.Button(ventana_empleado, text="Pacientes", width=20, height=2, bg="#007A8D", fg="white",
              command=menu_pacientes).pack(pady=10)

    # Botón para citas (nuevo)
    tk.Button(ventana_empleado, text="Citas", width=20, height=2, bg="#009150", fg="white",
              command=menu_citas).pack(pady=6)

    # Botón para cerrar sesión
    tk.Button(ventana_empleado, text="Cerrar Sesión", width=20, height=2, bg="#005563", fg="white",
              command=lambda:[ventana_empleado.destroy(), connect.ventana_login()]).place(relx=0.40, rely=0.95, anchor="se")

    # Botón para salir
    tk.Button(ventana_empleado, text="Salir", width=20, height=2, bg="#828181", fg="white",
              command=ventana_empleado.quit).place(relx=0.95, rely=0.95, anchor="se")

    ventana_empleado.mainloop()

# ==========================
# MENÚ DE PACIENTES
# ==========================
def menu_pacientes():
    global icon_path, titulo
    ventana_empleado.destroy()
    ventana_pac_menu = tk.Tk()
    ventana_pac_menu.title(titulo)
    ventana_pac_menu.geometry("400x350")
    ventana_pac_menu.configure(bg="#e6f0ff")

    if os.path.exists(icon_path):
        ventana_pac_menu.iconbitmap(icon_path)

    # Encabezado
    tk.Label(ventana_pac_menu, text="Gestión de Pacientes", font=("Arial", 16, "bold")).pack(pady=20)

    # Botón para insertar paciente
    tk.Button(ventana_pac_menu, text=" Insertar Paciente", bg="#007A8D", fg="white", width=25, height=2,
              command=lambda:[ventana_pac_menu.destroy(), abrir_paciente()]).pack(pady=10)

    # Botón para consultar pacientes
    tk.Button(ventana_pac_menu, text="Consultar Pacientes", bg="#00C0DE", fg="white", width=25, height=2,
              command=consultar_pacientes).pack(pady=5)

    # Botón para volver al menú principal
    tk.Button(ventana_pac_menu, text="↩ Volver al menú principal", bg="#005563", fg="white", width=25, height=2,
              command=lambda:[ventana_pac_menu.destroy(), vista_empleado(nom)]).place(relx=0.40, rely=0.95, anchor="se")

    # Botón para salir
    tk.Button(ventana_pac_menu, text="Salir", bg="#828181", fg="white", width=25, height=2,
              command=ventana_pac_menu.destroy).place(relx=0.95, rely=0.95, anchor="se")

    ventana_pac_menu.mainloop()

# ==========================
# VENTANA DE PACIENTES
# ==========================
def abrir_paciente():
    global entry_codigo, entry_nombre, entry_direccion, entry_telefono, entry_fecha_nac, combo_sexo, entry_edad, entry_estatura
    global icon_path, titulo
    ventana_pac = tk.Tk()
    ventana_pac.title(titulo)
    ventana_pac.geometry("900x600")
    ventana_pac.configure(bg="#e6f0ff")

    if os.path.exists(icon_path):
        ventana_pac.iconbitmap(icon_path)

    frame = tk.LabelFrame(ventana_pac, text="Insertar Paciente", padx=10, pady=10)
    frame.pack(fill="x", padx=10, pady=10)

    # Campos para paciente
    campos = [
        ("Código", "entry_codigo"),
        ("Nombre", "entry_nombre"),
        ("Dirección", "entry_direccion"),
        ("Teléfono", "entry_telefono"),
        ("Fecha Nac (YYYY-MM-DD)", "entry_fecha_nac"),
        ("Sexo", "combo_sexo"),
        ("Edad", "entry_edad"),
        ("Estatura", "entry_estatura"),
    ]

    for i, (label, var) in enumerate(campos):
        tk.Label(frame, text=label + ":").grid(row=i, column=0, sticky="e")
        if "combo" in var:
            if var == "combo_sexo":
                combo_sexo = ttk.Combobox(frame, values=["FEMENINO", "MASCULINO"])
                combo_sexo.grid(row=i, column=1)
        else:
            entry = tk.Entry(frame, width=40)
            entry.grid(row=i, column=1)
            globals()[var] = entry

    # Botón para insertar paciente
    tk.Button(frame, text="Insertar Paciente", command=insertar_paciente, bg="#00C0DE", fg="white").grid(row=len(campos), column=0, pady=15)

    # Botón para volver al menú principal
    tk.Button(ventana_pac, text="↩ Volver al menú principal", bg="#005563", fg="white", width=25, height=2,
              command=lambda:[ventana_pac.destroy(), vista_empleado(nom)]).place(relx=0.40, rely=0.95, anchor="se")

    # Botón para salir
    tk.Button(ventana_pac, text="Salir", bg="#828181", fg="white", width=25, height=2,
              command=ventana_pac.destroy).place(relx=0.95, rely=0.95, anchor="se")

    ventana_pac.mainloop()

# ==========================
# FUNCIÓN DE CONSULTA PACIENTES
# ==========================
def consultar_pacientes():
    global icon_path, titulo
    conn = connect.conectar()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM hospital.paciente ORDER BY codigo;")
            registros = cur.fetchall()
            cur.close()
            conn.close()

            ventana_consulta = tk.Toplevel()
            ventana_consulta.title(titulo)
            ventana_consulta.geometry("900x400")

            if os.path.exists(icon_path):
                ventana_consulta.iconbitmap(icon_path)

            # Definir columnas para pacientes
            columnas = ("Código", "Nombre", "Dirección", "Teléfono", "Fecha Nac", "Sexo", "Edad", "Estatura")
            tree = ttk.Treeview(ventana_consulta, columns=columnas, show="headings")

            for col in columnas:
                tree.heading(col, text=col)
                tree.column(col, width=100)

            tree.pack(fill="both", expand=True)

            # Insertar registros en la tabla
            for fila in registros:
                tree.insert("", "end", values=fila)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo consultar:\n{e}")

# ==========================
# FUNCIÓN DE INSERCIÓN PACIENTES
# ==========================
def insertar_paciente():
    codigo = entry_codigo.get().strip()
    nombre = entry_nombre.get().strip()
    direccion = entry_direccion.get().strip()
    telefono = entry_telefono.get().strip()
    fecha_nac = entry_fecha_nac.get().strip()
    sexo = combo_sexo.get().strip()
    edad = entry_edad.get().strip()
    estatura = entry_estatura.get().strip()

    # Validación de campos vacíos
    if not (codigo and nombre and direccion and telefono and fecha_nac and sexo and edad and estatura):
        messagebox.showwarning("Campos vacíos", "Por favor, llena todos los campos.")
        return

    try:
        # Validar fecha y convertir edad/estatura a números
        fecha_obj = datetime.strptime(fecha_nac, "%Y-%m-%d").date()
        edad_valor = int(edad)
        estatura_valor = float(estatura)
    except ValueError:
        messagebox.showerror("Error", "Verifica el formato de fecha (YYYY-MM-DD), edad (entero) y estatura (número).")
        return

    conn = connect.conectar()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO hospital.paciente (codigo, nombre, direccion, telefono, fecha_nac, sexo, edad, estatura)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (codigo, nombre, direccion, telefono, fecha_obj, sexo, edad_valor, estatura_valor))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Éxito", "Paciente insertado correctamente.")
        except Exception as e:
            conn.rollback()
            conn.close()
            messagebox.showerror("Error", f"No se pudo insertar:\n{e}")

# ==========================
#  NUEVO: MENÚ CITAS (consultar / insertar)
# ==========================
def menu_citas():
    global icon_path, titulo
    try:
        ventana_empleado.destroy()
    except:
        pass

    ventana_citas = tk.Tk()
    ventana_citas.title(titulo)
    ventana_citas.geometry("400x350")
    ventana_citas.configure(bg="#e6f0ff")

    if os.path.exists(icon_path):
        ventana_citas.iconbitmap(icon_path)

    tk.Label(ventana_citas, text="Gestión de Citas", font=("Arial", 16, "bold")).pack(pady=20)

    tk.Button(ventana_citas, text="Agregar Cita", bg="#009150", fg="white", width=25, height=2,
              command=lambda:[ventana_citas.destroy(), ventana_agregar_cita()]).pack(pady=10)

    tk.Button(ventana_citas, text="Consultar Citas", bg="#00C0DE", fg="white", width=25, height=2,
              command=consultar_citas).pack(pady=10)

    tk.Button(ventana_citas, text="↩ Volver al menú principal", bg="#005563", fg="white",
              width=25, height=2, command=lambda:[ventana_citas.destroy(), vista_empleado(nom)]).place(relx=0.40, rely=0.95, anchor="se")

    tk.Button(ventana_citas, text="Salir", bg="#828181", fg="white",
              width=25, height=2, command=ventana_citas.destroy).place(relx=0.95, rely=0.95, anchor="se")

    ventana_citas.mainloop()

# ==========================
#  UTIL: cargar pacientes y doctores para combobox
# ==========================
def cargar_pacientes_doctores():
    """
    Devuelve dos listas:
    pacientes_list: list of "codigo - nombre"
    doctores_list: list of "codigo - nombre"
    y dos diccionarios map_codigo_por_display para conversión.
    """
    pacientes_list = []
    doctores_list = []
    map_pac = {}
    map_doc = {}

    conn = connect.conectar()
    if not conn:
        return pacientes_list, doctores_list, map_pac, map_doc

    try:
        cur = conn.cursor()
        cur.execute("SELECT codigo, nombre FROM hospital.paciente ORDER BY nombre;")
        for codigo, nombre in cur.fetchall():
            display = f"{codigo} - {nombre}"
            pacientes_list.append(display)
            map_pac[display] = codigo

        cur.execute("SELECT codigo, nombre FROM hospital.doctor ORDER BY nombre;")
        for codigo, nombre in cur.fetchall():
            display = f"{codigo} - {nombre}"
            doctores_list.append(display)
            map_doc[display] = codigo

        cur.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar pacientes/doctores:\n{e}")
    finally:
        conn.close()

    return pacientes_list, doctores_list, map_pac, map_doc

# ==========================
#  VENTANA AGREGAR CITA
# ==========================
def ventana_agregar_cita():
    # Ventana principal más ancha para incluir la agenda a la derecha
    win = tk.Tk()
    win.title("Agregar Cita")
    win.geometry("900x360")
    win.configure(bg="#e6f0ff")

    if os.path.exists(icon_path):
        try:
            win.iconbitmap(icon_path)
        except Exception:
            pass

    tk.Label(win, text="Agregar Cita", font=("Arial", 14, "bold"), bg="#e6f0ff").pack(pady=8)

    # Contenedor principal con dos columnas: izquierda -> formulario, derecha -> agenda
    contenedor = tk.Frame(win, bg="#e6f0ff")
    contenedor.pack(fill="both", expand=True, padx=8, pady=4)

    # FRAME IZQUIERDO: formulario de la cita
    frame = tk.Frame(contenedor, padx=10, pady=10, bg="#e6f0ff")
    frame.grid(row=0, column=0, sticky="nsew")

    # FRAME DERECHO: agenda del doctor (tabla)
    frame_agenda = tk.LabelFrame(contenedor, text="Agenda del Doctor", padx=5, pady=5, bg="#e6f0ff")
    frame_agenda.grid(row=0, column=1, sticky="nsew", padx=(10,0))

    # Configurar que columna 0 ocupe más y la agenda tenga ancho fijo razonable
    contenedor.grid_columnconfigure(0, weight=0)
    contenedor.grid_columnconfigure(1, weight=1)

    # Código cita
    tk.Label(frame, text="Código Cita:", bg="#e6f0ff").grid(row=0, column=0, sticky="e", pady=4)
    entry_cod_cita = tk.Entry(frame, width=30)
    entry_cod_cita.grid(row=0, column=1, pady=4)

    # Paciente / Doctor
    tk.Label(frame, text="Paciente:", bg="#e6f0ff").grid(row=1, column=0, sticky="e", pady=4)
    pacientes_list, doctores_list, map_pac, map_doc = cargar_pacientes_doctores()
    combo_paciente = ttk.Combobox(frame, values=pacientes_list, width=28)
    combo_paciente.grid(row=1, column=1, pady=4)

    tk.Label(frame, text="Doctor:", bg="#e6f0ff").grid(row=2, column=0, sticky="e", pady=4)
    combo_doctor = ttk.Combobox(frame, values=doctores_list, width=28)
    combo_doctor.grid(row=2, column=1, pady=4)

    # Fecha -> DateEntry
    tk.Label(frame, text="Fecha (YYYY-MM-DD):", bg="#e6f0ff").grid(row=3, column=0, sticky="e", pady=4)
    entry_fecha_cita = DateEntry(frame, width=27, date_pattern='yyyy-mm-dd', background='darkblue', foreground='white')
    entry_fecha_cita.grid(row=3, column=1, pady=4)

    # Hora
    tk.Label(frame, text="Hora (HH:MM) 08:00-20:00:", bg="#e6f0ff").grid(row=4, column=0, sticky="e", pady=4)
    entry_hora_cita = tk.Entry(frame, width=30)
    entry_hora_cita.grid(row=4, column=1, pady=4)

    # Botón Insertar
    tk.Button(frame, text="Insertar Cita", bg="#009150", fg="white", width=20, command=lambda: on_insert()).grid(row=5, column=0, columnspan=2, pady=12)

    # Botones Inferiores
    tk.Button(win, text="↩ Volver", bg="#005563", fg="white", width=15, command=lambda: [win.destroy(), menu_citas()]).place(relx=0.25, rely=0.92, anchor="se")
    tk.Button(win, text="Salir", bg="#828181", fg="white", width=15, command=win.destroy).place(relx=0.95, rely=0.92, anchor="se")

    # -------------------------
    # Treeview AGENDA (derecha)
    # -------------------------
    columnas_agenda = ("Código cita", "Paciente", "Fecha", "Hora")
    tree_agenda = ttk.Treeview(frame_agenda, columns=columnas_agenda, show="headings", height=12)
    for col in columnas_agenda:
        tree_agenda.heading(col, text=col)
        tree_agenda.column(col, width=120, anchor="center")
    tree_agenda.pack(fill="both", expand=True, padx=4, pady=4)

    # Pequeño label cuando no hay doctor seleccionado
    lbl_sin_seleccion = tk.Label(frame_agenda, text="Seleccione un doctor para ver su agenda.", bg="#e6f0ff")
    lbl_sin_seleccion.place(relx=0.5, rely=0.5, anchor="center")

    # -------------------------
    # Funciones internas
    # -------------------------

    def cargar_agenda_por_doctor(cod_doctor):
        """
        Consulta la BD por todas las citas del doctor (cod_doctor) y llena el tree_agenda.
        """
        # Limpiar tree
        for i in tree_agenda.get_children():
            tree_agenda.delete(i)

        # Ocultar el label de instrucción si está visible
        try:
            lbl_sin_seleccion.place_forget()
        except Exception:
            pass

        conn = connect.conectar()
        if not conn:
            messagebox.showerror("DB", "No se pudo conectar a la base de datos para cargar la agenda.")
            return

        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT c.codigo, p.nombre, c.fecha, c.hora
                FROM hospital.cita c
                LEFT JOIN hospital.paciente p ON c.cod_paciente = p.codigo
                WHERE c.cod_doctor = %s
                ORDER BY c.fecha, c.hora;
            """, (cod_doctor,))
            filas = cur.fetchall()
            cur.close()
            conn.close()

            if not filas:
                # Mostrar texto claro si no hay citas
                tree_agenda.insert("", "end", values=("—", "No tiene citas", "—", "—"))
                return

            for fila in filas:
                codigo_cita, nombre_paciente, fecha, hora = fila
                # Formatear fecha/hora si vienen como objetos
                try:
                    fecha_str = fecha.strftime("%Y-%m-%d")
                except Exception:
                    fecha_str = str(fecha)
                hora_str = hora.strftime("%H:%M") if hasattr(hora, "strftime") else str(hora)
                tree_agenda.insert("", "end", values=(codigo_cita, nombre_paciente, fecha_str, hora_str))

        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            messagebox.showerror("Error", f"No se pudo cargar la agenda:\n{e}")

    # Evento cuando se selecciona doctor en el combobox
    def evento_doctor_seleccionado(event):
        doc_disp = combo_doctor.get().strip()
        if not doc_disp:
            return

        if doc_disp not in map_doc:
            # No es una selección válida (p. ej. escritura manual)
            messagebox.showerror("Doctor inválido", "Selecciona un doctor válido del desplegable.")
            return

        cod_doc_seleccionado = map_doc[doc_disp]
        cargar_agenda_por_doctor(cod_doc_seleccionado)

    # Vincular evento
    combo_doctor.bind("<<ComboboxSelected>>", evento_doctor_seleccionado)

    # -------------------------
    # Lógica de insertar cita (igual a la tuya, con la revisión de conflicto)
    # -------------------------
    def on_insert():
        cod = entry_cod_cita.get().strip()
        pac_disp = combo_paciente.get().strip()
        doc_disp = combo_doctor.get().strip()
        fecha = entry_fecha_cita.get().strip()
        hora = entry_hora_cita.get().strip()

        if not (cod and pac_disp and doc_disp and fecha and hora):
            messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
            return

        if pac_disp not in map_pac:
            messagebox.showerror("Paciente inválido", "Selecciona un paciente válido del desplegable.")
            return
        if doc_disp not in map_doc:
            messagebox.showerror("Doctor inválido", "Selecciona un doctor válido del desplegable.")
            return

        cod_pac = map_pac[pac_disp]
        cod_doc = map_doc[doc_disp]

        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
            hora_obj = datetime.strptime(hora, "%H:%M").time()
        except ValueError:
            messagebox.showerror("Formato incorrecto", "Asegúrate de usar los formatos: YYYY-MM-DD y HH:MM")
            return

        if fecha_obj.weekday() > 4:
            messagebox.showerror("Día inválido", "Solo se permiten citas de lunes a viernes.")
            return

        if not (dtime(8,0) <= hora_obj <= dtime(20,0)):
            messagebox.showerror("Hora inválida", "Horario permitido para iniciar cita: 08:00 a 20:00.")
            return

        conn = connect.conectar()
        if not conn:
            messagebox.showerror("DB", "No se pudo conectar a la base de datos.")
            return

        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT 1 FROM hospital.cita
                WHERE cod_doctor = %s AND fecha = %s AND hora = %s
                LIMIT 1;
            """, (cod_doc, fecha_obj, hora_obj))
            if cur.fetchone():
                resp = messagebox.askyesno(
                    "Conflicto horario",
                    "El doctor ya tiene una cita a esa hora.\n¿Quieres ingresar una nueva?"
                )

                if resp:
                    # Limpiar campos
                    entry_cod_cita.delete(0, tk.END)
                    combo_paciente.set("")
                    combo_doctor.set("")
                    entry_fecha_cita.set_date(datetime.now().date())
                    entry_hora_cita.delete(0, tk.END)

                    messagebox.showinfo(
                        "Campos reiniciados",
                        "Ahora puedes ingresar una nueva cita."
                    )
                    # Al limpiar el doctor, también limpiar la agenda
                    for i in tree_agenda.get_children():
                        tree_agenda.delete(i)
                    lbl_sin_seleccion.place(relx=0.5, rely=0.5, anchor="center")
                else:
                    messagebox.showinfo("Cancelado", "No se realizó ninguna acción.")

                cur.close()
                conn.close()
                return

            # Si no hay conflicto, insertar
            cur.execute("""
                INSERT INTO hospital.cita (codigo, cod_paciente, cod_doctor, fecha, hora)
                VALUES (%s, %s, %s, %s, %s);
            """, (cod, cod_pac, cod_doc, fecha_obj, hora_obj))
            conn.commit()
            cur.close()
            conn.close()

            messagebox.showinfo("Éxito", "Cita agregada correctamente.")

            # Después de insertar, refrescar la agenda si el doctor seleccionado es el mismo
            sel_doc = combo_doctor.get().strip()
            if sel_doc and sel_doc in map_doc and map_doc[sel_doc] == cod_doc:
                cargar_agenda_por_doctor(cod_doc)

            # opcional: limpiar campos tras insertar
            entry_cod_cita.delete(0, tk.END)
            combo_paciente.set("")
            entry_fecha_cita.set_date(datetime.now().date())
            entry_hora_cita.delete(0, tk.END)

        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            messagebox.showerror("Error", f"No se pudo insertar la cita:\n{e}")

    win.mainloop()

# ==========================
#  CONSULTAR CITAS
# ==========================
def consultar_citas():
    conn = connect.conectar()
    if conn:
        try:
            cur = conn.cursor()
            # Mostrar con joins para ver nombres
            cur.execute("""
                SELECT c.codigo, p.nombre as paciente, d.nombre as doctor, c.fecha, c.hora
                FROM hospital.cita c
                LEFT JOIN hospital.paciente p ON c.cod_paciente = p.codigo
                LEFT JOIN hospital.doctor d ON c.cod_doctor = d.codigo
                ORDER BY c.fecha, c.hora;
            """)
            registros = cur.fetchall()
            cur.close()
            conn.close()

            ventana = tk.Toplevel()
            ventana.title("Citas")
            ventana.geometry("700x400")

            columnas = ("Código", "Paciente", "Doctor", "Fecha", "Hora")
            tree = ttk.Treeview(ventana, columns=columnas, show="headings")

            for col in columnas:
                tree.heading(col, text=col)
                tree.column(col, width=130)

            tree.pack(fill="both", expand=True)

            for fila in registros:
                # fila ejemplo: (codigo, paciente, doctor, fecha, hora)
                # convertir fecha/hora a string
                cod, pac, doc, fecha, hora = fila
                if isinstance(fecha, datetime):
                    fecha_str = fecha.strftime("%Y-%m-%d")
                else:
                    try:
                        fecha_str = fecha.isoformat()
                    except:
                        fecha_str = str(fecha)
                hora_str = hora.strftime("%H:%M") if hasattr(hora, "strftime") else str(hora)
                tree.insert("", "end", values=(cod, pac, doc, fecha_str, hora_str))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo consultar citas:\n{e}")