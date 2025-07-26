# core/base_tela.py
import datetime
import customtkinter as ctk
from tkinter import messagebox, Toplevel
from tkcalendar import DateEntry

class BaseTela:
    def __init__(self, app):
        self.app = app
        self.conn = app.conn
        self.container = app.container
        self.text_area = None

    def mostrar_mensagem(self, texto):
        if self.text_area:
            self.text_area.delete("0.0", "end")
            self.text_area.insert("end", texto)
        else:
            print("text_area não está definido ainda.")

    def pedir_texto(self, texto_prompt):
        return ctk.CTkInputDialog(text=texto_prompt).get_input()

    def pedir_data(self, titulo="Selecionar Data", prompt="Selecione a data:"):
        resultado = {'data': None}
        win = Toplevel()
        win.title(titulo)
        win.geometry("300x200")
        win.configure(bg="#2b2b2b")
        win.grab_set()

        ctk.CTkLabel(win, text=prompt).pack(pady=10)
        cal = DateEntry(win)
        cal.pack(pady=5)

        def salvar():
            resultado['data'] = cal.get_date()
            win.destroy()

        def cancelar():
            resultado['data'] = None
            win.destroy()

        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Salvar", command=salvar).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancelar", command=cancelar).pack(side="left", padx=5)

        win.wait_window()
        return resultado['data']
