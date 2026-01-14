# CAVALEIRO DO FEUDO - RPG TEXTUAL
# Cole este código no ChatGPT para jogar

class CavaleiroDoFeudo:
    def __init__(self):
        self.nome = ""
        self.vida = 100
        self.vida_max = 100
        self.ataque = 15
        self.defesa = 10
        self.ouro = 50
        self.experiencia = 0
        self.nivel = 1

        # Itens
        self.espada = "Espada de Ferro"
        self.armadura = "Armadura de Couro"
        self.escudo = "Escudo de Madeira"
        self.montaria = False  # Começa sem cavalo

        # Inventário
        self.inventario = {
            "poção_cura": 2,
            "minério_raro": 0,
            "couro_grosso": 0,
            "mapa_traicao": False,
            "chave_castelo": False
        }

        # Progressão das quests
        self.quests = {
            "espada_ferreiro": False,  # Quest 1
            "mapa_traicao": False,     # Quest 2
            "invasao_final": False     # Quest 3
        }

        # Localização atual
        self.local = "Praça do Feudo"

        # Áreas do jogo
        self.mundo = {
            "Praça do Feudo": {
                "descricao": "O coração do seu feudo. Mercadores, camponeses e guardas circulam.",
                "opcoes": ["Taverna", "Ferraria", "Estábulo", "Castelo", "Floresta"],
                "npcs": ["Ferreiro", "Estalajadeiro", "Mercador"]
            },
            "Ferraria": {
                "descricao": "A forja está quente. O ferreiro trabalha em novas lâminas.",
                "opcoes": ["Voltar para Praça"],
                "npcs": ["Ferreiro"]
            },
            "Floresta": {
                "descricao": "Árvores antigas, sons de animais. Cuidado com bandidos!",
                "opcoes": ["Voltar para Praça", "Explorar profundamente", "Minas Abandonadas"],
                "npcs": [],
                "inimigos": ["Lobo", "Bandido"]
            },
            "Taverna": {
                "descricao": "Cheiro de cerveja e comida. Homens conversam em mesas.",
                "opcoes": ["Voltar para Praça", "Conversar com estranho"],
                "npcs": ["Estalajadeiro", "Estranho Misterioso"]
            },
            "Castelo": {
                "descricao": "Sala do trono. Seu senhor feudal discute estratégias.",
                "opcoes": ["Voltar para Praça"],
                "npcs": ["Senhor Feudal"]
            }
        }

    # MECÂNICA DE COMBATE SIMPLES
    def combate(self, inimigo):
        inimigo_vida = inimigo["vida"]
        print(f"\n⚔️ COMBATE CONTRA {inimigo['nome'].upper()}!")
        print(f"Você: {self.vida}/{self.vida_max} HP")
        print(f"Inimigo: {inimigo_vida}/{inimigo['vida_max']} HP")

        defendendo = False
        while self.vida > 0 and inimigo_vida > 0:
            print("\n1. Ataque Forte (Dano alto, chance de errar)")
            print("2. Ataque Fraco (Dano baixo, sempre acerta)")
            print("3. Defender com Escudo (Reduz dano)")
            if self.experiencia >= 30:
                print("4. Golpe Especial (Corte Carregado)")

            escolha = input("\nEscolha sua ação: ")

            # Ação do jogador
            if escolha == "1":
                # Ataque forte
                if self.rolar_dado(20) >= 8:  # 60% de chance
                    dano = self.ataque + self.rolar_dado(10)
                    inimigo_vida -= dano
                    print(f"💥 Você acerta um golpe forte! {dano} de dano!")
                else:
                    print("❌ Seu golpe forte erra o alvo!")

            elif escolha == "2":
                # Ataque fraco
                dano = max(5, self.ataque // 2)
                inimigo_vida -= dano
                print(f"⚔️ Ataque fraco conecta! {dano} de dano.")

            elif escolha == "3":
                # Defender
                defendendo = True
                print("🛡️ Você levanta o escudo! Defesa aumentada.")
                # Vamos reduzir o próximo ataque

            elif escolha == "4" and self.experiencia >= 30:
                # Golpe especial
                dano = self.ataque * 2
                inimigo_vida -= dano
                self.vida -= 5  # Custa vida
                print(f"🔥 GOLPE ESPECIAL! {dano} de dano! (Você perde 5 HP)")

            else:
                print("Ataque cancelado!")
                continue

            # Verifica se inimigo morreu
            if inimigo_vida <= 0:
                print(f"\n🎉 Você derrotou {inimigo['nome']}!")
                recompensa = inimigo.get("recompensa", {"ouro": 10, "xp": 15})
                self.ouro += recompensa["ouro"]
                self.experiencia += recompensa["xp"]
                print(f"Você ganha {recompensa['ouro']} ouro e {recompensa['xp']} XP!")
                self.checar_nivel()
                return True

            # Ataque do inimigo
            if not defendendo:
                dano_inimigo = inimigo["ataque"] - (self.defesa // 2)
                dano_inimigo = max(1, dano_inimigo)
                self.vida -= dano_inimigo
                print(f"{inimigo['nome']} te ataca! {dano_inimigo} de dano.")
            else:
                # Defendeu - dano reduzido
                dano_inimigo = max(1, (inimigo["ataque"] - self.defesa) // 2)
                self.vida -= dano_inimigo
                print(f"🛡️ Seu escudo absorve parte do golpe! {dano_inimigo} de dano.")
                defendendo = False

            print(f"\nSeu HP: {self.vida}/{self.vida_max}")
            print(f"Inimigo HP: {max(0, inimigo_vida)}/{inimigo['vida_max']}")

            if self.vida <= 0:
                print("\n💀 Você foi derrotado...")
                self.vida = self.vida_max // 2  # Respawn com metade da vida
                print(f"Você acorda na taverna com {self.vida} HP")
                return False

        return True

    def rolar_dado(self, lados):
        import random
        return random.randint(1, lados)

    def checar_nivel(self):
        if self.experiencia >= self.nivel * 50:
            self.nivel += 1
            self.vida_max += 20
            self.vida = self.vida_max
            self.ataque += 5
            self.defesa += 3
            print(f"\n✨ VOCÊ SUBIU PARA NÍVEL {self.nivel}!")
            print(f"HP máximo: {self.vida_max}")
            print(f"Ataque: {self.ataque}")
            print(f"Defesa: {self.defesa}")

    # SISTEMA DE QUESTS
    def iniciar_quest_ferreiro(self):
        print("\n🎯 QUEST ACEITA: A ESPADA DO FERREIRO")
        print("O ferreiro precisa de materiais para forjar uma espada melhor:")
        print("1. Encontre 3 Minérios Raros na Floresta")
        print("2. Encontre 5 Couros Grossos (derrote Lobos)")
        print("3. Retorne ao Ferreiro com os itens")
        self.quests["espada_ferreiro"] = True

    def verificar_quest_ferreiro(self):
        if (self.inventario["minério_raro"] >= 3 and
            self.inventario["couro_grosso"] >= 5):

            print("\n⭐ QUEST COMPLETA: A ESPADA DO FERREIRO")
            print("Você entrega os materiais ao ferreiro...")
            print("Ele forja uma ESPADA DE AÇO para você!")

            self.espada = "Espada de Aço"
            self.ataque += 10
            self.ouro += 50
            self.experiencia += 100

            print(f"\n✨ Recompensas:")
            print(f"- Nova arma: {self.espada}")
            print(f"- Ataque aumentado para: {self.ataque}")
            print(f"- +50 ouro")
            print(f"- +100 XP")

            self.inventario["minério_raro"] -= 3
            self.inventario["couro_grosso"] -= 5
            self.quests["espada_ferreiro"] = False
            return True
        return False

    # MÉTODO PRINCIPAL PARA JOGAR
    def jogar(self):
        print("=" * 50)
        print("🏰 CAVALEIRO DO FEUDO - RPG TEXTUAL")
        print("=" * 50)

        self.nome = input("Qual o nome do seu cavaleiro? ")
        print(f"\nBem-vindo, Cavaleiro {self.nome}!")
        print("Você está na Praça do Feudo. O que deseja fazer?")

        while True:
            self.mostrar_status()
            self.mostrar_local()

            acao = input("\n> ").lower()

            # COMANDOS GERAIS
            if acao in ["sair", "quit", "exit"]:
                print("Até a próxima, Cavaleiro!")
                break

            elif acao in ["status", "s", "info"]:
                continue  # Já mostra status

            elif acao in ["inventario", "i", "inv"]:
                self.mostrar_inventario()

            # MOVIMENTAÇÃO
            elif acao in ["norte", "sul", "leste", "oeste", "n", "s", "l", "o"]:
                self.mover(acao)

            elif "ir para" in acao:
                destino = acao.replace("ir para ", "")
                self.ir_para(destino)

            # AÇÕES ESPECÍFICAS POR LOCAL
            elif self.local == "Praça do Feudo":
                self.acoes_praca(acao)

            elif self.local == "Ferraria":
                self.acoes_ferraria(acao)

            elif self.local == "Floresta":
                self.acoes_floresta(acao)

            elif self.local == "Taverna":
                self.acoes_taverna(acao)

            else:
                print("Comando não reconhecido. Tente: norte, sul, inventario, status")

    def mostrar_status(self):
        print(f"\n{'=' * 40}")
        print(f"👤 {self.nome} | ⚔️ Nv. {self.nivel} | XP: {self.experiencia}")
        print(f"❤️  {self.vida}/{self.vida_max} HP | 💰 {self.ouro} ouro")
        print(f"🗡️  {self.espada} | 🛡️ {self.armadura}")
        if self.montaria:
            print("🐎 Montaria: Cavalo de Guerra")
        print(f"📍 Local: {self.local}")
        print(f"{'=' * 40}")

    def mostrar_local(self):
        local_info = self.mundo[self.local]
        print(f"\n{local_info['descricao']}")
        print("\nO que você faz?")

        for i, opcao in enumerate(local_info["opcoes"], 1):
            print(f"{i}. {opcao}")

        if local_info["npcs"]:
            print("\nNPCs aqui:")
            for npc in local_info["npcs"]:
                print(f"- {npc}")

    def acoes_praca(self, acao):
        if acao == "1" or "taverna" in acao:
            print("\nVocê entra na taverna...")
            self.local = "Taverna"

        elif acao == "2" or "ferraria" in acao:
            print("\nVocê vai até a ferraria...")
            self.local = "Ferraria"

            # Inicia quest se ainda não começou
            if not self.quests["espada_ferreiro"] and not self.quests["mapa_traicao"]:
                print("\n🧔 Ferreiro: 'Cavaleiro! Preciso de ajuda!'")
                resposta = input("Aceitar missão do ferreiro? (sim/não): ")
                if resposta.lower() in ["sim", "s"]:
                    self.iniciar_quest_ferreiro()

        elif acao == "3" or "estábulo" in acao:
            if self.ouro >= 100 and not self.montaria:
                print("\n🏇 Você compra um cavalo por 100 ouro!")
                self.montaria = True
                self.ouro -= 100
                print("Agora você pode se mover mais rápido!")
            elif self.montaria:
                print("Você já tem um cavalo!")
            else:
                print("Você precisa de 100 ouro para comprar um cavalo.")

        elif acao == "4" or "castelo" in acao:
            print("\nVocê entra no castelo...")
            self.local = "Castelo"

        elif acao == "5" or "floresta" in acao:
            print("\nVocê segue para a floresta...")
            self.local = "Floresta"

    def acoes_ferraria(self, acao):
        if "voltar" in acao or acao == "1":
            self.local = "Praça do Feudo"

        elif "conversar" in acao or "ferreiro" in acao:
            if self.quests["espada_ferreiro"]:
                if self.verificar_quest_ferreiro():
                    print("\n🧔 Ferreiro: 'Obrigado, cavaleiro! Esta espada servirá bem!'")
                else:
                    print("\n🧔 Ferreiro: 'Ainda precisa dos materiais, cavaleiro!'")
                    print(f"Minério Raro: {self.inventario['minério_raro']}/3")
                    print(f"Couro Grosso: {self.inventario['couro_grosso']}/5")
            else:
                print("\n🧔 Ferreiro: 'Bem-vindo à forja!'")

    def acoes_floresta(self, acao):
        if "voltar" in acao:
            self.local = "Praça do Feudo"

        elif "explorar" in acao:
            print("\nVocê explora a floresta...")

            encontro = self.rolar_dado(6)
            if encontro <= 2:
                # Encontro com lobo
                lobo = {"nome": "Lobo", "vida": 30, "vida_max": 30, "ataque": 8}
                if self.combate(lobo):
                    self.inventario["couro_grosso"] += 1
                    print("Você coleta o couro do lobo.")

            elif encontro == 3:
                # Encontro com bandido
                bandido = {"nome": "Bandido", "vida": 50, "vida_max": 50, "ataque": 12}
                if self.combate(bandido):
                    self.ouro += 25
                    print("Você encontra 25 ouro no corpo do bandido.")

            elif encontro == 4:
                # Encontra minério
                print("💎 Você encontra um minério raro!")
                self.inventario["minério_raro"] += 1

            else:
                print("Você explora, mas não encontra nada de interessante.")

        elif "minas" in acao:
            print("\n⚠️  As minas estão bloqueadas por uma pedra enorme.")
            print("Você precisará de explosivos para entrar.")
            # Para uma versão futura do jogo

    def acoes_taverna(self, acao):
        if "voltar" in acao:
            self.local = "Praça do Feudo"

        elif "conversar" in acao or "estranho" in acao:
            if not self.quests["mapa_traicao"] and self.quests["espada_ferreiro"] == False:
                print("\n👤 Estranho Misterioso: 'Psst... Cavaleiro...'")
                print("'Há um traidor no feudo. Procure nas masmorras do castelo.'")
                resposta = input("Investigar as masmorras? (sim/não): ")
                if resposta.lower() in ["sim", "s"]:
                    print("🎯 NOVA QUEST: O MAPA DA TRAIÇÃO")
                    self.quests["mapa_traicao"] = True
            elif self.quests["mapa_traicao"]:
                print("\n👤 Estranho: 'Já encontrou o mapa?'")

    def mostrar_inventario(self):
        print("\n🎒 INVENTÁRIO:")
        print(f"💰 Ouro: {self.ouro}")
        print(f"🧪 Poções de Cura: {self.inventario['poção_cura']}")

        if self.inventario["minério_raro"] > 0:
            print(f"💎 Minério Raro: {self.inventario['minério_raro']}")

        if self.inventario["couro_grosso"] > 0:
            print(f"🐺 Couro Grosso: {self.inventario['couro_grosso']}")

        if self.inventario["mapa_traicao"]:
            print("🗺️  Mapa da Traição: ✓")

        if self.inventario["chave_castelo"]:
            print("🔑 Chave do Castelo: ✓")

    def ir_para(self, destino):
        destino_normalizado = destino.strip().title()
        local_info = self.mundo[self.local]
        opcoes_normalizadas = [opcao.title() for opcao in local_info["opcoes"]]
        if destino_normalizado in opcoes_normalizadas:
            print(f"\nVocê segue para {destino_normalizado}...")
            self.local = destino_normalizado
            return
        print("Destino inválido para esta área.")

    def mover(self, direcao):
        direcoes = {
            "norte": ["norte", "n"],
            "sul": ["sul", "s"],
            "leste": ["leste", "l"],
            "oeste": ["oeste", "o"]
        }

        print(f"\nVocê segue para o {direcao}...")
        # Lógica de movimento simplificada
        self.local = "Praça do Feudo"  # Sempre retorna à praça por enquanto

# INICIAR O JOGO
if __name__ == "__main__":
    print("Para jogar, copie TODO este código e cole no ChatGPT!")
    print("Em seguida, digite: Vamos jogar Cavaleiro do Feudo")
    CavaleiroDoFeudo().jogar()
