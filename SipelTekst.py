import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font
from tkinter import colorchooser
def valikoik(_=None):
    global tekst
    tekst.tag_add("sel", "1.0", "end")
def ntinfot(_=None):
    messagebox.showinfo("SipelTekst", """SipelTekst on lihtne tekstiredaktor, mille tegi valeNimi4. Litsents GPL v3.""")
def varv(_=None):
    global tekst
    varvinimi = colorchooser.askcolor(title="Vali värv")
    if varvinimi[1]:
        try:
            tekst.configure(fg=varvinimi[1])
        except:
            messagebox.showerror("SipelTekst", "Ilmselt kirjutasid värvi valesti.")
def taust(_=None):
    global tekst
    varvinimi = colorchooser.askcolor(title="Vali värv")
    if varvinimi[1]:
        try:
            tekst.configure(bg=varvinimi[1])
        except:
            messagebox.showerror("SipelTekst", "Ilmselt kirjutasid värvi valesti.")
def vaiksemaks(_=None):
    global font
    if font["size"] > 4:
        font.configure(size=font["size"]-1)
def suuremaks(_=None):
    global font
    if font["size"] < 100:
        font.configure(size=font["size"]+1)
def asenda(_=None):
    global tekst
    asendatekst = simpledialog.askstring("SipelTekst", "Mis teksti tahad asendada?")
    if asendatekst:
        asendaja = simpledialog.askstring("SipelTekst", f"Millega asendad {asendatekst}?")
        if asendaja:
            kiri = tekst.get(1.0, "end")
            kiri = kiri.replace(asendatekst, asendaja)
            tekst.delete(1.0, "end")
            tekst.insert(1.0, kiri)
            return None
    messagebox.showerror("SipelTekst", "Toiming katkestati.")
def otsi(_=None):
    global tekst
    tekst.tag_remove("highlight", "1.0", tk.END)
    otsing = simpledialog.askstring("SipelTekst", "Mida tahad otsida?")
    if otsing:
        pos = tekst.search(otsing, "1.0", stopindex="end")
        if pos:
            tekst.tag_add("highlight", pos, f"{pos}+{len(otsing)}c")
            tekst.tag_configure("highlight", background="lightgreen")
            tekst.see(pos)
        else:
            messagebox.showerror("SipelTekst", f"{otsing} ei leitud.")
def teinefont():
    global font
    fontinimi = simpledialog.askstring("SipelTekst", "Mis fonti tahad kasutada?")
    if fontinimi:
        try:
            font.configure(family=fontinimi)
        except:
            messagebox.showerror("SipelTekst", "Viga!")
def kopeeri(_=None):
    global tekst
    global aken
    try:
        valitud = tekst.get("sel.first", "sel.last")
        aken.clipboard_clear()
        aken.clipboard_append(valitud)
    except:
        pass
def kleebi(_=None):
    global tekst
    global aken
    try:
        tekst.insert("end", aken.clipboard_get())
    except Exception as e:
        print(e)
def kasonsalvestatud():
    global salvestatud
    global failinimi
    if failinimi and salvestatud:
        return "Jah"
    return "Ei"
def tekstiinfo():
    global tekst
    global failinimi
    global muudatused
    global salvestatud
    messagebox.showinfo("SipelTekst",
f"""Failinimi: {failinimi}
Tähemärke: {len(tekst.get(1.0, "end"))}
Ridu: {len(tekst.get(1.0, "end").split("\n"))}
Muudatusi: {len(muudatused)}
Salvestatud: {kasonsalvestatud()}""")
def votatagasi(_=None):
    global undonr
    global muudatused
    global tekst
    global salvestatud
    if undonr > 0:
        undonr -= 1
        tekst.delete(1.0, "end")
        tekst.insert(1.0, muudatused[undonr])
        salvestatud = False
def teeuuesti(_=None):
    global undonr
    global muudatused
    global tekst
    global salvestatud
    if undonr < len(muudatused) - 1:
        undonr += 1
        tekst.delete(1.0, "end")
        tekst.insert(1.0, muudatused[undonr])
        salvestatud = False
def muudatus():
    global automaatsalvestus
    global vanatekst
    global failinimi
    global tekst
    global muudatused
    global undonr
    if automaatsalvestus.get() and not failinimi:
        automaatsalvestus.set(False)
        messagebox.showerror("SipelTekst", "Automaatsalvestust ei saa tööle panna sest pole failinime. Salvesta või ava fail et kasutada seda funktsiooni.")
    if tekst.get(1.0, "end") != vanatekst:
        if automaatsalvestus.get():
            salv()
        vanatekst = tekst.get(1.0, "end")
        undonr += 1
        muudatused.insert(undonr, vanatekst)
    aken.after(100, muudatus)
def polesalvestatud(_):
    global salvestatud
    global failinimi
    global undonr
    global muudatused
    muudatus()
    salvestatud = False
    if failinimi:
        faili_nimi = failinimi
    else:
        faili_nimi = "Nimetu"
    aken.title(faili_nimi+"* - SipelTekst")
    tekst.edit_modified(True)
def uus(_=None):
    global salvestatud
    global failinimi
    global muudatused
    global undonr
    if salvestatud or messagebox.askquestion("SipelTekst", "Fail pole salvestatud!\nTeha ikkagi uus fail?") == "yes":
        undonr = 0
        tekst.delete(1.0, "end")
        failinimi = None
        aken.title("Nimetu - SipelTekst")
        muudatused = [""]
        salvestatud = True
