from collections import defaultdict

class CFG:
    def __init__(self):
        self.rules = defaultdict(list)  # Maps non-terminals to lists of productions
        self.non_terminals = set()
        self.terminals = set()

    def add_rule(self, non_terminal, symbols):
        self.non_terminals.add(non_terminal)
        self.rules[non_terminal].append(symbols)
        for symbol in symbols:
            if symbol.isupper():
                self.non_terminals.add(symbol)
            else:
                self.terminals.add(symbol)

    def get_rules(self, non_terminal):
        return self.rules.get(non_terminal, [])

    def __str__(self):
        lines = ["Grammar Rules:"]
        if not self.rules:
            lines.append("  (No rules defined)")
        for nt in sorted(self.rules):
            for prod in self.rules[nt]:
                rhs = " ".join(prod) if prod else "ε"
                lines.append(f"  {nt} -> {rhs}")
        lines.append(f"Non-Terminals: {sorted(self.non_terminals)}")
        lines.append(f"Terminals: {sorted(self.terminals)}")
        return "\n".join(lines)

class AmbiguityChecker:
    def __init__(self, cfg):
        self.cfg = cfg
        self.memo = {}

    def _is_terminal(self, symbol):
        return symbol not in self.cfg.non_terminals

    def _count_derivations(self, symbol, string):
        key = (symbol, string)
        if key in self.memo:
            return self.memo[key]

        if self._is_terminal(symbol):
            count = 1 if string == symbol else 0
            self.memo[key] = count
            return count

        count = 0
        for production in self.cfg.get_rules(symbol):
            count += self._count_prod_derivations(production, string)
        self.memo[key] = count
        return count

    def _count_prod_derivations(self, production, string):
        key = (tuple(production), string)
        if key in self.memo:
            return self.memo[key]

        if not production:
            count = 1 if not string else 0
            self.memo[key] = count
            return count

        count = 0
        first, rest = production[0], production[1:]
        for i in range(len(string) + 1):
            prefix, suffix = string[:i], string[i:]
            first_count = self._count_derivations(first, prefix)
            if first_count > 0:
                rest_count = self._count_prod_derivations(rest, suffix)
                count += first_count * rest_count

        self.memo[key] = count
        return count

    def check(self, start_symbol, string):
        self.memo.clear()
        if start_symbol not in self.cfg.non_terminals:
            print(f"Error: '{start_symbol}' is not a valid non-terminal.")
            return False, 0

        print(f"\nChecking if '{string}' can be derived from start symbol '{start_symbol}':")
        count = self._count_derivations(start_symbol, string)
        print(f"Number of parse trees: {count}")

        if count > 1:
            print("Result: Grammar is AMBIGUOUS.")
        elif count == 1:
            print("Result: Grammar is NOT ambiguous.")
        else:
            print("Result: String cannot be derived from the grammar.")

        return count > 1, count

def get_cfg_from_user():
    cfg = CFG()
    print("Enter grammar rules (e.g., S -> a S b). Use 'ε' for epsilon. Type 'done' to finish.")
    while True:
        rule = input("Rule: ").strip()
        if rule.lower() == "done":
            break
        if "->" not in rule:
            print("Invalid rule format. Use '->' (e.g., S -> a B).")
            continue

        left, right = map(str.strip, rule.split("->", 1))
        if not left or not left.isupper():
            print("Non-terminal must be uppercase (e.g., S).")
            continue

        if right == "ε":
            symbols = []
        else:
            symbols = right.split()

        cfg.add_rule(left, symbols)
        print(f"Added: {left} -> {' '.join(symbols) if symbols else 'ε'}")

    print("\nFinal Grammar:")
    print(cfg)
    return cfg

def main():
    print("=== Context-Free Grammar Ambiguity Checker ===")
    print("Note: Avoid left-recursive grammars (e.g., E -> E + T).")
    print()

    while True:
        cfg = get_cfg_from_user()
        start_symbol = input("Enter the start symbol: ").strip()
        checker = AmbiguityChecker(cfg)

        while True:
            string = input("Enter string to check (or type 'new' for new grammar, 'exit' to quit): ").strip()
            if string.lower() == "exit":
                print("Goodbye!")
                return
            if string.lower() == "new":
                break
            checker.check(start_symbol, string)

        restart = input("Do you want to define a new grammar? (y/n): ").strip().lower()
        if restart != 'y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
