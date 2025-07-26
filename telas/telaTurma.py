import customtkinter as ctk
from tkinter import messagebox
from core.baseTela import BaseTela
import turma

class TelaTurma(BaseTela):
    def __init__(self, app):
        super().__init__(app)

    def abrir(self):
        for widget in self.container.winfo_children():
            widget.destroy()
            
        ctk.CTkLabel(self.container, text="Studee - Turmas", font=self.app.minha_fonte).pack(pady=10)   
            
        btn_frame = ctk.CTkFrame(self.container)
        btn_frame.pack(pady=10, fill="x")
        for i in range(5):
            btn_frame.grid_columnconfigure(i, weight=1)
            
        ctk.CTkButton(self.container, text="Voltar", command=self.app.tela_principal).pack(pady=10)
        ctk.CTkButton(btn_frame, text="Listar", command=self.listar_turma).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Inserir", command=self.inserir_turma).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Buscar", command=self.buscar_turma).grid(row=0, column=2, padx=5)
        ctk.CTkButton(btn_frame, text="Atualizar", command=self.atualizar_turma).grid(row=0, column=3, padx=5)
        ctk.CTkButton(btn_frame, text="Deletar", command=self.deletar_turma).grid(row=0, column=4, padx=5)
        
        self.text_area = ctk.CTkTextbox(self.container, width=680, height=300)
        self.text_area.configure(font=("Consolas", 12))
        self.text_area.pack(pady=10)
        
        filtro_frame = ctk.CTkFrame(self.container)
        filtro_frame.pack(pady=10, fill="x", padx=20)

        ctk.CTkLabel(filtro_frame, text="Ordenar por:").pack(side="left", padx=(0, 5))

        opcoes_ordenacao = ["ID", "Turno", "Ano"] 
        self.combo_ordenar = ctk.CTkComboBox(filtro_frame, values=opcoes_ordenacao)
        self.combo_ordenar.set(opcoes_ordenacao[0])
        self.combo_ordenar.pack(side="left", padx=5)

        ctk.CTkLabel(filtro_frame, text="Ordem:").pack(side="left", padx=(20, 5))
        self.combo_ordem = ctk.CTkComboBox(filtro_frame, values=["Asc", "Desc"])
        self.combo_ordem.set("Asc")
        self.combo_ordem.pack(side="left", padx=5)

        btn_aplicar = ctk.CTkButton(filtro_frame, text="Aplicar", command=self.aplicar_ordenacao)
        btn_aplicar.pack(side="left", padx=10)
        
        self.listar_turma()
        
    def aplicar_ordenacao(self):
        coluna = self.combo_ordenar.get()
        ordem = self.combo_ordem.get()
        self.listar_turma(coluna, ordem)
        
    def listar_turma(self, coluna="ID", ordem="Asc"):
        try:
            colunas_bd = {
                "ID": "id_turma",
                "Turno": "nome",
                "Ano": "ano"
            }
            ordem_sql = "ASC" if ordem.lower() == "asc" else "DESC"
            coluna_sql = colunas_bd.get(coluna, "id_turma")

            registros = turma.listar_turmas_com_disciplinas(self.conn, coluna_sql, ordem_sql)

            if not registros:
                self.mostrar_mensagem("Nenhuma turma encontrada.")
                return

            texto = f"{'ID':<5} | {'Turno':<14} | {'Ano':<5} | Disciplinas Ofertadas\n"
            texto += "-" * 60 + "\n"

            for t in registros:
                id_turma, nome, ano, disciplinas = t
                texto += f"{id_turma:<5} | {nome:<14} | {ano:<5} |\n"

                if disciplinas:
                    lista = disciplinas.split(", ")
                    for item in lista:
                        texto += f"{'':<5} | {'':<14} | {'':<5} | - {item}\n"
                else:
                    texto += f"{'':<5} | {'':<14} | {'':<5} | - Nenhuma\n"

                texto += "-" * 60 + "\n"

            self.mostrar_mensagem(texto)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar turmas: {e}")
            
    def inserir_turma(self):   
        while True:
            ano = self.pedir_texto("Digite o ano da turma:")
            if ano is None:  # Usuário cancelou
                return
            if ano.isdigit():
                break
            else:
                messagebox.showerror("Erro", "Ano inválido, digite só números.")
                
        nome = self.pedir_texto("Digite o turno da turma:")
        if not nome:
            return

        try:
            turma.inserir_turma(self.conn, nome, ano)
            messagebox.showinfo("Sucesso", "Turma inserida!")
            self.listar_turma()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir turma: {e}")
            
    def buscar_turma(self):
        id_turma = self.pedir_texto("Digite o ID da turma:")
        if not id_turma:
            return
        try:
            t = turma.buscar_turma_por_id(self.conn, id_turma)
            if not t:
                self.mostrar_mensagem("Turma não encontrada.")
                return
            texto = f"ID: {t[0]} |  Ano: {t[1]} | Nome: {t[2]}"
            self.mostrar_mensagem(texto)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar turma: {e}")
            
    def atualizar_turma(self):
        id_turma = self.pedir_texto("Digite o ID da turma a ser atualizada:")
        if not id_turma:
            return
        try:
            turma_atual = turma.buscar_turma_por_id(self.conn, id_turma)
            if not turma_atual:
                messagebox.showinfo("Aviso", "Turma não encontrada.")
                return
            
            # Abre modal de edição passando dados atuais
            self.abrir_modal_edicao_turma(id_turma, turma_atual[1], turma_atual[2])
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar turma: {e}")
        
    def deletar_turma(self):
        id_turma = self.pedir_texto("Digite o ID da turma a ser deletada:")
        if not id_turma:
            return
        try:
            turma_existe = turma.buscar_turma_por_id(self.conn, id_turma)
            if not turma_existe:
                messagebox.showinfo("Aviso", "Turma não encontrada.")
                return
            confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja deletar a turma {turma_existe[1]}?")
            if confirm:
                turma.deletar_turma(self.conn, id_turma)
                messagebox.showinfo("Sucesso", "Turma deletada com sucesso!")
                self.listar_turma()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar turma: {e}")
            
    
        