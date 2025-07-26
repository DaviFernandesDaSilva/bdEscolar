import customtkinter as ctk
from tkinter import messagebox
from core.baseTela import BaseTela
import matricula  # seu módulo com funções para Matricula
import aluno
import turma
from datetime import datetime

class TelaMatricula(BaseTela):
    def __init__(self, app):
        super().__init__(app)
        self.ordem_ascendente = True  # controle da ordem

    def abrir(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.container, text="Studee - Matrículas", font=self.app.minha_fonte).pack(pady=10)

        btn_frame = ctk.CTkFrame(self.container)
        btn_frame.pack(pady=10, fill="x")
        for i in range(4):
            btn_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkButton(btn_frame, text="Listar", command=self.listar_matriculas).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Inserir", command=self.inserir_matricula).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Deletar", command=self.deletar_matricula).grid(row=0, column=2, padx=5)
        ctk.CTkButton(self.container, text="Voltar", command=self.app.tela_principal).pack(pady=10)
        
        self.text_area = ctk.CTkTextbox(self.container, width=680, height=300)
        self.text_area.configure(font=("Consolas", 12))
        self.text_area.pack(pady=10)

        filtro_frame = ctk.CTkFrame(self.container)
        filtro_frame.pack(pady=10, fill="x", padx=20)

        ctk.CTkLabel(filtro_frame, text="Ordenar por:").pack(side="left", padx=(0, 5))

        self.opcoes_ordenacao = ["ID", "Aluno", "Turma", "Ano", "Data"]
        self.combo_ordenar = ctk.CTkComboBox(filtro_frame, values=self.opcoes_ordenacao)
        self.combo_ordenar.set(self.opcoes_ordenacao[0])  # padrão
        self.combo_ordenar.pack(side="left", padx=5)

        ctk.CTkLabel(filtro_frame, text="Ordem:").pack(side="left", padx=(20, 5))
        self.combo_ordem = ctk.CTkComboBox(filtro_frame, values=["Asc", "Desc"])
        self.combo_ordem.set("Asc")  # padrão
        self.combo_ordem.pack(side="left", padx=5)

        btn_aplicar = ctk.CTkButton(filtro_frame, text="Aplicar", command=self.aplicar_ordenacao)
        btn_aplicar.pack(side="left", padx=10)

        # Lista inicial com ordenação padrão
        self.listar_matriculas()

    def aplicar_ordenacao(self):
        coluna = self.combo_ordenar.get()
        ordem = self.combo_ordem.get()
        asc = ordem == "Asc"
        self.listar_matriculas(coluna_ordenacao=coluna, asc=asc)

    def listar_matriculas(self, coluna_ordenacao="ID", asc=True):
        try:
            colunas_map = {
                "ID": "m.id_matricula",
                "Aluno": "a.nome",
                "Turma": "t.nome",
                "Ano": "t.ano",
                "Data": "m.data_matricula"
            }
            ordem_sql = colunas_map.get(coluna_ordenacao, "m.id_matricula")
            ordem_sql += " ASC" if asc else " DESC"

            query = f"""
                SELECT m.id_matricula, a.nome, t.nome, t.ano, m.data_matricula
                FROM Matricula m
                JOIN Aluno a ON m.id_aluno = a.id_aluno
                JOIN Turma t ON m.id_turma = t.id_turma
                ORDER BY {ordem_sql};
            """

            with self.conn.cursor() as cur:
                cur.execute(query)
                registros = cur.fetchall()

            if not registros:
                self.mostrar_mensagem("Nenhuma matrícula encontrada.")
                return

            texto = f"{'ID':<4} | {'Aluno':<25} | {'Ano':<4} | {'Turma':<15} | {'Data da Matrícula':<12}\n"
            texto += "-" * 75 + "\n"

            for m in registros:
                data_str = m[4].strftime("%d/%m/%Y") if m[4] else "N/A"
                texto += f"{m[0]:<4} | {m[1]:<25} | {m[3]:<4} | {m[2]:<15} | {data_str:<12}\n"

            self.mostrar_mensagem(texto)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar matrículas: {e}")

    def mostrar_mensagem(self, texto):
        self.text_area.configure(state="normal")
        self.text_area.delete("1.0", "end")
        self.text_area.insert("1.0", texto)
        self.text_area.configure(state="disabled")

    def inserir_matricula(self):
        try:
            alunos = aluno.listar_alunos_sem_matricula(self.conn)
            turmas = turma.listar_turmas(self.conn)

            if not alunos or not turmas:
                messagebox.showinfo("Aviso", "Não há alunos ou turmas disponíveis.")
                return

            popup = ctk.CTkToplevel(self.container)
            popup.title("Inserir Matrícula")
            popup.geometry("400x420")
            popup.grab_set()

            alunos_dict = {f"{a[1]} (ID: {a[0]})": a[0] for a in alunos}
            turmas_dict = {f"{t[1]} (ID: {t[0]})": t[0] for t in turmas}

            ctk.CTkLabel(popup, text="Selecione a turma:").pack(pady=(10, 5))
            turma_combo = ctk.CTkComboBox(popup, values=list(turmas_dict.keys()))
            turma_combo.pack(pady=5)

            ctk.CTkLabel(popup, text="Selecione os alunos para matrícula:").pack(pady=(15, 5))
            alunos_frame = ctk.CTkScrollableFrame(popup, width=340, height=200)
            alunos_frame.pack(pady=10)

            checkboxes = []
            for nome, id_aluno in alunos_dict.items():
                var = ctk.BooleanVar()
                cb = ctk.CTkCheckBox(alunos_frame, text=nome, variable=var)
                cb.pack(anchor='w', padx=10)
                checkboxes.append((var, id_aluno))

            def confirmar():
                nome_turma = turma_combo.get()
                if not nome_turma:
                    messagebox.showinfo("Aviso", "Selecione a turma.")
                    return

                id_turma = turmas_dict[nome_turma]
                alunos_selecionados = [id_ for var, id_ in checkboxes if var.get()]

                if not alunos_selecionados:
                    messagebox.showinfo("Aviso", "Selecione pelo menos um aluno.")
                    return

                data_matricula = datetime.now().strftime('%Y-%m-%d')

                from matricula import inserir_matricula_em_lote
                inserir_matricula_em_lote(self.conn, alunos_selecionados, id_turma, data_matricula)

                messagebox.showinfo("Sucesso", "Matrícula(s) inserida(s) com sucesso!")
                popup.destroy()
                self.listar_matriculas()

            ctk.CTkButton(popup, text="Confirmar", command=confirmar).pack(pady=15)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir matrícula: {e}")

    def deletar_matricula(self):
        try:
            registros = matricula.listar_matriculas(self.conn)
            if not registros:
                messagebox.showinfo("Aviso", "Nenhuma matrícula para deletar.")
                return
            
            popup = ctk.CTkToplevel(self.container)
            popup.title("Deletar Matrículas")
            popup.geometry("400x420")
            popup.grab_set()

            ctk.CTkLabel(popup, text="Selecione as matrículas para deletar:").pack(pady=(10, 5))

            scroll_frame = ctk.CTkScrollableFrame(popup, width=380, height=300)
            scroll_frame.pack(pady=10)

            checkboxes = []
            for reg in registros:
                # reg tem (id_matricula, id_aluno, nome_aluno, id_turma, nome_turma, data_matricula, ano)
                data_str = reg[5].strftime("%d/%m/%Y") if reg[5] else "N/A"
                texto = f"ID {reg[0]} | Aluno: {reg[2]} | Turma: {reg[4]} | Data: {data_str}"
                var = ctk.BooleanVar()
                cb = ctk.CTkCheckBox(scroll_frame, text=texto, variable=var)
                cb.pack(anchor="w", padx=10, pady=2)
                checkboxes.append((var, reg[0]))

            def confirmar_delecao():
                ids_selecionados = [id_ for var, id_ in checkboxes if var.get()]
                if not ids_selecionados:
                    messagebox.showinfo("Aviso", "Selecione pelo menos uma matrícula para deletar.")
                    return
                confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja deletar {len(ids_selecionados)} matrícula(s)?")
                if confirm:
                    try:
                        for id_mat in ids_selecionados:
                            matricula.deletar_matricula(self.conn, id_mat)
                        messagebox.showinfo("Sucesso", "Matrícula(s) deletada(s) com sucesso!")
                        popup.destroy()
                        self.listar_matriculas()
                    except Exception as e:
                        messagebox.showerror("Erro", f"Erro ao deletar matrícula(s): {e}")

            ctk.CTkButton(popup, text="Confirmar", command=confirmar_delecao).pack(pady=15)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir tela de deleção: {e}")
