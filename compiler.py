import dfa


def number_dfa():
    states = ['0', '1', '2']
    transitions = []
    transitions.append(dfa.Transition('0', '\d', '1'))
    transitions.append(dfa.Transition('1', '\d', '1'))
    transitions.append(dfa.Transition('1', '[^\d]', '2'))
    initial = '0'
    finals = ['2']
    return dfa.DFA(states, transitions, initial, finals)


if __name__ == '__main__':
    print("salam")