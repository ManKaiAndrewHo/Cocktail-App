from convert import parse_amount

tests = ["2 oz", "1.5 tsp", "1/2 cup", "6", "Top up", "rim the glass", "2 dashes"]
for t in tests:
    print(repr(t), "→", parse_amount(t))