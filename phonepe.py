import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector
import plotly.express as px
import requests
import json
from PIL import Image

#DataFrame_Creation
#aggregated_transaction_DF
sqlconnection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345678',
    database='phonepe_data'
)
cursor = sqlconnection.cursor(buffered=True)

cursor.execute("select * from aggregated_transaction")
sqlconnection.commit()
table1 = cursor.fetchall()

Aggregated_Transaction = pd.DataFrame(table1, columns = ("States", "Years", "Quarter", "Transaction_Type", "Transaction_Count", "Transaction_Amount"))

#aggregated_user_DF
cursor.execute("select * from aggregated_user")
sqlconnection.commit()
table2 = cursor.fetchall()

Aggregated_User = pd.DataFrame(table2, columns = ("States", "Years", "Quarter", "Brands", "Transaction_Count", "Percentage"))

#map_transaction_DF
cursor.execute("select * from map_transaction")
sqlconnection.commit()
table3 = cursor.fetchall()

Map_Transaction = pd.DataFrame(table3, columns = ("States", "Years", "Quarter", "Districts_Name", "Transaction_Count", "Transaction_Amount"))

#map_user_DF
cursor.execute("select * from map_user")
sqlconnection.commit()
table4 = cursor.fetchall()

Map_User = pd.DataFrame(table4, columns = ("States", "Years", "Quarter", "Districts_Name", "Registered_Users", "App_Opens_Count"))

#top_transaction_DF
cursor.execute("select * from top_transaction")
sqlconnection.commit()
table5 = cursor.fetchall()

Top_Transaction = pd.DataFrame(table5, columns = ("States", "Years", "Quarter", "PinCodes", "Transaction_Count", "Transaction_Amount"))

#top_user_DF
cursor.execute("select * from top_user")
sqlconnection.commit()
table6 = cursor.fetchall()

Top_User = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "PinCodes", "Registered_Users"))

def Transaction_amt_cnt_Y(df, year):
    
    transaction_year = df[df["Years"] == year]
    transaction_year.reset_index(drop = True, inplace = True)
    
    transaction_group = transaction_year.groupby("States")[["Transaction_Count", "Transaction_Amount"]].sum()
    transaction_group.reset_index(inplace = True)

    col1,col2 = st.columns(2)
    with col1:    
        fig_amount = px.bar(transaction_group, x = "States", y = "Transaction_Amount", title = f"{year} TRANSACTION AMOUNT",
                           color_discrete_sequence = px.colors.sequential.Agsunset, height = 650, width = 600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(transaction_group, x = "States", y = "Transaction_Count", title = f"{year} TRANSACTION COUNT",
                           color_discrete_sequence = px.colors.sequential.Bluered, height = 650, width = 600)
        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)
    with col1:    
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        States_name = []
        for feature in data1["features"]:
            States_name.append(feature["properties"]["ST_NM"])
        States_name.sort()
        
        fig_India_1 = px.choropleth(transaction_group, geojson = data1, locations = "States", featureidkey = "properties.ST_NM",
                                   color = "Transaction_Amount", color_continuous_scale = "Rainbow",
                                   range_color = (transaction_group["Transaction_Amount"].min(), transaction_group["Transaction_Amount"].max()),
                                   hover_name = "States", title = f"{year} TRANSACTION AMOUNT", fitbounds = "locations",
                                   height = 600, width = 600)
        
        fig_India_1.update_geos(visible = False)
        st.plotly_chart(fig_India_1)
        
    with col2:
        fig_India_2 = px.choropleth(transaction_group, geojson = data1, locations = "States", featureidkey = "properties.ST_NM",
                                   color = "Transaction_Count", color_continuous_scale = "Rainbow",
                                   range_color = (transaction_group["Transaction_Count"].min(), transaction_group["Transaction_Count"].max()),
                                   hover_name = "States", title = f"{year} TRANSACTION COUNT", fitbounds = "locations",
                                   height = 600, width = 600)
        
        fig_India_2.update_geos(visible = False)
        st.plotly_chart(fig_India_2)

    return transaction_year


