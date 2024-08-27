import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

class EquipmentInspectionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inspeção de Equipamentos")
        self.geometry("800x600")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        self.tab_imagem = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_imagem, text='Seleção de Imagem')

        self.tab_trabalho = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_trabalho, text='Trabalho Realizado')

        self.create_imagem_widgets()
        self.create_trabalho_widgets()

    def create_imagem_widgets(self):
        label_imagem = ttk.Label(self.tab_imagem, text="Selecione uma imagem:", font=('Arial', 12))
        label_imagem.pack(pady=20)

        self.selected_image = tk.StringVar()

        def select_image():
            filename = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
            if filename:
                self.selected_image.set(filename)
                label_preview.config(text=f"Imagem selecionada: {filename}")
                btn_next.config(state=tk.NORMAL)  # Ativar o botão "Próximo" após selecionar a imagem

        btn_select_image = ttk.Button(self.tab_imagem, text="Selecionar Imagem", command=select_image)
        btn_select_image.pack(pady=10)

        label_preview = ttk.Label(self.tab_imagem, text="", font=('Arial', 10))
        label_preview.pack()

        btn_next = ttk.Button(self.tab_imagem, text="Próximo", command=lambda: self.notebook.select(self.tab_trabalho), state=tk.DISABLED)
        btn_next.pack(pady=20)

    def create_trabalho_widgets(self):
        fields_trabalho = [
            "CLIENTE", "TIPO DE EQUIPAMENTO", "Equipamentos/Componentes", "NOME DO INSPETOR"
        ]

        self.fields_entries_trabalho = {}

        for idx, field in enumerate(fields_trabalho):
            label = ttk.Label(self.tab_trabalho, text=field + ": ", font=('Arial', 12))
            label.grid(row=idx, column=0, padx=10, pady=5, sticky=tk.E)

            if field == "CLIENTE":
                options = ["BRK_Q3", "ACELEN_BA", "EQUINOR - WHA"]
                var = tk.StringVar()
                entry = ttk.Combobox(self.tab_trabalho, width=40, textvariable=var, values=options, state='readonly')
                entry.current(0)
                entry.grid(row=idx, column=1, padx=10, pady=5, sticky=tk.W)
                self.fields_entries_trabalho[field] = entry

            elif field == "TIPO DE EQUIPAMENTO":
                options = ["Circuito", "Trocador", "Compressor"]
                var = tk.StringVar()
                entry = ttk.Combobox(self.tab_trabalho, width=40, textvariable=var, values=options, state='readonly')
                entry.current(0)
                entry.grid(row=idx, column=1, padx=10, pady=5, sticky=tk.W)
                self.fields_entries_trabalho[field] = entry

            elif field == "Equipamentos/Componentes":
                options = ["IA-6-H2X", "CASCO", "EIXO DO COMPRESSOR", "O-4-18-13011 (A1A1)", "CASCO", "6-PT-31214_SHT01", "6-PT-31224_SHT05", "4-PT-31225_SHT04"]
                var = tk.StringVar()
                entry = ttk.Combobox(self.tab_trabalho, width=40, textvariable=var, values=options, state='readonly')
                entry.current(0)
                entry.grid(row=idx, column=1, padx=10, pady=5, sticky=tk.W)
                self.fields_entries_trabalho[field] = entry

            elif field == "NOME DO INSPETOR":
                options = [
                    "João 1", "João 2", "João 3", "Bruno 1", "Bruno 2", "Bruno 3", "Jessé"
                ]
                self.clicked = tk.StringVar()
                self.clicked.set(options[0])
                entry = ttk.OptionMenu(self.tab_trabalho, self.clicked, *options)
                entry.grid(row=idx, column=1, padx=10, pady=5, sticky=tk.W)
                self.fields_entries_trabalho[field] = entry

        self.btn_export = ttk.Button(self.tab_trabalho, text="Exportar para CSV", command=self.export_to_csv, state=tk.DISABLED)
        self.btn_export.grid(row=len(fields_trabalho), column=0, columnspan=2, pady=10)

    def export_to_csv(self):
        all_data = {}
        for field, entry in self.fields_entries_trabalho.items():
            if isinstance(entry, (ttk.Combobox, ttk.OptionMenu)):
                value = entry.get()
            all_data[field] = value

        with open('dados_inspecao.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Campo', 'Valor'])

            for field, value in all_data.items():
                writer.writerow([field, value])

        messagebox.showinfo("Exportação Concluída", "Dados exportados para dados_inspecao.csv")

if __name__ == "__main__":
    app = EquipmentInspectionApp()
    app.mainloop()
