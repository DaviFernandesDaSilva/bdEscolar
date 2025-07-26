import customtkinter as ctk
from tkinter import messagebox, StringVar
from core.baseTela import BaseTela
import responsavel  # seu módulo com as funções do responsável

class TelaResponsavel(BaseTela):
    def __init__(self, app):
        super().__init__(app)

    def abrir(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.container, text="Studee - Responsáveis", font=self.app.minha_fonte).pack(pady=10)

        btn_frame = ctk.CTkFrame(self.container)
        btn_frame.pack(pady=10, fill="x")
        for i in range(5):
            btn_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkButton(btn_frame, text="Listar", command=self.listar_responsaveis).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Inserir", command=self.inserir_responsavel).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Buscar", command=self.buscar_responsavel).grid(row=0, column=2, padx=5)
        ctk.CTkButton(btn_frame, text="Atualizar", command=self.atualizar_responsavel).grid(row=0, column=3, padx=5)
        ctk.CTkButton(btn_frame, text="Deletar", command=self.deletar_responsavel).grid(row=0, column=4, padx=5)

        ctk.CTkButton(self.container, text="Voltar", command=self.app.tela_principal).pack(pady=20)

        self.text_area = ctk.CTkTextbox(self.container, width=680, height=280)
        self.text_area.configure(font=("Consolas", 12))
        self.text_area.pack(pady=10)
        
        filtro_frame = ctk.CTkFrame(self.container)
        filtro_frame.pack(pady=10, fill="x", padx=20)

        ctk.CTkLabel(filtro_frame, text="Ordenar por:").pack(side="left", padx=(0, 5))

        opcoes_ordenacao = ["ID", "Nome"] 
        self.combo_ordenar = ctk.CTkComboBox(filtro_frame, values=opcoes_ordenacao)
        self.combo_ordenar.set(opcoes_ordenacao[0])
        self.combo_ordenar.pack(side="left", padx=5)

        ctk.CTkLabel(filtro_frame, text="Ordem:").pack(side="left", padx=(20, 5))
        self.combo_ordem = ctk.CTkComboBox(filtro_frame, values=["Asc", "Desc"])
        self.combo_ordem.set("Asc")
        self.combo_ordem.pack(side="left", padx=5)

        btn_aplicar = ctk.CTkButton(filtro_frame, text="Aplicar", command=self.aplicar_ordenacao)
        btn_aplicar.pack(side="left", padx=10)
        
        self.listar_responsaveis()

    def mostrar_mensagem(self, texto):
        self.text_area.delete("0.0", "end")
        self.text_area.insert("end", texto)
        
    def aplicar_ordenacao(self):
        coluna = self.combo_ordenar.get()
        ordem = self.combo_ordem.get()
        self.listar_responsaveis(coluna, ordem)

    def listar_responsaveis(self, coluna="id_responsavel", ordem="ASC"):
        try:
            responsaveis = responsavel.listar_responsaveis(self.conn, coluna, ordem)
            if not responsaveis:
                self.mostrar_mensagem("Nenhum responsável encontrado.\n")
            else:
                texto = f"{'ID':<5} | {'Nome':<30} | {'Telefone':<15} | {'CPF':<14} |\n"
                texto += "-" * 75 + "\n"
                for r in responsaveis:
                    texto += f"{r[0]:<5} | {r[1]:<30} | {r[2]:<15} | {r[3]:<14} |\n"
                self.mostrar_mensagem(texto)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar responsáveis: {e}")
            

    def validar_entrada_cpf(self, texto):
        return texto.isdigit() and len(texto) <= 11 or texto == ""
    
    def validar_entrada_telefone(self, texto):
        return texto.isdigit() and len(texto) <= 10 or texto == ""
    
    def inserir_responsavel(self):
        nome = self.pedir_texto("Digite o nome do responsável:")
        if not nome:
            return

        # Janela modal para telefone e cpf sem máscara
        janela = ctk.CTkToplevel(self.container.winfo_toplevel())
        janela.title("Telefone e CPF")
        janela.geometry("300x250")
        janela.grab_set()  # modal
        
        vcmd = (janela.register(self.validar_entrada_cpf), "%P")
        vtmd = (janela.register(self.validar_entrada_telefone), "%P")

        ctk.CTkLabel(janela, text="Telefone:").pack(pady=(10, 0))
        entry_telefone = ctk.CTkEntry(janela, validate="key", validatecommand=vtmd)
        entry_telefone.pack(pady=5)

        ctk.CTkLabel(janela, text="CPF:").pack(pady=(10, 0))
        entry_cpf = ctk.CTkEntry(janela, validate="key", validatecommand=vcmd)
        entry_cpf.pack(pady=5)

        def confirmar():
            cpf = ''.join(filter(str.isdigit, entry_cpf.get()))
            telefone = ''.join(filter(str.isdigit, entry_telefone.get()))
            if not telefone and not cpf:
                messagebox.showerror("Erro", "Telefone e CPF não podem estar vazios!")
                return
            if not cpf or len(cpf) != 11:
                messagebox.showerror("Erro", "CPF inválido!")
                return
            if not telefone or len(telefone) > 10:
                messagebox.showerror("Erro", "Telefone inválido!")
                return
            try:
                responsavel.inserir_responsavel(self.conn, nome, telefone, cpf)
            except Exception as e:
                erro_msg = str(e).lower()
                if "duplicate" in erro_msg or "unique constraint" in erro_msg or "duplicar" in erro_msg:
                    messagebox.showerror("Erro", "CPF já cadastrado no sistema.")
                else:
                    messagebox.showerror("Erro", f"Erro ao inserir responsável: {e}")
                return 
            else:
                janela.destroy()
                messagebox.showinfo("Sucesso", "Responsável inserido com sucesso!")
                self.listar_responsaveis()

        ctk.CTkButton(janela, text="Confirmar", command=confirmar).pack(pady=10)

    def atualizar_responsavel(self):
        id_resp = self.pedir_texto("Digite o ID do responsável a ser atualizado:")
        if not id_resp:
            return
        try:
            resp_atual = responsavel.buscar_responsavel_por_id(self.conn, id_resp)
            if not resp_atual:
                messagebox.showinfo("Aviso", "Responsável não encontrado.")
                return
            nome_atual = resp_atual[1]
            telefone_atual = resp_atual[2]
            cpf_atual = resp_atual[3]

            novo_nome = self.pedir_texto(f"Nome atual: {nome_atual}\nDigite o novo nome:")
            if not novo_nome:
                return
            novo_telefone = self.pedir_texto(f"Telefone atual: {telefone_atual}\nDigite o novo telefone:")
            if novo_telefone is None:
                novo_telefone = telefone_atual
            novo_cpf = self.pedir_texto(f"CPF atual: {cpf_atual}\nDigite o novo CPF:")
            if not novo_cpf:
                return

            responsavel.atualizar_responsavel(self.conn, id_resp, novo_nome, novo_telefone, novo_cpf)
            messagebox.showinfo("Sucesso", "Responsável atualizado com sucesso!")
            self.listar_responsaveis()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar responsável: {e}")

    def buscar_responsavel(self):
        id_resp = self.pedir_texto("Digite o ID do responsável:")
        if not id_resp:
            return
        try:
            resultado = responsavel.buscar_responsavel_por_id(self.conn, id_resp)
            if resultado:
                texto = f"ID: {resultado[0]} | Nome: {resultado[1]} | Telefone: {resultado[2]} | CPF: {resultado[3]}"
                self.mostrar_mensagem(texto)
            else:
                self.mostrar_mensagem("Responsável não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar responsável: {e}")

    def deletar_responsavel(self):
        id_resp = self.pedir_texto("Digite o ID do responsável a ser deletado:")
        if not id_resp:
            return
        try:
            resp_existe = responsavel.buscar_responsavel_por_id(self.conn, id_resp)
            if not resp_existe:
                messagebox.showinfo("Aviso", "Responsável não encontrado.")
                return
            confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja deletar o responsável {resp_existe[1]}?")
            if confirm:
                responsavel.deletar_responsavel(self.conn, id_resp)
                messagebox.showinfo("Sucesso", "Responsável deletado com sucesso!")
                self.listar_responsaveis()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar responsável: {e}")
