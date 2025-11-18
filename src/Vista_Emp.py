import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime
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