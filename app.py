from datetime import datetime
import streamlit as st
from pint import UnitRegistry
import random
import time

ureg = UnitRegistry()
st.set_page_config(page_title="Super Assistant Quotidien", layout="wide", page_icon="🧰")

# Sidebar - Calculatrice
st.sidebar.title("🧮 Calculatrice rapide")
expr = st.sidebar.text_input("Expression (ex: 2+2)", "1 + 1")
try:
    result = eval(expr)
    st.sidebar.success(f"= {result}")
except:
    st.sidebar.warning("⛔ Expression invalide")

st.sidebar.markdown("---")
st.sidebar.caption("Créé par Noah 💡")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15 = st.tabs([
    "🔁 Convertisseur", "📆 Dates & Temps", "🍽️ Cuisine", "📝 Notes", "🎲 Fun",
    "🔔 Alertes", "🧠 Mot du jour", "📊 Épargne", "🧘 Bien-être","🔍 Recherche Web", "📁 Téléversement", "🗓️ Planning",
    "🔐 MDP Sécurisé", "🤖 Chatbot", "📊 Crypto", 
])

# 1️⃣ Convertisseur
with tab1:
    st.header("🔁 Convertisseur d'unités et devises")
    unit_map = {
        "Longueur": {"mètre": "meter", "kilomètre": "kilometer", "centimètre": "centimeter", "millimètre": "millimeter", "pouce": "inch", "pied": "foot", "yard": "yard", "mille": "mile"},
        "Poids": {"gramme": "gram", "kilogramme": "kilogram", "livre": "pound", "once": "ounce", "tonne": "tonne"},
        "Surface": {"mètre carré": "square_meter", "kilomètre carré": "square_kilometer", "hectare": "hectare", "acre": "acre", "mile carré": "square_mile"},
        "Volume": {"litre": "liter", "millilitre": "milliliter", "gallon": "gallon", "mètre cube": "cubic_meter", "tasse": "cup"},
        "Température": {"celsius": "degC", "fahrenheit": "degF", "kelvin": "kelvin"}
    }
    currency_map = {
        "euro": "EUR", "dollar américain": "USD", "livre sterling": "GBP",
        "yen japonais": "JPY", "dollar canadien": "CAD", "franc suisse": "CHF"
    }
    taux_local = {
        ("EUR", "USD"): 1.08, ("USD", "EUR"): 0.93, ("EUR", "GBP"): 0.86, ("GBP", "EUR"): 1.16,
        ("USD", "GBP"): 0.79, ("GBP", "USD"): 1.26, ("EUR", "JPY"): 165.25, ("JPY", "EUR"): 0.006,
        ("EUR", "CHF"): 0.98, ("CHF", "EUR"): 1.02, ("EUR", "CAD"): 1.46, ("CAD", "EUR"): 0.68
    }

    category = st.selectbox("Catégorie", list(unit_map.keys()) + ["Devise"])
    value = st.number_input("Valeur à convertir", value=1.0)

    if category == "Devise":
        from_cur = st.selectbox("De", currency_map.keys(), key="dev_from")
        to_cur = st.selectbox("Vers", currency_map.keys(), key="dev_to")
        from_code, to_code = currency_map[from_cur], currency_map[to_cur]
        if from_code == to_code:
            result = value
        else:
            taux = taux_local.get((from_code, to_code))
            result = value * taux if taux else None
        if result:
            st.success(f"{value} {from_cur} = {result:.2f} {to_cur}")
        else:
            st.error("Taux non disponible.")
    else:
        units_fr = list(unit_map[category].keys())
        from_unit = st.selectbox("De", units_fr, key="from_unit")
        to_unit = st.selectbox("Vers", units_fr, key="to_unit")

        if st.button("🔄 Inverser les unités"):
            from_unit, to_unit = to_unit, from_unit

        u_from = unit_map[category][from_unit]
        u_to = unit_map[category][to_unit]
        try:
            q = ureg.Quantity(value, u_from)
            result = q.to(u_to).magnitude
            st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")
        except Exception as e:
            st.error(f"Erreur de conversion : {e}")

# 2️⃣ Dates & Temps
with tab2:
    st.header("📆 Outils de date & temps")
    date1 = st.date_input("Date 1")
    date2 = st.date_input("Date 2")
    st.info(f"Jours entre : {abs((date2 - date1).days)}")
    now = datetime.now()
    st.write(f"Aujourd'hui : {now.strftime('%A %d %B %Y, %H:%M:%S')}")

# 3️⃣ Cuisine
with tab3:
    st.header("🍽️ Convertisseur de cuisine")
    cuisine_map = {
        "sucre": {"cuillère à soupe": 12.5, "cuillère à café": 4.2, "grammes": 1},
        "farine": {"cuillère à soupe": 10, "cuillère à café": 3.3, "grammes": 1},
        "beurre": {"cuillère à soupe": 14, "cuillère à café": 5, "grammes": 1}
    }
    ingr = st.selectbox("Ingrédient", cuisine_map.keys())
    from_c = st.selectbox("De", cuisine_map[ingr].keys())
    to_c = st.selectbox("Vers", cuisine_map[ingr].keys())
    val = st.number_input("Quantité", value=1.0)
    ratio = cuisine_map[ingr][from_c] / cuisine_map[ingr][to_c]
    st.success(f"{val} {from_c} de {ingr} = {val * ratio:.2f} {to_c}")

