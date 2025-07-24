import datetime
import customtkinter as ctk
from tkinter import messagebox, Toplevel
from tkcalendar import DateEntry
from db import conectar
import aluno  # Futuramente professores, disciplinas etc

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

    def tela_principal(self):
        # Limpa container
        for widget in self.container.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.container, text="Menu Principal", font=self.minha_fonte).pack(pady=20)

        ctk.CTkButton(self.container, text="Alunos", command=self.tela_alunos).pack(pady=10, fill="x")
        ctk.CTkButton(self.container, text="Professores", command=self.tela_professores).pack(pady=10, fill="x")
        ctk.CTkButton(self.container, text="Disciplinas", command=self.tela_disciplinas).pack(pady=10, fill="x")
        ctk.CTkButton(self.container, text="Turmas", command=self.tela_turmas).pack(pady=10, fill="x")

    # Exemplo tela alunos
    def tela_alunos(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.container, text="Gestão de Alunos", font=self.minha_fonte).pack(pady=10)

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

    # Aqui você reutiliza as funções do exemplo anterior, ajustando para usar self.text_area
    def mostrar_mensagem(self, texto):
        self.text_area.delete("0.0", "end")
        self.text_area.insert("end", texto)

    def listar_alunos(self):
        try:
            alunos = aluno.listar_alunos(self.conn)
            if not alunos:
                self.mostrar_mensagem("Nenhum aluno encontrado.\n")
            else:
                # Cabeçalho com alinhamento
                texto = f"{'ID':<5} | {'Nome':<30} | {'Nascimento':<12}\n"
                texto += "-" * 52 + "\n"  # linha separadora

                for a in alunos:
                    id_aluno = str(a[0])
                    nome = a[1]
                    nascimento = a[2].strftime("%d/%m/%Y") if a[2] else "N/A"
                    texto += f"{id_aluno:<5} | {nome:<30} | {nascimento:<12}\n"

                self.mostrar_mensagem(texto)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar alunos: {e}")

    def inserir_aluno(self):
        from customtkinter import CTkInputDialog

        nome = CTkInputDialog(text="Digite o nome do aluno:").get_input()
        if not nome:
            return

        # Criar modal para escolher a data
        win = Toplevel(self)
        win.title("Selecionar Data de Nascimento")
        win.geometry("320x200")
        win.configure(bg="#2b2b2b")
        win.grab_set()  # bloqueia a janela principal enquanto modal aberto

        ctk.CTkLabel(win, text="Selecione a data de nascimento:").pack(pady=10)

        hoje = datetime.date.today()
        cal = DateEntry(win, width=12, background='darkblue', foreground='white', borderwidth=2, year=hoje.year, month=hoje.month, day=hoje.day)
        cal.pack(pady=5)

        # Frame para botões lado a lado
        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=15)


        def salvar_data():
            data_selecionada = cal.get_date()  # tipo datetime.date
            data_str = data_selecionada.strftime("%Y-%m-%d")
            try:
                aluno.inserir_aluno(self.conn, nome, data_str)
                messagebox.showinfo("Sucesso", "Aluno inserido com sucesso!")
                self.listar_alunos()
                win.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao inserir aluno: {e}")

        def cancelar():
            win.destroy()

        btn_salvar = ctk.CTkButton(btn_frame, text="Salvar", command=salvar_data)
        btn_salvar.grid(row=0, column=0, padx=10)
        btn_cancelar = ctk.CTkButton(btn_frame, text="Cancelar", command=cancelar)
        btn_cancelar.grid(row=0, column=1, padx=10)

    def buscar_aluno(self):
        from customtkinter import CTkInputDialog
        id_aluno = CTkInputDialog(text="Digite o ID do aluno:").get_input()
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
            nome_atual, data_atual = aluno_atual[1], aluno_atual[2]
            novo_nome = CTkInputDialog(text=f"Nome atual: {nome_atual}\nDigite o novo nome:").get_input()
            if not novo_nome:
                return
            nova_data = CTkInputDialog(text=f"Data atual: {data_atual}\nDigite a nova data (YYYY-MM-DD):").get_input()
            if not nova_data:
                return
            aluno.atualizar_aluno(self.conn, id_aluno, novo_nome, nova_data)
            messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
            self.listar_alunos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar aluno: {e}")

    def deletar_aluno(self):
        from customtkinter import CTkInputDialog
        id_aluno = CTkInputDialog(text="Digite o ID do aluno a ser deletado:").get_input()
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

    # Placeholders para os outros módulos, só mostrando mensagem por enquanto
    def tela_professores(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.container, text="Gestão de Professores (em desenvolvimento)", font=self.minha_fonte).pack(pady=20)
        ctk.CTkButton(self.container, text="Voltar", command=self.tela_principal).pack(pady=10)

    def tela_disciplinas(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.container, text="Gestão de Disciplinas (em desenvolvimento)", font=self.minha_fonte).pack(pady=20)
        ctk.CTkButton(self.container, text="Voltar", command=self.tela_principal).pack(pady=10)

    def tela_turmas(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.container, text="Gestão de Turmas (em desenvolvimento)", font=self.minha_fonte).pack(pady=20)
        ctk.CTkButton(self.container, text="Voltar", command=self.tela_principal).pack(pady=10)

if __name__ == "__main__":
    app = SistemaEscolarApp()
    app.mainloop()
