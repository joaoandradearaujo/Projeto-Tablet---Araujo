import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk, UnidentifiedImageError, ImageDraw

# Função para desenhar uma imagem com bordas arredondadas
def criar_imagem_com_bordas_arredondadas(imagem, raio):
    largura, altura = imagem.size
    imagem_com_bordas_arredondadas = Image.new("RGBA", (largura, altura), (255, 255, 255, 0))
    mask = Image.new("L", (largura, altura), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (largura, altura)], raio, fill=255)
    imagem_com_bordas_arredondadas.paste(imagem, (0, 0), mask)
    return imagem_com_bordas_arredondadas

# Função para carregar a imagem
def carregar_imagem():
    caminho_imagem = filedialog.askopenfilename(filetypes=[("Imagem", "*.png;*.jpg;*.jpeg;*.bmp")])
    if caminho_imagem:
        try:
            imagem = Image.open(caminho_imagem)
            largura_maxima = 500  # Ajuste o valor para o tamanho desejado
            altura_maxima = 400   # Ajuste o valor para o tamanho desejado
            imagem.thumbnail((largura_maxima, altura_maxima), Image.LANCZOS)  # Ajusta a imagem para caber na caixa de visualização
            imagem = criar_imagem_com_bordas_arredondadas(imagem, raio=20)
            imagem_tk = ImageTk.PhotoImage(imagem)
            rotulo_imagem.config(image=imagem_tk)
            rotulo_imagem.image = imagem_tk  # Manter referência da imagem
        except UnidentifiedImageError:
            messagebox.showerror("Erro", "O arquivo selecionado não é uma imagem válida.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao carregar a imagem: {e}")

# Função para criar uma nova janela com base no botão clicado
def abrir_pagina(tela):
    nova_janela = tk.Toplevel(root)
    nova_janela.title(f"Página {tela}")
    nova_janela.geometry("400x300")  # Tamanho da nova janela

    mensagem = tk.Label(nova_janela, text=f"Você está na página {tela}", font=("Helvetica", 16, "bold"))
    mensagem.pack(pady=20)

    fechar_botao = tk.Button(nova_janela, text="Fechar", command=nova_janela.destroy, bg="#D3D3D3", fg="black")
    fechar_botao.pack(pady=10)

    # Frame para o botão "OK" na nova janela
    frame_botao_ok = tk.Frame(nova_janela, bg="#3D3D3D")
    botao_ok = tk.Button(frame_botao_ok, text="OK", command=acao_botao_ok, bg="#D3D3D3", fg="black")
    botao_ok.pack(pady=5)
    frame_botao_ok.pack(pady=10)  # Exibe o frame com o botão "OK"

# Função do botão "OK"
def acao_botao_ok():
    messagebox.showinfo("Informação", "Botão OK clicado!")
 
# Função para iniciar o bloqueio do botão
def iniciar_bloqueio(label):
    if not botoes[label]['bloqueado']:
        botoes[label]['bloqueado'] = True
        botoes[label]['botao'].config(state=tk.DISABLED, style="Disabled.TButton")
        botoes[label]['botao'].unbind("<Button-1>")  # Remove o evento de clique
        botoes[label]['botao'].config(text=f"{label} (Bloqueado)")

# Função chamada após clicar e segurar
def iniciar_temporizador(label):
    global temporizador
    temporizador = root.after(1000, lambda: iniciar_bloqueio(label))  # 1000 ms = 1 segundo

# Função chamada quando o clique é liberado
def parar_temporizador(event):
    if 'temporizador' in globals():
        root.after_cancel(temporizador)  # Cancela o temporizador

# Função para tratar o clique no botão
def tratar_clique(label):
    if not botoes[label]['bloqueado']:
        abrir_pagina(label)

# Criação da janela principal
root = tk.Tk()
root.title("Aplicação Formal com Imagens")

# Configuração da tela principal
root.geometry("900x600")
root.configure(bg="#2E2E2E")

# Estilo para botões com bordas arredondadas
style = ttk.Style()
style.configure("Rounded.TButton", borderwidth=1, relief="flat", padding=10)
style.map("Rounded.TButton",
          background=[("active", "#D3D3D3")],
          foreground=[("active", "black")])

style.configure("Disabled.TButton", background="#6c6c6c", foreground="white")

# Seção Esquerda
frame_esquerdo = tk.Frame(root, bg="#4F4F4F", padx=10, pady=10)
frame_esquerdo.grid(row=0, column=0, sticky="nsew")

botao_selecionar_imagem = ttk.Button(frame_esquerdo, text="Selecionar Imagem", style="Rounded.TButton",
                                     command=carregar_imagem)
botao_selecionar_imagem.grid(row=0, column=0, padx=10, pady=10)

# Ajuste o Label para acomodar a imagem
rotulo_imagem = tk.Label(frame_esquerdo, bg="#4F4F4F", borderwidth=2, relief="solid")
rotulo_imagem.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Seção Direita
frame_direito = tk.Frame(root, bg="#3D3D3D", padx=10, pady=10)
frame_direito.grid(row=0, column=1, sticky="nsew")

# Título na seção direita
titulo = tk.Label(frame_direito, text="LOCAIS", font=("Helvetica", 18, "bold"), bg="#3D3D3D", fg="#D3D3D3")
titulo.grid(row=0, column=0, columnspan=4, pady=10)

# Adicionar botões na seção direita
botao_labels = [
    ["A1", "A2", "A3", "A4"],
    ["B1", "B2", "B3", "B4"],
    ["C1", "C2", "C3", "C4"],
    ["D1", "D2", "D3", "D4"]
]

botoes = {}
for i, linha in enumerate(botao_labels):
    for j, label in enumerate(linha):
        botao = ttk.Button(frame_direito, text=label, style="Rounded.TButton",
                          command=lambda l=label: tratar_clique(l))
        botao.grid(row=i+1, column=j, padx=5, pady=5)
        botao.bind("<ButtonPress-1>", lambda event, l=label: iniciar_temporizador(l))
        botao.bind("<ButtonRelease-1>", parar_temporizador)
        botoes[label] = {'botao': botao, 'bloqueado': False}

# Campo de Observações
rotulo_observacoes = tk.Label(frame_direito, text="Observações:", font=("Helvetica", 12), bg="#3D3D3D", fg="#D3D3D3")
rotulo_observacoes.grid(row=6, column=0, columnspan=4, pady=10, sticky="w")

campo_observacoes = tk.Text(frame_direito, height=10, width=40, bg="#2E2E2E", fg="#D3D3D3", borderwidth=1, relief="solid")
campo_observacoes.grid(row=7, column=0, columnspan=4, padx=10, pady=10)

# Adaptação da tela a diferentes tamanhos e resoluções
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