def ava(_=None):
    global failinimi
    global tekst
    global salvestatud
    global muudatused
    global undonr
    if salvestatud or messagebox.askquestion("SipelTekst", "Fail pole salvestatud!\nAvada ikkagi mõni teine fail?") == "yes":
        fail = filedialog.askopenfilename()
        if fail:
            undonr = 0
            failinimi = fail
            aken.title(failinimi+" - SipelTekst")
            tekst.delete(1.0, "end")
            tekst.insert(1.0, open(failinimi).read())
            salvestatud = True
            muudatused = [tekst.get(1.0, "end")]
def salv(_=None):
    global failinimi
    global tekst
    global salvestatud
    if failinimi:
        open(failinimi, "w").write(tekst.get(1.0, "end"))
        aken.title(failinimi+" - SipelTekst")
        salvestatud = True
        return True
    else:
        return salvnim()
def salvnim(_=None):
    global failinimi
    fail = filedialog.asksaveasfilename()
    if fail:
        failinimi = fail
        return salv()
    else:
        return False
def valju(_=None):
    if salvestatud or messagebox.askquestion("SipelTekst", "Fail pole salvestatud!\nSulgeda ikkagi?") == "yes":
        aken.destroy()
        exit()
aken = tk.Tk()
aken.pack_propagate(False)
automaatsalvestus = tk.BooleanVar(value=False)
tugev_kiri = tk.BooleanVar(value=False)
kaldkiri = tk.BooleanVar(value=False)
font = font.Font(family="Arial", slant="roman", weight="normal", size=12)
salvestatud = True
aken.title("Nimetu - SipelTekst")
muudatused = [""]
undonr = 0
vanatekst = ""
aken.after(100, muudatus)
failinimi = None
tekst = tk.Text(aken, wrap="word")
tekst.pack(fill="both", expand=True)
tekst.configure(font=font, fg="black", bg="white")
menuu = tk.Menu(aken)
aken.configure(menu=menuu)
fail = tk.Menu(aken)
fail.add_command(label="Uus", accelerator="Control+n",command=uus)
fail.add_command(label="Ava...", accelerator="Control+o",command=ava)
fail.add_command(label="Salvesta", accelerator="Control+s",command=salv)
fail.add_command(label="Salvesta kui...", accelerator="Control+S",command=salv)
fail.add_checkbutton(label="Automaatsalvestus", variable=automaatsalvestus)
fail.add_separator()
fail.add_command(label="Välju",accelerator="Control+q", command=valju)
redigeerimine = tk.Menu(aken)
redigeerimine.add_command(label="Kopeeri", accelerator="Control+c",command=kopeeri)
redigeerimine.add_command(label="Kleebi", accelerator="Control+v",command=kleebi)
redigeerimine.add_command(label="Vali kõik",accelerator="Control+a", command=valikoik)
redigeerimine.add_separator()
redigeerimine.add_command(label="Võta tagasi", accelerator="Control+z",command=votatagasi)
redigeerimine.add_command(label="Tee uuesti", accelerator="Control+y",command=teeuuesti)
redigeerimine.add_separator()
redigeerimine.add_command(label="Otsi...", accelerator="Control+f",command=otsi)
redigeerimine.add_separator()
redigeerimine.add_command(label="Asenda...", accelerator="Control+r",command=asenda)
vaade = tk.Menu(aken)
vaade.add_command(label="Muuda fonti...", command=teinefont)
vaade.add_separator()
vaade.add_command(label="Tee font suuremaks", accelerator="Control++",command=suuremaks)
vaade.add_command(label="Tee font väiksemaks", accelerator="Control+-",command=vaiksemaks)
vaade.add_separator()
vaade.add_command(label="Muuda teksti värvi...", command=varv)
vaade.add_command(label="Muuda tausta värvi...", command=taust)
infomenuu = tk.Menu(aken)
infomenuu.add_command(label="Teksti info", command=tekstiinfo)
infomenuu.add_command(label="Sipeltekstist", command=ntinfot)
menuu.add_cascade(label="Fail", menu=fail)
menuu.add_cascade(label="Redigeerimine", menu=redigeerimine)
menuu.add_cascade(label="Vaade", menu=vaade)
menuu.add_cascade(label="Info", menu=infomenuu)
tekst.bind("<<Modified>>",polesalvestatud)
aken.bind("<Control-n>", uus)
aken.bind("<Control-q>", valju)
aken.bind("<Control-z>", votatagasi)
aken.bind("<Control-y>", teeuuesti)
aken.bind("<Control-s>", salv)
aken.bind("<Control-c>", kopeeri)
aken.bind("<Control-v>", kleebi)
aken.bind("<Control-f>", otsi)
aken.bind("<Control-r>", asenda)
aken.bind("<Control-S>", salvnim)
aken.bind("<Control-o>", ava)
aken.bind("<Control-a>", valikoik)
aken.bind("<Control-KP_Add>", suuremaks)
aken.bind("<Control-KP_Subtract>", vaiksemaks)
aken.protocol("WM_DELETE_WINDOW", valju)
aken.mainloop()