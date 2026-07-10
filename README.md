# Neural Approximation of Bayesian Game Strategies

> Bachelor's Thesis – B.Sc. in Mathematics, Universitat Autònoma de Barcelona

This project explores how **Neural Networks** can approximate decision-making strategies in **Bayesian Games** by learning the behaviour of **Pluribus**, one of the strongest AI poker agents ever developed.

The project combines concepts from **Game Theory**, **Machine Learning**, and **Artificial Intelligence** to model strategic decision-making under imperfect information.

---

## Project Overview

Unlike games such as Chess or Go, poker is an **imperfect-information game** where players must make decisions without knowing their opponents' private information.

Instead of designing a strategy manually, this project investigates whether a neural network can learn to imitate the decisions made by Pluribus from historical gameplay data.

The work consists of two complementary parts:

- **Theoretical foundation**, introducing Bayesian Games, Nash Equilibria and Neural Networks.
- **Practical implementation**, where a Multilayer Perceptron (MLP) is trained to approximate Pluribus' decision policy.

---

## Methodology

### Input Encoding

Each poker state is transformed into a fixed-size numerical vector containing relevant information such as:

- Private cards
- Community cards
- Betting round
- Table position
- Stack-to-Pot Ratio (SPR)
- Number of active players
- Chips invested by the player

Special care was taken to avoid **data leakage**, ensuring that only information available at the decision point was provided to the model.

### Neural Network

The strategy approximation is formulated as a **supervised multiclass classification problem**.

Architecture:

```
Input (40)
      ↓
Hidden Layer (64) + ReLU
      ↓
Hidden Layer (32) + ReLU
      ↓
Output (5) + Softmax
```

The network predicts one of the five possible poker actions:

- Fold
- Check
- Call
- Bet
- Raise

Training configuration:

- Optimizer: Adam
- Loss Function: Cross-Entropy Loss
- L2 Regularization
- Early Stopping
- 5-Fold Cross Validation

The implementation was developed using **Python** and **Scikit-learn**.

---

## Results

The trained model successfully learned to approximate Pluribus' decision policy.

Main results:

- **84.97% Test Accuracy**
- **83.1% Average Cross-Validation Accuracy**
- Strong performance for the most frequent actions (*Fold* and *Check*)
- Good generalization with no significant signs of overfitting

These results suggest that relatively simple neural architectures can effectively learn complex strategic behaviours in imperfect-information games.

---

## Technologies

- Python
- Scikit-learn
- NumPy
- Pandas
- Matplotlib

---

## Repository Structure

```
.
├── src/                # Source code
├── docs/               # Bachelor's thesis
├── figures/            # Images used in the README and thesis
├── README.md
```

---

## Future Improvements

Possible extensions include:

- Incorporating sequential betting history
- Experimenting with deeper neural architectures
- Reinforcement Learning approaches

---

## Thesis

The complete Bachelor's Thesis can be found in the **docs/** directory.

---

## Author

**Álvaro Martorell Ortuño**

B.Sc. in Mathematics  
Universitat Autònoma de Barcelona
