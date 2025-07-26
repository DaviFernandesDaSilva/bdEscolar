import customtkinter as ctk
from tkinter import messagebox
from core.baseTela import BaseTela
import professor

class TelaProfessor(BaseTela):
    def __init__(self, app):
        super().__init__(app)

    def abrir(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.container, text="Studee - Professores", font=self.app.minha_fonte).pack(pady=10)

        btn_frame = ctk.CTkFrame(self.container)
        btn_frame.pack(pady=10, fill="x")
        for i in range(5):
            btn_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkButton(btn_frame, text="Listar", command=self.listar).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Inserir", command=self.inserir_professor).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Buscar", command=self.buscar_professor).grid(row=0, column=2, padx=5)
        ctk.CTkButton(btn_frame, text="Atualizar", command=self.atualizar_professor).grid(row=0, column=3, padx=5)
        ctk.CTkButton(btn_frame, text="Deletar", command=self.deletar_professor).grid(row=0, column=4, padx=5)

        ctk.CTkButton(self.container, text="Voltar", command=self.app.tela_principal).pack(pady=20)

        self.text_area = ctk.CTkTextbox(self.container, width=680, height=280)
        self.text_area.configure(font=("Consolas", 12))
        self.text_area.pack(pady=10)
        
        filtro_frame = ctk.CTkFrame(self.container)
        filtro_frame.pack(pady=10, fill="x", padx=20)

        ctk.CTkLabel(filtro_frame, text="Ordenar por:").pack(side="left", padx=(0, 5))

        opcoes_ordenacao = ["ID", "Nome"]  # Ajuste conforme colunas do seu BD
        self.combo_ordenar = ctk.CTkComboBox(filtro_frame, values=opcoes_ordenacao)
        self.combo_ordenar.set(opcoes_ordenacao[0])
        self.combo_ordenar.pack(side="left", padx=5)

        ctk.CTkLabel(filtro_frame, text="Ordem:").pack(side="left", padx=(20, 5))
        self.combo_ordem = ctk.CTkComboBox(filtro_frame, values=["Asc", "Desc"])
        self.combo_ordem.set("Asc")
        self.combo_ordem.pack(side="left", padx=5)

        btn_aplicar = ctk.CTkButton(filtro_frame, text="Aplicar", command=self.aplicar_ordenacao)
        btn_aplicar.pack(side="left", padx=10)
        
        self.listar()
        
    def mostrar_mensagem(self, texto):
        self.text_area.delete("0.0", "end")
        self.text_area.insert("end", texto)
        
    def aplicar_ordenacao(self):
        coluna = self.combo_ordenar.get()
        ordem = self.combo_ordem.get()
        self.listar(coluna, ordem)

    def listar(self, coluna="ID", ordem="Asc"):
        try:
            colunas_bd = {
                "ID": "id_professor",
                "Nome": "nome",
            }
            ordem_sql = "ASC" if ordem.lower() == "asc" else "DESC"
            coluna_sql = colunas_bd.get(coluna, "id_professor")

            registros = professor.listar_professor(self.conn, coluna_sql, ordem_sql)
            # registros esperado: (id_professor, nome, "Disciplina1 (Turma1), Disciplina2 (Turma2), ...")

            if not registros:
                self.mostrar_mensagem("Nenhum professor encontrado.")
                return

            texto = f"{'ID':<5} | {'Nome':<30} |\n"
            texto += "-" * 80 + "\n"

            for p in registros:
                disciplinas_turmas = p[2] if p[2] else "Nenhuma"
                lista = disciplinas_turmas.split(", ")

                texto += f"{p[0]:<5} | {p[1]:<30} | Ministra:\n"  # linha do professor (sem disciplinas)
                for item in lista:
                    # Apenas na coluna das disciplinas, então alinhamento só pra disciplina (coluna 38 em diante)
                    texto += f"{'':<38} | - {item}\n"

                texto += "-" * 80 + "\n"

            self.mostrar_mensagem(texto)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar professores: {e}")


    def inserir_professor(self):
        nome = self.pedir_texto("Digite o nome do professor:")
        if not nome:
            return

        try:
            professor.inserir_professor(self.conn, nome)
            messagebox.showinfo("Sucesso", "Professor inserido com sucesso!")
            self.listar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir professor: {e}")

    def buscar_professor(self):
        id_professor = self.pedir_texto("Digite o ID do professor:")
        if not id_professor:
            return
        try:
            resultado = professor.buscar_professor_por_id(self.conn, id_professor)
            if resultado:
                texto = f"ID: {resultado[0]} | Nome: {resultado[1]} |"
                self.mostrar_mensagem(texto)
            else:
                self.mostrar_mensagem("Professor não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar professor: {e}")

    def atualizar_professor(self):
        id_professor = self.pedir_texto("Digite o ID do professor a ser atualizado:")
        if not id_professor:
            return
        try:
            professor_atual = professor.buscar_professor_por_id(self.conn, id_professor)
            if not professor_atual:
                messagebox.showinfo("Aviso", "Professor não encontrado.")
                return
            nome_atual = professor_atual[1]
            novo_nome = self.pedir_texto(f"Nome atual: {nome_atual}\nDigite o novo nome:")
            if not novo_nome:
                return
            professor.atualizar_professor(self.conn, id_professor, novo_nome)
            messagebox.showinfo("Sucesso", "Professor atualizado com sucesso!")
            self.listar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar professor: {e}")

    def deletar_professor(self):
        id_professor = self.pedir_texto("Digite o ID do professor a ser deletado:")
        if not id_professor:
            return
        try:
            professor_existe = professor.buscar_professor_por_id(self.conn, id_professor)
            if not professor_existe:
                messagebox.showinfo("Aviso", "Professor não encontrado.")
                return
            confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja deletar o professor {professor_existe[1]}?")
            if confirm:
                professor.deletar_professorID(self.conn, id_professor)
                messagebox.showinfo("Sucesso", "Professor deletado com sucesso!")
                self.listar()
            else:
                messagebox.showinfo("Cancelado", "Operação cancelada.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar professor: {e}")

    