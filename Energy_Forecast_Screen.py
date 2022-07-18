import streamlit as st
import requests
import json
import re
import datetime

def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}


def main():
    
    st.title("Energy Consumption Forecasting")
    session = requests.Session()
    with st.form("my_form"):
        
        d = st.date_input("Please enter a date",     datetime.date(2022, 7, 18))
       
        horizon = st.radio("Please Choose Forecasting Horizon",  ('Long Term[Quarterly]', 'Short Term[Monthly]'))

        
        submitted = st.form_submit_button("Submit")

        if submitted:
            text = ''
            st.write("Predicted Consumption")
            if horizon== 'Short Term[Monthly]' :
            #data = fetch(session, f"http://384ffed9-f7b6-4bc0-955e-8ec10ca4fec8.eastasia.azurecontainer.io/score")
            
             url = 'http://384ffed9-f7b6-4bc0-955e-8ec10ca4fec8.eastasia.azurecontainer.io/score'
             #
             row_data = { "Inputs": {    "data": [{"Country": 'United States',  "Time": d.strftime("%Y-%m-%d") ,"Balance": "example_value","Product": "example_value",   "Unit": "example_value" }  ]   },   "GlobalParameters": {
            "quantiles": [      0.025,       0.975     ]   } }
             
            if horizon =='Long Term[Quarterly]' :
              url = 'http://6256662e-9fce-472b-94db-2f4feb1f56f3.eastasia.azurecontainer.io/score'
              row_data = { "Inputs": {    "data": [{"Country": 'United States',  "Time": d.strftime("%Y-%m-%d") ,"Balance": "example_value","Product": "example_value",   "Unit": "example_value" }  ]   },   "GlobalParameters": {
            "quantiles": [      0.025,       0.975     ]   } }
            response = requests.post(url, data=json.dumps(row_data), headers= {'Content-type': 'application/json'})
            #print(response)
            if response:
                #st.write(response['forecast'])
                 json_data = json.loads(response.text)
                 text = str(json_data['Results']['forecast'])
                 st.write(re.sub(r"[\([{})\]]", "", text  +'   GWh'))
                 #st.write(json_data['Results']['forecast'])
            else:   
                st.error("Error")


if __name__ == '__main__':
    main()