# app.py
from PIL import Image
from telas.telaAluno import TelaAluno
from telas.telaMatricula import TelaMatricula
from telas.telaProfessor import TelaProfessor
from telas.telaDisciplina import TelaDisciplina
from telas.telaTurma import TelaTurma
from telas.telaResponsavel import TelaResponsavel
from db import conectar
import customtkinter as ctk

class SistemaEscolarApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Escolar")
        self.geometry("640x540")
        self.conn = conectar()
        self.minha_fonte = ctk.CTkFont(family="Montserrat", size=24, weight="bold")

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        self.tela_principal()

    def tela_principal(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.container, text="Menu Principal", font=self.minha_fonte).pack(pady=(0, 20))

        # Frame de botões principais (Aluno, Professor, etc.)
        btn_frame = ctk.CTkFrame(self.container)
        btn_frame.pack(padx=40, pady=(0, 10), fill="both")

        for i in range(2):
            btn_frame.grid_columnconfigure(i, weight=1, uniform="col")

        botoes = [
            ("Alunos", lambda: TelaAluno(self).abrir()),
            ("Responsáveis", lambda: TelaResponsavel(self).abrir()),
            ("Professores", lambda: TelaProfessor(self).abrir()),
            ("Disciplinas", lambda: TelaDisciplina(self).abrir()),
            ("Turmas", lambda: TelaTurma(self).abrir()),
        ]

        btn_font = ctk.CTkFont(family="Montserrat", size=18, weight="bold")
        btn_color = "#3B82F6"

        for idx, (text, cmd) in enumerate(botoes):
            r = idx // 2
            c = idx % 2
            ctk.CTkButton(
                btn_frame,
                text=text,
                command=cmd,
                font=btn_font,
                fg_color=btn_color,
                hover_color="#2563EB"
            ).grid(row=r, column=c, padx=15, pady=15, sticky="ew")

        # Frame separado só para Matrícula e futuras ações administrativas
        box_matricula = ctk.CTkFrame(self.container)
        box_matricula.pack(padx=40, pady=(10, 0), fill="x")

        ctk.CTkLabel(box_matricula, text="Ações Administrativas", font=("Montserrat", 16, "bold")).pack(pady=(10, 5))

        ctk.CTkButton(
            box_matricula,
            text="Matriculas",
            command=lambda: TelaMatricula(self).abrir(),
            font=btn_font,
            fg_color="#10B981",  # Verde bonito
            hover_color="#059669"
        ).pack(pady=(0, 10), padx=15, fill="x")

if __name__ == "__main__":
    app = SistemaEscolarApp()
    app.mainloop()
