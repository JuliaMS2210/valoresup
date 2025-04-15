import tkinter as tk
from tkinter import messagebox
import csv

class CalculadoraPrecos:
    def __init__(self):
        self.produtos = []
        self.root = tk.Tk()
        self.root.title("Calculadora de Precificação")
        self.setup_ui()

    def calcular_precos(self, valor_produto, frete, porcentagem_imposto, origem):
        # Calcula o imposto como porcentagem do valor do produto
        imposto = valor_produto * (porcentagem_imposto / 100)
        valor_total = valor_produto + imposto + frete  # Soma do produto, imposto e frete

        # Cálculos de margem CORRIGIDOS
        valor_88 = valor_total / 0.88  # Divisão por 88% (equivalente a 12% de margem)
        valor_84 = valor_total / 0.84  # Divisão por 84% (equivalente a 16% de margem)

        return valor_88, valor_84, valor_total, imposto

    def adicionar_produto(self, nome_produto, valor_final, prazo_entrega, observacao):
        # Adiciona no início da lista
        self.produtos.insert(0, {
            'nome': nome_produto,
            'valor': valor_final,
            'prazo': prazo_entrega,
            'obs': observacao
        })
        
        # Salva no CSV
        with open('produtos.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([nome_produto, valor_final, prazo_entrega, observacao])

    def setup_ui(self):
        # Frame de entrada
        self.frame_entrada = tk.Frame(self.root)
        self.frame_entrada.pack(padx=20, pady=20)

        # Widgets de entrada
        tk.Label(self.frame_entrada, text="Nome do Produto:").pack()
        self.entry_nome = tk.Entry(self.frame_entrada)
        self.entry_nome.pack()

        tk.Label(self.frame_entrada, text="Valor do Produto (R$):").pack()
        self.entry_valor = tk.Entry(self.frame_entrada)
        self.entry_valor.pack()

        tk.Label(self.frame_entrada, text="Frete (R$):").pack()
        self.entry_frete = tk.Entry(self.frame_entrada)
        self.entry_frete.pack()

        tk.Label(self.frame_entrada, text="Imposto (%):").pack()
        self.entry_imposto = tk.Entry(self.frame_entrada)
        self.entry_imposto.pack()

        self.origem_var = tk.StringVar(value='revendedor')
        tk.Label(self.frame_entrada, text="Origem:").pack()
        tk.Radiobutton(self.frame_entrada, text="Revendedor", variable=self.origem_var, value='revendedor').pack()
        tk.Radiobutton(self.frame_entrada, text="Fábrica", variable=self.origem_var, value='fabrica').pack()

        tk.Button(self.frame_entrada, text="Calcular", command=self.calcular).pack(pady=10)

        # Frame de resultados
        self.frame_resultados = tk.Frame(self.root)
        
        self.label_resultados = tk.Label(self.frame_resultados, text="Resultados:", font=('Arial', 12, 'bold'))
        self.label_resultados.pack()
        
        self.labels = {
            'nome': tk.Label(self.frame_resultados, text="Produto: "),
            'valor_imposto': tk.Label(self.frame_resultados, text="Imposto (R$): "),
            'valor_total': tk.Label(self.frame_resultados, text="Valor Total (c/ imposto + frete): "),
            'margem88': tk.Label(self.frame_resultados, text="Valor ÷ 88% (Margem 12%): "),
            'margem84': tk.Label(self.frame_resultados, text="Valor ÷ 84% (Margem 16%): ")
        }
        for lbl in self.labels.values():
            lbl.pack()

        # Frame de escolha
        self.frame_escolha = tk.Frame(self.root)
        
        tk.Label(self.frame_escolha, text="Escolha o valor final:").pack()
        self.escolha_var = tk.StringVar(value='margem88')
        tk.Radiobutton(self.frame_escolha, text="Usar Valor ÷ 88%", variable=self.escolha_var, value='margem88').pack()
        tk.Radiobutton(self.frame_escolha, text="Usar Valor ÷ 84%", variable=self.escolha_var, value='margem84').pack()

        tk.Label(self.frame_escolha, text="Prazo (ex: '15 dias úteis'):").pack()
        self.entry_prazo = tk.Entry(self.frame_escolha)
        self.entry_prazo.pack()

        tk.Label(self.frame_escolha, text="Observações:").pack()
        self.entry_obs = tk.Entry(self.frame_escolha)
        self.entry_obs.pack()

        tk.Button(self.frame_escolha, text="Adicionar Produto", command=self.salvar_produto).pack(pady=10)
        tk.Button(self.frame_escolha, text="Novo Cálculo", command=self.resetar).pack()

    def calcular(self):
        try:
            nome = self.entry_nome.get()
            valor = float(self.entry_valor.get())
            frete = float(self.entry_frete.get() or 0)
            porcentagem_imposto = float(self.entry_imposto.get() or 0)
            origem = self.origem_var.get()

            self.valor_88, self.valor_84, valor_total, imposto = self.calcular_precos(
                valor, frete, porcentagem_imposto, origem
            )
            self.nome_produto = nome

            # Atualiza labels
            self.labels['nome'].config(text=f"Produto: {nome}")
            self.labels['valor_imposto'].config(text=f"Imposto Calculado: R$ {imposto:.2f}")
            self.labels['valor_total'].config(text=f"Valor Total: R$ {valor_total:.2f}")
            self.labels['margem88'].config(text=f"Valor ÷ 88%: R$ {self.valor_88:.2f}")
            self.labels['margem84'].config(text=f"Valor ÷ 84%: R$ {self.valor_84:.2f}")

            self.frame_entrada.pack_forget()
            self.frame_resultados.pack()
            self.frame_escolha.pack()

        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos! Verifique os números digitados.")

    def salvar_produto(self):
        prazo = self.entry_prazo.get()
        obs = self.entry_obs.get()
        
        if self.escolha_var.get() == 'margem88':
            valor_final = self.valor_88
        else:
            valor_final = self.valor_84

        self.adicionar_produto(self.nome_produto, valor_final, prazo, obs)
        messagebox.showinfo("Sucesso", "Produto adicionado ao topo da lista!")
        self.resetar()

    def resetar(self):
        self.frame_resultados.pack_forget()
        self.frame_escolha.pack_forget()
        self.frame_entrada.pack()
        
        # Limpa campos
        self.entry_nome.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
        self.entry_frete.delete(0, tk.END)
        self.entry_imposto.delete(0, tk.END)
        self.entry_prazo.delete(0, tk.END)
        self.entry_obs.delete(0, tk.END)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CalculadoraPrecos()
    app.run()