from tkinter import *
from tkinter import messagebox

# Paprasti klausimai: tekstas, pasirinkimai, teisingas.
# Kiekvienas klausimas turi rodomą tekstą ir kelis pasirinkimus.
klausimai = [
    {
        "tekstas": "Klausimas " + str(i +1),
        "pasirinkimai": [("Variantas1", "1"), ("Variantas2", "2"), ("Variantas3", "3")],
        "teisingas": "2"
    }
    for i in range(10)
]

# Būsena:
# dabartinis – rodomo klausimo indeksas
# atsakymai – naudotojo pasirinkimų žemėlapis (indeksas -> reikšmė)
# liko – kiek sekundžių liko laikmačiui
dabartinis =0
atsakymai = {}
liko =60

# Funkcija: pradėti testą nuo pradžių.
# Veiksmai: nustato pradinę būseną, paslepia pradžios langą, sukuria testo langą.
def pradeti():
    global dabartinis, atsakymai, liko
    dabartinis =0
    atsakymai = {}
    liko =60
    pagrindinis.withdraw() # paslepiame pagrindinį langą
    sukurti_testo_lang()

# Funkcija: sukurti testo langą.
# Veiksmai: sukuria sritis klausimui, laikui, pasirinkimams ir mygtukams.
# Viskas išdėstoma su place(), nenaudojant pack().
def sukurti_testo_lang():
    global testas

    testas = Toplevel()
    testas.title("KET Testas")
    testas.geometry("560x420")
    testas.minsize(520,380)

    # Viršus: klausimo tekstas
    virsus = Frame(testas)
    virsus.place(x=16, y=12, width=528, height=40)

    klausimo_zenklelis = Label(virsus, text="", font=("Arial",16, "bold"))
    klausimo_zenklelis.place(x=0, y=0)

    # Laiko rodymas dešinėje
    laiko_remas = Frame(testas)
    laiko_remas.place(x=16, y=56, width=528, height=28)

    laikmatis_zenklelis = Label(laiko_remas, text="Laikas: " + str(liko) + " s", font=("Arial",12))
    laikmatis_zenklelis.place(x=408, y=0) # paprasta dešinė zona

    # Pasirinkimų sritis
    pasirinkimu_remas = Frame(testas, bd=1, relief="ridge")
    pasirinkimu_remas.place(x=16, y=92, width=528, height=250)

    # Kintamasis radiomygtukų grupei
    pasirinkimas = StringVar()

    # Mygtukai apačioje: Atgal, Kitas, Baigti
    mygtuku_remas = Frame(testas)
    mygtuku_remas.place(x=16, y=352, width=528, height=40)

    mygtukas_atgal = Button(mygtuku_remas, text="Atgal", width=12, command=atgal)
    mygtukas_atgal.place(x=0, y=0)

    mygtukas_kitas = Button(mygtuku_remas, text="Kitas", width=12, command=kitas, state=DISABLED)
    mygtukas_kitas.place(x=140, y=0)

    mygtukas_baigti = Button(mygtuku_remas, text="Baigti", width=12, command=baigti)
    mygtukas_baigti.place(x=280, y=0)

    # Būsena apačioje: rodom ar pasirinkta
    busenos_zenklelis = Label(testas, text="Nepasirinkta", font=("Arial",10))
    busenos_zenklelis.place(x=16, y=396)

    # Pagalbinė funkcija: įjungti/išjungti „Kitas“ pagal pasirinkimą
    def ijungti_kita():
        if pasirinkimas.get():
            mygtukas_kitas.config(state=NORMAL)
        else:
            mygtukas_kitas.config(state=DISABLED)

    # Išsaugome nuorodas į valdiklius objekte testas
    testas.klausimo_zenklelis = klausimo_zenklelis
    testas.pasirinkimu_remas = pasirinkimu_remas
    testas.pasirinkimas = pasirinkimas
    testas.mygtukas_kitas = mygtukas_kitas
    testas.busenos_zenklelis = busenos_zenklelis
    testas.ijungti_kita = ijungti_kita
    testas.laikmatis_zenklelis = laikmatis_zenklelis

    # Parodome pirmą klausimą ir paleidžiame laikmatį
    rodyti_klausima()
    tikseti()