def Transaction_amt_cnt_Q(df, quarter):
    transaction_year = df[df["Quarter"] == quarter]
    transaction_year.reset_index(drop = True, inplace = True)
    
    transaction_group = transaction_year.groupby("States")[["Transaction_Count", "Transaction_Amount"]].sum()
    transaction_group.reset_index(inplace = True)

    col1,col2 = st.columns(2)
    with col1:        
        fig_amount = px.bar(transaction_group, x = "States", y = "Transaction_Amount", title = f"{transaction_year['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                           color_discrete_sequence = px.colors.sequential.Agsunset, height = 650, width = 600)
        st.plotly_chart(fig_amount)
        
    with col2:            
        fig_count = px.bar(transaction_group, x = "States", y = "Transaction_Count", title = f"{transaction_year['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                           color_discrete_sequence = px.colors.sequential.Bluered, height = 650, width = 600)
        st.plotly_chart(fig_count)

    col1, col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        States_name = []
        for feature in data1["features"]:
            States_name.append(feature["properties"]["ST_NM"])
        States_name.sort()
        
        fig_India_1 = px.choropleth(transaction_group, geojson = data1, locations = "States", featureidkey = "properties.ST_NM",
                                   color = "Transaction_Amount", color_continuous_scale = "Rainbow",
                                   range_color = (transaction_group["Transaction_Amount"].min(), transaction_group["Transaction_Amount"].max()),
                                   hover_name = "States", title = f"{transaction_year['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds = "locations",
                                   height = 600, width = 600)
        
        fig_India_1.update_geos(visible = False)
        st.plotly_chart(fig_India_1)

    with col2:
        fig_India_2 = px.choropleth(transaction_group, geojson = data1, locations = "States", featureidkey = "properties.ST_NM",
                                   color = "Transaction_Count", color_continuous_scale = "Rainbow",
                                   range_color = (transaction_group["Transaction_Count"].min(), transaction_group["Transaction_Count"].max()),
                                   hover_name = "States", title = f"{transaction_year['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds = "locations",
                                   height = 600, width = 600)
        
        fig_India_2.update_geos(visible = False)
        st.plotly_chart(fig_India_2)

    return transaction_year

def Aggre_TrnsType(df, state):
    transaction_year = df[df["States"] == state]
    transaction_year.reset_index(drop = True, inplace = True)
    transaction_group = transaction_year.groupby("Transaction_Type")[["Transaction_Count", "Transaction_Amount"]].sum()
    transaction_group.reset_index(inplace = True)

    col1, col2 = st.columns(2)
    with col1:
        fig_pie_1 = px.pie(data_frame = transaction_group, names = "Transaction_Type", values = "Transaction_Amount",
                          width = 600, title = f"{state.upper()} TRANSACTION AMOUNT", hole = 0.5)
        st.plotly_chart(fig_pie_1)
        
    with col2:
        fig_pie_2 = px.pie(data_frame = transaction_group, names = "Transaction_Type", values = "Transaction_Count",
                          width = 600, title = f"{state.upper()} TRANSACTION COUNT", hole = 0.5)
        st.plotly_chart(fig_pie_2)

def Aggre_user_plot1(df,year):
    Agguyear = df[df["Years"] == year]
    Agguyear.reset_index(drop = True, inplace = True)
    
    Agguyrgrp = pd.DataFrame(Agguyear.groupby("Brands")["Transaction_Count"].sum())
    Agguyrgrp.reset_index(inplace = True)
    
    fig_bar_1 = px.bar(Agguyrgrp, x = "Brands", y = "Transaction_Count", title = f"{year} BRANDS and TRANSACTIONS COUNT",
                      width = 1000, color_discrete_sequence = px.colors.sequential.haline_r, hover_name = "Brands")
    st.plotly_chart(fig_bar_1)

    return Agguyear

def Aggre_user_plot2(df, quarter):
    Agguqrtr = df[df["Quarter"] == quarter]
    Agguqrtr.reset_index(drop = True, inplace = True)
    
    Agguqrtrgrp = pd.DataFrame(Agguqrtr.groupby("Brands")["Transaction_Count"].sum())
    Agguqrtrgrp.reset_index(inplace = True)
    
    fig_bar_1 = px.bar(Agguqrtrgrp, x = "Brands", y = "Transaction_Count", title = f"{quarter} QUARTER BRANDS and TRANSACTIONS COUNT",
                          width = 1000, color_discrete_sequence = px.colors.sequential.Burg, hover_name = "Brands")
    st.plotly_chart(fig_bar_1)

    return Agguqrtr

#Aggregated_User_Analysis_3
def Aggre_user_plot_3(df, state):
    Aggustate = df[df["States"] == state]
    Aggustate.reset_index(drop = True, inplace = True)
    
    aguqyg= pd.DataFrame(Aggustate.groupby("Brands")["Transaction_Count"].sum())
    aguqyg.reset_index(inplace= True)    
    
    fig_line_1 = px.line(aguqyg, x = "Brands", y = "Transaction_Count",
                        title = f"{state.upper()} BRANDS, TRANSACTION COUNT and PERCENTAGE", width = 1000, markers = True)
    st.plotly_chart(fig_line_1)

#Map_transaction_district_based
def Map_Trns_District(df, state):
    transaction_year = df[df["States"] == state]
    transaction_year.reset_index(drop = True, inplace = True)
    
    transaction_group = transaction_year.groupby("Districts_Name")[["Transaction_Count", "Transaction_Amount"]].sum()
    transaction_group.reset_index(inplace = True)

    col1,col2 = st.columns(2)
    with col1:
        fig_bar_1 = px.bar(transaction_group, x = "Transaction_Amount", y = "Districts_Name", orientation = "h", height = 600,
                          title = f"{state.upper()} DISTRICT and TRANSACTION AMOUNT", color_discrete_sequence = px.colors.sequential.Magenta_r)
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2 = px.bar(transaction_group, x = "Transaction_Count", y = "Districts_Name", orientation = "h", height = 600,
                          title = f"{state.upper()} DISTRICT and TRANSACTION COUNT", color_discrete_sequence = px.colors.sequential.Magenta)
        st.plotly_chart(fig_bar_2)


#map_user_plot_1
def map_user_plot1(df, year):
    mapuyear = df[df["Years"] == year]
    mapuyear.reset_index(drop = True, inplace = True)
    
    mapuyrgrp = mapuyear.groupby("States")[["Registered_Users", "App_Opens_Count"]].sum()
    mapuyrgrp.reset_index(inplace = True)
    
    fig_line_1 = px.line(mapuyrgrp, x = "States", y = ["Registered_Users", "App_Opens_Count"],
                            title = f"{year} REGISTERED USERS and APP OPENS", height = 800, markers = True)
    st.plotly_chart(fig_line_1)

    return mapuyear

#map_user_plot_2
def map_user_plot2(df, quarter):
    mapuquarter = df[df["Quarter"] == quarter]
    mapuquarter.reset_index(drop = True, inplace = True)
    
    mapuqrtrgrp = mapuquarter.groupby("States")[["Registered_Users", "App_Opens_Count"]].sum()
    mapuqrtrgrp.reset_index(inplace = True)
    
    fig_line_1 = px.line(mapuqrtrgrp, x = "States", y = ["Registered_Users", "App_Opens_Count"],
                            title = f"{df['Years'].min()} YEAR {quarter} QUARTER REGISTERED USERS and APP OPENS", height = 800, markers = True,
                        color_discrete_sequence = px.colors.sequential.Mint_r)
    st.plotly_chart(fig_line_1)

    return mapuquarter

#map_user_plot_3
def map_user_plot3(df, state):
    Map_user_S = df[df["States"] == state]
    Map_user_S.reset_index(drop = True, inplace = True)

    col1,col2 = st.columns(2)
    with col1:
        fig_bar_1 = px.bar(Map_user_S, x = "Registered_Users", y = "Districts_Name", orientation = "h",
                           title = f"{state.upper()} REGISTERED USERS", height = 800, color_discrete_sequence = px.colors.sequential.Magenta_r)
        st.plotly_chart(fig_bar_1)
        
    with col2:
        fig_bar_2 = px.bar(Map_user_S, x = "App_Opens_Count", y = "Districts_Name", orientation = "h",
                           title = f"{state.upper()} APP OPENS", height = 800, color_discrete_sequence = px.colors.sequential.Magenta)
        st.plotly_chart(fig_bar_2)


#top_transaction_plot_1
def top_trnsctn_plot_1(df, state):
    topts = df[df["States"] == state]
    topts.reset_index(drop = True, inplace = True)
    
    toptsgrp = topts.groupby("PinCodes")[["Transaction_Count", "Transaction_Amount"]].sum()
    toptsgrp.reset_index(inplace = True)
    
    col1,col2 = st.columns(2)
    with col1:
        fig_bar_1 = px.bar(topts, x = "Quarter", y = "Transaction_Amount", hover_data = "PinCodes",
                           title = f"{state.upper()} TRANSACTION AMOUNT", height = 650, width = 600, color_discrete_sequence = px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2 = px.bar(topts, x = "Quarter", y = "Transaction_Count", hover_data = "PinCodes",
                           title = f"{state.upper()} TRANSACTION COUNT", height = 650, width = 600, color_discrete_sequence = px.colors.sequential.algae)
        st.plotly_chart(fig_bar_2)

def top_user_plot_1(df, year):
    Topuyear = df[df["Years"] == 2022]
    Topuyear.reset_index(drop = True, inplace = True)
    
    Topuyrgrp = pd.DataFrame(Topuyear.groupby(["States", "Quarter"])["Registered_Users"].sum())
    Topuyrgrp.reset_index(inplace = True)
    
    fig_top_bar_1 = px.bar(Topuyrgrp, x = "States", y = "Registered_Users", color = "Quarter", width = 1000, height = 800,
                          color_discrete_sequence = px.colors.sequential.PuBu_r, hover_name = "States",
                          title = f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_bar_1)

    return Topuyear

#top_user_plot_2
def top_user_plot_2(df, state):
    Topustate = df[df["States"] == state]
    Topustate.reset_index(drop = True, inplace = True)
    
    fig_top_bar2 = px.bar(Topustate, x = "Quarter", y = "Registered_Users", title = f"{state.upper()} REGISTERED USERS, PINCODES and QUARTER",
                         width = 1000, height = 800, color = "Registered_Users", hover_data = "PinCodes",
                         color_continuous_scale = px.colors.sequential.Magma_r)
    st.plotly_chart(fig_top_bar2)

#questions_sql_queries
def top_chart_transaction_amount(table_name):
    sqlconnection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='phonepe_data'
    )
    cursor = sqlconnection.cursor(buffered=True)
    
    #plot1
    query1 = f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC LIMIT 10;'''
    
    cursor.execute(query1)
    table1 = cursor.fetchall()
    sqlconnection.commit()
    
    df1 = pd.DataFrame(table1, columns = ("States", "Transaction_Amount"))

    col1, col2 = st.columns(2)
    with col1:
        fig_amount_1 = px.bar(df1, x = "States", y = "Transaction_Amount", title = "TOP 10 of TRANSACTION AMOUNT",
                               color_discrete_sequence = px.colors.sequential.Agsunset, height = 650, width = 600, hover_name = "States")
        st.plotly_chart(fig_amount_1)
        
    #plot2
    query2 = f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount LIMIT 10;'''
    
    cursor.execute(query2)
    table2 = cursor.fetchall()
    sqlconnection.commit()
    
    df2 = pd.DataFrame(table2, columns = ("States", "Transaction_Amount"))
    with col2:
        fig_amount_2 = px.bar(df2, x = "States", y = "Transaction_Amount", title = "LAST 10 of TRANSACTION AMOUNT",
                               color_discrete_sequence = px.colors.sequential.Agsunset_r, height = 650, width = 600, hover_name = "States")
        st.plotly_chart(fig_amount_2)
    
    #plot3
    query3 = f'''SELECT states, AVG(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount;'''
    
    cursor.execute(query3)
    table3 = cursor.fetchall()
    sqlconnection.commit()
    
    df3 = pd.DataFrame(table3, columns = ("States", "Transaction_Amount"))
    fig_amount_3 = px.bar(df3, y = "States", x = "Transaction_Amount", title = "AVERAGE of TRANSACTION AMOUNT", orientation = "h",
                           color_discrete_sequence = px.colors.sequential.Blugrn_r, height = 800, width = 1000, hover_name = "States")
    st.plotly_chart(fig_amount_3)

def top_chart_transaction_count(table_name):
    sqlconnection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='phonepe_data'
    )
    cursor = sqlconnection.cursor(buffered=True)
    
    #plot1
    query1 = f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count DESC LIMIT 10;'''
    
    cursor.execute(query1)
    table1 = cursor.fetchall()
    sqlconnection.commit()
    
    df1 = pd.DataFrame(table1, columns = ("States", "Transaction_Count"))
    col1, col2 = st.columns(2)
    with col1:
        fig_amount_1 = px.bar(df1, x = "States", y = "Transaction_Count", title = "TOP 10 of TRANSACTION COUNT",
                               color_discrete_sequence = px.colors.sequential.Agsunset, height = 650, width = 600, hover_name = "States")
        st.plotly_chart(fig_amount_1)
    
    #plot2
    query2 = f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count LIMIT 10;'''
    
    cursor.execute(query2)
    table2 = cursor.fetchall()
    sqlconnection.commit()
    
    df2 = pd.DataFrame(table2, columns = ("States", "Transaction_Count"))
    with col2:
        fig_amount_2 = px.bar(df2, x = "States", y = "Transaction_Count", title = "LAST 10 of TRANSACTION COUNT",
                               color_discrete_sequence = px.colors.sequential.Agsunset_r, height = 650, width = 600, hover_name = "States")
        st.plotly_chart(fig_amount_2)
    
    #plot3
    query3 = f'''SELECT states, AVG(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count;'''
    
    cursor.execute(query3)
    table3 = cursor.fetchall()
    sqlconnection.commit()
    
    df3 = pd.DataFrame(table3, columns = ("States", "Transaction_Count"))
    fig_amount_3 = px.bar(df3, y = "States", x = "Transaction_Count", title = "AVERAGE of TRANSACTION COUNT", orientation = "h",
                           color_discrete_sequence = px.colors.sequential.Blugrn_r, height = 800, width = 1000, hover_name = "States")
    st.plotly_chart(fig_amount_3)

#questions_sql_queries
def top_chart_registered_user(table_name, state):
    sqlconnection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='phonepe_data'
    )
    cursor = sqlconnection.cursor(buffered=True)
    
    #plot1
    query1 = f'''SELECT Districts_Name, SUM(Registered_Users) AS Registered_Users 
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY Districts_Name
                ORDER BY Registered_Users DESC LIMIT 10;'''
    
    cursor.execute(query1)
    table1 = cursor.fetchall()
    sqlconnection.commit()
    
    df1 = pd.DataFrame(table1, columns = ("Districts_Name", "Registered_Users"))
    col1, col2 = st.columns(2)
    with col1:
        fig_amount_1 = px.bar(df1, x = "Districts_Name", y = "Registered_Users", title = "TOP 10 of REGISTERED USERS",
                               color_discrete_sequence = px.colors.sequential.Agsunset, height = 650, width = 600, hover_name = "Districts_Name")
        st.plotly_chart(fig_amount_1)
    
    #plot2
    query2 = f'''SELECT Districts_Name, SUM(Registered_Users) AS Registered_Users 
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY Districts_Name
                ORDER BY Registered_Users LIMIT 10;'''
    
    cursor.execute(query2)
    table2 = cursor.fetchall()
    sqlconnection.commit()
    
    df2 = pd.DataFrame(table2, columns = ("Districts_Name", "Registered_Users"))
    with col2:
        fig_amount_2 = px.bar(df2, x = "Districts_Name", y = "Registered_Users", title = "LAST 10 of REGISTERED USERS",
                               color_discrete_sequence = px.colors.sequential.Agsunset_r, height = 650, width = 600, hover_name = "Districts_Name")
        st.plotly_chart(fig_amount_2)
    
    #plot3
    query3 = f'''SELECT Districts_Name, AVG(Registered_Users) AS Registered_Users 
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY Districts_Name
                ORDER BY Registered_Users;'''
    
    cursor.execute(query3)
    table3 = cursor.fetchall()
    sqlconnection.commit()
    
    df3 = pd.DataFrame(table3, columns = ("Districts_Name", "Registered_Users"))
    fig_amount_3 = px.bar(df3, y = "Districts_Name", x = "Registered_Users", title = "AVERAGE of REGISTERED USERS", orientation = "h",
                           color_discrete_sequence = px.colors.sequential.Blugrn_r, height = 800, width = 1000, hover_name = "Districts_Name")
    st.plotly_chart(fig_amount_3)
    
