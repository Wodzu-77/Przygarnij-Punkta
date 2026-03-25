import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- KONFIGURACJA ---
PLIK_BAZY = "oceny_uczestnikow.csv"
UCZESTNICY = [f"Uczestnik nr {i}" for i in range(1, 81)]
PUNKTY = [f"Punkt nauczania {i}" for i in range(1, 5)]
DNI = [f"Dzień {i}" for i in range(1, 15)]

st.set_page_config(page_title="System Oceniania", layout="centered")

st.title("📋 Panel Oceniania")

# Inicjalizacja pliku bazy, jeśli nie istnieje
if not os.path.exists(PLIK_BAZY):
    df_init = pd.DataFrame(columns=["Data", "Instruktor", "Dzien", "Punkt", "Uczestnik", "Ocena"])
    df_init.to_csv(PLIK_BAZY, index=False)

# --- FORMULARZ ---
with st.form("form_oceny", clear_on_submit=True):
    instruktor = st.text_input("Imię/Nazwisko Instruktor")
    dzien = st.selectbox("Wybierz Dzień", DNI)
    punkt = st.selectbox("Wybierz Punkt Nauczania", PUNKTY)
    uczestnik = st.selectbox("Wybierz Uczestnika", UCZESTNICY)
    ocena = st.select_slider("Ocena", options=[1, 2, 3, 4, 5])
    
    submit = st.form_submit_button("ZAPISZ OCENĘ")

    if submit:
        if instruktor:
            nowa_ocena = {
                "Data": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Instruktor": instruktor,
                "Dzien": dzien,
                "Punkt": punkt,
                "Uczestnik": uczestnik,
                "Ocena": ocena
            }
            df = pd.read_csv(PLIK_BAZY)
            df = pd.concat([df, pd.DataFrame([nowa_ocena])], ignore_index=True)
            df.to_csv(PLIK_BAZY, index=False)
            st.success(f"Dodano ocenę {ocena} dla {uczestnik}!")
        else:
            st.error("Proszę wpisać imię instruktora!")

# --- PODGLĄD DANYCH ---
if st.checkbox("Pokaż tabelę wyników"):
    df_view = pd.read_csv(PLIK_BAZY)
    st.dataframe(df_view.tail(10)) # pokazuje 10 ostatnich ocen
    st.download_button("Pobierz wszystko (CSV)", df_view.to_csv(index=False), "wyniki.csv")
