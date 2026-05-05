from decimal import Decimal, ROUND_HALF_UP


def quantize(value):
    return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def build_load_summary(data):
    load_profile = {
        "fans": (Decimal("80"), Decimal("0.85")),
        "lights": (Decimal("20"), Decimal("0.95")),
        "ac": (Decimal("1500"), Decimal("0.75")),
        "fridge": (Decimal("300"), Decimal("0.70")),
        "heater": (Decimal("2000"), Decimal("0.45")),
        "iron": (Decimal("1000"), Decimal("0.35")),
        "computers": (Decimal("200"), Decimal("0.85")),
        "motors": (Decimal("750"), Decimal("0.80")),
    }

    total_load = Decimal("0.00")
    diversified_load = Decimal("0.00")
    for field_name, (wattage, diversity) in load_profile.items():
        quantity = Decimal(data.get(field_name, 0))
        total_load += quantity * wattage
        diversified_load += quantity * wattage * diversity

    other_load = Decimal(data["other_load_watts"])
    total_load += other_load
    diversified_load += other_load * Decimal("0.70")

    average_sun_hours = Decimal(data["average_sun_hours"])
    backup_hours = Decimal(data["backup_hours"])
    battery_voltage = Decimal(data["battery_voltage"])

    design_load = diversified_load if diversified_load > Decimal("0.00") else total_load
    solar_kw = (design_load / Decimal("1000")) * Decimal("1.10")
    battery_kwh = (design_load * backup_hours * Decimal("0.70")) / Decimal("1000")
    battery_ah = (battery_kwh * Decimal("1000")) / battery_voltage if battery_voltage else Decimal("0.00")
    inverter_kw = (design_load * Decimal("1.20")) / Decimal("1000")

    return {
        "total_load_watts": quantize(total_load),
        "diversified_load_watts": quantize(diversified_load),
        "solar_required_kw": quantize(solar_kw),
        "battery_required_ah": quantize(battery_ah),
        "battery_required_kwh": quantize(battery_kwh),
        "inverter_required_kw": quantize(inverter_kw),
    }