#questions_sql_queries
def top_chart_app_opens(table_name, state):
    sqlconnection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='phonepe_data'
    )
    cursor = sqlconnection.cursor(buffered=True)
    
    #plot1
    query1 = f'''SELECT Districts_Name, SUM(App_Opens_Count) AS App_Opens_Count 
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY Districts_Name
                ORDER BY App_Opens_Count DESC LIMIT 10;'''
    
    cursor.execute(query1)
    table1 = cursor.fetchall()
    sqlconnection.commit()
    
    df1 = pd.DataFrame(table1, columns = ("Districts_Name", "App_Opens_Count"))
    col1,col2 = st.columns(2)
    with col1:
        fig_amount_1 = px.bar(df1, x = "Districts_Name", y = "App_Opens_Count", title = "TOP 10 of APP OPENS COUNT",
                               color_discrete_sequence = px.colors.sequential.Agsunset, height = 650, width = 600, hover_name = "Districts_Name")
        st.plotly_chart(fig_amount_1)
    
    #plot2
    query2 = f'''SELECT Districts_Name, SUM(App_Opens_Count) AS App_Opens_Count 
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY Districts_Name
                ORDER BY App_Opens_Count LIMIT 10;'''
    
    cursor.execute(query2)
    table2 = cursor.fetchall()
    sqlconnection.commit()
    
    df2 = pd.DataFrame(table2, columns = ("Districts_Name", "App_Opens_Count"))
    with col2:
        fig_amount_2 = px.bar(df2, x = "Districts_Name", y = "App_Opens_Count", title = "LAST 10 of APP OPENS COUNT",
                               color_discrete_sequence = px.colors.sequential.Agsunset_r, height = 650, width = 600, hover_name = "Districts_Name")
        st.plotly_chart(fig_amount_2)
    
    #plot3
    query3 = f'''SELECT Districts_Name, AVG(App_Opens_Count) AS App_Opens_Count 
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY Districts_Name
                ORDER BY App_Opens_Count;'''
    
    cursor.execute(query3)
    table3 = cursor.fetchall()
    sqlconnection.commit()
    
    df3 = pd.DataFrame(table3, columns = ("Districts_Name", "App_Opens_Count"))
    fig_amount_3 = px.bar(df3, y = "Districts_Name", x = "App_Opens_Count", title = "AVERAGE of APP OPENS COUNT", orientation = "h",
                           color_discrete_sequence = px.colors.sequential.Blugrn_r, height = 800, width = 1000, hover_name = "Districts_Name")
    st.plotly_chart(fig_amount_3)
    

