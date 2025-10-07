import streamlit as st
import pandas as pd

# Simple page config
st.set_page_config(page_title="Stock Bro", page_icon="📈")

# Title
st.title("📈 Stock Bro - Simple Portfolio")

# Add a stock
st.header("Add Stock to Portfolio")

# Input form
with st.form("add_stock"):
    ticker = st.text_input("Stock Ticker (e.g., AAPL)")
    shares = st.number_input("Number of Shares", min_value=1, value=1)
    price = st.number_input("Purchase Price", min_value=0.01, value=100.0)
    
    submitted = st.form_submit_button("Add Stock")
    
    if submitted and ticker:
        st.success(f"Added {shares} shares of {ticker} at ${price}")

# Show portfolio
st.header("My Portfolio")

# Sample portfolio data
portfolio = pd.DataFrame({
    'Stock': ['AAPL', 'GOOGL', 'MSFT'],
    'Shares': [10, 5, 15],
    'Price': [150.0, 2800.0, 300.0],
    'Value': [1500.0, 14000.0, 4500.0]
})

# Display table
st.dataframe(portfolio)

# Calculate total
total_value = portfolio['Value'].sum()
st.metric("Total Portfolio Value", f"${total_value:,.2f}")

# Simple chart
st.header("Portfolio Chart")
st.bar_chart(portfolio.set_index('Stock')['Value'])
