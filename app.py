import pandas as pd
import streamlit as st

st.set_page_config(page_title="Analyse des appels", layout="wide")

st.title("📞 Analyse des appels téléphoniques")

# Charger le fichier CSV depuis Google Drive
@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?id=1eJcROCTnoXQ2xCXndT3bdAlQBKn6qL1K"
    df = pd.read_csv(url)
    return df

df = load_data()

# Calcul des durées totales et montants totaux par destination
agg_df = df.groupby("Destination Group").agg({
    "Duration (Seconds)": "sum",
    "Amount": "sum"
}).reset_index()

# Formater les colonnes
agg_df["Duration (Seconds)"] = agg_df["Duration (Seconds)"].astype(int)
agg_df["Montant (€)"] = agg_df["Amount"].round(2)
agg_df.drop("Amount", axis=1, inplace=True)

# Tableau complet avec ligne de total
all_dest_df = agg_df.copy()
total_row = pd.DataFrame({
    "Destination Group": ["✅ Total général"],
    "Duration (Seconds)": [all_dest_df["Duration (Seconds)"].sum()],
    "Montant (€)": [all_dest_df["Montant (€)"].sum()]
})
all_dest_df = pd.concat([all_dest_df, total_row], ignore_index=True)

# Top 10
top10_df = agg_df.sort_values(by="Duration (Seconds)", ascending=False).head(10)

# Affichage
st.subheader("🏆 Top 10 des destinations par durée totale d'appels")
st.dataframe(top10_df.style.format({"Duration (Seconds)": "{:,}".format, "Montant (€)": "{:,.2f} €".format}))

st.subheader("📋 Toutes les destinations : durée cumulée et montant total")
st.dataframe(all_dest_df.style.format({"Duration (Seconds)": "{:,}".format, "Montant (€)": "{:,.2f} €".format}))
