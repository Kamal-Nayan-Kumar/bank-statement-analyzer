# Bank Statement Analyzer 💰

A simple web application to analyze PDF bank statements and calculate total debits, credits, and net balance automatically.

## What it does

- Upload your bank statement PDF file
- Automatically extracts and calculates:
  - Total Debit amount
  - Total Credit amount  
  - Net Balance
- Works with most Indian bank statements (SBI, HDFC, ICICI, etc.)

## How to use

1. Visit the live app: https://bank-statement-analyzer-m9mgzgwx47mpx8s8vnymvo.streamlit.app/
2. Click "Choose a PDF file" and upload your bank statement
3. Click "Analyze Statement" button
4. View your results instantly!

## Features

✅ Easy PDF upload  
✅ Automatic calculation  
✅ Mobile-friendly interface  
✅ Secure - no data stored  
✅ Works on any device with internet  

## Technology Used

- **Python** - Core logic
- **Streamlit** - Web interface
- **pdfplumber** - PDF processing
- **pandas** - Data analysis

## Run Locally

If you want to run this on your computer:

## Clone the repository
```git clone https://github.com/Kamal-Nayan-Kumar/bank-statement-analyzer.git```

## Install requirements
```pip install -r requirements.txt```

## Run the app
```streamlit run streamlit_app.py```


## Privacy & Security

- Your PDF files are processed locally and not stored anywhere
- No personal data is collected or saved
- All calculations happen in real-time

---

**Made with ❤️ for easy financial analysis**

*Note: This tool is for personal use only. Always verify important calculations manually.*
