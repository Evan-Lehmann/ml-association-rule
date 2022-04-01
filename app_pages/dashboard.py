import streamlit as st
import matplotlib as plt
import pandas as pd 
import altair as alt
from app_pages.model import dataset
import numpy as np

#get number of times each item purchased
def items_func():
    original_groceries_list = dataset().drop(columns="Items").fillna("none")
    items_frequency = []
    for col in original_groceries_list:
        all_items = original_groceries_list[col]
        for all_itms in all_items:
            items_frequency.append(all_itms)
    items_frequency = pd.Series([val for val in items_frequency if val != "none"])
    items_frequency = items_frequency.value_counts()
    return items_frequency

def app():
    global items_func
    st.title('Dashboard')

    #transaction stats and distribution
    purchases_frequency_df = dataset()["Items"].value_counts()
    purchases_frequency_df = pd.DataFrame(pd.concat([pd.Series(purchases_frequency_df.index), 
                                                    pd.Series(purchases_frequency_df.values)], axis=1))
    purchases_frequency_df.columns = ["Items Purchased", "Frequency"]

    purchases_df = pd.DataFrame(dataset()["Items"])
    purchases_df.columns = ["Items Purchased"]

    groceries = dataset().drop(columns=["Items"])
    groceries = groceries.fillna("none")

    purchases_total, purchases_mean = st.columns(2)
    purchases_total.metric("Number of Transactions", len(dataset()))
    purchases_mean.metric("Mean Number of Items Purchased per Transaction", dataset()["Items"].mean().round(2))

    transaction_dist = alt.Chart(purchases_frequency_df).mark_bar(size=15).encode(
        x='Items Purchased',
        y='Frequency'
    ).properties(
    title='Items Purchased per Transactions Distribution',
    width=750,
    height=500
    )
    
    st.metric("Standard Deviation of Number of Items Purchased per Transaction", dataset()["Items"].std().round(2))
    st.altair_chart(transaction_dist)
    st.write("")

    #item purchases stats and distribution
    items_total, items_unique = st.columns(2)
    items_total.metric("Total Items Purchased", items_func().values.sum())
    items_unique.metric("Unique Items", len(np.unique(items_func().index)))

    items_mean, items_std = st.columns(2)
    items_mean.metric("Mean Purchases per Item", items_func().values.mean().round(2))
    items_std.metric("Standard Deviation of Purchases per Item",  items_func().values.std().round(2))
    
    cols_number = st.slider(label='Number of Items shown', min_value=1, max_value=len(np.unique(items_func().index)), value=[0, 30], step=5)
    cols_number = list(cols_number)

    items_frequency = []
    for col in groceries:
        all_items = groceries[col]
        for all_itms in all_items:
            items_frequency.append(all_itms)

    items_frequency = pd.Series([val for val in items_frequency if val != "none"])

    items_frequency = items_frequency.value_counts()

    items_frequency_df = pd.DataFrame(pd.concat([pd.Series(items_frequency[cols_number[0]:cols_number[1]].index), pd.Series(items_frequency[cols_number[0]:cols_number[1]].values)], axis=1))
    items_frequency_df.columns = ["Item", "Purchases"]

    items_frequency_df = items_frequency_df.sort_values("Purchases")

    item_purchase_dist = alt.Chart(items_frequency_df).mark_bar().encode(
        x=alt.Y('Purchases'),
        y=alt.X('Item', sort='-x')
    ).properties(
    title=f'Purchases per Item Distribution',
    width=750,
    height=500
    )
    st.altair_chart(item_purchase_dist)