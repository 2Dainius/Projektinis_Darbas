from tkinter import *
from tkinter import messagebox

quiz = None
timer = None
pagrindinis = None
testas = None
laikmacio_after_id = None

def sukurti_gui(root, quiz_obj, timer_obj):
    global quiz, timer, pagrindinis
    quiz = quiz_obj
    timer = timer_obj
    pagrindinis = root

    pagrindinis.title("KET Testas")
    pagrindinis.geometry("360x180")

    sakninis_remas = Frame(pagrindinis)
    sakninis_remas.place(x=20, y=20, width=320, height=140)

    Label(sakninis_remas, text="KET Testas", font=("Arial",16, "bold")).place(x=0, y=0)

    mygtuku_sritis = Frame(sakninis_remas)
    mygtuku_sritis.place(x=0, y=64, width=300, height=60)

    Button(mygtuku_sritis, text="Pradėti testą", command=pradeti, width=20).place(x=0, y=0)
    Button(mygtuku_sritis, text="Išeiti", command=pagrindinis.destroy, width=20).place(x=0, y=32)
    Button(mygtuku_sritis, text="Apie").place(relx=0.8, y=32)


def pradeti():
    global laikmacio_after_id

    timer.stop()
    if laikmacio_after_id is not None and pagrindinis.winfo_exists():
        try:
            pagrindinis.after_cancel(laikmacio_after_id)
        except Exception:
            pass
        laikmacio_after_id = None

    timer.reset() # reset timer without turning the app off

    quiz.current_index = 0
    quiz.user_answers = [None] * len(quiz.questions)
    quiz.finished = False

    pagrindinis.withdraw()
    sukurti_testo_lang()
    timer.start()
    atnaujinti_laikmati()


def sukurti_testo_lang():
    global testas

    testas = Toplevel(pagrindinis)
    testas.title("KET Testas")
    testas.geometry("560x420")
    testas.minsize(520, 380)

    virsus = Frame(testas)
    virsus.place(x=16, y=12, width=528, height=70)

    klausimo_zenklelis = Label(virsus, text="", font=("Arial", 14, "bold"), justify=LEFT, anchor="w")
    klausimo_zenklelis.place(x=0, y=0)
    klausimo_zenklelis.config(wraplength=520)

    laiko_remas = Frame(testas)
    laiko_remas.place(x=16, y=86, width=528, height=28)

    laikmatis_zenklelis = Label(laiko_remas, text="Laikas: -- s", font=("Arial", 12))
    laikmatis_zenklelis.place(x=408, y=0)

    pasirinkimu_remas = Frame(testas, bd=1, relief="ridge")
    pasirinkimu_remas.place(x=16, y=122, width=528, height=220)

    pasirinkimas = IntVar(value=-1)

    mygtuku_remas = Frame(testas)
    mygtuku_remas.place(x=16, y=352, width=528, height=40)

    mygtukas_atgal = Button(mygtuku_remas, text="Atgal", width=12, command=atgal)
    mygtukas_atgal.place(x=0, y=0)

    mygtukas_kitas = Button(mygtuku_remas, text="Kitas", width=12, command=kitas, state=DISABLED)
    mygtukas_kitas.place(x=140, y=0)

    mygtukas_baigti = Button(mygtuku_remas, text="Baigti", width=12, command=baigti)
    mygtukas_baigti.place(x=280, y=0)

    busenos_zenklelis = Label(testas, text="Nepasirinkta", font=("Arial", 10))
    busenos_zenklelis.place(x=16, y=396)

    def ijungti_kita():
        if testas.pasirinkimas.get() != -1:
            testas.mygtukas_kitas.config(state=NORMAL)
            testas.busenos_zenklelis.config(text="Pasirinkta") # atnaujina statusą
        else:
            testas.mygtukas_kitas.config(state=DISABLED)
            testas.busenos_zenklelis.config(text="Nepasirinkta") # atnaujina statusą


    testas.klausimo_zenklelis = klausimo_zenklelis
    testas.pasirinkimu_remas = pasirinkimu_remas
    testas.pasirinkimas = pasirinkimas
    testas.mygtukas_kitas = mygtukas_kitas
    testas.busenos_zenklelis = busenos_zenklelis
    testas.ijungti_kita = ijungti_kita
    testas.laikmatis_zenklelis = laikmatis_zenklelis

    rodyti_klausima()


def rodyti_klausima():
    q = quiz.get_current_question()


    testas.klausimo_zenklelis.config(
        text=f"{quiz.current_index + 1}/{len(quiz.questions)} - {q['question']}"
    )


    for w in testas.pasirinkimu_remas.winfo_children():
        w.destroy()


    prev = quiz.user_answers[quiz.current_index]
    testas.pasirinkimas.set(prev if prev is not None else -1)


    for i, option_text in enumerate(q["options"]):
        Radiobutton(
            testas.pasirinkimu_remas,
            text=f"{i+1}. {option_text}",
            value=i,                     # 0..3
            variable=testas.pasirinkimas,
            command=testas.ijungti_kita
        ).place(x=10, y=10 + i * 32)

    testas.ijungti_kita()

    testas.busenos_zenklelis.config(
        text="Pasirinkta" if quiz.user_answers[quiz.current_index] is not None else "Nepasirinkta"
    )

