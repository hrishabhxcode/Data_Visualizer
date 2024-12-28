import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("This App is created by Hrishabh by Python")

st.title("Data Visualizer")

st.write("This app will help to plot the graph between various parameters of CSV or Excel Documents")

uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        st.write(f"Uploaded File Name is: **{file.name}**")
        st.write(f"Uploaded File Extension is: **{file_ext}**")
        st.write(f"Uploaded File Size is: **{file.size / 1024:.2f} KB**")

        st.write("Preview the Head of Dataframe:")
        st.dataframe(df.head())

        st.subheader("Data Cleaning Actions:")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    duplicates_count = df.duplicated().sum()
                    df.drop_duplicates(inplace=True)
                    st.write(f"Duplicates Removed: **{duplicates_count}**")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been successfully filled.")


        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose Column for {file.name}",df.columns , default=df.columns)
        df = df[columns]

        st.subheader("Data Visualization")
        if st.checkbox(f"Visualize Data for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        st.subheader("Conversion Actions:")
        conversion_type = st.radio(f"Convert {file.name} to :", ["CSV", "EXCEL"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "EXCEL":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer.getvalue(),
                filename=file_name,
                mime=mime_type
            )

st.success("All Files are Processed Successfully")
