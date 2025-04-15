import pandas as pd
import streamlit as st

st.set_page_config(page_title="Analyse des appels", layout="wide")

st.title("📞 Analyse des appels par groupe de destination")

# 📤 Upload CSV
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Aperçu du fichier")
    st.dataframe(df.head())

    # 📊 Groupement par destination avec somme
    grouped = df.groupby('Destination Group').agg({
        'Duration (Seconds)': 'sum',
        'Amount': 'sum'
    }).reset_index()

    # 🔝 Top 10 par durée
    top_10 = grouped.sort_values(by='Duration (Seconds)', ascending=False).head(10)
    top_10_formatted = top_10.copy()
    top_10_formatted["Duration (Seconds)"] = top_10_formatted["Duration (Seconds)"].apply(lambda x: "{:,}".format(int(x)))
    top_10_formatted["Amount"] = top_10_formatted["Amount"].apply(lambda x: "{:,.2f}".format(x))

    st.subheader("🔝 Top 10 des groupes de destination par durée cumulée d'appels")
    st.dataframe(top_10_formatted)

    # 📋 Toutes les destinations avec total
    grouped_all_sorted = grouped.sort_values(by='Duration (Seconds)', ascending=False).copy()
    total_duration = grouped_all_sorted["Duration (Seconds)"].sum()
    total_amount = grouped_all_sorted["Amount"].sum()

    total_row = pd.DataFrame({
        "Destination Group": ["Total général"],
        "Duration (Seconds)": [total_duration],
        "Amount": [total_amount]
    })

    grouped_all_with_total = pd.concat([grouped_all_sorted, total_row], ignore_index=True)
    grouped_all_formatted = grouped_all_with_total.copy()
    grouped_all_formatted["Duration (Seconds)"] = grouped_all_formatted["Duration (Seconds)"].apply(lambda x: "{:,}".format(int(x)))
    grouped_all_formatted["Amount"] = grouped_all_formatted["Amount"].apply(lambda x: "{:,.2f}".format(x))

    st.subheader("📋 Toutes les destinations (avec total global)")
    st.dataframe(grouped_all_formatted)

else:
    st.info("Veuillez importer un fichier CSV pour lancer l'analyse.")

