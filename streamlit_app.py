# streamlit_app.py
import streamlit as st
import pdfplumber
import pandas as pd
import re
import tempfile

def clean_amount(amount_str):
    if pd.isna(amount_str) or amount_str == '' or amount_str is None:
        return 0.0
    
    amount_str = str(amount_str).strip()
    if len(amount_str) < 1 or amount_str.lower() in ['nan', 'none', '-']:
        return 0.0
    
    amount_str = re.sub(r'[,\s₹]', '', amount_str)
    is_negative = amount_str.startswith('-')
    amount_str = amount_str.lstrip('-')
    
    try:
        amount = float(amount_str)
        return -amount if is_negative else amount
    except:
        return 0.0

def calculate_totals(pdf_file):
    total_debit = 0.0
    total_credit = 0.0
    
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    if table and len(table) > 1:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        df = df.astype(str)
                        
                        debit_cols = [col for col in df.columns if any(keyword in col.lower() 
                                     for keyword in ['debit', 'dr', 'withdrawal', 'paid'])]
                        credit_cols = [col for col in df.columns if any(keyword in col.lower() 
                                      for keyword in ['credit', 'cr', 'deposit', 'received'])]
                        
                        for col in debit_cols:
                            for value in df[col]:
                                amount = clean_amount(value)
                                if amount > 0:
                                    total_debit += amount
                        
                        for col in credit_cols:
                            for value in df[col]:
                                amount = clean_amount(value)
                                if amount > 0:
                                    total_credit += amount
        
        return total_debit, total_credit, None
    except Exception as e:
        return 0, 0, str(e)

# Streamlit App
st.set_page_config(page_title="Bank Statement Analyzer", page_icon="💰")

st.title("🏦 Bank Statement Analyzer")
st.markdown("Upload your PDF bank statement to calculate total debits and credits")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")
    
    if st.button("🔍 Analyze Statement", type="primary"):
        with st.spinner("Analyzing your statement..."):
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Analyze the statement
            debit, credit, error = calculate_totals(tmp_file_path)
            
            if error:
                st.error(f"Error analyzing statement: {error}")
            else:
                # Display results in columns
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Debits", f"₹{debit:,.2f}", delta=None)
                
                with col2:
                    st.metric("Total Credits", f"₹{credit:,.2f}", delta=None)
                
                with col3:
                    net_balance = credit - debit
                    delta_color = "normal" if net_balance >= 0 else "inverse"
                    st.metric("Net Balance", f"₹{net_balance:,.2f}", delta=None)
                
                # Additional info
                st.info(f"Analysis complete! Your statement shows a net {'surplus' if net_balance >= 0 else 'deficit'} of ₹{abs(net_balance):,.2f}")

st.markdown("---")
st.markdown("💡 **Tip**: Make sure your PDF contains tabular data with clear debit/credit columns")
