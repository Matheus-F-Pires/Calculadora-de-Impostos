import tkinter as tk
from tkinter import messagebox, ttk, filedialog

# Lista para armazenar o histórico de cálculos
historico_calculos = []

# Função para validar entradas
def validar_entrada(valor):
    try:
        valor = float(valor.replace(',', '.'))
        if valor < 0:
            raise ValueError("Valor não pode ser negativo.")
        return valor
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos e positivos.")
        return None

# Função para calcular um imposto individual
def calcular_imposto(base, aliquota):
    return base * (aliquota / 100)

# Função principal para calcular impostos
def calcular_impostos():
    try:
        # Valida e converte as entradas
        valor = validar_entrada(entrada_valor.get())
        aliquota_icms = validar_entrada(entrada_aliquota_icms.get())
        aliquota_pis = validar_entrada(entrada_aliquota_pis.get())
        aliquota_cofins = validar_entrada(entrada_aliquota_cofins.get())
        
        if valor is None:
            return
        
        # Verifica qual imposto deve ser calculado
        imposto_selecionado = imposto_var.get()
        
        if imposto_selecionado == "ICMS":
            if aliquota_icms is None:
                return
            imposto_icms = calcular_imposto(valor, aliquota_icms)
            total_impostos = imposto_icms
            resultado_icms_var.set(f"ICMS: R$ {imposto_icms:.2f} (Base: R$ {valor:.2f})")
            resultado_pis_var.set("PIS: -")
            resultado_cofins_var.set("COFINS: -")
        
        elif imposto_selecionado == "PIS":
            if aliquota_pis is None:
                return
            imposto_pis = calcular_imposto(valor, aliquota_pis)
            total_impostos = imposto_pis
            resultado_icms_var.set("ICMS: -")
            resultado_pis_var.set(f"PIS: R$ {imposto_pis:.2f} (Base: R$ {valor:.2f})")
            resultado_cofins_var.set("COFINS: -")
        
        elif imposto_selecionado == "COFINS":
            if aliquota_cofins is None:
                return
            imposto_cofins = calcular_imposto(valor, aliquota_cofins)
            total_impostos = imposto_cofins
            resultado_icms_var.set("ICMS: -")
            resultado_pis_var.set("PIS: -")
            resultado_cofins_var.set(f"COFINS: R$ {imposto_cofins:.2f} (Base: R$ {valor:.2f})")
        
        else:  # Calcula todos os impostos
            if aliquota_icms is None or aliquota_pis is None or aliquota_cofins is None:
                return
            imposto_icms = calcular_imposto(valor, aliquota_icms)
            imposto_pis = calcular_imposto(valor, aliquota_pis)
            imposto_cofins = calcular_imposto(valor, aliquota_cofins)
            total_impostos = imposto_icms + imposto_pis + imposto_cofins
            resultado_icms_var.set(f"ICMS: R$ {imposto_icms:.2f} (Base: R$ {valor:.2f})")
            resultado_pis_var.set(f"PIS: R$ {imposto_pis:.2f} (Base: R$ {valor:.2f})")
            resultado_cofins_var.set(f"COFINS: R$ {imposto_cofins:.2f} (Base: R$ {valor:.2f})")
        
        # Atualiza o preço final e o total de impostos
        preco_final = valor + total_impostos
        resultado_total_var.set(f"Total dos Impostos: R$ {total_impostos:.2f}")
        resultado_preco_final_var.set(f"Preço Final: R$ {preco_final:.2f}")
        
        # Adiciona o cálculo ao histórico
        historico_calculos.append({
            "Valor": valor,
            "ICMS": imposto_icms if imposto_selecionado in ["ICMS", "Todos"] else 0,
            "PIS": imposto_pis if imposto_selecionado in ["PIS", "Todos"] else 0,
            "COFINS": imposto_cofins if imposto_selecionado in ["COFINS", "Todos"] else 0,
            "Total Impostos": total_impostos,
            "Preço Final": preco_final
        })
        
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para limpar os dados inseridos
def limpar_dados():
    entrada_valor.delete(0, tk.END)
    entrada_aliquota_icms.delete(0, tk.END)
    entrada_aliquota_pis.delete(0, tk.END)
    entrada_aliquota_cofins.delete(0, tk.END)
    resultado_icms_var.set("")
    resultado_pis_var.set("")
    resultado_cofins_var.set("")
    resultado_total_var.set("")
    resultado_preco_final_var.set("")

# Função para exibir o histórico de cálculos
def exibir_historico():
    historico_window = tk.Toplevel(janela)
    historico_window.title("Histórico de Cálculos")
    
    texto_historico = tk.Text(historico_window, wrap=tk.WORD, width=60, height=20)
    texto_historico.pack(padx=10, pady=10)
    
    for calculo in historico_calculos:
        texto_historico.insert(tk.END, f"Valor: R$ {calculo['Valor']:.2f}\n")
        if calculo['ICMS'] != 0:
            texto_historico.insert(tk.END, f"ICMS: R$ {calculo['ICMS']:.2f}\n")
        if calculo['PIS'] != 0:
            texto_historico.insert(tk.END, f"PIS: R$ {calculo['PIS']:.2f}\n")
        if calculo['COFINS'] != 0:
            texto_historico.insert(tk.END, f"COFINS: R$ {calculo['COFINS']:.2f}\n")
        texto_historico.insert(tk.END, f"Total Impostos: R$ {calculo['Total Impostos']:.2f}\n")
        texto_historico.insert(tk.END, f"Preço Final: R$ {calculo['Preço Final']:.2f}\n")
        texto_historico.insert(tk.END, "-" * 50 + "\n")

