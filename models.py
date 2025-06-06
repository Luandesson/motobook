# Criando um programa que ajuda os motoqueiros a monitorar os gastos de gasolina/km
# models.py onde fica as classes coom a lógica do programa

# models.py — onde ficam as classes com a lógica do programa

from datetime import datetime

# ------------------- Classe que representa 1 abastecimento -------------------
class Abastecimento:
    def __init__(self, data, litros, valor, km_atual):
        self.data = data                # Data do abastecimento (formato datetime)
        self.litros = litros            # Quantos litros foram abastecidos
        self.valor = valor              # Quanto foi pago
        self.km_atual = km_atual        # Quilometragem no momento do abastecimento

    def media_consumo(self, km_anterior):
        """Calcula quantos KM por litro o motoqueiro fez desde o último abastecimento"""
        if self.litros == 0:
            return 0
        return (self.km_atual - km_anterior) / self.litros


# ------------------- Classe principal da Moto -------------------
class Moto:
    def __init__(self):
        self.abastecimentos = []              # Lista com todos os abastecimentos
        self.km_ultima_troca_oleo = None      # Quilometragem da última troca de óleo

    def adicionar_abastecimento(self, data_str, litros, valor, km_atual):
        """Adiciona um novo abastecimento, calcula o custo e mostra o resumo"""
        try:
            # Converte string para objeto datetime
            data = datetime.strptime(data_str, "%d/%m/%Y")
        except ValueError:
            print("❌ Data inválida. Use o formato dd/mm/aaaa.")
            return

        # Verifica se é o primeiro abastecimento
        if not self.abastecimentos:
            novo = Abastecimento(data, litros, valor, km_atual)
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
        novo = Abastecimento(data, litros, valor, km_atual)
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
