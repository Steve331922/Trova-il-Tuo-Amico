
import tkinter as tk
from tkinter import messagebox
import requests
API_KEY = "" #va inserita una chiave API personale
API_URL = "https://api.groq.com/openai/v1/chat/completions"
NOMI_ANIMALI = ["cane", "gatto", "coniglio", "cavia", "pesci", "testuggine", "tartarughe_dacqua", "serpenti", "ragni", "pappagallo", "salamandra", "rana", "camaleonte", "iguana", "insetti"]
NECESSITA_GIARDINO = ["tanto", "", "tanto", "poco", "", "tanto", "poco", "", "", "", "", "", "", "poco", ""]
TEMPO_GIORNALIERO = [3, 1, 1, 1, 0.25, 1, 0.5, 0.17, 0.09, 3, 0.17, 0.26, 0.34, 1, 0.1]
BUDGET = [175, 70, 50, 40, 50, 30, 50, 50, 20, 100, 30, 40, 70, 100, 20]
TIPOLOGIA = ["mammifero", "mammifero", "mammifero", "mammifero", "pesci", "rettili", "rettili", "rettili", "aracnidi", "uccelli", "anfibi", "anfibi", "rettili", "rettili", "insetti"]
PERSONALITA = ["energico", "silenzioso", "silenzioso", "silenzioso", "silenzioso", "silenzioso", "silenzioso", "silenzioso", "silenzioso", "energico", "silenzioso", "energico", "silenzioso", "silenzioso", "energico"]
COMODITA_VIAGGIARE = ["poco", "poco", "poco", "poco", "tanto", "poco", "poco", "tanto", "tanto", "tanto", "poco", "poco", "poco", "poco", "tanto"]
NOTTURNO = ["", "sì", "sì", "sì", "", "", "", "sì", "sì", "", "sì", "sì", "sì", "", "sì"]
FOBIE_ANIMALI = ["Cinofobia", "Ailurofobia", "", "", "Ichthyofobia", "Herpetofobia", "erpetofobia", "erpetofobia", "Aracnofobia", "Ornitofobia", "Batrachofobia", "Batrachofobia", "erpetofobia", "erpetofobia", "Entomofobia", "Nessuna"]
ALLERGENI_ANIMALI = ["pelo di animale", "pelo di animale", "pelo di animale", "pelo di animale", "", "", "", "", "insetti", "piume", "", "", "", "", "insetti"]

COLORS = {
    'primary_green': '#1B7A4D',
    'light_green': '#85E0A3',
    'dark_green': '#0F5C39',
    'white': '#FFFFFF',
    'light_gray': '#F5F7F6',
    'text_dark': '#1A1A1A',
    'hover_green': '#4CAF7F',
    'accent': '#2ECC71'
}

FONTS = {
    'title': ('Segoe UI', 32, 'bold'),
    'heading': ('Segoe UI', 22, 'bold'),
    'text': ('Segoe UI', 15),
    'button': ('Segoe UI', 13, 'bold'),
    'small': ('Segoe UI', 11)
}

def crea_bottone(parent, text, command, width=None, px=40, py=20):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=FONTS['button'],
        bg=COLORS['primary_green'],
        fg=COLORS['white'],
        activebackground=COLORS['accent'],
        activeforeground=COLORS['white'],
        relief='flat',
        bd=0,
        padx=px,
        pady=py,
        cursor='hand2',
        highlightthickness=0
    )
    if width:
        btn.config(width=width)

    def on_enter(e):
        btn.config(bg=COLORS['accent'])

    def on_leave(e):
        btn.config(bg=COLORS['primary_green'])

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    return btn

def crea_radio(parent, text, variable, value):
    return tk.Radiobutton(
        parent,
        text=text,
        variable=variable,
        value=value,
        font=FONTS['text'],
        bg=COLORS['white'],
        fg=COLORS['text_dark'],
        selectcolor=COLORS['light_green'],
        activebackground=COLORS['light_gray'],
        activeforeground=COLORS['text_dark'],
        relief='flat',
        bd=0,
        padx=20,
        pady=12,
        highlightthickness=0
    )

