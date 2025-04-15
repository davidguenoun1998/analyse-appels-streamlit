# 📊 Streamlit - Analyse des appels téléphoniques

Cette application vous permet d'importer un fichier `.csv` de facturation d'appels (format Viadialog) et d'obtenir :

- 🔝 Le **Top 10** des groupes de destination par **durée totale d'appels**
- 📋 Un tableau **complet** avec :
  - La **durée totale** par groupe de destination
  - Le **montant total facturé**
  - Une ligne de **totaux globaux**
- 📤 Export possible des résultats

---

## 🚀 Lancer l'app en local

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application Streamlit
streamlit run app.py