def issaugoti():
    val = testas.pasirinkimas.get()
    if val != -1:
        quiz.answer(val)
        testas.busenos_zenklelis.config(text="Pasirinkta")


def atgal():
    if quiz.current_index > 0:
        issaugoti()
        quiz.previous()
        rodyti_klausima()


def kitas():
    issaugoti()
    if quiz.current_index < len(quiz.questions) - 1:
        quiz.next()
        rodyti_klausima()
    else:
        baigti()


def baigti():
    global laikmacio_after_id
    issaugoti()
    timer.stop()
    if laikmacio_after_id is not None:
        try:
            testas.after_cancel(laikmacio_after_id)
        except Exception:
            pass
        laikmacio_after_id = None

    if testas and testas.winfo_exists():
        testas.destroy()
    rodyti_rezultatus()


def rodyti_rezultatus():
    langas = Toplevel(pagrindinis)
    langas.title("Rezultatai")
    langas.geometry("520x240")

    teisingi = quiz.calculate_score()
    Label(langas, text=f"Jūsų rezultatas: {teisingi} / {len(quiz.questions)}",
          font=("Arial",16, "bold")).place(x=16, y=16)

    Button(langas, text="Grįžti į pradžią",
           command=lambda: (timer.stop(), langas.destroy(), pagrindinis.deiconify()),
           width=20).place(x=16, y=80)

    Button(langas, text="Peržiūrėti atsakymus",
           command=lambda: perziura(langas),
           width=20).place(x=200, y=80)

def perziura(rezultatu_langas):
    perziuros_langas = Toplevel(pagrindinis)
    perziuros_langas.title("Peržiūra")
    perziuros_langas.geometry("640x420")

    idx = 0  # review index (separate from quiz.current_index)

    klausimas_lbl = Label(perziuros_langas, font=("Arial", 12, "bold"), justify=LEFT, anchor="w")
    klausimas_lbl.place(x=16, y=16, width=608, height=80)

    options_frame = Frame(perziuros_langas)
    options_frame.place(x=16, y=110, width=608, height=220)

    info_lbl = Label(perziuros_langas, font=("Arial", 11), justify=LEFT, anchor="w")
    info_lbl.place(x=16, y=340, width=608, height=30)

    def rodyti():
        nonlocal idx
        q = quiz.questions[idx]
        user = quiz.user_answers[idx]
        correct = q["correct"]

        # question text (wrap so it doesn't cut)
        klausimas_lbl.config(
            text=f"{idx+1}/{len(quiz.questions)} - {q['question']}",
            wraplength=600
        )

        for w in options_frame.winfo_children():
            w.destroy()

        for i, opt in enumerate(q["options"]):
            prefix = ""
            if user is not None and i == user and user != correct:
                prefix = "❌ JŪSŲ: "
            if i == correct:
                prefix = "✅ TEISINGAS: "

            Label(options_frame, text=f"{i+1}. {prefix}{opt}", anchor="w", justify=LEFT, wraplength=580)\
                .pack(anchor="w", pady=3)

        if user is None:
            info_lbl.config(text="Jūsų atsakymas: Neatsakyta")
        else:
            info_lbl.config(text=f"Jūsų atsakymas: {user+1}    Teisingas: {correct+1}")

        btn_back.config(state=NORMAL if idx > 0 else DISABLED)
        btn_next.config(state=NORMAL if idx < len(quiz.questions)-1 else DISABLED)

    def back():
        nonlocal idx
        if idx > 0:
            idx -= 1
            rodyti()

    def nxt():
        nonlocal idx
        if idx < len(quiz.questions)-1:
            idx += 1
            rodyti()

    btn_back = Button(perziuros_langas, text="Atgal", command=back, width=12)
    btn_back.place(x=16, y=375)

    btn_next = Button(perziuros_langas, text="Kitas", command=nxt, width=12)
    btn_next.place(x=150, y=375)

    Button(perziuros_langas, text="Uždaryti", command=perziuros_langas.destroy, width=12)\
        .place(x=512, y=375)

    rodyti()

def atnaujinti_laikmati():
    global laikmacio_after_id

    if testas is None or not testas.winfo_exists():
        laikmacio_after_id = None
        return

    testas.laikmatis_zenklelis.config(text=f"Laikas: {timer.time_left} s")

    if timer.time_left <= 0:
        baigti()
        return

    laikmacio_after_id = testas.after(1000, atnaujinti_laikmati)
