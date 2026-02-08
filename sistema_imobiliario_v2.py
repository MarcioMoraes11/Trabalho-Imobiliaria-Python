import csv
from datetime import datetime

class Imovel:
    def __init__(self, tipo):
        self.tipo = tipo
        self.valor_base = 0.0
        self.adicionais = 0.0
        self.valor_mensal_final = 0.0
        self.valor_contrato = 2000.00 

    def calcular_aluguel(self):
        pass

    def exibir_contrato(self):
        print("\n--- DETALHES DO ORÇAMENTO ---")
        print(f"Tipo do Imóvel: {self.tipo}")
        print(f"Valor Mensal do Aluguel: R$ {self.valor_mensal_final:.2f}")
        
        total_anual = self.valor_mensal_final * 12
        print(f"Custo Total em 1 ano (apenas aluguel): R$ {total_anual:.2f}")
        print("-----------------------------")

        print("\n--- CUSTO ADMINISTRATIVO (CONTRATO) ---")
        print(f"Valor Taxa de Contrato: R$ {self.valor_contrato:.2f}")
        print("Opções de parcelamento da taxa:")
        for i in range(1, 6):
            parcela = self.valor_contrato / i
            print(f"{i}x de R$ {parcela:.2f}")
        print("---------------------------------------")

    def gerar_csv(self):
        nome_arquivo = f"orcamento_{self.tipo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
                escritor = csv.writer(arquivo, delimiter=';')
                
                escritor.writerow(["Referência", "Tipo Imóvel", "Valor"])
                
                total_acumulado = 0
                
                for mes in range(1, 13):
                    escritor.writerow([f"Mês {mes}", self.tipo, f"R$ {self.valor_mensal_final:.2f}"])
                    total_acumulado += self.valor_mensal_final
                
                escritor.writerow([])
                escritor.writerow(["TOTAL ANUAL (12 Meses)", "", f"R$ {total_acumulado:.2f}"])
                
                escritor.writerow(["Taxa Administrativa (Contrato)", "", f"R$ {self.valor_contrato:.2f}"])
            
            print(f"\n[SUCESSO] Arquivo '{nome_arquivo}' gerado com o total anual!")
        except Exception as e:
            print(f"Erro ao gerar CSV: {e}")


class Apartamento(Imovel):
    def __init__(self, quartos, tem_garagem, tem_criancas):
        super().__init__("Apartamento")
        self.quartos = quartos
        self.tem_garagem = tem_garagem
        self.tem_criancas = tem_criancas
        self.valor_base = 700.00

    def calcular_aluguel(self):
        if self.quartos == 2:
            self.valor_base += 200.00
        
        if self.tem_garagem:
            self.adicionais += 300.00
            
        subtotal = self.valor_base + self.adicionais
        
        if not self.tem_criancas:
            desconto = subtotal * 0.05
            print(f"Desconto aplicado (Sem crianças): -R$ {desconto:.2f}")
            subtotal -= desconto
            
        self.valor_mensal_final = subtotal
        return self.valor_mensal_final

class Casa(Imovel):
    def __init__(self, quartos, tem_garagem):
        super().__init__("Casa")
        self.quartos = quartos
        self.tem_garagem = tem_garagem
        self.valor_base = 900.00

    def calcular_aluguel(self):
        if self.quartos == 2:
            self.valor_base += 250.00
            
        if self.tem_garagem:
            self.adicionais += 300.00
            
        self.valor_mensal_final = self.valor_base + self.adicionais
        return self.valor_mensal_final

class Estudio(Imovel):
    def __init__(self, vagas_extras, quer_estacionamento):
        super().__init__("Estúdio")
        self.vagas_extras = vagas_extras
        self.quer_estacionamento = quer_estacionamento
        self.valor_base = 1200.00

    def calcular_aluguel(self):
        custo_estacionamento = 0.0
        custo_extras = 0.0

        if self.quer_estacionamento:
            custo_estacionamento = 250.00
            custo_extras = self.vagas_extras * 60.00
        
        self.adicionais = custo_estacionamento + custo_extras
        self.valor_mensal_final = self.valor_base + self.adicionais
        return self.valor_mensal_final


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
            garagem = input("Deseja garagem? (S/N): ").strip().upper() == 'S'
            criancas = input("Possui crianças? (S/N): ").strip().upper() == 'S'
            
            imovel_selecionado = Apartamento(qts, garagem, criancas)
            
        elif opcao == '2':
            print("\n-- Configuração Casa --")
            qts = int(input("Número de quartos (1 ou 2): "))
            garagem = input("Deseja garagem? (S/N): ").strip().upper() == 'S'
            
            imovel_selecionado = Casa(qts, garagem)
            
        elif opcao == '3':
            print("\n-- Configuração Estúdio --")
            print("O aluguel base é R$ 1200,00.")
            quer_vaga = input("Deseja incluir estacionamento (2 vagas por +R$250)? (S/N): ").strip().upper() == 'S'
            
            extras = 0
            if quer_vaga:
                extras = int(input("Quantas vagas EXTRAS (além das 2)? R$ 60 cada: "))
            
            imovel_selecionado = Estudio(extras, quer_vaga)

        elif opcao == '4':
            print("Saindo do sistema...")
            exit() 
        else:
            print("Opção inválida. Tente novamente.")
            return

      
        if imovel_selecionado:
            imovel_selecionado.calcular_aluguel()
            imovel_selecionado.exibir_contrato()
            
            salvar = input("\nDeseja gerar o arquivo Excel (.csv)? (S/N): ").strip().upper()
            if salvar == 'S':
                imovel_selecionado.gerar_csv()

    except ValueError:
        print("Erro: Você digitou um texto onde deveria ser número. Tente de novo.")

if __name__ == "__main__":
    while True:
        menu()