# 4️⃣ Notes
with tab4:
    st.header("📝 Bloc-notes personnel")
    note = st.text_area("Tes notes ici :", value=st.session_state.get("notes", ""), height=200)
    if st.button("💾 Sauvegarder la note"):
        st.session_state["notes"] = note
        st.success("Note sauvegardée !")

# 5️⃣ Fun
with tab5:
    st.header("🎲 Outils fun & aléatoires")
    a = st.number_input("Min", value=1)
    b = st.number_input("Max", value=10)
    if st.button("🎰 Tirer un nombre"):
        st.success(f"Résultat : {random.randint(int(a), int(b))}")

    st.subheader("📋 Choix dans une liste")
    liste = st.text_area("Liste (séparée par virgules)", "pizza, burger, sushi")
    if st.button("🎯 Choisir au hasard"):
        items = [i.strip() for i in liste.split(",") if i.strip()]
        st.success(f"Choix aléatoire : {random.choice(items)}") if items else st.warning("Liste vide")

# 6️⃣ Alertes
with tab6:
    # == ALERTES / MINUTEUR VISUEL ==
    st.header("🔔 Minuteur visuel")
    minutes = st.number_input("⏱️ Durée (minutes)", min_value=1, max_value=120, value=1, key="alert_timer")
    if st.button("▶️ Lancer le minuteur"):
        seconds = int(minutes * 60)
        progress = st.progress(0)
        status_text = st.empty()
        for i in range(seconds):
            remaining = seconds - i
            mins, secs = divmod(remaining, 60)
            status_text.markdown(f"⏳ Temps restant : **{mins:02d}:{secs:02d}**")
            progress.progress(i / seconds)
            time.sleep(1)
        status_text.success("✅ Temps écoulé !")
        progress.progress(1.0)

# 7️⃣ Citation du jour
with tab7:
    st.header("🧠 Citation ou fait du jour")
    citations = [
        "💡 La meilleure façon de prédire l’avenir, c’est de le créer.",
        "🎯 Celui qui déplace une montagne commence par déplacer de petites pierres.",
        "🚀 Le succès, c’est d’aller d’échec en échec sans perdre son enthousiasme.",
        "🧘 Respire profondément. Tout ira bien."
    ]
    if st.button("📢 Afficher une citation aléatoire"):
        st.info(random.choice(citations))

# 8️⃣ Simulateur d'épargne
with tab8:
    st.header("📊 Simulateur d'épargne")
    montant = st.number_input("Montant épargné par mois (€)", value=100)
    mois = st.slider("Nombre de mois", 1, 120, 12)
    total = montant * mois
    st.success(f"En {mois} mois, tu auras épargné : {total:.2f} €")

# == POMODORO ==
with tab9:
    st.header("🧘 Timer Pomodoro visuel")
    if st.button("🍅 Lancer une session Pomodoro"):
        durations = [("Travail", 25 * 60), ("Pause", 5 * 60)]
        for label, duration in durations:
            st.subheader(f"⏱️ Phase : {label}")
            progress = st.progress(0)
            status_text = st.empty()
            for i in range(duration):
                mins, secs = divmod(duration - i, 60)
                status_text.markdown(f"Temps restant : **{mins:02d}:{secs:02d}**")
                progress.progress(i / duration)
                time.sleep(1)
            st.success(f"✅ {label} terminé !")

with tab10:
    st.header("🔍 Recherche Google")
    query = st.text_input("Tape ta recherche")
    if st.button("🔗 Rechercher"):
        st.markdown(f"[Clique ici pour voir les résultats](https://www.google.com/search?q={query.replace(' ', '+')})")

with tab11:
    st.header("📁 Uploader un fichier")
    uploaded = st.file_uploader("Choisis un fichier")
    if uploaded:
        st.success(f"Fichier '{uploaded.name}' reçu ✅")
        st.download_button("📥 Télécharger le fichier", uploaded.read(), file_name=uploaded.name)
    


with tab12:
    st.header("🗓️ Ajouter une tâche au planning")
    task = st.text_input("Tâche à planifier")
    date = st.date_input("Pour quel jour ?")
    if st.button("➕ Ajouter la tâche"):
        st.success(f"Tâche '{task}' prévue pour le {date}")
import string
import random

with tab13:
    st.header("🔐 Générateur de mot de passe")
    length = st.slider("Longueur", 6, 32, 12)
    if st.button("🔒 Générer"):
        mdp = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=length))
        st.code(mdp)
with tab14:
    st.header("🤖 Chatbot IA (local)")
    user_input = st.text_input("Tu :")
    if user_input:
        st.write("Bot :", "Hmm... intéressant !" if "?" in user_input else "Tu peux m'en dire plus ?")
    
import requests

with tab15:
    st.header("📊 Prix des cryptos en direct")
    coins = ["bitcoin", "ethereum", "dogecoin"]
    url = "https://api.coingecko.com/api/v3/simple/price"
    try:
        res = requests.get(url, params={"ids": ",".join(coins), "vs_currencies": "eur"}).json()
        for coin in coins:
            st.metric(label=coin.capitalize(), value=f"{res[coin]['eur']} €")
    except:
        st.error("Erreur de connexion à l'API CoinGecko.")




