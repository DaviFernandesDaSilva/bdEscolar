import datetime
import customtkinter as ctk
from tkinter import messagebox, Toplevel
from tkcalendar import DateEntry
from db import conectar
import aluno
import professor
import disciplina
import turma

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("orange.json")


class SistemaEscolarApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão Escolar")
        self.geometry("700x500")
        self.conn = conectar()
        self.minha_fonte = ctk.CTkFont(family="Montserrat", size=24, weight="bold")

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        self.tela_principal()

    def pedir_texto(self, texto_prompt):
        return ctk.CTkInputDialog(text=texto_prompt).get_input()

    def pedir_id(self, texto_prompt):
        id_str = ctk.CTkInputDialog(text=texto_prompt).get_input()
        if id_str and id_str.isdigit():
            return int(id_str)
        else:
            if id_str is not None:
                messagebox.showerror("Erro", "ID inválido. Digite um número.")
            return None

    def pedir_data(self, titulo="Selecionar Data", prompt="Selecione a data:"):
        data_resultado = {'data': None}

        win = Toplevel(self)
        win.title(titulo)
        win.geometry("320x200")
        win.configure(bg="#2b2b2b")
        win.grab_set()

        ctk.CTkLabel(win, text=prompt).pack(pady=10)

        hoje = datetime.date.today()
        cal = DateEntry(
            win,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            year=hoje.year,
            month=hoje.month,
            day=hoje.day
        )
        cal.pack(pady=5)

        def salvar():
            data_resultado['data'] = cal.get_date()
            win.destroy()

        def cancelar():
            data_resultado['data'] = None
            win.destroy()

        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=15)

        ctk.CTkButton(btn_frame, text="Salvar", command=salvar).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", command=cancelar).grid(row=0, column=1, padx=10)

        win.wait_window()

        return data_resultado['data']

    def tela_principal(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.container, text="Menu Principal", font=self.minha_fonte).pack(pady=20)

        ctk.CTkButton(self.container, text="Alunos", command=self.tela_alunos).pack(pady=10, fill="x")
        ctk.CTkButton(self.container, text="Professores", command=self.tela_professores).pack(pady=10, fill="x")
        ctk.CTkButton(self.container, text="Disciplinas", command=self.tela_disciplinas).pack(pady=10, fill="x")
        ctk.CTkButton(self.container, text="Turmas", command=self.tela_turmas).pack(pady=10, fill="x")

    # Tela Alunos
    def tela_alunos(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.container, text="Studee - Alunos", font=self.minha_fonte).pack(pady=10)

        btn_frame = ctk.CTkFrame(self.container)
        btn_frame.pack(pady=10, fill="x")
        for i in range(5):
            btn_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkButton(btn_frame, text="Listar", command=self.listar_alunos).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Inserir", command=self.inserir_aluno).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Buscar", command=self.buscar_aluno).grid(row=0, column=2, padx=5)
        ctk.CTkButton(btn_frame, text="Atualizar", command=self.atualizar_aluno).grid(row=0, column=3, padx=5)
        ctk.CTkButton(btn_frame, text="Deletar", command=self.deletar_aluno).grid(row=0, column=4, padx=5)

        ctk.CTkButton(self.container, text="Voltar", command=self.tela_principal).pack(pady=20)

        self.text_area = ctk.CTkTextbox(self.container, width=680, height=300)
        self.text_area.configure(font=("Consolas", 12))
        self.text_area.pack(pady=10)

    def mostrar_mensagem(self, texto):
        self.text_area.delete("0.0", "end")
        self.text_area.insert("end", texto)

    def listar_alunos(self):
        try:
            alunos = aluno.listar_alunos(self.conn)
            if not alunos:
                self.mostrar_mensagem("Nenhum aluno encontrado.\n")
            else:
                texto = f"{'ID':<5} | {'Nome':<30} | {'Nascimento':<12}\n"
                texto += "-" * 52 + "\n"

                for a in alunos:
                    id_aluno = str(a[0])
                    nome = a[1]
                    nascimento = a[2].strftime("%d/%m/%Y") if a[2] else "N/A"
                    texto += f"{id_aluno:<5} | {nome:<30} | {nascimento:<12}\n"

                self.mostrar_mensagem(texto)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar alunos: {e}")

    def inserir_aluno(self):
        nome = self.pedir_texto("Digite o nome do aluno:")
        if not nome:
            return

        data_selecionada = self.pedir_data()
        if not data_selecionada:
            return

        data_str = data_selecionada.strftime("%Y-%m-%d")

        try:
            aluno.inserir_aluno(self.conn, nome, data_str)
            messagebox.showinfo("Sucesso", "Aluno inserido com sucesso!")
            self.listar_alunos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir aluno: {e}")

    def buscar_aluno(self):
        id_aluno = self.pedir_texto("Digite o ID do aluno:")
        if not id_aluno:
            return
        try:
            resultado = aluno.buscar_aluno_por_id(self.conn, id_aluno)
            if resultado:
                texto = f"ID: {resultado[0]} | Nome: {resultado[1]} | Nascimento: {resultado[2]}"
                self.mostrar_mensagem(texto)
            else:
                self.mostrar_mensagem("Aluno não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar aluno: {e}")

    def atualizar_aluno(self):
        from customtkinter import CTkInputDialog
        id_aluno = CTkInputDialog(text="Digite o ID do aluno a ser atualizado:").get_input()
        if not id_aluno:
            return
        try:
            aluno_atual = aluno.buscar_aluno_por_id(self.conn, id_aluno)
            if not aluno_atual:
                messagebox.showinfo("Aviso", "Aluno não encontrado.")
                return
            
            # Abre modal de edição passando dados atuais
            self.abrir_modal_edicao_aluno(id_aluno, aluno_atual[1], aluno_atual[2])
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar aluno: {e}")

    def abrir_modal_edicao_aluno(self, id_aluno, nome_atual, data_atual):
        win = Toplevel(self)
        win.title("Editar Aluno")
        win.geometry("350x220")
        win.configure(bg="#2b2b2b")
        win.grab_set()

        ctk.CTkLabel(win, text="Nome:").pack(pady=(15,5))
        input_nome = ctk.CTkEntry(win, width=300)
        input_nome.pack()
        input_nome.insert(0, nome_atual)

        ctk.CTkLabel(win, text="Data de Nascimento:").pack(pady=(15,5))

        # Data atual pode ser None, trata para hoje se for
        if data_atual is None:
            data_atual = datetime.date.today()
        elif isinstance(data_atual, str):
            data_atual = datetime.datetime.strptime(data_atual, "%Y-%m-%d").date()
        elif isinstance(data_atual, datetime.datetime):
            data_atual = data_atual.date()

        cal = DateEntry(win, width=12, background='darkblue', foreground='white', borderwidth=2,
                        year=data_atual.year, month=data_atual.month, day=data_atual.day)
        cal.pack(pady=5)

        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=15)

        def salvar():
            novo_nome = input_nome.get().strip()
            nova_data = cal.get_date()

            if not novo_nome:
                messagebox.showerror("Erro", "Nome não pode ficar vazio.")
                return

            try:
                aluno.atualizar_aluno(self.conn, id_aluno, novo_nome, nova_data.strftime("%Y-%m-%d"))
                messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
                self.listar_alunos()
                win.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar aluno: {e}")

        def cancelar():
            win.destroy()

        ctk.CTkButton(btn_frame, text="Salvar", command=salvar).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", command=cancelar).grid(row=0, column=1, padx=10)

    def deletar_aluno(self):
        id_aluno = self.pedir_texto("Digite o ID do aluno a ser deletado:")
        if not id_aluno:
            return
        try:
            aluno_existe = aluno.buscar_aluno_por_id(self.conn, id_aluno)
            if not aluno_existe:
                messagebox.showinfo("Aviso", "Aluno não encontrado.")
                return
            confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja deletar o aluno {aluno_existe[1]}?")
            if confirm:
                aluno.deletar_alunoID(self.conn, id_aluno)
                messagebox.showinfo("Sucesso", "Aluno deletado com sucesso!")
                self.listar_alunos()
            else:
                messagebox.showinfo("Cancelado", "Operação cancelada.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar aluno: {e}")
    

    def tela_turmas(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.container, text="Gestão de Turmas (em desenvolvimento)", font=self.minha_fonte).pack(pady=20)
        ctk.CTkButton(self.container, text="Voltar", command=self.tela_principal).pack(pady=10)


if __name__ == "__main__":
    app = SistemaEscolarApp()
    app.mainloop()
