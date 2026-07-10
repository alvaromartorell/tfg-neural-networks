import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

from state_encoder import encode_state
from data_loader import parse_logs

# === CONSTANTES ===
LOG_PATH = "pluribus_logs/*.txt"

# === 1. Cargar los datos ===
print("Leyendo logs de Pluribus...")
df = parse_logs(LOG_PATH)
print(f"Total decisiones de Pluribus: {len(df)}")

# === 2. Limpieza y preparación ===
df['action'] = df['action'].str.lower().str.strip()
df['action'] = df['action'].replace({
    'folds': 'fold',
    'calls': 'call',
    'raises': 'raise',
    'bets': 'bet',
    'checks': 'check'
})

acciones_validas = ['fold', 'call', 'raise', 'bet', 'check']
df = df[df['action'].isin(acciones_validas)]

# === 3. Función para calcular SPR ===
def compute_spr(row):
    pot = row.get('pot_size', 0)
    stack = row.get('stack', 0)
    if pot <= 0:
        return 0.0
    return round(stack / pot, 2)

df['spr'] = df.apply(compute_spr, axis=1)

max_spr = df['spr'].max()


# === 4. Codificar X e y ===
def encode_row(row):
    hole = [row['hole1'], row['hole2']]
    board = row['board'] if isinstance(row['board'], list) else []
    street_map = {'Preflop': 0, 'Flop': 1, 'Turn': 2, 'River': 3}
    street_idx = street_map.get(row['street'], 0)
    position = row.get('seat', 0) - 1  # asiento de 1 a 6 -> 0 a 5
    spr = row['spr']
    players_active = row.get('num_players_active', 6)
    invested = row.get('invested_by_pluribus', 0)
    return encode_state(hole, board, street_idx, position, spr, max_spr, players_active,  invested) 

print("Codificando jugadas...")
X = np.vstack(df.apply(encode_row, axis=1).values)
y = df['action'].values


print("\n=== EJEMPLO DE MANOS CODIFICADAS ===")
print(f"Tamaño de los vectores: {len(X[0])}")
for ejemplo_idx in range(0,15):
    print("Acción original:", y[ejemplo_idx])
    print("Vector codificado:", X[ejemplo_idx][:])



#print(f"Vector de entrada: shape={X.shape}")

# === 5. Entrenar y evaluar modelo ===


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#model = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)

print("Realizando validación cruzada (5-fold)...")
#scores = cross_val_score(model, X_train, y_train, cv=5)
#print("Accuracy medio validación cruzada:", scores.mean())
#print("Accuracies individuales:", scores)


print("Entrenando red neuronal...")
#model.fit(X_train, y_train)

print("Evaluando el modelo...")
#y_pred = model.predict(X_test)
#print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
#print(classification_report(y_test, y_pred))


action_to_int = {
    'fold': 0,
    'check': 1,
    'call': 2,
    'bet': 3,
    'raise': 4
}

#y_test_int = [action_to_int[y] for y in y_test]
#y_pred_int = [action_to_int[y] for y in y_pred]
#cm = confusion_matrix(y_test_int, y_pred_int, labels=[0, 1, 2, 3, 4])
#disp = ConfusionMatrixDisplay(confusion_matrix=cm,
#                              display_labels=['fold', 'check', 'call', 'bet', 'raise'])
#disp.plot(cmap='Blues', xticks_rotation=45)
#plt.title('Matriz de confusión')
#plt.tight_layout()
#plt.savefig("confusion_matrix.png", dpi=300)
#plt.show()
