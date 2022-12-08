import streamlit as st
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

#Calculations: Products 85% commission, Services 35% commission, Deduct Cash Payments
def payment_calc(revenue):
    global provider, gratuity, revenuecopy, products, services
    revenue['Product'] = ''
    #if provider != 'All Providers':
        #revenue = revenue[revenue["Provider or Instructor"] == provider].reset_index()
    revenue["Amount Charged"] = revenue["Amount Charged"].replace('[\$,]', '', regex=True).astype(float)
    #revenue["Gratuity"] = revenue["Gratuity"].replace('[\$,]', '', regex=True).astype(float)
    gross = round(revenue["Amount Charged"].sum(), 2)
    #gratuity = round(revenue["Gratuity"].sum(), 2)
    #products = revenue[revenue["Product"] == 'Y']
    products["Amount Charged"] = products["Amount Charged"].replace('[\$,]', '', regex=True).astype(float)
    gross_products = round(products["Amount Charged"].sum(), 2)
    #services = revenue[revenue["Product"] == 'N']
    services["Amount Charged"] = services["Amount Charged"].replace('[\$,]', '', regex=True).astype(float)
    gross_services = round(services["Amount Charged"].sum(), 2)
    products_services = round(((gross_products + gross_services) - gratuity), 2)
    cash_payments = revenue[revenue['Tender Type'] == 'Cash']
    cash_payments["Amount Charged"] = cash_payments["Amount Charged"].replace('[\$,]', '', regex=True).astype(float)
    cash = round(cash_payments["Amount Charged"].sum(), 2)
    cash_commission = round((cash*0.3), 2)
    net_cash = round((cash - cash_commission), 2)
    digital_payments = round((products_services - cash), 2)
    prod_commission = round(gross_products*0.85, 2)
    serv_commission = round(gross_services*0.30, 2)
    commission = round((gross_products*0.85 + gross_services*0.3), 2)
    final_payment = round((((gross_products*0.15 + gross_services*0.7) - net_cash) + gratuity), 2)

    results = {
        'Gross': gross,
        'Total Electronic Gratuity': gratuity,
        'Net Services/Products': products_services,
        'Digital Transactions': digital_payments,
        'Cash Transactions': cash,
        #'Cash Commissions': cash_commission,
        #'Disbursed Cash Payments': net_cash,
        'Product Commissions': prod_commission,
        'Service Commissions': serv_commission,
        'Total Commissions': commission,
        'Final Electronic Payment Due': final_payment
    }
    st.write(results)
    keep = ['Processed On','Description','Provider or Instructor','Client Name','Amount Charged','Gratuity','Confirmation Code','Product']
    st.write('Services:')
    st.write(services[keep])
    st.write('Products:')
    st.write(products[keep])

def calc(revenue):
    global gratuity, revenuecopy, products, services, provider
    gratuity = 0
    revenue['Description'] = revenue['Description'].replace('No show fee','No show fee|$40.00')
    revenue["Gratuity"] = revenue["Gratuity"].replace('[\$,]', '', regex=True).astype(float)
    gratuity = round(revenue["Gratuity"].sum(), 2)
    revenue['Product'] = ''
    revenuelist = list(revenue['Description'].to_list())
    revenuecopy = pd.DataFrame(columns = revenue.columns)
    restrictlist = ['Retightening', 'Reti', 'reti' 'hrs', 'Consultation', 'Install', 'install', 'Follow-up', 'Maintenance', 'maintenance', 'Deep Conditioning', 'Repair', 'Shampoo', 'Balance', 'balance', 'Color', 'color']
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
    if provider != 'All Providers':
        revenuecopy = revenuecopy[revenuecopy["Provider or Instructor"] == provider].reset_index()
    products = revenuecopy[revenuecopy["Product"] == 'Y']
    services = revenuecopy[revenuecopy["Product"] == 'N']
    payment_calc(revenuecopy)

gratuity = 0
revenuecopy = pd.DataFrame()
products = pd.DataFrame()
services = pd.DataFrame()
st.markdown("<h2 style='text-align: center; color: #F7349F;'>GlisteningLocks™ Payment Calculator</h1>", unsafe_allow_html=True)
provider = st.selectbox('Provider:', ('All Providers', 'Kristany Niblack', 'Avril Johnson', 'Ty-Ree Jackson', 'Shelia Vines'))
file = st.file_uploader("Upload Worksheet (downloaded 'Recorded_Revenues.xls' report from Schedulicity):")
if file is not None:
    sheet = pd.read_csv(file, delimiter='\t')
    calc(sheet)
