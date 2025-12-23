# Deployment Guide: GitHub & Streamlit Community Cloud

This guide explains how to host your Expense Analytics app for free so you can access it from anywhere.

## Part 1: Push Code to GitHub

1.  **Initialize Git** (if not already done):

    ```bash
    git init
    # Create .gitignore to exclude virtual env and database
    echo ".venv/" >> .gitignore
    echo "__pycache__/" >> .gitignore
    echo "data/*.db" >> .gitignore  # Exclude DB if you want a fresh start on cloud
    ```

    _(Note: If you want to keep your current data, do NOT ignore `expenses.db`, but it's recommended to store data in a cloud DB for production apps. For this demo, committing the DB is acceptable if it's just for you.)_

2.  **Commit Code**:

    ```bash
    git add .
    git commit -m "Initial commit of Expense Analytics App"
    ```

3.  **Push to GitHub**:
    - Go to [GitHub.com](https://github.com/new) and create a new repository (e.g., `expense-analytics`).
    - Run the commands shown by GitHub:
      ```bash
      git remote add origin https://github.com/YOUR_USERNAME/expense-analytics.git
      git branch -M main
      git push -u origin main
      ```

## Part 2: Deploy to Streamlit Cloud

1.  **Sign Up/Login**:

    - Go to [share.streamlit.io](https://share.streamlit.io/).
    - Log in with your GitHub account.

2.  **New App**:

    - Click **"New app"**.
    - Select **"Use existing repo"**.

3.  **Configure**:

    - **Repository**: Select `YOUR_USERNAME/expense-analytics`.
    - **Branch**: `main`.
    - **Main file path**: `app.py` (or `Project_1_Streamlit_Expense_Analytics/app.py` if you pushed the whole monorepo).
    - **Python version**: 3.11.

4.  **Deploy**:
    - Click **"Deploy!"**.
    - Watch the logs. It will install `requirements.txt` automatically.

## Part 3: Verify Data & Freshness

- **Data Seeding**: When the app starts on the cloud for the first time, it will generate the 100 sample records automatically (since `data/expenses.db` likely won't exist or will be fresh).
- **Timezone**: Streamlit Cloud runs in UTC. Your `datetime.today()` calls will use UTC.
- **Persistence**:
  - **Warning**: On Streamlit Community Cloud, **local files (like SQLite DBs) are ephemeral**. They disappear if the app restarts or goes to sleep.
  - **Solution for Demo**: It works fine for showing off the project.
  - **Solution for Real Use**: Connect to Google Sheets or a cloud database (Supabase/Neon).

## Troubleshooting

- **ModuleNotFoundError**: Ensure `requirements.txt` is in the root of your deployed directory or specified correctly.
- **app.py not found**: check your file path setting in the deployment screen.