def crea_entry(parent, width=10):
    return tk.Entry(
        parent,
        font=FONTS['text'],
        width=width,
        relief='solid',
        bd=1,
        bg=COLORS['white'],
        fg=COLORS['text_dark'],
        insertbackground=COLORS['primary_green']
    )

def chiedi_ai_razza(animale_consigliato, dati_utente):
    try:
        prompt = f"""
        Basandoti sui seguenti dati di un utente che cerca un animale domestico, suggerisci 2-3 razze specifiche di {animale_consigliato} che sarebbero ideali per questa persona.

        DATI UTENTE:
        - Ore disponibili al giorno: {dati_utente['ore_disponibili']}
        - Budget mensile: €{dati_utente['budget']}
        - Ha un giardino: {dati_utente['ha_giardino']}
        - Esperienza precedente con animali: {dati_utente['esperienza_precedente']}
        - Frequenza di viaggio: {dati_utente['viaggia']}
        - Preferisce dormire tanto: {dati_utente['piace_dormire']}
        - Personalità animale desiderata: {dati_utente['personalita_desiderata']}
        - Ha allergie: {dati_utente['allergie']}
        {f"- Tipo di allergia: {dati_utente['tipo_allergia']}" if dati_utente.get('tipo_allergia') else ""}

        Fornisci una risposta strutturata con:
        1. 2-3 razze specifiche consigliate
        2. Breve spiegazione del perché ogni razza è adatta
        3. Consigli specifici per la cura

        Rispondi in italiano e sii conciso ma informativo. Non usare tabelle o altre cose che non siano leggibili in una finestra Tkinter
        """

        payload = {
            "model": "openai/gpt-oss-120b", #la versione può diventare obsoleta o non disponibile, ultima volta che è stata aggiornata 13/10/2026
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1200, #i token potrebbero non essere sufficenti per versioni più aggiornate del modello
            "temperature": 0.7
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }

        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        return "Errore: connessione scaduta. Riprova tra qualche istante."

    except requests.exceptions.ConnectionError:
        return "Errore: impossibile connettersi a Groq. Controlla la connessione Internet."

    except requests.exceptions.RequestException:
        return "Errore: problema durante la richiesta all'API di Groq."

    except (ValueError, KeyError, IndexError, TypeError):
        return "Errore: risposta dell'API non valida o inattesa."

def mostra_risultato_finale(animale, punteggio, suggerimento_ai):
    for widget in frame.winfo_children():
        widget.destroy()

    main_container = tk.Frame(frame, bg=COLORS['white'])
    main_container.pack(fill=tk.BOTH, expand=True)

    header_frame = tk.Frame(main_container, bg=COLORS['primary_green'], padx=40, pady=40)
    header_frame.pack(fill=tk.X)

    tk.Label(
        header_frame,
        text="Il tuo Animale ideale",
        font=FONTS['title'],
        bg=COLORS['primary_green'],
        fg=COLORS['white']
    ).pack(pady=(0, 20))

    tk.Label(
        header_frame,
        text=f"Animale consigliato: {animale.upper()}",
        font=FONTS['heading'],
        bg=COLORS['primary_green'],
        fg=COLORS['white']
    ).pack(pady=10)

    tk.Label(
        header_frame,
        text=f"Punteggio compatibilità: {punteggio}",
        font=FONTS['text'],
        bg=COLORS['primary_green'],
        fg=COLORS['white']
    ).pack(pady=10)

    content_frame = tk.Frame(main_container, bg=COLORS['white'])
    content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

    ai_label = tk.Label(
        content_frame,
        text="Razze consigliate dall'AI",
        font=FONTS['heading'],
        bg=COLORS['white'],
        fg=COLORS['primary_green']
    )
    ai_label.pack(pady=(0, 30), anchor='w')

    text_area = tk.Text(
        content_frame,
        wrap=tk.WORD,
        font=FONTS['text'],
        bg=COLORS['light_gray'],
        fg=COLORS['text_dark'],
        relief='solid',
        bd=2,
        padx=20,
        pady=20
    )
    text_area.pack(fill=tk.BOTH, expand=True, pady=(0, 30))
    text_area.insert(tk.END, suggerimento_ai)
    text_area.config(state=tk.DISABLED)

    button_frame = tk.Frame(content_frame, bg=COLORS['white'])
    button_frame.pack(fill=tk.X)

    crea_bottone(button_frame, "Chiudi Applicazione", root.quit, px=30, py=15).pack(pady=20)

