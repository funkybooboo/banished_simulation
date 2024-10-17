import random
import numpy as np
import matplotlib.pyplot as plt

class Citizen:
    def __init__(self, skills):
        self.skills = skills
        self.health = 100
        self.happiness = 100
        self.role = random.choice(['farmer', 'builder', 'doctor', 'trader'])

class Resource:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

class Building:
    def __init__(self, building_type, capacity):
        self.type = building_type
        self.capacity = capacity
        self.current_population = 0

class Town:
    def __init__(self):
        self.population = []
        self.resources = {}
        self.buildings = []
        self.year = 0
        self.insurance_fund = 0
        self.events = []
        self.history = {"Food": [], "Firewood": [], "Tools": [], "Population": [], "Happiness": []}

    def add_citizen(self, citizen):
        self.population.append(citizen)

    def add_resource(self, resource):
        self.resources[resource.name] = resource

    def add_building(self, building):
        self.buildings.append(building)

    def simulate_year(self):
        food_consumed = len(self.population) * 200
        firewood_consumed = len(self.population) * 50
        self.resources["Food"].quantity -= food_consumed
        self.resources["Firewood"].quantity -= firewood_consumed

        if self.resources["Food"].quantity < 0:
            starving_population = len(self.population) // 2
            self.population = self.population[:-starving_population]

        if self.resources["Food"].quantity < 0 < self.insurance_fund:
            self.insurance_fund -= 100

        self.handle_events()
        self.manage_citizens()
        self.record_history()
        self.year += 1

    def monte_carlo_simulation(self, num_trials):
        results = []
        for _ in range(num_trials):
            self.reset()
            while self.resources["Food"].quantity >= 0 and len(self.population) > 0:
                if self.should_stop():
                    break
                self.simulate_year()
                results.append(self.year)
        return np.mean(results), np.std(results)

    def reset(self):
        self.population = [Citizen({"farming": 5}) for _ in range(10)]
        self.resources = {
            "Food": Resource("Food", 1000),
            "Firewood": Resource("Firewood", 500),
            "Tools": Resource("Tools", 100),
            "Medicine": Resource("Medicine", 50)  # New resource
        }
        self.insurance_fund = 500
        self.year = 0
        self.events = []
        self.history = {"Food": [], "Firewood": [], "Tools": [], "Population": [], "Happiness": []}

    def should_stop(self):
        return self.resources["Food"].quantity < 200

    def handle_events(self):
        if random.random() < 0.1:
            event_type = random.choice(["drought", "plague", "bounty", "trade", "festival"])
            if event_type == "drought":
                self.resources["Food"].quantity -= 300
                self.events.append("Drought occurred, food reduced!")
            elif event_type == "plague":
                if self.population:
                    affected = random.randint(1, len(self.population) // 2)
                    self.population = self.population[:-affected]
                    self.events.append(f"Plague occurred, {affected} citizens lost!")
            elif event_type == "bounty":
                self.resources["Food"].quantity += 500
                self.events.append("Bounty! Food increased!")
            elif event_type == "trade":
                self.resources["Tools"].quantity += 50
                self.events.append("Successful trade! Tools gained.")
            elif event_type == "festival":
                for citizen in self.population:
                    citizen.happiness += 20  # Boost happiness
                self.events.append("Festival! Happiness increased for citizens.")

    def manage_citizens(self):
        if self.resources["Food"].quantity < 200:
            for citizen in self.population:
                citizen.happiness -= 10
                citizen.health -= 5

        # Example to increase happiness if there are hospitals
        for building in self.buildings:
            if building.type == "Hospital":
                for citizen in self.population:
                    citizen.health += 5  # Heal citizens
                    citizen.happiness += 2  # Increase happiness

    def record_history(self):
        self.history["Food"].append(self.resources["Food"].quantity)
        self.history["Firewood"].append(self.resources["Firewood"].quantity)
        self.history["Tools"].append(self.resources["Tools"].quantity)
        self.history["Population"].append(len(self.population))
        self.history["Happiness"].append(np.mean([c.happiness for c in self.population]))  # Track average happiness

class DecisionMaker:
    def __init__(self, epsilon=0.1):
        self.epsilon = epsilon

    def choose_action(self, options):
        if random.random() < self.epsilon:
            return random.choice(options)
        else:
            return max(options, key=lambda x: x['value'])

# Example of usage
town = Town()
town.add_resource(Resource("Food", 1000))
town.add_resource(Resource("Firewood", 500))
town.add_resource(Resource("Tools", 100))
town.add_resource(Resource("Medicine", 50))  # Add initial medicine
decision_maker = DecisionMaker(epsilon=0.1)

# Running a Monte Carlo simulation
mean_years, std_dev = town.monte_carlo_simulation(num_trials=100)
print(f"Mean Years Survived: {mean_years}, Std Dev: {std_dev}")

# Epsilon-Greedy decision-making example
options = [{'action': 'Build Farm', 'value': 10}, {'action': 'Build Hospital', 'value': 8}, {'action': 'Build School', 'value': 5}]
chosen_action = decision_maker.choose_action(options)
print(f"Chosen action: {chosen_action['action']}")

# Visualize the town's resources and happiness over time
plt.figure(figsize=(12, 8))
plt.plot(town.history["Food"], label='Food', color='green')
plt.plot(town.history["Firewood"], label='Firewood', color='brown')
plt.plot(town.history["Tools"], label='Tools', color='blue')
plt.plot(town.history["Population"], label='Population', color='orange')
plt.plot(town.history["Happiness"], label='Average Happiness', color='purple', linestyle='--')
plt.title('Town Resources, Population, and Happiness Over Time')
plt.xlabel('Year')
plt.ylabel('Quantity')
plt.legend()
plt.show()
