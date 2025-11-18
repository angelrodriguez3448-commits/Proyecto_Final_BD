import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime
import Conectar_DB as connect

titulo = "ND: La salud lo es todo"

def directorio_img(elemento):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    IMG_DIR = os.path.join(BASE_DIR, "img")
    path = os.path.join(IMG_DIR, elemento)
    return path

icon_path = directorio_img("ND_icono.ico")

# ==========================
# MENÚ PRINCIPAL
# ==========================
def menu_principal(nombre):
    global ventana_menu, nom, icon_path, titulo
    nom = nombre
    imagen_path = directorio_img("fondo_interfaz.jpg")
    ventana_menu = tk.Tk()
    ventana_menu.title(titulo)
    ventana_menu.geometry("400x300")
    ventana_menu.configure(bg="#e6f0ff")

    if os.path.exists(icon_path):
        ventana_menu.iconbitmap(icon_path)

    try:
        if os.path.exists(imagen_path):
            imagen = Image.open(imagen_path)
            imagen = imagen.resize((400, 300))
            imagen_tk = ImageTk.PhotoImage(imagen)
            tk.Label(ventana_menu, image=imagen_tk).place(x=0, y=0, relwidth=1, relheight=1)

    except FileNotFoundError as e:
        messagebox.showerror("Error", str(e))

    tk.Label(ventana_menu, text="Menú principal", font=("Arial", 14, "bold")).pack(pady=30)
    tk.Label(ventana_menu, text=f"Hola: {nombre}", font=("Arial", 12)).place(relx=1.0, y=10, anchor="ne")
    tk.Button(ventana_menu, text="Empleados", width=20, height=2, bg="#007A8D", fg="white", 
              command=menu_empleados).pack(pady=10)
    tk.Button(ventana_menu, text="Doctores", width=20, height=2, bg="#00C0DE", fg="white",
              command=menu_doctores).pack(pady=10)
    tk.Button(ventana_menu, text="Cerrar Sesión", width=20, height=2, bg="#005563", fg="white", 
              command=lambda:[ventana_menu.destroy(), connect.ventana_login()]).place(relx=0.40, rely=0.95, anchor="se")
    tk.Button(ventana_menu, text="Salir", width=20, height=2, bg="#828181", fg="white", 
              command=ventana_menu.quit).place(relx=0.95, rely=0.95, anchor="se")

    ventana_menu.mainloop()

# ==========================
# FUNCIONES DE CONSULTA
# ==========================
def consultar_empleados():
    global icon_path, titulo
    conn = connect.conectar()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM hospital.empleado ORDER BY codigo;")
            registros = cur.fetchall()
            cur.close()
            conn.close()

            ventana_consulta = tk.Toplevel()
            ventana_consulta.title(titulo)
            ventana_consulta.geometry("800x400")

            if os.path.exists(icon_path):
                ventana_consulta.iconbitmap(icon_path)

            tree = ttk.Treeview(ventana_consulta, columns=("ID","Nombre","Dirección","Teléfono","Fecha","Sexo","Sueldo","Turno"), show="headings")
            for col in tree["columns"]:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            tree.pack(fill="both", expand=True)

            for fila in registros:
                tree.insert("", "end", values=fila)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo consultar:\n{e}")

def consultar_doctores():
    global icon_path, titulo
    conn = connect.conectar()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM hospital.doctor ORDER BY codigo;")
            registros = cur.fetchall()
            cur.close()
            conn.close()

            ventana_consulta = tk.Toplevel()
            ventana_consulta.title(titulo)
            ventana_consulta.geometry("800x400")

            if os.path.exists(icon_path):
                ventana_consulta.iconbitmap(icon_path)

            tree = ttk.Treeview(ventana_consulta, columns=("ID","Nombre","Dirección","Teléfono","Fecha","Sexo","Especialidad"), show="headings")
            for col in tree["columns"]:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            tree.pack(fill="both", expand=True)

            for fila in registros:
                tree.insert("", "end", values=fila)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo consultar:\n{e}")

# ==========================
# FUNCIONES DE INSERCIÓN
# ==========================
def insertar_empleado():
    codigo = entry_id.get().strip()
    nombre = entry_nombre.get().strip()
    direccion = entry_direccion.get().strip()
    telefono = entry_telefono.get().strip()
    fecha_nac = entry_fecha.get().strip()
    sexo = combo_sexo.get().strip()
    sueldo = entry_sueldo.get().strip()
    turno = combo_turno.get().strip()
    contrasenna = entry_contrasena.get().strip()

    if not (codigo and nombre and direccion and telefono and fecha_nac and sexo and sueldo and turno and contrasenna):
        messagebox.showwarning("Campos vacíos", "Por favor, llena todos los campos.")
        return

    try:
        fecha_obj = datetime.strptime(fecha_nac, "%Y-%m-%d").date()
        sueldo_valor = float(sueldo)
    except ValueError:
        messagebox.showerror("Error", "Verifica el formato de fecha (YYYY-MM-DD) y sueldo (número).")
        return

    conn = connect.conectar()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO hospital.empleado (codigo, nombre, direccion, telefono, fecha_nac, sexo, sueldo, turno, contrasenna)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (codigo, nombre, direccion, telefono, fecha_obj, sexo, sueldo_valor, turno, contrasenna))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Éxito", "Empleado insertado correctamente.")
        except Exception as e:
            conn.rollback()
            conn.close()
            messagebox.showerror("Error", f"No se pudo insertar:\n{e}")