# Função para exportar o histórico para um arquivo
def exportar_historico():
    if not historico_calculos:
        messagebox.showwarning("Aviso", "Nenhum cálculo no histórico para exportar.")
        return
    
    arquivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt")])
    if arquivo:
        with open(arquivo, "w") as f:
            for calculo in historico_calculos:
                f.write(f"Valor: R$ {calculo['Valor']:.2f}\n")
                if calculo['ICMS'] != 0:
                    f.write(f"ICMS: R$ {calculo['ICMS']:.2f}\n")
                if calculo['PIS'] != 0:
                    f.write(f"PIS: R$ {calculo['PIS']:.2f}\n")
                if calculo['COFINS'] != 0:
                    f.write(f"COFINS: R$ {calculo['COFINS']:.2f}\n")
                f.write(f"Total Impostos: R$ {calculo['Total Impostos']:.2f}\n")
                f.write(f"Preço Final: R$ {calculo['Preço Final']:.2f}\n")
                f.write("-" * 50 + "\n")
        messagebox.showinfo("Sucesso", "Histórico exportado com sucesso!")

# Configuração da janela principal
janela = tk.Tk()
janela.title("Calculadora de Impostos")

# Variável para controlar qual imposto será calculado
imposto_var = tk.StringVar(value="Todos")

# Frame para os botões de rádio
frame_impostos = ttk.LabelFrame(janela, text="Calcular")
frame_impostos.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

ttk.Radiobutton(frame_impostos, text="Todos", variable=imposto_var, value="Todos").grid(row=0, column=0, padx=5, pady=2)
ttk.Radiobutton(frame_impostos, text="Apenas ICMS", variable=imposto_var, value="ICMS").grid(row=0, column=1, padx=5, pady=2)
ttk.Radiobutton(frame_impostos, text="Apenas PIS", variable=imposto_var, value="PIS").grid(row=0, column=2, padx=5, pady=2)
ttk.Radiobutton(frame_impostos, text="Apenas COFINS", variable=imposto_var, value="COFINS").grid(row=0, column=3, padx=5, pady=2)

# Campo para entrada do valor
ttk.Label(janela, text="Valor:").grid(row=1, column=0, padx=10, pady=5)
entrada_valor = ttk.Entry(janela)
entrada_valor.grid(row=1, column=1, padx=10, pady=5)

# Campos para entrada das alíquotas
ttk.Label(janela, text="Alíquota ICMS (%):").grid(row=2, column=0, padx=10, pady=5)
entrada_aliquota_icms = ttk.Entry(janela)
entrada_aliquota_icms.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(janela, text="Alíquota PIS (%):").grid(row=3, column=0, padx=10, pady=5)
entrada_aliquota_pis = ttk.Entry(janela)
entrada_aliquota_pis.grid(row=3, column=1, padx=10, pady=5)

ttk.Label(janela, text="Alíquota COFINS (%):").grid(row=4, column=0, padx=10, pady=5)
entrada_aliquota_cofins = ttk.Entry(janela)
entrada_aliquota_cofins.grid(row=4, column=1, padx=10, pady=5)

# Botão para calcular impostos
ttk.Button(janela, text="Calcular", command=calcular_impostos).grid(row=5, column=0, columnspan=2, pady=10)

# Botão para limpar dados
ttk.Button(janela, text="Limpar Dados", command=limpar_dados).grid(row=5, column=1, columnspan=2, pady=10)

# Labels para mostrar os resultados
resultado_icms_var = tk.StringVar()
resultado_pis_var = tk.StringVar()
resultado_cofins_var = tk.StringVar()
resultado_total_var = tk.StringVar()
resultado_preco_final_var = tk.StringVar()

ttk.Label(janela, textvariable=resultado_icms_var).grid(row=6, column=0, columnspan=2, padx=10, pady=5)
ttk.Label(janela, textvariable=resultado_pis_var).grid(row=7, column=0, columnspan=2, padx=10, pady=5)
ttk.Label(janela, textvariable=resultado_cofins_var).grid(row=8, column=0, columnspan=2, padx=10, pady=5)
ttk.Label(janela, textvariable=resultado_total_var).grid(row=9, column=0, columnspan=2, padx=10, pady=5)
ttk.Label(janela, textvariable=resultado_preco_final_var).grid(row=10, column=0, columnspan=2, padx=10, pady=5)

# Lembrete sobre redução de impostos
lembrete = ttk.Label(janela, text="*Os valores calculados são estimativas. Impostos podem ter reduções dependendo do tipo de produto ou regime tributário.", foreground="red")
lembrete.grid(row=11, column=0, columnspan=2, padx=10, pady=5)

# Botões para histórico e exportação
ttk.Button(janela, text="Ver Histórico", command=exibir_historico).grid(row=12, column=0, pady=10)
ttk.Button(janela, text="Exportar Histórico", command=exportar_historico).grid(row=12, column=1, pady=10)

# Executa a interface gráfica
janela.mainloop()