# Funkcija: parodyti dabartinį klausimą ir jo atsakymo variantus.
# Veiksmai: nustato tekstą, išvalo senus pasirinkimus, sukuria naujus radiomygtukus, atnaujina būseną.
def rodyti_klausima():
    q = klausimai[dabartinis]
    testas.klausimo_zenklelis.config(text=str(dabartinis +1) + "/" + str(len(klausimai)) + " - " + q["tekstas"]) # pvz.: "1/10 - Klausimas1"

    # Išvalome senus radiomygtukus
    for valdiklis in testas.pasirinkimu_remas.winfo_children():
        valdiklis.destroy()

    # Atstatome anksčiau pasirinktas reikšmes
    testas.pasirinkimas.set(atsakymai.get(dabartinis, ""))

    # Sukuriame naujus radiomygtukus su place()
    indeksas =1
    for pasirinkimas_item in q["pasirinkimai"]:
        tekstas = pasirinkimas_item[0]
        reiksme = pasirinkimas_item[1]
        Radiobutton(
            testas.pasirinkimu_remas,
            text=str(indeksas) + ". " + tekstas,
            value=reiksme,
            variable=testas.pasirinkimas,
            command=testas.ijungti_kita,
        ).place(x=10, y=10 + (indeksas -1) *32)
        indeksas = indeksas +1

    # Atnaujiname mygtuko „Kitas“ būseną
    testas.ijungti_kita()

    # Atnaujiname būsenos tekstą
    if atsakymai.get(dabartinis):
        testas.busenos_zenklelis.config(text="Pasirinkta")
    else:
        testas.busenos_zenklelis.config(text="Nepasirinkta")

# Funkcija: išsaugoti dabartinį pasirinkimą.
# Veiksmai: jei yra pasirinkta, įrašo į žemėlapį ir atnaujina būseną.
def issaugoti():
    if testas.pasirinkimas.get():
        atsakymai[dabartinis] = testas.pasirinkimas.get()
    testas.busenos_zenklelis.config(text="Pasirinkta")

# Funkcija: eiti į ankstesnį klausimą.
# Veiksmai: jei įmanoma, išsaugo pasirinkimą, pereina atgal, parodo klausimą.
def atgal():
    global dabartinis
    if dabartinis >0:
        issaugoti()
        dabartinis = dabartinis -1
        rodyti_klausima()

# Funkcija: eiti į kitą klausimą (arba baigti testą, jei tai paskutinis).
# Veiksmai: saugo pasirinkimą, pereina pirmyn, arba kviečia baigti().
def kitas():
    global dabartinis
    issaugoti()
    paskutinis = len(klausimai) -1
    if dabartinis < paskutinis:
        dabartinis = dabartinis +1
        rodyti_klausima()
    else:
        baigti()

# Funkcija: paprastas laikmatis.
# Veiksmai: kas sekundę mažina „liko“, atnaujina tekstą, ir jei pasibaigė – baigia testą.
def tikseti():
    global liko
    if not testas.winfo_exists():
        return
    if liko <=0:
        baigti()
        return
    liko = liko -1
    testas.laikmatis_zenklelis.config(text="Laikas: " + str(liko) + " s")
    testas.after(1000, tikseti)

# Funkcija: baigti testą.
# Veiksmai: išsaugo pasirinkimus, uždaro testą, parodo rezultatų langą.
def baigti():
    issaugoti()
    if testas.winfo_exists():
        testas.destroy()
    rodyti_rezultatus()

