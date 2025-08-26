import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Database setup
conn = sqlite3.connect('expenses.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        amount REAL,
        description TEXT
    )
''')
conn.commit()

# Initialize session state for refresh
if "refresh" not in st.session_state:
    st.session_state.refresh = False

# Title
st.title("💰 Expense Tracker App")

# Input form
st.header("Add a New Expense")
with st.form("expense_form"):
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Transport", "Utilities", "Entertainment", "Other"])
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    description = st.text_input("Description")
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        cursor.execute(
            "INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
            (str(date), category, amount, description)
        )
        conn.commit()
        st.success("✅ Expense added successfully!")
        st.session_state.refresh = not st.session_state.refresh  # trigger refresh

# Show all expenses
st.header("📋 Expense Records")
# Category filter
categories = ["All"] + [row[0] for row in cursor.execute("SELECT DISTINCT category FROM expenses").fetchall()]
selected_cat = st.selectbox("Filter by Category", categories)

if selected_cat == "All":
    cursor.execute("SELECT id, date, category, amount, description FROM expenses")
else:
    cursor.execute("SELECT id, date, category, amount, description FROM expenses WHERE category=?", (selected_cat,))
rows = cursor.fetchall()

if rows:
    df = pd.DataFrame(rows, columns=["ID", "Date", "Category", "Amount", "Description"])
    
    # Display rows with delete button
    for i, row in df.iterrows():
        cols = st.columns([1,2,2,2,2,1])
        cols[0].write(row["ID"])
        cols[1].write(row["Date"])
        cols[2].write(row["Category"])
        cols[3].write(row["Amount"])
        cols[4].write(row["Description"])
        if cols[5].button("🗑️", key=f"del_{row['ID']}"):
            cursor.execute("DELETE FROM expenses WHERE id=?", (row["ID"],))
            conn.commit()
            st.session_state.refresh = not st.session_state.refresh  # trigger refresh
            st.experimental_rerun = lambda: None  # safe hack to suppress old rerun call
            st.experimental_rerun()  # triggers automatic refresh

else:
    st.info("No expenses recorded yet.")

# Total expense
st.header("💵 Total Expenses")
cursor.execute("SELECT SUM(amount) FROM expenses")
total = cursor.fetchone()[0]
st.write(f"Total Expenses: ${total if total else 0:.2f}")

# Summary chart
st.header("📊 Expense Summary")
cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
data = cursor.fetchall()
if data:
    categories, amounts = zip(*data)
    fig, ax = plt.subplots()
    ax.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
    ax.set_title("Expense Summary by Category")
    st.pyplot(fig)
else:
    st.warning("No expenses found!")