def scegli_opzione(titolo, opzioni, callback):
    for widget in frame.winfo_children():
        widget.destroy()

    main_container = tk.Frame(frame, bg=COLORS['primary_green'])
    main_container.pack(fill=tk.BOTH, expand=True)

    left_section = tk.Frame(main_container, bg=COLORS['white'])
    left_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=60, pady=60)

    title_label = tk.Label(
        left_section,
        text=titolo,
        font=FONTS['heading'],
        bg=COLORS['white'],
        fg=COLORS['primary_green'],
        wraplength=400,
        justify=tk.LEFT
    )
    title_label.pack(pady=(0, 40), anchor='nw')

    options_frame = tk.Frame(left_section, bg=COLORS['white'])
    options_frame.pack(fill=tk.BOTH, expand=True, anchor='nw')

    var = tk.StringVar(value="")

    for opzione in opzioni:
        radio_frame = tk.Frame(options_frame, bg=COLORS['white'], padx=15, pady=15)
        radio_frame.pack(fill=tk.X, anchor="w")

        radio = crea_radio(radio_frame, opzione.capitalize(), var, opzione)
        radio.pack(anchor="w")

    right_section = tk.Frame(main_container, bg=COLORS['primary_green'])
    right_section.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    button_container = tk.Frame(right_section, bg=COLORS['primary_green'])
    button_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

    crea_bottone(button_container, "Conferma", lambda: callback(var)).pack(expand=True)

def conferma(var):
    if var.get() == "":
        messagebox.showwarning("Attenzione", "Devi selezionare un'opzione!")
    else:
        if current_step == "tipo_animale":
            dati_utente['tipo_animale'] = var.get()
            mostra_fobia()
        elif current_step == "fobia":
            dati_utente['fobia'] = var.get()
            mostra_giardino()
        elif current_step == "giardino":
            dati_utente['ha_giardino'] = var.get()
            mostra_esperienza()
        elif current_step == "esperienza":
            dati_utente['esperienza_precedente'] = var.get()
            mostra_viaggio()
        elif current_step == "viaggio":
            dati_utente['viaggia'] = var.get()
            mostra_dormire()
        elif current_step == "dormire":
            dati_utente['piace_dormire'] = var.get()
            mostra_personalita()
        elif current_step == "personalita":
            dati_utente['personalita_desiderata'] = var.get()
            chiedi_allergia()
        elif current_step == "allergia":
            dati_utente['allergie'] = var.get()
            if var.get() == "Si":
                scegli_opzione("A cosa sei allergico?", ["pelo di animale", "piume", "insetti"], conferma_allergia)
            else:
                mostra_risultato()


def conferma_allergia(var):
    if var.get() == "":
        messagebox.showwarning("Attenzione", "Devi selezionare un'opzione!")
        return
    dati_utente['tipo_allergia'] = var.get()
    mostra_risultato()

def mostra_risultato():
    vn, vincitore = calcola_punteggi(dati_utente)
    suggerimento_ai = chiedi_ai_razza(vn, dati_utente)
    mostra_risultato_finale(vn, vincitore, suggerimento_ai)