#questions_sql_queries
def top_chart_registered_users(table_name):
    sqlconnection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='phonepe_data'
    )
    cursor = sqlconnection.cursor(buffered=True)
    
    #plot1
    query1 = f'''SELECT States, SUM(Registered_Users) AS Registered_Users 
                FROM {table_name}
                GROUP BY States
                ORDER BY Registered_Users DESC LIMIT 10;'''
    
    cursor.execute(query1)
    table1 = cursor.fetchall()
    sqlconnection.commit()
    
    df1 = pd.DataFrame(table1, columns = ("States", "Registered_Users"))
    col1, col2 = st.columns(2)
    with col1:
        fig_amount_1 = px.bar(df1, x = "States", y = "Registered_Users", title = "TOP 10 of REGISTERED USERS",
                               color_discrete_sequence = px.colors.sequential.Agsunset, height = 650, width = 600, hover_name = "States")
        st.plotly_chart(fig_amount_1)
    
    #plot2
    query2 = f'''SELECT States, SUM(Registered_Users) AS Registered_Users 
                FROM {table_name}
                GROUP BY States
                ORDER BY Registered_Users LIMIT 10;'''
    
    cursor.execute(query2)
    table2 = cursor.fetchall()
    sqlconnection.commit()
    
    df2 = pd.DataFrame(table2, columns = ("States", "Registered_Users"))
    with col2:
        fig_amount_2 = px.bar(df2, x = "States", y = "Registered_Users", title = "LAST 10 of REGISTERED USERS",
                               color_discrete_sequence = px.colors.sequential.Agsunset_r, height = 650, width = 600, hover_name = "States")
        st.plotly_chart(fig_amount_2)
    
    #plot3
    query3 = f'''SELECT States, AVG(Registered_Users) AS Registered_Users 
                FROM {table_name}
                GROUP BY States
                ORDER BY Registered_Users;'''
    
    cursor.execute(query3)
    table3 = cursor.fetchall()
    sqlconnection.commit()
    
    df3 = pd.DataFrame(table3, columns = ("States", "Registered_Users"))
    fig_amount_3 = px.bar(df3, y = "States", x = "Registered_Users", title = "AVERAGE of REGISTERED USERS", orientation = "h",
                           color_discrete_sequence = px.colors.sequential.Blugrn_r, height = 800, width = 1000, hover_name = "States")
    st.plotly_chart(fig_amount_3)
    

