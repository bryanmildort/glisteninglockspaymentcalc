import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def payment_calc(revenue):
    global provider
    if provider != 'All Providers':
        revenue = revenue[revenue["Provider or Instructor"] == provider]
    revenue["Amount Charged"] = revenue["Amount Charged"].replace('[\$,]', '', regex=True).astype(float)
    revenue["Gratuity"] = revenue["Gratuity"].replace('[\$,]', '', regex=True).astype(float)
    gross = round(revenue["Amount Charged"].sum(), 2)
    gratuity = round(revenue["Gratuity"].sum(), 2)
    services = round((gross - gratuity), 2)
    cash_payments = round(revenue[revenue['Tender Type'] == 'Cash']['Amount Charged'].sum())
    cash_commission = round((cash_payments*0.3), 2)
    cash_total = round((cash_payments - cash_commission), 2)
    digital_payments = round((services - cash_payments), 2)
    commission = round(digital_payments*0.3, 2)
    final_payment = round(digital_payments*0.7 + gratuity, 2)

    return {
        'Gross': gross,
        'Gratuity': gratuity,
        'Net Services': services,
        'Digital Payments': digital_payments,
        'Cash Payments': cash_payments,
        'Cash Commissions': cash_commission,
        'Total Cash Payments Paid': cash_total,
        'Digital Commissions': commission,
        'Final Payment': final_payment
    }

st.markdown("<h2 style='text-align: center; color: #F7349F;'>GlisteningLocks™ Payment Calculator</h1>", unsafe_allow_html=True)
provider = st.selectbox('Provider:', ('All Providers', 'Kristany Niblack', 'Avril Johnson', 'Ty-Ree Jackson', 'Shelia Vines'))
file = st.file_uploader("Upload Worksheet (downloaded 'Recorded_Revenues.xls' report from Schedulicity):")
if file is not None:
    sheet = pd.read_csv(file, delimiter='\t')
    results = payment_calc(sheet)
    st.write(results.pop('Final Payment'))
    final = 'Final Payment: ' + str(results.get('Final Payment'))
    st.write(final)
