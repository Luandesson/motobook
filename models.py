# Criando um programa que ajuda os motoqueiros a monitorar os gastos de gasolina/km
# models.py onde fica as classes coom a lógica do programa

from datetime import datetime
import json

# ------------------- Classe que representa 1 abastecimento -------------------
class Abastecimento:
    def __init__(self, posto, data, litros, valor, km_atual):
        self.posto = posto
        self.data = data                # Data do abastecimento (formato datetime)
        self.litros = litros            # Quantos litros foram abastecidos
        self.valor = valor              # Quanto foi pago
        self.km_atual = km_atual        # Quilometragem no momento do abastecimento

    def media_consumo(self, km_anterior):
        """Calcula quantos KM por litro o motoqueiro fez desde o último abastecimento"""
        if self.litros == 0:
            return 0
        return (self.km_atual - km_anterior) / self.litros
    def to_dict(self):
        """
        Converte o objeto Abastecimento em um dicionário para salvar em JSON.
        Como a data é um tipo especial (datetime), convertemos para string.
        """
        return {
            "posto": self.posto,
            "data": self.data.strftime("%d/%m/%Y"), # converte data para string
            "litros": self.litros,
            "valor": self.valor,
            "km_atual": self.km_atual
        }
    @staticmethod
    def from_dict(dados):
        """ 
        Cria um objeto Abastecimento a partir de um dicionário lido do JSON.
        Precisamos converter a string de data de volta para datetime.
        """
        data = datetime.strptime(dados["data"], "%d/%m/%Y") # Converte string para data
        return Abastecimento(
            posto=dados ["posto"],
            data=data,
            litros=dados["litros"],
            valor=dados["valor"],
            km_atual=dados["km_atual"]
        )