def mostra_fobia():
    global current_step
    current_step = "fobia"
    scegli_opzione("Seleziona la tua fobia (se presente)", sorted(set(f for f in FOBIE_ANIMALI if f != "")), conferma)

def mostra_giardino():
    global current_step
    current_step = "giardino"
    scegli_opzione("Hai un giardino?", ["Si", "No"], conferma)

def mostra_esperienza():
    global current_step
    current_step = "esperienza"
    scegli_opzione("Hai già avuto animali prima?", ["Si", "No"], conferma)

def mostra_viaggio():
    global current_step
    current_step = "viaggio"
    scegli_opzione("Ti piace viaggiare?", ["Tanto", "Poco"], conferma)

def mostra_dormire():
    global current_step
    current_step = "dormire"
    scegli_opzione("Quanto ti piace dormire?", ["Tanto", "Poco"], conferma)

def mostra_personalita():
    global current_step
    current_step = "personalita"
    scegli_opzione("Cerchi un animale silenzioso o vivace ed energico?", ["Silenzioso", "Energico"], conferma)

def chiedi_allergia():
    global current_step
    current_step = "allergia"
    scegli_opzione("Sei allergico a qualcosa?", ["Si", "No", "Non lo so"], conferma)

def chiedi_ore_budget():
    for widget in frame.winfo_children():
        widget.destroy()

    main_container = tk.Frame(frame, bg=COLORS['primary_green'])
    main_container.pack(fill=tk.BOTH, expand=True)

    inner_container = tk.Frame(main_container, bg=COLORS['white'])
    inner_container.pack(fill=tk.BOTH, expand=True, padx=60, pady=30)

    title_label = tk.Label(
        main_container,
        text="INIZIAMO IL QUESTIONARIO",
        font=FONTS['title'],
        bg=COLORS['white'],
        fg=COLORS['primary_green']
    )
    title_label.pack(pady=(0, 40))

    time_section = tk.Frame(main_container, bg=COLORS['light_gray'], padx=40, pady=40)
    time_section.pack(fill=tk.X, pady=(0, 40))

    time_title = tk.Label(
        time_section,
        text="Quanto tempo hai da dedicare all'animale al giorno:",
        font=FONTS['heading'],
        bg=COLORS['light_gray'],
        fg=COLORS['text_dark']
    )
    time_title.pack(pady=(0, 30), anchor='w')

    time_frame = tk.Frame(time_section, bg=COLORS['light_gray'])
    time_frame.pack(fill=tk.X)

    tk.Label(time_frame, text="Ore:", font=FONTS['text'], bg=COLORS['light_gray'], fg=COLORS['text_dark']).pack(side=tk.LEFT, padx=(0, 10))
    ore_entry = crea_entry(time_frame, 10)
    ore_entry.pack(side=tk.LEFT, padx=(0, 30))

    tk.Label(time_frame, text="Minuti:", font=FONTS['text'], bg=COLORS['light_gray'], fg=COLORS['text_dark']).pack(side=tk.LEFT, padx=(0, 10))
    minuti_entry = crea_entry(time_frame, 10)
    minuti_entry.pack(side=tk.LEFT)

    budget_section = tk.Frame(main_container, bg=COLORS['light_gray'], padx=40, pady=40)
    budget_section.pack(fill=tk.X, pady=(0, 40))

    budget_title = tk.Label(
        budget_section,
        text="Qual è il tuo budget mensile:",
        font=FONTS['heading'],
        bg=COLORS['light_gray'],
        fg=COLORS['text_dark']
    )
    budget_title.pack(pady=(0, 30), anchor='w')

    budget_frame = tk.Frame(budget_section, bg=COLORS['light_gray'])
    budget_frame.pack(fill=tk.X)

    tk.Label(budget_frame, text="Euro:", font=FONTS['text'], bg=COLORS['light_gray'], fg=COLORS['text_dark']).pack(side=tk.LEFT, padx=(0, 10))
    budget_entry = crea_entry(budget_frame, 10)
    budget_entry.pack(side=tk.LEFT, padx=(0, 30))

    tk.Label(budget_frame, text="Centesimi:", font=FONTS['text'], bg=COLORS['light_gray'], fg=COLORS['text_dark']).pack(side=tk.LEFT, padx=(0, 10))
    cent_entry = crea_entry(budget_frame, 10)
    cent_entry.pack(side=tk.LEFT)

    def conferma_budget():
        try:
            ore = int(ore_entry.get() or "0")
            minuti = int(minuti_entry.get() or "0")
            budget_euro = int(budget_entry.get() or "0")
            budget_cent = int(cent_entry.get() or "0")
            dati_utente['ore_disponibili'] = ore + minuti / 60
            dati_utente['budget'] = budget_euro + budget_cent / 100
            mostra_tipo_animale()
        except ValueError:
            messagebox.showerror("Errore", "Inserisci valori numerici validi.")

    crea_bottone(main_container, "Continua", conferma_budget, px=35, py=18).pack(pady=40)