# Funkcija: rodyti rezultatų langą.
# Veiksmai: suskaičiuoja teisingus atsakymus ir sukuria mygtukus peržiūrai/grįžimui.
# UI taip pat naudoja place(), jokio pack.
def rodyti_rezultatus():
    langas = Toplevel()
    langas.title("Rezultatai")
    langas.geometry("520x240")

    # rezultatų tekstas
    teisingi =0
    i =0
    while i < len(klausimai):
        if atsakymai.get(i) == klausimai[i]["teisingas"]:
            teisingi = teisingi +1
        i = i +1

    antraste = Label(langas, text="Jūsų rezultatas: " + str(teisingi) + " / " + str(len(klausimai)), font=("Arial",16, "bold"))
    antraste.place(x=16, y=16)

    mygtuku_remas = Frame(langas)
    mygtuku_remas.place(x=16, y=64, width=488, height=40)

    Button(mygtuku_remas, text="Peržiūrėti atsakymus", command=lambda: perziura(langas), width=20).place(x=0, y=0)
    Button(mygtuku_remas, text="Grįžti į pradžią", command=lambda: (langas.destroy(), pagrindinis.deiconify()), width=20).place(x=200, y=0)

# Funkcija: rodyti peržiūros langą su visais atsakymais.
# Veiksmai: sukuria paprastą sąrašą; išdėstymas su place().
def perziura(rezultatu_langas):
    perziuros_langas = Toplevel()
    perziuros_langas.title("Atsakymų peržiūra")
    perziuros_langas.geometry("600x420")

    vidus = Frame(perziuros_langas)
    vidus.place(x=16, y=16, width=568, height=388)

    # kiekvieną bloką dedame po80 px aukščiu
    i =0
    while i < len(klausimai):
        q = klausimai[i]
        virsus_y =8 + i *80

        Label(vidus, text="Klausimas " + str(i +1) + ": " + q["tekstas"], font=("Arial",12, "bold")).place(x=0, y=virsus_y)

        # teisingo atsakymo tekstas
        teisingas_tekstas = "-"
        j =0
        while j < len(q["pasirinkimai"]):
            t = q["pasirinkimai"][j][0]
            v = q["pasirinkimai"][j][1]
            if v == q["teisingas"]:
                teisingas_tekstas = t
            j = j +1

        # pasirinkto atsakymo tekstas
        pasirinktas_tekstas = "-"
        k =0
        while k < len(q["pasirinkimai"]):
            t2 = q["pasirinkimai"][k][0]
            v2 = q["pasirinkimai"][k][1]
            if v2 == atsakymai.get(i, ""):
                pasirinktas_tekstas = t2
            k = k +1

        Label(vidus, text="Jūsų: " + pasirinktas_tekstas).place(x=0, y=virsus_y +26)
        Label(vidus, text="Teisingas: " + teisingas_tekstas).place(x=0, y=virsus_y +46)

        i = i +1

# Pagrindinis langas (pradžia): viskas su place(), be pack().
pagrindinis = Tk()
pagrindinis.title("KET Testas")
pagrindinis.geometry("360x180")

sakninis_remas = Frame(pagrindinis)
sakninis_remas.place(x=20, y=20, width=320, height=140)

# Antraštės
Label(sakninis_remas, text="KET Testas", font=("Arial",16, "bold")).place(x=0, y=0)


# Mygtukų sritis – tik place()
mygtuku_sritis = Frame(sakninis_remas)
mygtuku_sritis.place(x=0, y=64, width=300, height=60)

button_pradeti = Button(mygtuku_sritis, text="Pradėti testą", command=pradeti, width=20)
button_pradeti.place(x=0, y=0)

button_iseiti = Button(mygtuku_sritis, text="Išeiti", command=pagrindinis.destroy, width=20)
button_iseiti.place(x=0, y=32)

buttom_apie = Button(mygtuku_sritis, text="Apie").place(relx=0.8, y=32)

# Paleidžiame programą
pagrindinis.mainloop()
