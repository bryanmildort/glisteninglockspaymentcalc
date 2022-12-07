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
    commission = round(services*0.3, 2)
    payment = round(services*0.7 + gratuity, 2)
    return {
        'Gross': gross,
        'Gratuity': gratuity,
        'Services': services,
        'Commission': commission,
        'Payment': payment
    }

st.markdown("<h2 style='text-align: center; color: #F7349F;'>GlisteningLocks™ Payment Calculator</h1>", unsafe_allow_html=True)
provider = st.selectbox('Provider:', ('All Providers', 'Kristany Niblack', 'Avril Johnson', 'Ty-Ree Jackson'))
file = st.file_uploader("Upload Worksheet (downloaded 'Recorded_Revenues.xls' report from Schedulicity):")
if file is not None:
    sheet = pd.read_csv(file, delimiter='\t')
    st.write(payment_calc(sheet))
