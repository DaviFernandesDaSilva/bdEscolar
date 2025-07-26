# telas/tela_aluno.py
import customtkinter as ctk
from tkinter import messagebox
from core.baseTela import BaseTela
import aluno
import responsavel

class TelaAluno(BaseTela):
    def __init__(self, app):
        super().__init__(app)

    def abrir(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.container, text="Studee - Alunos", font=self.app.minha_fonte).pack(pady=10)

        btn_frame = ctk.CTkFrame(self.container)
        btn_frame.pack(pady=10, fill="x")
        for i in range(5):
            btn_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkButton(btn_frame, text="Listar", command=self.listar).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Inserir", command=self.inserir).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Buscar", command=self.buscar).grid(row=0, column=2, padx=5)
        ctk.CTkButton(btn_frame, text="Atualizar", command=self.atualizar).grid(row=0, column=3, padx=5)
        ctk.CTkButton(btn_frame, text="Deletar", command=self.deletar).grid(row=0, column=4, padx=5)
        #ctk.CTkButton(btn_frame, text="Associar Responsáveis", command=self.abrir_modal_associar_responsaveis).grid(row=0, column=5, padx=5)

        ctk.CTkButton(self.container, text="Voltar", command=self.app.tela_principal).pack(pady=20)

        self.text_area = ctk.CTkTextbox(self.container, width=680, height=280)
        self.text_area.configure(font=("Consolas", 12))
        self.text_area.pack(pady=10)
        filtro_frame = ctk.CTkFrame(self.container)
        filtro_frame.pack(pady=10, fill="x", padx=20)

        ctk.CTkLabel(filtro_frame, text="Ordenar por:").pack(side="left", padx=(0,5))
        opcoes_coluna = ["id_aluno", "nome", "data_nascimento"]
        self.combo_coluna = ctk.CTkComboBox(filtro_frame, values=opcoes_coluna)
        self.combo_coluna.set(opcoes_coluna[0])
        self.combo_coluna.pack(side="left", padx=5)

        ctk.CTkLabel(filtro_frame, text="Ordem:").pack(side="left", padx=(20,5))
        self.combo_ordem = ctk.CTkComboBox(filtro_frame, values=["ASC", "DESC"])
        self.combo_ordem.set("ASC")
        self.combo_ordem.pack(side="left", padx=5)

        btn_aplicar = ctk.CTkButton(filtro_frame, text="Aplicar", command=self.aplicar_ordenacao)
        btn_aplicar.pack(side="left", padx=10)
        self.listar()
        
    def aplicar_ordenacao(self):
        coluna = self.combo_coluna.get()
        ordem = self.combo_ordem.get()
        self.listar(coluna, ordem)

    def listar(self, coluna="id_aluno", ordem="ASC"):
        alunos = aluno.listar_alunos(self.conn, coluna, ordem)
        if not alunos:
            self.mostrar_mensagem("Nenhum aluno encontrado.")
            return

        texto = f"{'ID':<5} | {'Nome':<30} | {'Nascimento':<12} | {'IDs Responsáveis':<15}\n"
        texto += "-" * 72 + "\n"

        for a in alunos:
            nascimento = a[2].strftime("%d/%m/%Y") if a[2] else "N/A"

            responsaveis = responsavel.listar_responsaveis_do_aluno(self.conn, a[0])
            ids_resp = ", ".join(str(r[0]) for r in responsaveis) if responsaveis else ""

            texto += f"{a[0]:<5} | {a[1]:<30} | {nascimento:<12} | {ids_resp:<15}\n"

        self.mostrar_mensagem(texto)



    def inserir(self):
        nome = self.pedir_texto("Digite o nome:")
        if not nome:
            return
        data = self.pedir_data()
        if not data:
            return

        id_aluno = aluno.inserir_aluno(self.conn, nome, data.strftime("%Y-%m-%d"))
        if id_aluno:
            # Chama o modal para associar responsáveis logo após inserir
            self.abrir_modal_associar_responsaveisID(id_aluno)
            # Depois que o modal fechar, mostra a mensagem de sucesso
        else:
            messagebox.showerror("Erro", "Falha ao inserir o aluno.")
        self.listar()

    def buscar(self):
        id_ = self.pedir_texto("Digite o ID:")
        if not id_: return
        resultado = aluno.buscar_aluno_por_id(self.conn, id_)
        if resultado:
            texto = f"ID: {resultado[0]} | Nome: {resultado[1]} | Nascimento: {resultado[2]}"
            self.mostrar_mensagem(texto)
        else:
            self.mostrar_mensagem("Aluno não encontrado.")

    def atualizar(self):
        try:
            alunos = aluno.listar_alunos(self.conn)
            if not alunos:
                messagebox.showinfo("Aviso", "Nenhum aluno encontrado para atualizar.")
                return

            popup = ctk.CTkToplevel(self.container)
            popup.title("Selecione o aluno para atualizar")
            popup.geometry("400x400")
            popup.grab_set()

            ctk.CTkLabel(popup, text="Buscar aluno por nome ou ID:").pack(pady=5)

            search_var = ctk.StringVar()

            entry_busca = ctk.CTkEntry(popup, textvariable=search_var)
            entry_busca.pack(fill="x", padx=10, pady=5)

            lista_frame = ctk.CTkScrollableFrame(popup, height=300)
            lista_frame.pack(fill="both", expand=True, padx=10, pady=5)

            alunos_dict = {f"{a[0]} - {a[1]}": a[0] for a in alunos}

            def atualizar_lista(filtro=""):
                # Limpa a lista
                for widget in lista_frame.winfo_children():
                    widget.destroy()

                filtro = filtro.lower()

                for nome_completo, id_aluno in alunos_dict.items():
                    if filtro in nome_completo.lower():
                        def on_select(id_aluno=id_aluno):
                            aluno_atual = aluno.buscar_aluno_por_id(self.conn, id_aluno)
                            if not aluno_atual:
                                messagebox.showinfo("Aviso", "Aluno não encontrado.")
                                return
                            popup.destroy()
                            self.abrir_modal_edicao_aluno(id_aluno, aluno_atual[1], aluno_atual[2])

                        btn = ctk.CTkButton(lista_frame, text=nome_completo, command=on_select)
                        btn.pack(fill="x", pady=2)

            def on_keyrelease(event):
                atualizar_lista(search_var.get())

            entry_busca.bind("<KeyRelease>", on_keyrelease)

            # Inicializa com todos os alunos
            atualizar_lista()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar aluno: {e}")

    def deletar(self):
        try:
            alunos = aluno.listar_alunos(self.conn)
            if not alunos:
                messagebox.showinfo("Aviso", "Nenhum aluno encontrado para deletar.")
                return

            popup = ctk.CTkToplevel(self.container)
            popup.title("Selecione o aluno para deletar")
            popup.geometry("400x400")
            popup.grab_set()

            ctk.CTkLabel(popup, text="Buscar aluno por nome ou ID:").pack(pady=5)

            search_var = ctk.StringVar()

            entry_busca = ctk.CTkEntry(popup, textvariable=search_var)
            entry_busca.pack(fill="x", padx=10, pady=5)

            lista_frame = ctk.CTkScrollableFrame(popup, height=300)
            lista_frame.pack(fill="both", expand=True, padx=10, pady=5)

            alunos_dict = {f"{a[0]} - {a[1]}": a[0] for a in alunos}

            def atualizar_lista(filtro=""):
                for widget in lista_frame.winfo_children():
                    widget.destroy()

                filtro = filtro.lower()

                for nome_completo, id_aluno in alunos_dict.items():
                    if filtro in nome_completo.lower():
                        def on_select(id_aluno=id_aluno, nome_completo=nome_completo):
                            confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja deletar o aluno {nome_completo}?")
                            if confirm:
                                try:
                                    aluno.deletar_alunoID(self.conn, id_aluno)
                                    messagebox.showinfo("Sucesso", "Aluno deletado com sucesso!")
                                    popup.destroy()
                                    self.listar()
                                except Exception as e:
                                    messagebox.showerror("Erro", f"Erro ao deletar aluno: {e}")

                        btn = ctk.CTkButton(lista_frame, text=nome_completo, command=on_select)
                        btn.pack(fill="x", pady=2)

            def on_keyrelease(event):
                atualizar_lista(search_var.get())

            entry_busca.bind("<KeyRelease>", on_keyrelease)

            atualizar_lista()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar aluno ele pode estar associado a outras entidades: {e}")
            
    def abrir_modal_edicao_aluno(self, id_aluno, nome_atual, nascimento_atual):
        janela = ctk.CTkToplevel(self.container.winfo_toplevel())
        janela.title(f"Editar Aluno - ID {id_aluno}")
        janela.geometry("400x500")
        janela.grab_set()

        # Campo nome
        ctk.CTkLabel(janela, text="Nome:").pack(pady=(10, 0))
        entry_nome = ctk.CTkEntry(janela)
        entry_nome.pack(pady=5, fill="x", padx=10)
        entry_nome.insert(0, nome_atual)

        # Campo nascimento
        ctk.CTkLabel(janela, text="Data de Nascimento (DD/MM/AAAA):").pack(pady=(10, 0))
        entry_nascimento = ctk.CTkEntry(janela)
        entry_nascimento.pack(pady=5, fill="x", padx=10)
        if nascimento_atual:
            entry_nascimento.insert(0, nascimento_atual.strftime("%d/%m/%Y"))

        # Area para selecionar responsáveis
        ctk.CTkLabel(janela, text="Responsáveis:").pack(pady=(15, 0))

        frame_check = ctk.CTkScrollableFrame(janela, height=200)
        frame_check.pack(fill="both", expand=True, padx=10, pady=5)

        # Pega todos responsáveis
        responsaveis = responsavel.listar_responsaveis(self.conn)
        # Pega os responsáveis já associados
        responsaveis_associados = responsavel.listar_responsaveis_do_aluno(self.conn, id_aluno)
        associados_ids = [r[0] for r in responsaveis_associados]

        check_vars = {}

        for r in responsaveis:
            var = ctk.BooleanVar()
            if r[0] in associados_ids:
                var.set(True)
            chk = ctk.CTkCheckBox(frame_check, text=f"{r[1]} (ID: {r[0]})", variable=var)
            chk.pack(anchor="w", pady=2)
            check_vars[r[0]] = var

        def confirmar():
            novo_nome = entry_nome.get().strip()
            nova_data_str = entry_nascimento.get().strip()

            if not novo_nome:
                messagebox.showerror("Erro", "O nome não pode ficar vazio.")
                return

            try:
                dia, mes, ano = map(int, nova_data_str.split('/'))
                from datetime import date
                nova_data = date(ano, mes, dia)
            except Exception:
                messagebox.showerror("Erro", "Data de nascimento inválida. Use o formato DD/MM/AAAA.")
                return

            selecionados = [id_resp for id_resp, var in check_vars.items() if var.get()]

            try:
                aluno.atualizar_aluno(self.conn, id_aluno, novo_nome, nova_data.strftime("%Y-%m-%d"))
                responsavel.associar_aluno_responsavel(self.conn, id_aluno, selecionados)
                messagebox.showinfo("Sucesso", "Aluno e responsáveis atualizados com sucesso!")
                janela.destroy()
                self.listar()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar: {e}")

        ctk.CTkButton(janela, text="Confirmar", command=confirmar).pack(pady=15)

            
    def abrir_modal_associar_responsaveis(self):
        id_aluno = self.pedir_texto("Digite o ID do aluno para associar responsáveis:")
        if not id_aluno:
            return

        aluno_atual = aluno.buscar_aluno_por_id(self.conn, id_aluno)
        if not aluno_atual:
            messagebox.showinfo("Aviso", "Aluno não encontrado.")
            return

        # Criar janela modal
        janela = ctk.CTkToplevel(self.container.winfo_toplevel())
        janela.title(f"Associar Responsáveis ao Aluno: {aluno_atual[1]}")
        janela.geometry("400x400")
        janela.grab_set()  # modal

        # Buscar responsáveis no banco
        responsaveis = responsavel.listar_responsaveis(self.conn)

        # Buscar responsáveis já associados
        responsaveis_associados = responsavel.listar_responsaveis_do_aluno(self.conn, id_aluno)  # cria essa função no módulo aluno!

        # Dicionário para guardar os checkbox
        self.check_vars = {}

        frame_check = ctk.CTkScrollableFrame(janela)
        frame_check.pack(fill="both", expand=True, padx=10, pady=10)

        for r in responsaveis:
            var = ctk.BooleanVar()
            # Marcar se já está associado
            if r[0] in [resp[0] for resp in responsaveis_associados]:
                var.set(True)
            chk = ctk.CTkCheckBox(frame_check, text=f"{r[1]} (CPF: {r[3]})", variable=var)
            chk.pack(anchor="w", pady=2)
            self.check_vars[r[0]] = var

        def confirmar():
            selecionados = [id_resp for id_resp, var in self.check_vars.items() if var.get()]
            try:
                responsavel.associar_aluno_responsavel(self.conn, id_aluno, selecionados)  # cria essa função para atualizar associações
                messagebox.showinfo("Sucesso", "Responsáveis associados com sucesso!")
                janela.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao associar responsáveis: {e}")

        ctk.CTkButton(janela, text="Confirmar", command=confirmar).pack(pady=10)
            
    def abrir_modal_associar_responsaveisID(self, id_aluno):
        responsaveis = responsavel.listar_responsaveis(self.conn)

        janela = ctk.CTkToplevel(self.container.winfo_toplevel())
        janela.title(f"Associar Responsáveis ao Aluno")
        janela.geometry("400x400")
        janela.grab_set()

        self.check_vars = {}

        for r in responsaveis:
            var = ctk.BooleanVar()
            chk = ctk.CTkCheckBox(janela, text=f"{r[1]} (ID: {r[0]})", variable=var)
            chk.pack(anchor="w", pady=2)
            self.check_vars[r[0]] = var

        confirmou = {"valor": False}  # flag mutável

        def confirmar():
            selecionados = [id_resp for id_resp, var in self.check_vars.items() if var.get()]
            try:
                responsavel.associar_aluno_responsavel(self.conn, id_aluno, selecionados)
                confirmou["valor"] = True
                messagebox.showinfo("Sucesso", "Aluno inserido com sucesso!")
                janela.destroy()
                self.listar()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao associar responsáveis: {e}")

        def on_close():
            if not confirmou["valor"]:
                # Se o modal fechar sem confirmação, delete o aluno
                try:
                    aluno.deletar_alunoID(self.conn, id_aluno)
                    messagebox.showinfo("Aviso", "Associação cancelada. Aluno deletado.")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao deletar aluno: {e}")
            janela.destroy()

        janela.protocol("WM_DELETE_WINDOW", on_close)

        ctk.CTkButton(janela, text="Confirmar", command=confirmar).pack(pady=10)
        