# ------------------- Classe principal da Moto -------------------
class Moto:
    def __init__(self):
        self.abastecimentos = []              # Lista com todos os abastecimentos
        self.km_ultima_troca_oleo = None      # Quilometragem da última troca de óleo

    def adicionar_abastecimento(self, posto, data_str, litros, valor, km_atual):
        """Adiciona um novo abastecimento, calcula o custo e mostra o resumo"""
        try:
            # Converte string para objeto datetime
            data = datetime.strptime(data_str, "%d/%m/%Y")
        except ValueError:
            print("❌ Data inválida. Use o formato dd/mm/aaaa.")
            return

        # Verifica se é o primeiro abastecimento
        if not self.abastecimentos:
            novo = Abastecimento(posto, data, litros, valor, km_atual)
            self.abastecimentos.append(novo)
            print("✅ Primeiro abastecimento registrado com sucesso.")
            return

        # Pega o último abastecimento anterior
        ultimo = self.abastecimentos[-1]

        # Verifica se o KM atual faz sentido
        if km_atual <= ultimo.km_atual:
            print("❌ O KM atual deve ser maior que o último registrado.")
            return

        # Calcula dados do novo abastecimento
        km_rodado = km_atual - ultimo.km_atual
        valor_por_litro = valor / litros
        custo_por_km = valor / km_rodado

        # Registra o novo abastecimento
        novo = Abastecimento(posto, data, litros, valor, km_atual)
        self.abastecimentos.append(novo)

        # Mostra o resumo
        print(f"\n✅ Abastecimento adicionado com sucesso!")
        print(f"🔸 Você abasteceu {litros:.2f} L por R$ {valor:.2f}")
        print(f"🔸 Valor por litro: R$ {valor_por_litro:.2f}")
        print(f"🔸 Distância rodada: {km_rodado} km")
        print(f"🔸 Custo por km: R$ {custo_por_km:.2f}\n")

    def troca_oleo(self):
        """Registra a troca de óleo com o KM do último abastecimento"""
        if not self.abastecimentos:
            print("❌ Nenhum abastecimento registrado ainda.")
            return
        self.km_ultima_troca_oleo = self.abastecimentos[-1].km_atual
        print(f"🛢️ Troca de óleo registrada! Novo KM base: {self.km_ultima_troca_oleo}")

    def relatorio(self):
        """Mostra o relatório de consumo desde a última troca de óleo"""
        if not self.abastecimentos:
            print("❌ Nenhum abastecimento registrado.")
            return
        if self.km_ultima_troca_oleo is None:
            print("❌ Nenhuma troca de óleo registrada.")
            return

        # Filtra abastecimentos depois da troca de óleo
        ab_pos_troca = [a for a in self.abastecimentos if a.km_atual > self.km_ultima_troca_oleo]

        if not ab_pos_troca:
            print("⚠️ Nenhum abastecimento após a última troca de óleo.")
            return

        km_inicial = self.km_ultima_troca_oleo
        km_final = ab_pos_troca[-1].km_atual
        km_total = km_final - km_inicial
        total_litros = sum(a.litros for a in ab_pos_troca)
        total_valor = sum(a.valor for a in ab_pos_troca)

        media_km_por_litro = km_total / total_litros if total_litros else 0
        custo_por_km = total_valor / km_total if km_total else 0

        # Mostra o relatório
        print("\n📊 Resumo desde a última troca de óleo:")
        print(f"🔸 KM rodado: {km_total} km")
        print(f"🔸 Total abastecido: {total_litros:.2f} L")
        print(f"🔸 Valor gasto: R$ {total_valor:.2f}")
        print(f"🔸 Consumo médio: {media_km_por_litro:.2f} km/L")
        print(f"🔸 Custo médio por km: R$ {custo_por_km:.2f}\n")  


    def salvar_em_arquivos(self, nome_arquivo="abastecimentos.json"):
        dados = [a.to_dict() for a in self.abastecimentos]
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        print("💾 Dados salvos com sucesso!")

    def carregar_de_arquivo(self, nome_arquivo="abastecimentos.json"):
        try:
            with open(nome_arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                self.abastecimentos =  [Abastecimento.from_dict(d) for d in dados]
            print(" Dados carregados com sucesso!")
        except FileNotFoundError:
            print(" Nenhum arquivo encontrado, Começando do zero.")
            self.abastecimentos = []

     
    def dashboard_consumo_geral(self):
        """Mostrar um painel com todos os dados dos abastecimentos"""
        if not self.abastecimentos:
            print(" Nenhum abastecimento registrado.")
            return
        ab = self.abastecimentos
        total_litros = sum(a.litros for a in ab)
        total_valor = sum(a.valor for a in ab)
        km_inicial = ab[0].km_atual
        km_final = ab[-1].km_atual
        km_total = km_final - km_inicial
        data_inicial = ab[0].data.strftime("%d/%m/%y")
        data_final = ab[-1].data.strftime("%d/%m/%y")
        media_km_por_litro = km_total / total_litros if total_litros else 0
        custo_por_km = total_valor / km_total if km_total else 0
        media_valor_por_litro = total_valor / total_litros if total_litros else 0

        print("\n📈 === DASHBOARD GERAL DE CONSUMO ===") 
        if self.km_ultima_troca_oleo:
            print(f"🛢️ Última troca de óleo: KM {self.km_ultima_troca_oleo}")
        else:
            print("🛢️ Nenhuma troca de óleo registrada ainda.")

        print(f"📅 Período: {data_inicial} até {data_final}")
        print(f"🔢 Total de abastecimentos: {len(ab)}")
        print(f"📍 KM rodado total: {km_total} km")
        print(f"⛽ Total abastecido: {total_litros:.2f} litros")
        print(f"💰 Total gasto: R$ {total_valor:.2f}")
        print(f"🚀 Consumo médio: {media_km_por_litro:.2f} km/L")
        print(f"📉 Custo por km: R$ {custo_por_km:.2f}")
        print(f"🧮 Valor médio por litro: R$ {media_valor_por_litro:.2f}\n")