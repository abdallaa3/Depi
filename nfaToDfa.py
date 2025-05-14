from collections import deque

# Computes the epsilon-closure of a set of NFA states
def epsilon_closure(states, transitions, eps=""):
    closure = set(states)
    stack = deque(states)
    while stack:
        state = stack.popleft()
        for next_state in transitions.get((state, eps), set()):
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return frozenset(closure)

# Computes the set of NFA states reachable from a set of states on a given symbol
def move(states, symbol, transitions):
    result = set()
    for state in states:
        result.update(transitions.get((state, symbol), set()))
    return result

# Converts an NFA (with optional epsilon transitions) to a DFA
def nfa_to_dfa(nfa_states, alphabet, transitions, start, accepts, eps=""):
    dfa_transitions = {}
    dfa_states = set()

    start_state = epsilon_closure({start}, transitions, eps)
    queue = deque([start_state])
    dfa_states.add(start_state)

    while queue:
        current = queue.popleft()
        for symbol in alphabet:
            next_nfa = move(current, symbol, transitions)
            next_dfa = epsilon_closure(next_nfa, transitions, eps)
            dfa_transitions[(current, symbol)] = next_dfa
            if next_dfa not in dfa_states and next_dfa:
                dfa_states.add(next_dfa)
                queue.append(next_dfa)

    dfa_accepts = {state for state in dfa_states if state & accepts}
    return dfa_states, dfa_transitions, start_state, dfa_accepts

# Prints DFA states and transitions clearly
def print_dfa(dfa_states, dfa_transitions, start_state, accept_states):
    all_states = set(dfa_states) | set(dfa_transitions.values())
    sorted_states = sorted(all_states, key=lambda s: tuple(sorted(s)) if s else ())
    state_names = {s: f"S{i}" for i, s in enumerate(sorted_states)}

    def format_state(s): return "{" + ", ".join(sorted(s)) + "}" if s else "{}"

    print("DFA States:")
    for state in sorted_states:
        accept_mark = " (Accept)" if state in accept_states else ""
        print(f"  {state_names[state]}: {format_state(state)}{accept_mark}")

    print(f"\nStart State: {state_names[start_state]} ({format_state(start_state)})")

    print("\nTransitions:")
    for (src, symbol), dst in sorted(dfa_transitions.items(), key=lambda x: (state_names[x[0][0]], x[0][1])):
        print(f"  {state_names[src]} --{symbol}--> {state_names[dst]}")

    print("\nAccept States:")
    for state in sorted(accept_states, key=lambda x: state_names[x]):
        print(f"  {state_names[state]} ({format_state(state)})")

if __name__ == "__main__":
    # Example 1: NFA for strings ending in 'ab' or 'b'
    print("--- Example 1: NFA for strings ending in 'ab' or 'b' ---")
    nfa_states_1 = {"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"}
    alphabet_1 = {"a", "b"}
    transitions_1 = {
        ("q0", ""): {"q1"},
        ("q1", "a"): {"q2"},
        ("q1", "b"): {"q5"},
        ("q2", ""): {"q3"},
        ("q3", "b"): {"q4"},
        ("q5", ""): {"q6"},
        ("q6", ""): {"q7"},
        ("q7", "b"): {"q10"},
        ("q7", "a"): {"q8"},
        ("q8", ""): {"q9"},
        ("q9", "b"): {"q10"},
    }
    start_1 = "q0"
    accepts_1 = {"q4", "q10"}

    dfa_1_states, dfa_1_trans, dfa_1_start, dfa_1_accepts = nfa_to_dfa(
        nfa_states_1, alphabet_1, transitions_1, start_1, accepts_1
    )
    print_dfa(dfa_1_states, dfa_1_trans, dfa_1_start, dfa_1_accepts)

    print("\n" + "=" * 50 + "\n")

    # Example 2: NFA for strings containing 'aa' or 'bb'
    print("--- Example 2: NFA for strings containing 'aa' or 'bb' ---")
    nfa_states_2 = {"q0", "q1", "q2", "q3"}
    alphabet_2 = {"a", "b"}
    transitions_2 = {
        ("q0", "a"): {"q0", "q1"},
        ("q0", "b"): {"q0", "q2"},
        ("q1", "a"): {"q3"},
        ("q1", "b"): {"q2"},
        ("q2", "b"): {"q3"},
        ("q2", "a"): {"q1"},
        ("q3", "a"): {"q3"},
        ("q3", "b"): {"q3"},
    }
    start_2 = "q0"
    accepts_2 = {"q3"}

    dfa_2_states, dfa_2_trans, dfa_2_start, dfa_2_accepts = nfa_to_dfa(
        nfa_states_2, alphabet_2, transitions_2, start_2, accepts_2
    )
    print_dfa(dfa_2_states, dfa_2_trans, dfa_2_start, dfa_2_accepts)