#streamlit code

st.set_page_config(layout = "wide")
st.title("PHONEPE DATA VISUALIZATION and EXPLORATION")

with st.sidebar:
    select = option_menu("Main Menu", ["Home Page", "Data Exploration", "Charts Visualization"])

if select == "Home Page":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video("D:\GUVI\projects\phonepe\PhonePe_Introduction.mp4")

    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"D:\GUVI\projects\phonepe\phonepe_img2.jpg"), width = 500)

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****Earn Great Rewards****")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"D:\GUVI\projects\phonepe\phonepe_img3.jpg"), width = 500)

elif select == "Data Exploration":
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        option = st.radio("Select the option", ["Aggregated Transaction", "Aggregated User"])
        if option == "Aggregated Transaction":
            col1, col2 = st.columns(2)
            with col1:            
                years = st.slider("Select the Year:", Aggregated_Transaction["Years"].min(), Aggregated_Transaction["Years"].max(), Aggregated_Transaction["Years"].min())
            trsctn_Y = Transaction_amt_cnt_Y(Aggregated_Transaction, years)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State:", trsctn_Y["States"].unique())
            Aggre_TrnsType(trsctn_Y, states)
            
            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter:", trsctn_Y["Quarter"].min(), trsctn_Y["Quarter"].max(), trsctn_Y["Quarter"].min())
            trsctn_Q = Transaction_amt_cnt_Q(trsctn_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State_Type:", trsctn_Q["States"].unique())
            Aggre_TrnsType(trsctn_Q, states)
                            
        elif option == "Aggregated User":
            col1, col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select the Year:", Aggregated_User["Years"].unique())
            Aggre_User_Y = Aggre_user_plot1(Aggregated_User, years)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select the Quarter:", Aggre_User_Y["Quarter"].unique())
            Aggre_User_Q = Aggre_user_plot2(Aggre_User_Y, quarters)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State:", Aggre_User_Y["States"].unique())
            Aggre_user_plot_3(Aggre_User_Q, states)
    
    with tab2:
        option2 = st.radio("Select the option", ["Map Transaction", "Map User"])
        if option2 == "Map Transaction":

            col1, col2 = st.columns(2)
            with col1:            
                years = st.slider("Select the Year :", Map_Transaction["Years"].min(), Map_Transaction["Years"].max(), Map_Transaction["Years"].min())
            map_trsctn_Y = Transaction_amt_cnt_Y(Map_Transaction, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State :", map_trsctn_Y["States"].unique())
            Map_Trns_District(map_trsctn_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter :", map_trsctn_Y["Quarter"].min(), map_trsctn_Y["Quarter"].max(), map_trsctn_Y["Quarter"].min())
            map_trsctn_Q = Transaction_amt_cnt_Q(map_trsctn_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State: ", map_trsctn_Q["States"].unique())
            Map_Trns_District(map_trsctn_Q, states)
            
        elif option2 == "Map User":
            col1, col2 = st.columns(2)
            with col1:            
                years = st.slider("Select the Year :", Map_User["Years"].min(), Map_User["Years"].max(), Map_User["Years"].min())
            map_user_Y = map_user_plot1(Map_User, years)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter : ", map_user_Y["Quarter"].min(), map_user_Y["Quarter"].max(), map_user_Y["Quarter"].min())
            map_user_Y_Q = map_user_plot2(map_user_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State : ", map_user_Y_Q["States"].unique())
            map_user_plot3(map_user_Y_Q, states)
    
            
    with tab3:
        option3 = st.radio("Select the option", ["Top Transaction", "Top User"])
        if option3 == "Top Transaction":
            col1, col2 = st.columns(2)
            with col1:            
                years = st.slider("Select the Year : ", Top_Transaction["Years"].min(), Top_Transaction["Years"].max(), Top_Transaction["Years"].min())
            top_trsctn_Y = Transaction_amt_cnt_Y(Top_Transaction, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State:  ", top_trsctn_Y["States"].unique())
            top_trnsctn_plot_1(top_trsctn_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter :  ", top_trsctn_Y["Quarter"].min(), top_trsctn_Y["Quarter"].max(), top_trsctn_Y["Quarter"].min())
            top_trnsctn_Y_Q = Transaction_amt_cnt_Q(top_trsctn_Y, quarters)
            
        elif option3 == "Top User":
            col1, col2 = st.columns(2)
            with col1:            
                years = st.slider("Select the Year :  ", Top_User["Years"].min(), Top_User["Years"].max(), Top_User["Years"].min())
            top_user_Y = top_user_plot_1(Top_User, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State :  ", top_user_Y["States"].unique())
            top_user_plot_2(top_user_Y, states)

elif select == "Charts Visualization":

    question = st.selectbox("Select the Question", ["1. Transaction Amount and Count of Aggregated Transaction",
                                                    "2. Transaction Amount and Count of Map Transaction",
                                                    "3. Transaction Amount and Count of Top Transaction",
                                                    "4. Transaction Count of Aggregated User",
                                                    "5. Registered Users of Map User",
                                                    "6. App Opens of Map User",
                                                    "7. Registered Users of Top User"
                                                   ])
    
    if question == "1. Transaction Amount and Count of Aggregated Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")
        
    elif question == "2. Transaction Amount and Count of Map Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")
        
    elif question == "3. Transaction Amount and Count of Top Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")
    
    elif question == "4. Transaction Count of Aggregated User":
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif question == "5. Registered Users of Map User":
        states = st.selectbox("Select the State", Map_User["States"].unique())
        st.subheader("REGISTERED USERS")       
        top_chart_registered_user("map_user", states)
        
    elif question == "6. App Opens of Map User":
        states = st.selectbox("Select the State", Map_User["States"].unique())
        st.subheader("APP OPENS COUNT")       
        top_chart_app_opens("map_user", states)

    elif question == "7. Registered Users of Top User":
        st.subheader("REGISTERED USERS")       
        top_chart_registered_users("top_user")