import pandas
import time
import tracemalloc

csv_action = pandas.read_csv("Data/ActionList.csv", delimiter=",")
csv_action["profit"] = csv_action["profit"].str.replace("%", "").astype(float)
data1 = pandas.read_csv("Data/dataset1.csv", delimiter=",")
data2 = pandas.read_csv("Data/dataset2.csv", delimiter=",")

class Optimized():
    def __init__(self, data, step):
        self.step = step
        self.data_original = self.clean_data(data)
        self.csv_action = self.data_original.copy()
        self.csv_action['price_int'] = (self.csv_action['price'] * 100).round().astype(int)
        self.actions = list(self.csv_action.itertuples())
        self.stockage = {}

    def clean_data(self, data):
        data_cleaned = data[(data['price'] > 0) & (data['profit'] > 0)].copy()
        print(f"📊 Actions totales : {len(data)}")
        print(f"❌ Actions filtrées : {len(data) - len(data_cleaned)}\n")
        return data_cleaned

    def opti_algo(self, wallet):
        wallet_int = int(wallet * 100)
        nombre_actions = len(self.actions)
        if nombre_actions == 0:
            return 0, []

        if self.step == 1:
            budget_range = range(wallet_int + 1)
        else:
            budget_range = range(0, wallet_int + 1, self.step)

        for budget_level in budget_range:
            self.stockage[(0, budget_level)] = (0, [])

        for index_action in range(1, nombre_actions + 1):
            current_action = self.actions[index_action - 1]
            cost_level = current_action.price_int
            
            profit = round(current_action.price * (current_action.profit / 100) * 100)

            for budget_level in budget_range:
                profit_without, combinaison_without = self.stockage.get(
                    (index_action - 1, budget_level), (0, [])
                )

                if cost_level <= budget_level:
                    budget_left = budget_level - cost_level
                    
                    if self.step == 1:
                        budget_key = budget_left
                    else:
                        budget_key = (budget_left // self.step) * self.step
                    
                    profit_leftover, combinaison_leftover = self.stockage.get(
                        (index_action - 1, budget_key), (0, [])
                    )
                    profit_with = profit + profit_leftover
                    combinaison_with = [current_action.name] + combinaison_leftover
                else:
                    profit_with, combinaison_with = 0, []

                if profit_with > profit_without:
                    self.stockage[(index_action, budget_level)] = (profit_with, combinaison_with)
                else:
                    self.stockage[(index_action, budget_level)] = (profit_without, combinaison_without)

        return self.stockage.get((nombre_actions, wallet_int), (0, []))

    def post_process(self, best_combinaison, wallet):
        if not best_combinaison:
            return best_combinaison
        
        cost_total = sum(a.price for a in self.actions if a.name in best_combinaison)
        
        while cost_total > wallet and best_combinaison:
            actions_in = [a for a in self.actions if a.name in best_combinaison]
            worst = min(actions_in, key=lambda a: (a.price * a.profit / 100) / a.price)
            best_combinaison.remove(worst.name)
            cost_total -= worst.price
        
        actions_not_taken = [a for a in self.actions if a.name not in best_combinaison]
        
        actions_sorted = sorted(
            actions_not_taken,
            key=lambda a: (a.price * a.profit / 100) / a.price,
            reverse=True
        )
        
        for action in actions_sorted:
            if cost_total + action.price <= wallet:
                best_combinaison.append(action.name)
                cost_total += action.price

        final_cost = sum(a.price for a in self.actions if a.name in best_combinaison)
    
        if final_cost > wallet:
            while final_cost > wallet and best_combinaison:
                actions_in = [a for a in self.actions if a.name in best_combinaison]
                worst = min(actions_in, key=lambda a: a.price * a.profit / 100)
                best_combinaison.remove(worst.name)
                final_cost -= worst.price
    
        
        return best_combinaison

    def display_result(self, wallet):
        start_time = time.time()
        profit_total_cent, best_combinaison = self.opti_algo(wallet)
        
        if self.step > 1:
            best_combinaison = self.post_process(best_combinaison, wallet)
        
        end_time = time.time()
        execution_time = end_time - start_time

        if not best_combinaison:
            print("Aucune solution trouvée")
            return [], 0, 0

        cost_total_real = sum(
            action.price
            for action in self.actions
            if action.name in best_combinaison
        )
        
        profit_total_real = sum(
            action.price * (action.profit / 100)
            for action in self.actions
            if action.name in best_combinaison
        )

        print("🎯 Meilleure combinaison :")
        print("\n".join(f"   - {action}" for action in best_combinaison))
        print(f"📋 Nombre d'actions : {len(best_combinaison)}")
        print(f"💰 Bénéfice total : {profit_total_real:.2f}€")
        print(f"💳 Coût total (réel) : {cost_total_real:.2f}€")
        print(f"💵 Budget restant : {wallet - cost_total_real:.2f}€\n")
        print(f"⏱️ Temps d'exécution : {execution_time:.4f} secondes")
        
        return best_combinaison, profit_total_real, cost_total_real

    def memory_calculation(self, wallet):
        tracemalloc.start()
        self.opti_algo(wallet)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"🧠 Consommation actuelle de la mémoire: {current / 10**6:.2f} MB; Pic de consommation: {peak / 10**6:.2f} MB\n")

algo = Optimized(data1, 100)  # Step = 1 -> Optimal results
algo.display_result(500)
algo.memory_calculation(500)