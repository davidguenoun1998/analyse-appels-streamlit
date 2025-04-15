import streamlit as st
import pandas as pd
import os
from io import StringIO

st.set_page_config(page_title="Analyse Appels", layout="wide")
st.title("📞 Analyse automatique de fichiers CSV d'appels")

uploaded_file = st.file_uploader("📤 Importez un fichier CSV", type=["csv"])

@st.cache_data(show_spinner=True)
def split_and_load_csv(file, chunk_size=100_000):
    content = file.getvalue().decode("utf-8")
    df_chunks = []
    for chunk in pd.read_csv(StringIO(content), chunksize=chunk_size):
        df_chunks.append(chunk)
    full_df = pd.concat(df_chunks, ignore_index=True)
    return full_df

if uploaded_file:
    try:
        df = split_and_load_csv(uploaded_file)

        st.success(f"✅ Fichier chargé : {len(df):,} lignes")
        st.dataframe(df.head(), use_container_width=True)

        # Agrégation
        agg_df = df.groupby("Destination Group").agg({
            "Duration (Seconds)": "sum",
            "Amount": "sum"
        }).reset_index()

        # Formatage
        agg_df["Duration (Seconds)"] = agg_df["Duration (Seconds)"].astype(int)
        agg_df["Montant (€)"] = agg_df["Amount"].round(2)
        agg_df.drop("Amount", axis=1, inplace=True)

        # Données complètes avec ligne total
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
        st.subheader("🏆 Top 10 des destinations")
        st.dataframe(top10_df.style.format({
            "Duration (Seconds)": "{:,}".format,
            "Montant (€)": "{:,.2f} €".format
        }), use_container_width=True)

        st.subheader("📋 Toutes les destinations")
        st.dataframe(all_dest_df.style.format({
            "Duration (Seconds)": "{:,}".format,
            "Montant (€)": "{:,.2f} €".format
        }), use_container_width=True)

    except Exception as e:
        st.error(f"❌ Erreur lors du traitement du fichier : {e}")
