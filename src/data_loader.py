import re
from glob import glob
import pandas as pd

# Expresiones regulares
HAND_START = re.compile(r"^PokerStars Hand #\d+:")
SEAT_LINE = re.compile(r"Seat (\d+): (\w+) \((\d+) in chips\)")
DEALT_LINE = re.compile(r"Dealt to Pluribus \[([2-9TJQKA][shdc]) ([2-9TJQKA][shdc])\]")
ACTION_LINE = re.compile(r"^(\w+): (folds|checks|calls(?: \d+)?|bets \d+|raises \d+ to \d+)")
BOARD_LINE = re.compile(r"\*\*\* (FLOP|TURN|RIVER) \*\*\* \[([^\]]+)\]")
SUMMARY_LINE = re.compile(r"\*\*\* SUMMARY \*\*\*")


def parse_logs(path_pattern):
    hands = []
    for path in glob(path_pattern):
        with open(path, 'r') as f:
            lines = f.readlines()

        current_hand = []
        for line in lines:
            if HAND_START.match(line):
                if current_hand:
                    hands.append(current_hand)
                current_hand = [line.strip()]
            else:
                current_hand.append(line.strip())
        if current_hand:
            hands.append(current_hand)

    print(f"Total manos detectadas: {len(hands)}")
    return _extract_pluribus_actions(hands)


def _extract_pluribus_actions(hands):
    records = []

    for hand in hands:
        players = {}
        board = []
        street = 'Preflop'
        hole_cards = ('??', '??')
        pot = 0
        last_action = 'none'
        folded = set()
        invested=0
        pluribus_stack=0
    

        for i, line in enumerate(hand):
            # Extraer asientos y stacks
            m = SEAT_LINE.match(line)
            if m:
                seat, name, stack = m.groups()
                players[name] = {'seat': int(seat), 'stack': int(stack)}
                for n in name:
                    if 'seat' == 1:
                        stack -= 50
                        if n == "Pluribus":
                            invested +=50
                    if 'seat' == 2:
                        stack-=100
                        if n == "Pluribus":
                            invested +=100
                if name == "Pluribus":
                    pluribus_stack = int(stack)
                    if seat == 1:
                        invested+=50
                    elif seat == 2:
                        stack-=100
                        invested+=100

                continue

            # Cartas privadas
            m = DEALT_LINE.match(line)
            if m:
                hole_cards = m.group(1), m.group(2)
                continue

            # Board
            m = BOARD_LINE.match(line)
            if m:
                street = m.group(1).capitalize()
                board = m.group(2).split()
                continue

            # Acción
            m = ACTION_LINE.match(line)
            if m:
                actor, action_raw = m.groups()
                amount=0
                if actor in folded:
                    continue

                # Sumar al bote si la acción tiene cantidad
                if action_raw.startswith("bets"):
                    amount = int(action_raw.split()[1])
                    pot += amount
                    last_action = 'bet'
                elif action_raw.startswith("calls"):
                    try:
                        amount = int(action_raw.split()[1])
                        pot += amount
                    except:
                        pass
                    last_action = 'call'
                elif action_raw.startswith("raises"):
                    amount = int(action_raw.split()[-1])
                    pot += amount
                    last_action = 'raise'
                elif action_raw == 'folds':
                    folded.add(actor)
                    last_action = 'fold'
                elif action_raw == 'checks':
                    last_action = 'check'

                # Guardar acción de Pluribus
                if actor == 'Pluribus':
                    act = action_raw.split()[0]
                    if act in ['posts', 'Uncalled', 'collected']:
                        continue

                    records.append({
                        'hole1': hole_cards[0],
                        'hole2': hole_cards[1],
                        'board': board,
                        'street': street,
                        'action': act,
                        'seat': players.get('Pluribus', {}).get('seat', -1),
                        'stack': pluribus_stack,
                        'num_players_active': 6 - len(folded),
                        'pot_size': pot,
                        'last_action': last_action,
                        'invested_by_pluribus': invested,
                    })
                    invested += amount
                    pluribus_stack -= amount

            if SUMMARY_LINE.match(line):
                break

    print(f"Manos con decisiones de Pluribus extraídas: {len(records)}")
    return pd.DataFrame(records)
