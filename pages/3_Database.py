import streamlit as st

from db import fetch_df


st.title("Database Management")

st.subheader("Tables in Database")
tables = fetch_df("SHOW TABLES")
st.write(tables)

table_name = st.selectbox("Select a table to view", tables['name'])

if table_name:
    st.subheader(f"Contents of {table_name}")
    table_data = fetch_df(f"SELECT * FROM {table_name}")
    st.dataframe(table_data)

    st.subheader(f"Table schema for {table_name}")
    schema = fetch_df(f"PRAGMA table_info({table_name})")
    st.dataframe(schema)

    st.subheader(f"Table creation DDL for {table_name}")
    ddl = f"CREATE TABLE {table_name} (\n"
    for index, row in schema.iterrows():
        ddl += f"    {row['name']} {row['type']}"
        if row['notnull'] == 1:
            ddl += " NOT NULL"
        if row['dflt_value'] is not None:
            ddl += f" DEFAULT {row['dflt_value']}"
        ddl += ",\n"
    ddl = ddl.rstrip(",\n") + "\n);"
    st.code(ddl, language="sql")

st.subheader("Execute Custom Query")
query = st.text_area("SQL Query", height=100)
if st.button("Execute"):
    try:
        query_result = fetch_df(query)
        st.write(query_result)
    except Exception as e:
        st.error(f"Error executing query: {e}")
