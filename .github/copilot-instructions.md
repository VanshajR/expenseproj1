# Copilot Instructions

## Project Context

This is a monorepo containing personal finance applications. **Current Focus: Project 1 (Streamlit Expense Analytics)**.

### Architecture

- **Framework**: Streamlit (Python) for the frontend/backend.
- **Database**: SQLite (`data/expenses.db`).
- **ORM**: Raw `sqlite3` with `row_factory = sqlite3.Row`.
- **Services**: Business logic in `services/` (CRUD, Analytics, Budgeting).
- **Visualization**: `plotly` (interactive) and `matplotlib` (saved PNGs in `plots/`).

### Key Files (Project 1)

- `app.py`: Main entry point and UI dispatcher.
- `db/database.py`: DB connection and initialization.
- `services/expense_service.py`: Core CRUD operations.
- `services/analytics_service.py`: Chart generation logic.
- `reports/main.tex`: LaTeX report source.

## Workflows

### Environment

- **Virtual Environment**: Located at `.venv`.
- **Activate**: `& ".\.venv\Scripts\Activate.ps1"` (PowerShell).

### Development

1.  **Run App**: `streamlit run Project_1_Streamlit_Expense_Analytics/app.py` (from repo root) or `streamlit run app.py` (from project dir).
2.  **Reset Data**: Delete `data/expenses.db` to trigger auto-seeding of sample data on next run.

## Coding Conventions

- **Paths**: ALWAYS use `pathlib.Path` for file system operations. `BASE_DIR` is typically defined relative to `__file__`.
- **Database**:
  - Use `get_connection()` context managers where possible or explicit `conn.close()`.
  - Always commit transactions (`conn.commit()`) after writes.
- **UI (Streamlit)**:
  - heavy use of `st.session_state` for persistence.
  - `st.sidebar` for navigation.
- **Styling**: `styles/` or inline CSS hacks are minimal; rely on native Streamlit layout.

## Project 2 (Tkinter) Notes

- `python main.py` to run.
- Uses strict MVC-like pattern with `ui/` files separated from `services/`.
