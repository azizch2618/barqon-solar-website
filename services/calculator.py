from decimal import Decimal

def calculate_solar_system(monthly_bill):
    """
    Intelligent Solar Calculation Engine
    Rules:
    1. Units = monthly_bill / 50 (PKR tariff)
    2. System Size (kW) = units / 120
    3. Monthly Generation = system_size * 130
    4. Monthly Savings = monthly_bill * 0.7
    5. Annual Savings = monthly_savings * 12
    6. ROI (Payback) = total_cost / annual_savings
    7. Panel Count = (system_size * 1000) / 550
    """
    
    # Constants
    TARIFF = 50
    UNITS_PER_KW = 120
    AVG_GENERATION_FACTOR = 130
    SAVINGS_FACTOR = 0.7
    COST_PER_KW = 180000 # Estimated PKR per kW for a premium system
    PANEL_WATTAGE = 550
    
    # Calculation
    monthly_bill = float(monthly_bill)
    
    units = monthly_bill / TARIFF
    system_size = units / UNITS_PER_KW
    
    # Clamp system size to common values if needed, but keeping it dynamic as requested
    if system_size < 3: system_size = 3.0 # Minimum 3kW
    
    generation = system_size * AVG_GENERATION_FACTOR
    monthly_savings = monthly_bill * SAVINGS_FACTOR
    annual_savings = monthly_savings * 12
    
    total_cost = system_size * COST_PER_KW
    payback = total_cost / annual_savings if annual_savings > 0 else 0
    
    panel_count = int((system_size * 1000) / PANEL_WATTAGE)
    if (system_size * 1000) % PANEL_WATTAGE > 0:
        panel_count += 1
        
    # Battery Suggestion
    battery_suggestion = "No Battery (On-Grid)"
    if system_size <= 5:
        battery_suggestion = "2x 200Ah Lead Acid or 1x 5kWh Lithium"
    elif system_size <= 10:
        battery_suggestion = "4x 200Ah Lead Acid or 2x 5kWh Lithium"
    else:
        battery_suggestion = "Custom Industrial Battery Bank"

    return {
        "system_size_kw": round(system_size, 2),
        "monthly_units": int(units),
        "monthly_generation": int(generation),
        "monthly_savings": round(monthly_savings, 2),
        "annual_savings": round(annual_savings, 2),
        "payback_years": round(payback, 2),
        "total_cost": round(total_cost, 2),
        "panel_count": panel_count,
        "battery_suggestion": battery_suggestion
    }
