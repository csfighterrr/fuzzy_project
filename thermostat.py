from fuzzy import FuzzySet, FuzzyInferenceSystem, FuzzyRule, triangular, trapezoidal

def thermostat_demo():
    # Universe of discourse
    temperature_universe = [i for i in range(0, 41)]  # 0-40°C
    power_universe = [i for i in range(-100, 101)]  # -100 (max cooling) to +100 (max heating)
    
    # Define fuzzy sets for temperature
    cold = FuzzySet(trapezoidal(0, 0, 10, 15), temperature_universe)
    cool = FuzzySet(triangular(10, 18, 22), temperature_universe)
    comfortable = FuzzySet(triangular(20, 23, 26), temperature_universe)
    warm = FuzzySet(triangular(24, 30, 35), temperature_universe)
    hot = FuzzySet(trapezoidal(30, 35, 40, 40), temperature_universe)
    
    # Define fuzzy sets for heating/cooling power
    high_cooling = FuzzySet(trapezoidal(-100, -100, -70, -40), power_universe)
    moderate_cooling = FuzzySet(triangular(-60, -30, 0), power_universe)
    no_change = FuzzySet(triangular(-20, 0, 20), power_universe)
    moderate_heating = FuzzySet(triangular(0, 30, 60), power_universe)
    high_heating = FuzzySet(trapezoidal(40, 70, 100, 100), power_universe)
    
    # Create fuzzy inference system
    fis = FuzzyInferenceSystem(temperature_universe, power_universe)
    
    # Define rules
    # IF temperature is cold THEN power is high heating
    fis.add_rule(FuzzyRule(lambda inp: cold.mu(inp['temperature']), high_heating))
    
    # IF temperature is cool THEN power is moderate heating
    fis.add_rule(FuzzyRule(lambda inp: cool.mu(inp['temperature']), moderate_heating))
    
    # IF temperature is comfortable THEN power is no change
    fis.add_rule(FuzzyRule(lambda inp: comfortable.mu(inp['temperature']), no_change))
    
    # IF temperature is warm THEN power is moderate cooling
    fis.add_rule(FuzzyRule(lambda inp: warm.mu(inp['temperature']), moderate_cooling))
    
    # IF temperature is hot THEN power is high cooling
    fis.add_rule(FuzzyRule(lambda inp: hot.mu(inp['temperature']), high_cooling))
    
    # Test with different temperatures
    test_temperatures = [5, 15, 23, 28, 38]
    
    print("Thermostat Fuzzy Control System")
    print("==============================")
    print("Temperature (°C) | Power Output | Action")
    print("----------------|--------------|-----------------")
    
    for temp in test_temperatures:
        inputs = {'temperature': temp}
        aggregated = fis.infer(inputs)
        power = fis.defuzzify(aggregated)
        
        # Determine action based on power value
        action = "No action"
        if power < -60:
            action = "High cooling"
        elif power < -20:
            action = "Moderate cooling"
        elif power < 20:
            action = "No change"
        elif power < 60:
            action = "Moderate heating"
        else:
            action = "High heating"
            
        print(f"{temp:^16} | {power:^12.2f} | {action}")

if __name__ == "__main__":
    thermostat_demo()
