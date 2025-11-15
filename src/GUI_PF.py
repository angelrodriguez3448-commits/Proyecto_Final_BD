import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import Conectar_DB as connect
import os
from datetime import datetime

# ==========================
# INICIO DEL PROGRAMA
# ==========================
connect.conectar()
connect.ventana_login()