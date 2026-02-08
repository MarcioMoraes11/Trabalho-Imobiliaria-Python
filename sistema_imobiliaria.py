import csv
from datetime import datetime

# Mãe
class Imovel:
    def __init__(self, tipo):
        self.tipo = tipo
        self.valor_base = 0.0
        self.adicionais = 0.0
        self.valor_mensal_final = 0.0
        # Valor fixo do contrato conforme foi requisitado no arquivoo
        self.valor_contrato = 2000.00 

    def calcular_aluguel(self):
        pass

    def exibir_contrato(self):
        print("\n--- DETALHES DO CONTRATO ---")
        print(f"Valor Total do Contrato: R$ {self.valor_contrato:.2f}")
        print("Opções de parcelamento do contrato (até 5x):")
        for i in range(1, 6):
            parcela = self.valor_contrato / i
            print(f"{i}x de R$ {parcela:.2f}")
        print("----------------------------")

    def gerar_csv(self):
        nome_arquivo = f"orcamento_{self.tipo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            
            with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
                escritor = csv.writer(arquivo, delimiter=';')
                
                escritor.writerow(["Mês", "Tipo Imóvel", "Valor Mensal Aluguel"])
                
                for mes in range(1, 13):
                    escritor.writerow([f"Mês {mes}", self.tipo, f"R$ {self.valor_mensal_final:.2f}"])
            
            print(f"\nSucesso! Arquivo '{nome_arquivo}' gerado com as 12 parcelas.")
        except Exception as e:
            print(f"Erro ao gerar CSV: {e}")
# AP
class Apartamento(Imovel):
    def __init__(self, quartos, tem_garagem, tem_criancas):
        super().__init__("Apartamento")
        self.quartos = quartos
        self.tem_garagem = tem_garagem
        self.tem_criancas = tem_criancas
        # Valor padrão: R$ 700,00 / 1 Quarto
        self.valor_base = 700.00

    def calcular_aluguel(self):
        # NSe 2 quartos, acrescenta R$ 200,00
        if self.quartos == 2:
            self.valor_base += 200.00
        
        # Garagem acrescenta R$ 300,00
        if self.tem_garagem:
            self.adicionais += 300.00
            
        subtotal = self.valor_base + self.adicionais
        
        # Desconto de 5% se não tiver filho 
        if not self.tem_criancas:
            desconto = subtotal * 0.05
            print(f"Desconto aplicado (Sem crianças): -R$ {desconto:.2f}")
            subtotal -= desconto
            
        self.valor_mensal_final = subtotal
        return self.valor_mensal_final

# Casa
class Casa(Imovel):
    def __init__(self, quartos, tem_garagem):
        super().__init__("Casa")
        self.quartos = quartos
        self.tem_garagem = tem_garagem
        # Valor padrão: R$ 900,00 / 1 Quarto 
        self.valor_base = 900.00

    def calcular_aluguel(self):
        # Se 2 quartos, acrescenta R$ 250,00 
        if self.quartos == 2:
            self.valor_base += 250.00
            
        # Garagem acrescenta R$ 300,00
        if self.tem_garagem:
            self.adicionais += 300.00
            
        self.valor_mensal_final = self.valor_base + self.adicionais
        return self.valor_mensal_final

# Estudio
class Estudio(Imovel):
    def __init__(self, vagas_extras):
        super().__init__("Estúdio")
        self.vagas_extras = vagas_extras
        
        self.valor_base = 1200.00

    def calcular_aluguel(self):
                
        custo_estacionamento = 250.00 
        
        # Vagas extras custam R$ 60,00
        custo_extras = self.vagas_extras * 60.00
        
        self.adicionais = custo_estacionamento + custo_extras
        self.valor_mensal_final = self.valor_base + self.adicionais
        return self.valor_mensal_final

# MENU 
def menu():
    print("\n=== SISTEMA IMOBILIÁRIA R.M ===")
    print("1. Orçamento Apartamento")
    print("2. Orçamento Casa")
    print("3. Orçamento Estúdio")
    print("4. Sair")
    
    opcao = input("Escolha uma opção: ")
    
    try:
        imovel_selecionado = None
        
        if opcao == '1':
            print("\n-- Configuração Apartamento --")
            qts = int(input("Número de quartos (1 ou 2): "))
            garagem = input("Deseja garagem? (S/N): ").upper() == 'S'
            criancas = input("Possui crianças? (S/N): ").upper() == 'S'
            
            imovel_selecionado = Apartamento(qts, garagem, criancas)
            
        elif opcao == '2':
            print("\n-- Configuração Casa --")
            qts = int(input("Número de quartos (1 ou 2): "))
            garagem = input("Deseja garagem? (S/N): ").upper() == 'S'
            
            imovel_selecionado = Casa(qts, garagem)
            
        elif opcao == '3':
            print("\n-- Configuração Estúdio --")
            print("Nota: O pacote básico de estacionamento inclui 2 vagas por R$ 250,00.")
            quer_vaga = input("Deseja incluir estacionamento? (S/N): ").upper() == 'S'
            
            if quer_vaga:
                extras = int(input("Quantas vagas EXTRAS além das 2 iniciais? (0 se nenhuma): "))
                imovel_selecionado = Estudio(extras)
            else:
                # Se não quer vaga, criamos um estúdio sem custo adicional de vaga
                
                imovel_selecionado = Estudio(0)
                imovel_selecionado.adicionais = -250 
                pass 

        elif opcao == '4':
            print("Saindo...")
            return

        else:
            print("Opção inválida.")
            return

        
        if imovel_selecionado:
            valor = imovel_selecionado.calcular_aluguel()
            print(f"\n>>> ORÇAMENTO FINAL MENSAL: R$ {valor:.2f}")
            
            imovel_selecionado.exibir_contrato()
            
            salvar = input("Deseja salvar o orçamento em CSV? (S/N): ").upper()
            if salvar == 'S':
                imovel_selecionado.gerar_csv()

    except ValueError:
        print("Erro: Digite apenas números válidos.")


if __name__ == "__main__":
    while True:
        menu()