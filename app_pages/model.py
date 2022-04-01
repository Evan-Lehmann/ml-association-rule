import streamlit as st
import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import joblib

#return original dataset
def dataset():
    groceries_data = pd.read_csv(r"https://raw.githubusercontent.com/Evan-Lehmann/ml-association-rule/main/data/groceries.csv")
    return groceries_data

def app():
    global groceries_data, dataset

    def convert_df(df):
        return df.to_csv().encode('utf-8') #allows datasets to be downloaded as CSVs
    st.title('Model')

    #original dataset
    st.subheader("Original Dataset")
    st.dataframe(dataset())
    st.write("Shape:", dataset().shape)

    #allow original dataset to be downloaded
    original_csv = convert_df(dataset())
    st.download_button(
        label="Download data as a CSV",
        data=original_csv,
        file_name='original_transactions.csv',
        mime='text/csv',
    )
    st.write("")

    #build model and deal with data
    st.subheader("Generate Association Rules")

    #select params 
    itemset_thresh =  st.number_input("Itemset Minimum Support", value=0.015, min_value=0.001, max_value=1.0, step=0.005, format="%.3f") 
    metric_type = st.selectbox("Rules Metric Type",
    ('lift', 
    'confidence', 
    'support',
    'antecedent support',
    'consequent support',
    'leverage',
    'conviction'))
    if metric_type == 'lift':
        rules_thresh = st.number_input(f"Minimum {metric_type} value", min_value=0.0, value=1.0, step=0.5) #good
    else:
        if metric_type == 'confidence':
            rules_thresh = st.number_input(f"Minimum {metric_type} value", min_value=0.0, value=0.25, step=0.025)
        else:
            if metric_type == 'support' or metric_type == 'antecedent support' or metric_type == 'consequent support':
                rules_thresh = st.number_input(f"Minimum {metric_type} value",value=0.01, min_value=0.001, max_value=1.0, step=0.005, format="%.3f")
            else:
                if metric_type == 'leverage':
                    rules_thresh = st.number_input(f"Minimum {metric_type} value", min_value=-1.0, max_value=1.0, value=0.005, step=0.005, format="%.3f")
                else:
                    rules_thresh = st.number_input(f"Minimum {metric_type} value", min_value=0.0, value=1.0, step=0.1)

    #clean data
    groceries = dataset().drop(columns="Items")
    groceries = groceries.fillna("none")
    groceries_list = groceries.values.tolist()
    cleaned_list = []
    for row in groceries_list:
        new_row = [val for val in row if val != "none"]
        cleaned_list.append(new_row)

    #build model
    enc = TransactionEncoder()
    enc.fit(cleaned_list)
    enc_groceries = pd.DataFrame(enc.transform(cleaned_list), columns=enc.columns_)

    #format and return rules
    temp = pd.DataFrame()
    itemset = apriori(enc_groceries, min_support=itemset_thresh, use_colnames=True)

    if st.button(label="Generate"):
        rules = association_rules(itemset, metric=metric_type, min_threshold=rules_thresh)

        #streamlit isn't able to recognize the frozenset datatype the rules values are saved in, so we have to conver them to string
        temp["antecedents"] = rules["antecedents"].apply(lambda x: ', '.join(list(x))).astype("unicode")
        temp["consequents"] = rules["consequents"].apply(lambda x: ', '.join(list(x))).astype("unicode")

        temp["support"] = rules["support"].copy()
        temp["confidence"] = rules["confidence"].copy()
        temp["lift"] = rules["lift"].copy()

        temp["antecedent support"] = rules["antecedent support"].copy()
        temp["consequent support"] = rules["consequent support"].copy()

        st.dataframe(temp)
        st.write("Shape:", temp.shape)

        rules_csv = convert_df(temp)
        st.download_button(
            label="Download data as a CSV",
            data=rules_csv,
            file_name='rules.csv',
            mime='text/csv',
        )