def insertar_doctor():
    codigo = entry_doc_id.get().strip()
    nombre = entry_doc_nombre.get().strip()
    direccion = entry_doc_direccion.get().strip()
    telefono = entry_doc_telefono.get().strip()
    fecha_nac = entry_doc_fecha.get().strip()
    sexo = combo_doc_sexo.get().strip()
    especialidad = entry_doc_especialidad.get().strip()
    contrasenna = entry_doc_contrasena.get().strip()

    if not (codigo and nombre and direccion and telefono and fecha_nac and sexo and especialidad and contrasenna):
        messagebox.showwarning("Campos vacíos", "Por favor, llena todos los campos.")
        return

    try:
        fecha_obj = datetime.strptime(fecha_nac, "%Y-%m-%d").date()
    except ValueError:
        messagebox.showerror("Error", "Formato de fecha incorrecto. Usa YYYY-MM-DD.")
        return

    conn = connect.conectar()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO hospital.doctor (codigo,nombre, direccion, telefono, fecha_nac, sexo, especialidad, contrasenna)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (codigo,nombre, direccion, telefono, fecha_obj, sexo, especialidad, contrasenna))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Éxito", "Doctor insertado correctamente.")
        except Exception as e:
            conn.rollback()
            conn.close()
            messagebox.showerror("Error", f"No se pudo insertar:\n{e}")

# ==========================
# MENÚ DE EMPLEADOS
# ==========================
def menu_empleados():
    global icon_path, titulo
    ventana_menu.destroy()
    ventana_emp_menu = tk.Tk()
    ventana_emp_menu.title(titulo)
    ventana_emp_menu.geometry("400x350")
    ventana_emp_menu.configure(bg="#e6f0ff")

    if os.path.exists(icon_path):
        ventana_emp_menu.iconbitmap(icon_path)

    tk.Label(ventana_emp_menu, text="Gestión de Empleados", font=("Arial", 16, "bold")).pack(pady=20)
    tk.Button(ventana_emp_menu, text=" Insertar Empleado", bg="#007A8D", fg="white", width=25, height=2, 
              command=lambda:[ventana_emp_menu.destroy(), abrir_empleado()]).pack(pady=10)
    tk.Button(ventana_emp_menu, text="Consultar Empleados", bg="#00C0DE", fg="white", width=25, height=2, 
              command=consultar_empleados).pack(pady=5)
    tk.Button(ventana_emp_menu, text="↩ Volver al menú principal",  bg="#005563", fg="white", width=25, height=2, 
              command=lambda:[ventana_emp_menu.destroy(), menu_principal(nom)]).place(relx=0.40, rely=0.95, anchor="se")
    tk.Button(ventana_emp_menu, text="Salir", bg="#828181", fg="white", width=25, height=2, 
              command=ventana_emp_menu.destroy).place(relx=0.95, rely=0.95, anchor="se")

# ==========================
# MENÚ DE DOCTORES
# ==========================
def menu_doctores():
    global icon_path, titulo
    ventana_menu.destroy()
    ventana_doc_menu = tk.Tk()
    ventana_doc_menu.title(titulo)
    ventana_doc_menu.geometry("400x350")
    ventana_doc_menu.configure(bg="#e6f0ff")

    if os.path.exists(icon_path):
        ventana_doc_menu.iconbitmap(icon_path)

    tk.Label(ventana_doc_menu, text="Gestión de Doctores", font=("Arial", 16, "bold")).pack(pady=20)
    tk.Button(ventana_doc_menu, text=" Insertar Doctor", bg="#007A8D", fg="white", width=25, height=2, 
              command=lambda:[ventana_doc_menu.destroy(), abrir_doctores()]).pack(pady=10)
    tk.Button(ventana_doc_menu, text="Consultar Doctores", bg="#00C0DE", fg="white", width=25, height=2, 
              command=consultar_doctores).pack(pady=5)
    tk.Button(ventana_doc_menu, text="↩ Volver al menú principal", bg="#005563", fg="white", width=25, height=2, 
              command=lambda:[ventana_doc_menu.destroy(), menu_principal(nom)]).place(relx=0.40, rely=0.95, anchor="se")
    tk.Button(ventana_doc_menu, text="Salir", bg="#828181", fg="white", width=25, height=2, 
              command=ventana_doc_menu.destroy).place(relx=0.95, rely=0.95, anchor="se")

