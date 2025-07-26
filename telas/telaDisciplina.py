import customtkinter as ctk
from tkinter import messagebox
from core.baseTela import BaseTela
import disciplina
import professor
import turma  # seu módulo com as funções de DB

class TelaDisciplina(BaseTela):
    def __init__(self, app):
        super().__init__(app)

    def abrir(self):
        # Limpa a tela
        for widget in self.container.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.container, text="Studee - Disciplinas", font=self.app.minha_fonte).pack(pady=10)

        btn_frame = ctk.CTkFrame(self.container)
        btn_frame.pack(pady=10, fill="x")
        for i in range(5):
            btn_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkButton(btn_frame, text="Listar", command=self.listar).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Inserir", command=self.inserir).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Buscar", command=self.buscar).grid(row=0, column=2, padx=5)
        ctk.CTkButton(btn_frame, text="Atualizar", command=self.editar).grid(row=0, column=3, padx=5)
        ctk.CTkButton(btn_frame, text="Deletar", command=self.deletar).grid(row=0, column=4, padx=5)

        ctk.CTkButton(self.container, text="Voltar", command=self.app.tela_principal).pack(pady=20)

        self.text_area = ctk.CTkTextbox(self.container, width=680, height=300)
        self.text_area.configure(font=("Consolas", 12))
        self.text_area.pack(pady=10)
        self.listar()

    def listar(self):
        try:
            registros = disciplina.listar_disciplinas_com_associacoes(self.conn)
            if not registros:
                self.mostrar_mensagem("Nenhuma disciplina encontrada.")
                return

            texto = f"{'ID':<3} | {'Disciplina':<24} | {'Turma':<16} | {'Professor':<25}\n"
            texto += "-" * 75 + "\n"
            for r in registros:
                texto += f"{r[0]:<3} | {r[1]:<24} | {r[2]:<16} | {r[3]:<25}\n"

            self.mostrar_mensagem(texto)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar disciplinas: {e}")
            
    def buscar(self):
        id_disciplina = self.pedir_texto("Digite o ID da disciplina:")
        if not id_disciplina:
            return
        try:
            d = disciplina.buscar_disciplina_por_id(self.conn, id_disciplina)
            if not d:
                self.mostrar_mensagem("Disciplina não encontrada.")
                return
            texto = f"{'ID':<3} | {'Disciplina':<24} | {'Turma':<16} | {'Professor':<25}\n"
            texto += "-" * 75 + "\n"
            texto += f"{d[0]:<3} | {d[1]:<24} | {d[2]:<16} | {d[3]:<25}\n"
            self.mostrar_mensagem(texto)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar disciplina: {e}")

    def inserir(self):
        try:
            turmas = turma.listar_turmas(self.conn)
            professores = professor.listar_professor(self.conn)

            if not turmas or not professores:
                messagebox.showinfo("Aviso", "Não há turmas ou professores disponíveis para associação.")
                return

            popup = ctk.CTkToplevel(self.container)
            popup.title("Inserir Disciplina com Turma e Professor")
            popup.geometry("400x350")
            popup.grab_set()

            # Entrada nome da disciplina
            ctk.CTkLabel(popup, text="Nome da disciplina:").pack(pady=(10, 5))
            entry_nome = ctk.CTkEntry(popup)
            entry_nome.pack(pady=5)

            # Dropdown turma
            turmas_dict = {f"{t[1]} (Ano {t[2]})": t[0] for t in turmas}
            ctk.CTkLabel(popup, text="Selecione a turma:").pack(pady=(10, 5))
            combo_turma = ctk.CTkComboBox(popup, values=list(turmas_dict.keys()))
            combo_turma.pack(pady=5)

            # Dropdown professor
            professores_dict = {p[1]: p[0] for p in professores}
            ctk.CTkLabel(popup, text="Selecione o professor:").pack(pady=(10, 5))
            combo_professor = ctk.CTkComboBox(popup, values=list(professores_dict.keys()))
            combo_professor.pack(pady=5)

            def confirmar():
                nome = entry_nome.get().strip()
                turma_nome = combo_turma.get()
                professor_nome = combo_professor.get()

                if not nome:
                    messagebox.showinfo("Aviso", "Digite o nome da disciplina.")
                    return
                if not turma_nome or not professor_nome:
                    messagebox.showinfo("Aviso", "Selecione turma e professor.")
                    return

                id_turma = turmas_dict[turma_nome]
                id_professor = professores_dict[professor_nome]

                try:
                    # Insere a disciplina e já pega o ID
                    id_disciplina = disciplina.inserir_disciplina(self.conn, nome)

                    # Associa usando o ID retornado
                    disciplina.associar_turma_disciplina_professor(self.conn, id_turma, id_disciplina, id_professor)

                    messagebox.showinfo("Sucesso", "Disciplina inserida e associada com sucesso!")
                    popup.destroy()
                    self.listar()

                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao inserir disciplina: {e}")

            ctk.CTkButton(popup, text="Confirmar", command=confirmar).pack(pady=20)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir modal: {e}")
            
    def editar(self):
        id_disciplina = self.pedir_texto("Digite o ID da disciplina a ser editada:")
        if not id_disciplina:
            return
        try:
            d = disciplina.buscar_disciplina_por_id(self.conn, id_disciplina)
            if not d:
                messagebox.showinfo("Aviso", "Disciplina não encontrada.")
                return
            novo_nome = self.pedir_texto(f"Digite o novo nome para a disciplina {d[1]}:")
            if not novo_nome:
                return
            disciplina.atualizar_disciplina(self.conn, id_disciplina, novo_nome)
            messagebox.showinfo("Sucesso", "Disciplina atualizada com sucesso!")
            self.listar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar disciplina: {e}")

    def deletar(self):
        id_disciplina = self.pedir_texto("Digite o ID da disciplina a ser deletada:")
        if not id_disciplina:
            return
        try:
            d = disciplina.buscar_disciplina_por_id(self.conn, id_disciplina)
            if not d:
                messagebox.showinfo("Aviso", "Disciplina não encontrada.")
                return
            confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja deletar a disciplina {d[1]}?")
            if confirm:
                try:
                    disciplina.deletar_disciplina(self.conn, id_disciplina)
                    messagebox.showinfo("Sucesso", "Disciplina deletada com sucesso!")
                    self.listar()
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao deletar disciplina: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar disciplina: {e}")
            
    def inserir_turma_disciplina_professor(self):
        try:
            turmas = turma.listar_turmas(self.conn)  # [(id_turma, nome_turma, ano), ...]
            disciplinas = disciplina.listar_disciplinas(self.conn)  # [(id_disciplina, nome_disciplina), ...]
            professores = professor.listar_professor(self.conn)  # [(id_professor, nome_professor), ...]

            if not turmas or not disciplinas or not professores:
                messagebox.showinfo("Aviso", "Não há turmas, disciplinas ou professores disponíveis.")
                return

            popup = ctk.CTkToplevel(self.container)
            popup.title("Associar Disciplina à Turma com Professor")
            popup.geometry("400x300")
            popup.grab_set()

            # Mapear nomes para ids
            turmas_dict = {f"{t[1]} (Ano {t[2]})": t[0] for t in turmas}
            disciplinas_dict = {d[1]: d[0] for d in disciplinas}
            professores_dict = {p[1]: p[0] for p in professores}

            ctk.CTkLabel(popup, text="Selecione a Turma:").pack(pady=(10, 5))
            combo_turma = ctk.CTkComboBox(popup, values=list(turmas_dict.keys()))
            combo_turma.pack(pady=5)

            ctk.CTkLabel(popup, text="Selecione a Disciplina:").pack(pady=(10, 5))
            combo_disciplina = ctk.CTkComboBox(popup, values=list(disciplinas_dict.keys()))
            combo_disciplina.pack(pady=5)

            ctk.CTkLabel(popup, text="Selecione o Professor:").pack(pady=(10, 5))
            combo_professor = ctk.CTkComboBox(popup, values=list(professores_dict.keys()))
            combo_professor.pack(pady=5)

            def confirmar():
                turma_nome = combo_turma.get()
                disciplina_nome = combo_disciplina.get()
                professor_nome = combo_professor.get()

                if not turma_nome or not disciplina_nome or not professor_nome:
                    messagebox.showinfo("Aviso", "Selecione todos os campos.")
                    return

                id_turma = turmas_dict[turma_nome]
                id_disciplina = disciplinas_dict[disciplina_nome]
                id_professor = professores_dict[professor_nome]

                try:
                    disciplina.associar_turma_disciplina_professor(self.conn, id_turma, id_disciplina, id_professor)
                    messagebox.showinfo("Sucesso", "Disciplina associada à turma com professor com sucesso!")
                    popup.destroy()
                    self.listar_associacoes()  # função para listar as associações atualizadas
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao associar: {e}")

            ctk.CTkButton(popup, text="Confirmar", command=confirmar).pack(pady=20)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir modal de inserção: {e}")

