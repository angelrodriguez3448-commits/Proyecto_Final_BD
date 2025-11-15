import psycopg2
import tkinter as tk
from tkinter import messagebox
import Vista_Emp as emp
import Vista_Admin as adm
import os

# ==========================
# CONFIGURACIÓN DE CONEXIÓN
# ==========================
DB_NAME = "Proyecto_final"
DB_USER = "postgres"
DB_PASSWORD = "12345"
DB_HOST = "localhost"
DB_PORT = "5432"
usuario = ""

titulo = "ND: La salud es lo primero"

def directorio_img(elemento):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    IMG_DIR = os.path.join(BASE_DIR, "img")
    path = os.path.join(IMG_DIR, elemento)
    return path

icon_path = directorio_img("ND_icono.ico")

def conectar():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.set_client_encoding('UTF8')
        return conn
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos:\n{e}")
        return None
    
# ==========================
# INTERFAZ DE LOGIN
# ==========================
def ventana_login():
    global icon_path,titulo
    login = tk.Tk()
    login.title(titulo)
    login.geometry("400x300")
    login.configure(bg="#e6f0ff")

    if os.path.exists(icon_path):
        login.iconbitmap(icon_path)

    tk.Label(login, text="La salud lo es todo", font=("Arial", 20, "bold")).pack(pady=20)
    tk.Label(login, text="Inicio de sesion", font=("Arial", 10, "bold")).pack(pady=20)
    tk.Label(login, text="Codigo:", font=("Arial", 12 )).pack()
    user_e = tk.Entry(login, width=30)
    user_e.pack(pady=5)
    tk.Label(login, text="Contraseña:", font=("Arial", 12)).pack()
    pass_e = tk.Entry(login, width=30, show="*")
    pass_e.pack(pady=5)

    def verificar_login():
        global nombre
        usuario = user_e.get().strip()
        contrasena = pass_e.get().strip()
        conn = conectar()
        
        if conn:
            try:
                if usuario == DB_USER and contrasena == DB_PASSWORD:
                    messagebox.showinfo("Acceso concedido", "Bienvenido al sistema.")
                    login.destroy()
                    adm.menu_principal("administrador")
                else:
                    usuario = int(usuario, 10)
                    cur = conn.cursor()
                    cur.execute("SELECT codigo, nombre, contrasenna FROM hospital.empleado ORDER BY codigo;")
                    registrosEmp = cur.fetchall()
                    cur.execute("SELECT codigo, nombre, contrasenna FROM hospital.doctor ORDER BY codigo;")
                    registrosDoc = cur.fetchall()
                    registros = registrosEmp + registrosDoc
                    cur.close()
                    conn.close()

                    for i in registros:
                        user, nombre, passw = i
                        print(i)
                        if usuario == user and contrasena == passw:
                            messagebox.showinfo("Acceso concedido", "Bienvenido al sistema.")
                            login.destroy()
                            if i in registrosEmp:
                                emp.vista_empleado(nombre)
                            else:
                                emp.menu_principal(nombre) #Temporal hasta tener las otras vistas
                            break
                        else:
                            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

            except Exception as e:
                messagebox.showerror("Error", f"No se ha podido conectar con la base de datos:\n{e}")



    tk.Button(login, text="Ingresar", bg="#005563", fg="white", width=25, height=2, command=verificar_login).pack(pady=20)
    login.mainloop()

