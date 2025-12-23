import matplotlib.pyplot as plt
import os

def create_placeholder(filename, text):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.text(0.5, 0.5, text, fontsize=20, ha='center', va='center')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title("Placeholder Screenshot", fontsize=14)
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

screenshots = [
    ("screenshots/add_expense.png", "Add Expense UI\n(Placeholder)"),
    ("screenshots/manage_expenses.png", "Manage Expenses UI\n(Placeholder)"),
    ("screenshots/budgets.png", "Budgets & Goals UI\n(Placeholder)"),
    ("screenshots/analytics_ui.png", "Analytics UI Controls\n(Placeholder)")
]

for path, label in screenshots:
    if not os.path.exists(path):
        create_placeholder(path, label)
        print(f"Created {path}")
    else:
        print(f"Exists {path}")
