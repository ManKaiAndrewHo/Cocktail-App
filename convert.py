import re
from difflib import get_close_matches

#convert tables
Volume = { #ml as base unit
    "ml": 1.0,
    "cl": 10.0,
    "oz": 29.5735,
    "tsp": 4.92892,
    "tbsp": 14.7868,
    "cup": 236.588,
    "l": 1000.0,
}

Weight = { #g as base unit
    "g": 1.0,
    "kg": 1000.0,
    "oz": 28.3495, #different from volume oz
}

#All recongized units (for typo correction)
All_Known_Units = set(Volume.keys()) | set(Weight.keys())

Skipped_Units = {"dash", "dashes", "pinch", "pinches", "drop", "drops", "slice", "slices", "piece",
                 "pieces", "whole", "cube", "cubes", "sprig", "sprigs", "leaf", "leaves", "twist",
                 "twists", "wedge", "wedges", "ring", "rings", "strip", "strips", "flame", "flames",
                 "rind", "rinds", "zest", "zests"}

def parse_amount(amount_str):
    """
    Parse string like '2 oz' or '1.5 ml', '9', 'Top up', 'rim of glass'.
    Returns (number, unit) or (None, None) if unparsable.
    """
    amount_str = amount_str.strip().lower()
    
    #match number + unit (e.g. "2 oz", "1.5 ml")
    match = re.match(r"^([\d]+(?:[./][\d]+)?)\s*([a-z]*)$", amount_str)
    if not match:
        return None, None
    
    raw_num, unit = match.groups(1), match.group(2).strip()
    
    #something like '1/2'
    if "/" in raw_num:
        parts = raw_num.split("/")
        try:
            number = float(parts[0]) / float(parts[1])
        except (ValueError, ZeroDivisionError):
            return None, None
    else:
        number = float(raw_num)
        
    return number, unit if unit else None #None unit = bare count like '6'

def detect_typo(unit_str):
    """
    If unit is not recongized, check if it looks like a typo of a known unit.
    Return a suggested correction or None if no close match found.
    """
    if not unit_str:
        return None
    matches = get_close_matches(unit_str, All_Known_Units, n=1, cutoff=0.6)
    return matches[0] if matches else None

def convert_unit(number, from_unit, to_unit):
    """
    Converting a number from from_unit to to_unit.
    Both must be from the same family (vol or weight).
    Return converted float or raises ValueError.
    """
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    if from_unit == to_unit:
        return number
        
    #vol convert
    if from_unit in Volume and to_unit in Volume:
        in_ml = number * Volume[from_unit]
        return in_ml / Volume[to_unit]
    
    #weight convert
    if from_unit in Weight and to_unit in Weight:
        in_g = number * Weight[from_unit]
        return in_g / Weight[to_unit]
    
    raise ValueError(f"Cannot convert '{from_unit}' to '{to_unit}' (different unit families.)")

def format_number(n):
    """
    Format a float - no trailing zeros, max 2 dec.
    """
    rounded = round(n, 2)
    return int(rounded) if rounded == int(rounded) else rounded

def convert_recipe(recipe, target_unit):
    """
    Convert all convertible ingredient amounts in a recipe to target_unit.
    Return a list of result dicts:
    {
        "item": str,
        "original": str,
        "converted": str,   new amount str, or original if skipped
        "status": "converted" | "skipped" | "typo" | "unparseable",
        "note": str         human-reable explanation if needed
    }
    """
    target_unit = target_unit.strip().lower()
    results = []
    
    for ing in recipe["ingredients"]:
        item = ing["item"]
        original = ing["amount"]
        number, unit = parse_amount(original)
        
        #completely unparseable like 'top up'
        if number is None:
            results.append({
                "item": item,
                "original": original,
                "converted": original,
                "status": "skipped",
                "note": "Count with no unit - kept as it is."
            })
            continue
        
        #bare count with no unit like '6 mint leaves'
        if unit is None:
            results.append({
                "item": item,
                "original": original,
                "converted": original,
                "status": "skipped",
                "note": "Count with no unit - kept as it is."
            })
            continue
        
        #count like 'dish, slice' that we choose to skip
        if unit in Skipped_Units:
            results.append({
                "item": item,
                "original": original,
                "converted": original,
                "status": "skipped",
                "note": f"Unit '{unit}' is not convertible - kept as it is."
            })
            continue
        
        #unknown unit - try typo correction
        if unit not in All_Known_Units:
            suggestion = detect_typo(unit)
            note = (f"Unknown unit '{unit}'. Did you mean '{suggestion}'?"
                    if suggestion else f"Unknown unit '{unit}'. No close match found.")
            results.append({
                "item": item,
                "original": original,
                "converted": original,
                "status": "typo",
                "note": note
            })
            continue
        
        #attempt conversion
        try:
            converted_num = convert_unit(number, unit, target_unit)
            converted_str = f"{format_number(converted_num)} {target_unit}"
            results.append({
                "item": item,
                "original": original,
                "converted": converted_str,
                "status": "converted",
                "note": ""
            })
        except ValueError as e:
            results.append({
                "item": item,
                "original": original,
                "converted": original,
                "status": "skipped",
                "note": str(e)
            })
        
    return results

def display_conversion_results(recipe,target_unit):
    """
    Nicely print the conversion results.
    """
    print(f"\n--- {recipe['name']} (converted to {target_unit}) ---")
    results = convert_recipe(recipe, target_unit)
    
    for r in results:
        if r["status"] == "converted":
            print(f"- {r['item']}: {r['original']} -> {r['converted']}")
        elif r["status"] == "typo":
            print(f" {r['item']}: '{r['original']}' ⚠ {r['note']}")
        else:
            #skipped/unparseable - show original
            print(f" {r['item']}: '{r['original']}' (kept as original)")
    print()