# ==========================
# VENTANA DE EMPLEADOS
# ==========================
def abrir_empleado():
    global entry_id, entry_nombre, entry_direccion, entry_telefono, entry_fecha, combo_sexo, entry_sueldo, combo_turno, entry_contrasena
    global nom, icon_path, titulo
    ventana_emp = tk.Tk()
    ventana_emp.title(titulo)
    ventana_emp.geometry("900x600")
    ventana_emp.configure(bg="#e6f0ff")

    if os.path.exists(icon_path):
        ventana_emp.iconbitmap(icon_path)

    frame = tk.LabelFrame(ventana_emp, text="Insertar Empleado", padx=10, pady=10)
    frame.pack(fill="x", padx=10, pady=10)

    campos = [
        ("ID", "entry_id"), ("Nombre", "entry_nombre"), ("Dirección", "entry_direccion"),
        ("Teléfono", "entry_telefono"), ("Fecha Nac (YYYY-MM-DD)", "entry_fecha"),
        ("Sexo", "combo_sexo"), ("Sueldo", "entry_sueldo"), ("Turno", "combo_turno"),
        ("Contraseña", "entry_contrasena"),
    ]

    for i, (label, var) in enumerate(campos):
        tk.Label(frame, text=label + ":").grid(row=i, column=0, sticky="e")
        if "combo" in var:
            if var == "combo_sexo":
                combo_sexo = ttk.Combobox(frame, values=["FEMENINO", "MASCULINO"])
                combo_sexo.grid(row=i, column=1)
            else:
                combo_turno = ttk.Combobox(frame, values=["MATUTINO", "VESPERTINO", "NOCTURNO"])
                combo_turno.grid(row=i, column=1)
        else:
            entry = tk.Entry(frame, width=40, show="*" if "contrasena" in var else "")
            entry.grid(row=i, column=1)
            globals()[var] = entry

    tk.Button(frame, text="Insertar Empleado", command=insertar_empleado,bg="#00C0DE", fg="white").grid(row=len(campos), column=0, pady=15)
    tk.Button(ventana_emp, text="↩ Volver al menú principal",  bg="#005563", fg="white", width=25, height=2, 
              command=lambda:[ventana_emp.destroy(), menu_principal(nom)]).place(relx=0.40, rely=0.95, anchor="se")
    tk.Button(ventana_emp, text="Salir", bg="#828181", fg="white", width=25, height=2, 
              command=ventana_emp.destroy).place(relx=0.95, rely=0.95, anchor="se")

# ==========================
# VENTANA DE DOCTORES
# ==========================
def abrir_doctores():
    global entry_doc_id, entry_doc_nombre, entry_doc_direccion, entry_doc_telefono, entry_doc_fecha, combo_doc_sexo, entry_doc_especialidad, entry_doc_contrasena 
    global nom, icon_path, titulo

    ventana_doc = tk.Tk()
    ventana_doc.title(titulo)
    ventana_doc.geometry("900x600")
    ventana_doc.configure(bg="#e6f0ff")

    if os.path.exists(icon_path):
        ventana_doc.iconbitmap(icon_path)

    frame = tk.LabelFrame(ventana_doc, text="Insertar nuevo doctor", padx=10, pady=10)
    frame.pack(fill="x", padx=10, pady=10)

    campos_doc = [
        ("ID", "entry_doc_id"),
        ("Nombre", "entry_doc_nombre"),
        ("Dirección", "entry_doc_direccion"),
        ("Teléfono", "entry_doc_telefono"),
        ("Fecha Nac (YYYY-MM-DD)", "entry_doc_fecha"),
        ("Sexo", "combo_doc_sexo"),
        ("Especialidad", "entry_doc_especialidad"),
        ("Contraseña", "entry_doc_contrasena"),
    ]

    for i, (label, var) in enumerate(campos_doc):
        tk.Label(frame, text=label + ":").grid(row=i, column=0, sticky="e")
        if var == "combo_doc_sexo":
            combo_doc_sexo = ttk.Combobox(frame, values=["FEMENINO", "MASCULINO"])
            combo_doc_sexo.grid(row=i, column=1)
        else:
            entry = tk.Entry(frame, width=40, show="*" if "contrasena" in var else "")
            entry.grid(row=i, column=1)
            globals()[var] = entry

    tk.Button(frame, text="Insertar Doctor", command=insertar_doctor,
              bg="#00C0DE", fg="white").grid(row=len(campos_doc), column=0, columnspan=2, pady=15)
    tk.Button(ventana_doc, text="↩ Volver al menú principal", bg="#005563", fg="white", width=25, height=2, 
              command=lambda:[ventana_doc.destroy(), menu_principal(nom)]).place(relx=0.40, rely=0.95, anchor="se")
    tk.Button(ventana_doc, text="Salir", bg="#828181", fg="white", width=25, height=2, 
              command=ventana_doc.destroy).place(relx=0.95, rely=0.95, anchor="se")