def calcola_punteggi(dati_utente):
    punti = [0] * len(NOMI_ANIMALI)
    vincitore = -10000000000000
    vn = ""

    for i in range(len(NOMI_ANIMALI)):
        if dati_utente['ore_disponibili'] >= TEMPO_GIORNALIERO[i]:
            punti[i] += 1
        else:
            punti[i] -= 1

        if dati_utente['budget'] >= BUDGET[i]:
            punti[i] += 1
        else:
            punti[i] -= 1

        if dati_utente['tipo_animale'] == TIPOLOGIA[i]:
            punti[i] += 10
        else:
            punti[i] -= 5


        if dati_utente['fobia'] == FOBIE_ANIMALI[i] and dati_utente['fobia']!="Nessuna": # se ha la fobia lo butto fuori
            punti[i] -= 10000

        if dati_utente['ha_giardino'] == "Si":
            if NECESSITA_GIARDINO[i] == "tanto":
                punti[i] += 2
            elif NECESSITA_GIARDINO[i] == "poco":
                punti[i] += 1

        if dati_utente['esperienza_precedente'] == "Si":
            punti[i] += 3

        if dati_utente['piace_dormire'] == "Tanto" and NOTTURNO[i] == "sì":
            punti[i] += 1

        if dati_utente['personalita_desiderata'] == "Energico" and PERSONALITA[i] == "energico":
            punti[i] += 1
        elif dati_utente['personalita_desiderata'] == "Silenzioso" and PERSONALITA[i] == "silenzioso":
            punti[i] += 1

        if dati_utente['allergie'] == "Si" and dati_utente.get('tipo_allergia') == ALLERGENI_ANIMALI[i]:
            punti[i] -= 5
        elif dati_utente['allergie'] == "Non lo so" and ALLERGENI_ANIMALI[i] == "":
            punti[i] += 3

        if punti[i] > vincitore:
            vincitore = punti[i]
            vn = NOMI_ANIMALI[i]

    return vn, vincitore

def mostra_tipo_animale():
    global current_step
    current_step = "tipo_animale"
    scegli_opzione("Seleziona il tipo di animale che preferisci", ["mammifero", "rettile", "anfibio", "uccelli", "aracnidi", "insetti"], conferma)

def main():
    global root, frame, dati_utente, current_step

    root = tk.Tk()
    root.state('zoomed')
    root.title("Trova il Tuo Animale Ideale")
    root.configure(bg=COLORS['white'])

    frame = tk.Frame(root, bg=COLORS['white'])
    frame.pack(fill=tk.BOTH, expand=True)

    dati_utente = {}
    current_step = ""

    chiedi_ore_budget()
    root.mainloop()

if __name__ == "__main__":
    main()
