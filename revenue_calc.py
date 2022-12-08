import streamlit as st
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

#Calculations: Products 85% commission, Services 35% commission, Deduct Cash Payments
def payment_calc(revenue):
    global provider, gratuity
    revenue['Product'] = ''
    if provider != 'All Providers':
        revenue = revenue[revenue["Provider or Instructor"] == provider].reset_index()
    revenue["Amount Charged"] = revenue["Amount Charged"].replace('[\$,]', '', regex=True).astype(float)
    revenue["Gratuity"] = revenue["Gratuity"].replace('[\$,]', '', regex=True).astype(float)
    gross = round(revenue["Amount Charged"].sum(), 2)
    #gratuity = round(revenue["Gratuity"].sum(), 2)
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
        'Disbursed Cash Payments': cash_total,
        'Digital Commissions': commission,
        'Final Payment': final_payment
    }

def calc(revenue):
    global gratuity
    gratuity = round(revenue["Gratuity"].sum(), 2)
    revenue['Product'] = ''
    revenuelist = list(revenue['Description'].to_list())
    revenuecopy = pd.DataFrame(columns = revenue.columns)
    restrictlist = ['Retightening', 'hrs', 'Consultation', 'Installation', 'Follow-up', 'Maintenance', 'Deep Conditioning', 'Repair', 'Shampoo', 'Balance', 'balance', 'Color', 'color']
    for i in revenuelist:
        description = str(i)
        size = len(description)
        mod_desc = description[:size - 2]
        desc_list = mod_desc.split('  ')
        for z in desc_list:
            revenuecopy = revenuecopy.append(revenue.iloc[revenuelist.index(i)])
            revenuecopy.iloc[-1:, 1] = z
            revenuecopy.iloc[-1: , -1:] = 'N' if any(x in z for x in restrictlist) else 'Y'

    revenuecopy = revenuecopy.dropna(subset=['Client Name']).reset_index()
    #Change Prices
    revenuelist = list(revenuecopy['Description'].to_list())
    index = -1
    for i in revenuelist:
        index = index + 1
        description = str(i)
        desc_list = description.split('|')
        price = desc_list[1]
        revenuecopy.loc[index, 'Amount Charged'] = price
    
    payment_calc(revenuecopy)

gratuity = 0
st.markdown("<h2 style='text-align: center; color: #F7349F;'>GlisteningLocks™ Payment Calculator</h1>", unsafe_allow_html=True)
provider = st.selectbox('Provider:', ('All Providers', 'Kristany Niblack', 'Avril Johnson', 'Ty-Ree Jackson', 'Shelia Vines'))
file = st.file_uploader("Upload Worksheet (downloaded 'Recorded_Revenues.xls' report from Schedulicity):")
if file is not None:
    sheet = pd.read_csv(file, delimiter='\t')
    st.write(calc(sheet))
