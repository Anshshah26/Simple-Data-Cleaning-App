import streamlit as st
import pandas as pd
import datetime

if "step" not in st.session_state:
    st.session_state.step = 1

st.title("Simple Data Cleaning App")

# Navigation buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Back") and st.session_state.step > 1:
        st.session_state.step -= 1

with col2:
    if st.button("Next") and st.session_state.step < 4:
        st.session_state.step += 1

st.write(f"Step {st.session_state.step} / 4")

if st.session_state.step == 1:
    st.header("Upload File")

    file = st.file_uploader("Upload CSV")

    if file:
        df = pd.read_csv(file)
        st.session_state.df = df

        st.write("Preview:")
        st.dataframe(df.head(100))

elif st.session_state.step == 2:
    st.header("Column Mapping")

    if "df" not in st.session_state:
        st.error("Upload file first")
        st.stop()

    df = st.session_state.df

    user_col = st.selectbox("User ID Column", df.columns)
    date_col = st.selectbox("Date Column", df.columns)
    amount_col = st.selectbox("Amount Column", df.columns)

    st.session_state.mapping = {
        "user": user_col,
        "date": date_col,
        "amount": amount_col
    }

    if not pd.api.types.is_numeric_dtype(df[amount_col]):
        st.error("Amount must be numeric")

    try:
        pd.to_datetime(df[date_col])
    except:
        st.error("Date format is wrong")

elif st.session_state.step == 3:
    st.header("Transformation")

    df = st.session_state.df.copy()

    # Remove duplicates
    if st.checkbox("Remove duplicates"):
        df = df.drop_duplicates()

    if st.checkbox("Fill null with 0"):
        df = df.fillna(0)

    if st.checkbox("Add Adjusted Amount"):
        multiplier = st.number_input("Multiplier", 1.0)
        amount_col = st.session_state.mapping["amount"]
        df["Adjusted_Amount"] = df[amount_col] * multiplier

    st.session_state.new_df = df

    st.write("Preview:")
    st.dataframe(df.head(100))

elif st.session_state.step == 4:
    st.header("Download")

    if "new_df" not in st.session_state:
        st.error("No data to download")
        st.stop()

    df = st.session_state.new_df

    filename = "output_" + datetime.datetime.now().strftime("%H%M%S")

    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        file_name=filename + ".csv"
    )