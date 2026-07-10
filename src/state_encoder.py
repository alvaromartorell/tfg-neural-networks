#encodingestados2
import numpy as np

def card_to_features(card_str):
    """Convierte una carta como 'As' a un vector con valor y palo one-hot"""
    ranks = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
             'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
    suits = {'c':0, 'd':1, 'h':2, 's':3}

    if len(card_str) != 2:
        return np.zeros(5)  # vector nulo si error

    rank_char, suit_char = card_str[0], card_str[1]
    value = (ranks.get(rank_char.upper(), 0)-1)/13
    suit_vector = np.zeros(4)
    suit_index = suits.get(suit_char.lower())
    if suit_index is not None:
        suit_vector[suit_index] = 1
    return np.array([value] + list(suit_vector))

def encode_cards(cards,max_cards):
    """Codifica una lista de cartas (pueden ser privadas o comunitarias)"""
    encoded = [card_to_features(card) for card in cards]
    while len(encoded) < max_cards:  # se rellenan hasta 7 con ceros (hole+board)
        encoded.append(np.zeros(5))
    return np.concatenate(encoded)

def encode_state(hole_cards, board_cards, street, position, spr=None, max_spr=1, num_players_active=None, invested_by_pluribus=None):
    """
    Devuelve el vector de estado codificado para la red neuronal
    - hole_cards: lista con 2 cartas propias, ej. ['As', 'Kc']                          10
    - board_cards: lista con cartas comunitarias                                        25
    - street: int (0=preflop, 1=flop, 2=turn, 3=river)                                  1
    - position: int (0=UTG, ..., 5=SB, 6=BB), rango depende del número de jugadores     1
    - spr: stack-to-pot ratio (float o None)                                            1
    - num_players_active: int (1 a 6), normalizado                                      1
    - invested_by_pluribus: float, dinero invertido (normalizado)                       1
    """
    hole_encoded = encode_cards(hole_cards,2)
    board_encoded = encode_cards(board_cards,5) 

    street_vec = (np.array([street]))/3
    position_vec = np.array([position])/6
    spr_vec = np.array([spr / max_spr if spr is not None else 0.0])
    players_vec = np.array([num_players_active / 6.0 if num_players_active is not None else 0.0])
    invested_vec = np.array([invested_by_pluribus / 10000.0 if invested_by_pluribus is not None else 0.0])


    return np.concatenate([hole_encoded, board_encoded, street_vec, position_vec, spr_vec, players_vec, invested_vec]) # 
