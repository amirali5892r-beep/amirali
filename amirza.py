"""آمیرزا - بازی ساخت کلمه با Tkinter و کتابخانهٔ استاندارد پایتون."""
import random
import sys
import tkinter as tk
import tkinter.font as tkfont
from collections import Counter

BG = "#241b4a"; BG2 = "#35256b"; CARD = "#fffdf8"; INK = "#2c2750"
GOLD = "#f7bd3d"; GREEN = "#2aa36b"; RED = "#d95464"; MUTED = "#77728b"


def normal(word):
    """یکسان‌سازی شکل‌های عربی حروف و فاصله‌ها برای مقایسهٔ کلمات."""
    return " ".join(str(word).replace("ي", "ی").replace("ى", "ی").replace("ك", "ک").split())


def persian_number(value):
    return str(value).translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))


def score_for(word):
    size = len(normal(word).replace(" ", ""))
    return 10 if size <= 3 else 15 if size == 4 else 20 if size == 5 else 25

# هر بسته با یک واژهٔ رایج و کلمات کوچک‌تر قابل ساخت از همان حروف آغاز می‌شود.
SEEDS = [
("کتاب", "کتاب تاب با تا کات"), ("مادر", "مادر مار دار در"), ("دوست", "دوست دود تو دست"),
("خانه", "خانه خان نان نه"), ("مدرسه", "مدرسه درس مهر سر"), ("بهار", "بهار بار بهر"),
("دریا", "دریا دار یار در"), ("باران", "باران بار ران نار"), ("پنجره", "پنجره پر پن جر"),
("آرام", "آرام مار رام را"), ("سیب", "سیب بی بس"), ("قلم", "قلم قم مل"),
("دفتر", "دفتر در فرد تر"), ("چراغ", "چراغ چار رخ"), ("گلستان", "گلستان گل گلت سال"),
("پرنده", "پرنده پر در نرد"), ("دوچرخه", "دوچرخه دو رخ ده"), ("کبوتر", "کبوتر کوب بر تو"),
("ستاره", "ستاره سر تار راست"), ("زمستان", "زمستان زمین ستان زمان"), ("تابستان", "تابستان تاب تان است"),
("دانش", "دانش دان شان"), ("دوستان", "دوستان دوست دان تان"), ("لبخند", "لبخند لب بند"),
("مهربان", "مهربان مهر بار من"), ("باغبان", "باغبان باغ بان"), ("آفتاب", "آفتاب تاب آب تا"),
("بازار", "بازار بار راز"), ("مسافر", "مسافر سفر سر"), ("دانایی", "دانایی دان نا"),
("کودک", "کودک کوک دو"), ("شادی", "شادی شاد یاد"), ("امید", "امید مید"),
("سلام", "سلام سال مال"), ("سلامت", "سلامت سالم مات"), ("چرخه", "چرخه رخ چه"),
("نقاش", "نقاش نقش ناش"), ("کلاس", "کلاس سال لاس"), ("تلاش", "تلاش تال اش"),
("زمان", "زمان مان زن"), ("زمین", "زمین مین زن"), ("رویا", "رویا رای رو"),
("جوان", "جوان جان جا"), ("خورشید", "خورشید شور خیر"), ("دانه", "دانه دان نه"),
("هوا", "هوا ها وا"), ("کوه", "کوه کوه"), ("رنگ", "رنگ نگر"),
("آینه", "آینه این نه"), ("کاغذ", "کاغذ کاه"),
]

def make_levels():
    """۱۰۰ مرحلهٔ مجزا می‌سازد؛ هر بار یک پاسخ دیگر به بسته اضافه می‌شود."""
    levels = []
    for variant in range(2):
        for base, words in SEEDS:
            target = [normal(x) for x in words.split()]
            # تفاوت نسخه‌ها: در نسخهٔ دوم همهٔ پاسخ‌ها؛ اول پاسخ‌های کوتاه‌تر هم دارد.
            if variant == 0:
                target = target[:min(len(target), 4)]
            letters = list(normal(base))
            # برای جواب‌هایی که ممکن است از حروف واژهٔ اصلی کوتاه‌تر باشند نیازی به تغییر نیست.
            levels.append({"letters": letters, "words": target})
    return validate_levels(levels)


def valid_word(word, letters):
    return not (Counter(normal(word).replace(" ", "")) - Counter(normal("".join(letters))))


def validate_levels(levels):
    clean = []
    for level in levels:
        letters = [normal(x) for x in level.get("letters", []) if normal(x)]
        seen, words = set(), []
        for word in level.get("words", []):
            word = normal(word)
            if word and word not in seen and valid_word(word, letters):
                words.append(word); seen.add(word)
        if letters and words:
            clean.append({"letters": letters, "words": words})
    return clean

LEVELS = make_levels()
# فرهنگ داخلی: پاسخ‌های مراحل + واژه‌های عمومی رایج؛ برای جست‌وجو به اینترنت نیاز نیست.
EXTRA_WORDS = """آب آسمان آتش آدرس آدم آواز آغاز آغوش آگاه آلبوم آمریکا آموزش آموختن امروز امشب انگور انرژی
انسان ایران ایستگاه اتاق اتفاق احساس اخبار اخلاق ابزار اردک ارزان آرامش آرزو آسیاب ابر ابرو ادبیات
بازی باد بادام باغچه باور بامداد بانو بستر بخش بخار بدن بدر بدرقه برنامه بزرگ بیمار بیابان بینا
پاییز پارک پدر پذیرایی پزشک پرچم پرواز پرتقال پرستو پیشانی پیاده پیروز پیام پول پنیر پناه پله
تابلو تاریخ تازه تاکسی تندر تماشاگر تمیز تلفن تمرین تند تپه توت توانا تور درخت دروازه دانشگاه
دوربین دنیا دیوار دیروز دوستانه دفترچه دل دریاچه دقیقه راه رودخانه روزنامه روشن رفیق رستوران
زندگی زبان زرد زرنگ زنگ زیبایی سبز ستاره‌شناس سفره ساعت ساده سرزمین سرگرمی سلامتی سنگ سیاره
سیستم شیر شهر شیشه شاعر شادیاب شاگرد صبح صدا صلح صورت غذا فوتبال فرش فروشگاه فصل فضای
قاشق قهوه قوی قانون قطار کتابخانه کودکستان کار کارگر کارت کافی کامیاب کلمه کلاسیک کلید کنار
لباس لاله لیمو مادرانه ماشین ماهی مدرسه‌ای مزرعه مسجد مسافرت موسیقی میدان میوه نامه نانوا
نخود نردبان نزدیک نگاه نور نوروز نویسنده نهال نقشه نقاشی هواپیما هفت هفته هدیه هنر هندوانه
یادگار یخ یوسف یکشنبه ورزش وطن وقت ویژه گل گلدان گلخانه گنج گربه گرم گوشت گوسفند گیاه
بهترین زیباتر مهربانی خواندن نوشتن دیدن شنیدن گفتن رفتن آمدن داشتن بودن کردن ساختن خوردن
خوابیدن نشستن ایستادن خندیدن گریه کردن دانستن خواستن توانستن یادگرفتن دوست‌داشتن""".split()
DICTIONARY = {normal(w) for level in LEVELS for w in level["words"]} | {normal(w) for w in EXTRA_WORDS}

class SearchWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("جست‌وجو در فرهنگ کلمات")
        self.configure(bg=BG); self.geometry("580x420"); self.minsize(480, 350)
        self.transient(parent); self.grab_set()
        tk.Label(self, text="جست‌وجو در فرهنگ کلمات", bg=BG, fg="white", font=parent.font(22, "bold")).pack(pady=(30, 15))
        row = tk.Frame(self, bg=BG); row.pack(padx=40, fill="x")
        self.entry = tk.Entry(row, justify="right", font=parent.font(16), bg=CARD, fg=INK, relief="flat")
        self.entry.pack(side="right", fill="x", expand=True, ipady=10)
        parent.button(row, "جست‌وجو", self.search, GOLD, INK).pack(side="right", padx=(0, 8))
        self.result = tk.Label(self, text="یک کلمهٔ فارسی وارد کنید.", justify="right", wraplength=450, bg=BG, fg="#e7e2ff", font=parent.font(14))
        self.result.pack(pady=30)
        self.count = tk.Label(self, text=f"فرهنگ بازی: {persian_number(len(DICTIONARY))} واژه", bg=BG, fg="#bdb3e7", font=parent.font(11))
        self.count.pack()
        parent.button(self, "بستن", self.destroy, "#65558f", "white").pack(pady=28)
        self.entry.bind("<Return>", lambda e: self.search()); self.entry.focus_set()
    def search(self):
        query = normal(self.entry.get())
        if query in DICTIONARY:
            self.result.config(text=f"✓ کلمهٔ «{query}» در فرهنگ بازی وجود دارد.", fg="#7af0af")
        else:
            matches = sorted(w for w in DICTIONARY if query and query in w)[:8]
            text = "کلمه‌ای با این مشخصات پیدا نشد." if not matches else "نتایج مشابه:\n" + "   •   ".join(matches)
            self.result.config(text=text, fg="#ffd77c" if matches else "#ff9ca6")
        self.count.config(text=f"تعداد نتیجه: {persian_number(1 if query in DICTIONARY else len(matches))}")

class AmirzaGame:
    def __init__(self, root):
        self.root = root; root.title("آمیرزا | بازی ساخت کلمه"); root.geometry("1000x760"); root.minsize(850,650); root.configure(bg=BG)
        self.family = self.detect_font(); self.score = 0; self.order = []; self.order_pos = 0
        self.current = []; self.found = set(); self.letter_items = []; self.hint_letters = set()
        root.bind("<Return>", lambda e: self.check()); root.bind("<BackSpace>", lambda e: self.backspace()); root.bind("<Escape>", lambda e: self.clear())
        self.show_start()
    def detect_font(self):
        available = set(tkfont.families())
        return next((f for f in ("Vazirmatn", "B Nazanin", "IRANSans", "Tahoma", "Segoe UI") if f in available), "TkDefaultFont")
    def font(self, size, weight="normal"): return (self.family, size, weight)
    def button(self, parent, label, command, bg, fg="white"):
        return tk.Button(parent, text=label, command=command, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, relief="flat", bd=0, cursor="hand2", font=self.font(13,"bold"), padx=20, pady=10)
    def clear_screen(self):
        for child in self.root.winfo_children(): child.destroy()
    def rounded(self, canvas, x1,y1,x2,y2,r, fill, **kw):
        p=[x1+r,y1,x2-r,y1,x2,y1,x2,y1+r,x2,y2-r,x2,y2,x2-r,y2,x1+r,y2,x1,y2,x1,y2-r,x1,y1+r,x1,y1]
        return canvas.create_polygon(p, smooth=True, fill=fill, **kw)
    def show_start(self):
        self.clear_screen(); c=tk.Canvas(self.root,bg=BG,highlightthickness=0); c.pack(fill="both",expand=True)
        def draw(e=None):
            c.delete("all"); w,h=max(c.winfo_width(),850),max(c.winfo_height(),650)
            c.create_oval(-150,-180,w*.68,h*.8,fill=BG2,outline="")
            self.rounded(c,w/2-270,h/2-210,w/2+270,h/2+220,30,"#fffdf8")
            c.create_text(w/2,h/2-110,text="آمیرزا",fill=INK,font=self.font(36,"bold"))
            c.create_text(w/2,h/2-62,text="بازی ساخت کلمه",fill=MUTED,font=self.font(17))
            for index, (y, text, color, cmd) in enumerate([(h/2-10,"شروع بازی",GOLD,self.start_game),(h/2+58,"جست‌وجوی کلمه","#65558f",self.open_search),(h/2+126,"خروج","#eee9f7",self.root.destroy)]):
                tag = f"go{index}"
                self.rounded(c,w/2-170,y,w/2+170,y+48,18,color, tags=(tag,))
                c.create_text(w/2,y+24,text=text,fill=INK if color in (GOLD,"#eee9f7") else "white",font=self.font(15,"bold"),tags=(tag,))
                c.tag_bind(tag, "<Button-1>", lambda e, f=cmd: f())
                c.tag_bind(tag, "<Enter>", lambda e: c.config(cursor="hand2"))
                c.tag_bind(tag, "<Leave>", lambda e: c.config(cursor=""))
        c.bind("<Configure>",draw); draw()
    def start_game(self):
        self.order=list(range(len(LEVELS))); random.shuffle(self.order); self.order_pos=0; self.load_level()
    def load_level(self):
        if self.order_pos >= len(self.order): random.shuffle(self.order); self.order_pos=0
        self.level=LEVELS[self.order[self.order_pos]]; self.letters=list(self.level["letters"]); random.shuffle(self.letters)
        self.current=[]; self.found=set(); self.hint_letters=set(); self.build_game()
    def build_game(self):
        self.clear_screen()
        header=tk.Frame(self.root,bg=BG2,height=95); header.pack(fill="x"); header.pack_propagate(False)
        tk.Label(header,text="آمیرزا",bg=BG2,fg="white",font=self.font(27,"bold")).pack(side="left",padx=42)
        self.score_label=tk.Label(header,bg=BG2,fg="#ffdb6e",font=self.font(15,"bold")); self.score_label.pack(side="right",padx=42)
        self.level_label=tk.Label(header,bg=BG2,fg="white",font=self.font(15,"bold")); self.level_label.pack(side="right",padx=20)
        self.score_label.config(text=f"امتیاز {persian_number(self.score)}"); self.level_label.config(text=f"مرحله {persian_number(self.order_pos+1)}")
        body=tk.Frame(self.root,bg=BG); body.pack(fill="both",expand=True,padx=45,pady=22)
        card=tk.Frame(body,bg=CARD,highlightthickness=0); card.pack(fill="x",pady=(0,18))
        tk.Label(card,text="کلمات پیدا شده",bg=CARD,fg=INK,font=self.font(17,"bold")).pack(pady=(18,3))
        self.progress=tk.Label(card,bg=CARD,fg=MUTED,font=self.font(12)); self.progress.pack()
        self.chips=tk.Frame(card,bg=CARD); self.chips.pack(pady=(10,18))
        tk.Label(body,text="با حروف زیر کلمه بساز",bg=BG,fg="#dcd5ff",font=self.font(14)).pack()
        self.word_label=tk.Label(body,text="—",bg=BG,fg="white",font=self.font(30,"bold"),height=2); self.word_label.pack()
        self.message=tk.Label(body,text="",bg=BG,fg="#dcd5ff",font=self.font(12,"bold")); self.message.pack()
        self.letter_canvas=tk.Canvas(body,bg=BG,highlightthickness=0,height=190); self.letter_canvas.pack(fill="x",pady=(3,5)); self.letter_canvas.bind("<Configure>",lambda e:self.draw_letters())
        actions=tk.Frame(body,bg=BG); actions.pack(pady=3)
        self.button(actions,"راهنما (-۲۰)",self.hint,"#65558f").pack(side="right",padx=6)
        self.button(actions,"پاک کردن",self.clear,"#514b72").pack(side="right",padx=6)
        self.button(actions,"بررسی جواب",self.check,GOLD,INK).pack(side="right",padx=6)
        self.next_button=self.button(body,"مرحله بعد",self.next_level,GREEN); self.search_button=self.button(body,"جست‌وجوی کلمه",self.open_search,"#3f3770")
        self.search_button.pack(pady=(10,0)); self.refresh()
    def draw_letters(self):
        c=self.letter_canvas; c.delete("all"); w=max(c.winfo_width(),600); count=len(self.letters); cols=min(6,max(3,count)); rows=(count+cols-1)//cols
        for i, letter in enumerate(self.letters):
            col=i%cols; row=i//cols; x=w/2+(col-(cols-1)/2)*92; y=45+row*88
            used=Counter(self.current)[letter]; total=Counter(self.letters)[letter]; disabled=used>=total
            fill="#8172bb" if disabled else (GOLD if letter in self.hint_letters else "#fffdf8")
            shadow="#171130" if not disabled else BG
            c.create_oval(x-34,y-29,x+34,y+39,fill=shadow,outline="",tags=(f"letter{i}",))
            c.create_oval(x-34,y-34,x+34,y+34,fill=fill,outline="#e8ddbd" if not disabled else "#8172bb",width=2,tags=(f"letter{i}", f"bubble{i}"))
            c.create_text(x,y,text=letter,fill=INK if not disabled else "#ded7f7",font=self.font(24,"bold"),tags=(f"letter{i}",))
            if not disabled:
                c.tag_bind(f"letter{i}","<Button-1>",lambda e, ch=letter:self.add_letter(ch))
                c.tag_bind(f"letter{i}", "<Enter>", lambda e, tag=f"bubble{i}": (c.config(cursor="hand2"), c.itemconfigure(tag, outline=GOLD, width=3)))
                c.tag_bind(f"letter{i}", "<Leave>", lambda e, tag=f"bubble{i}": (c.config(cursor=""), c.itemconfigure(tag, outline="#e8ddbd", width=2)))
    def add_letter(self, letter):
        if Counter(self.current)[letter] < Counter(self.letters)[letter]: self.current.append(letter); self.hint_letters.discard(letter); self.refresh()
    def refresh(self):
        word="".join(self.current); self.word_label.config(text=word or "—")
        self.progress.config(text=f"{persian_number(len(self.found))} / {persian_number(len(self.level['words']))} کلمه")
        for item in self.chips.winfo_children(): item.destroy()
        for word in self.level["words"]:
            if word in self.found:
                tk.Label(self.chips,text=word,bg="#daf4e5",fg="#18774c",font=self.font(12,"bold"),padx=12,pady=5).pack(side="right",padx=4,pady=3)
        self.draw_letters()
    def flash(self, text, color):
        self.message.config(text=text,fg=color); self.root.after(2500,lambda:self.message.config(text=""))
    def clear(self): self.current=[]; self.hint_letters=set(); self.refresh()
    def backspace(self):
        if self.current: self.current.pop(); self.refresh()
    def check(self):
        word=normal("".join(self.current))
        if not word: self.flash("کلمه‌ای وارد نشده است.",RED); return
        if word in self.found: self.flash("این کلمه قبلاً پیدا شده است.","#ffbb69")
        elif word in self.level["words"]:
            self.found.add(word); gained=score_for(word); self.score+=gained; self.flash(f"جواب درست است!  +{persian_number(gained)}",GREEN); self.current=[]
            if len(self.found)==len(self.level["words"]): self.flash("مرحله کامل شد!",GREEN); self.next_button.pack(pady=(8,0))
        else:
            self.score=max(0,self.score-2); self.flash("این کلمه در این مرحله نیست.",RED)
        self.score_label.config(text=f"امتیاز {persian_number(self.score)}"); self.refresh()
    def hint(self):
        remaining=[w for w in self.level["words"] if w not in self.found]
        if not remaining: self.flash("همهٔ کلمات پیدا شده‌اند.",GREEN); return
        if self.score < 20: self.flash("برای راهنما دست‌کم ۲۰ امتیاز لازم است.","#ffbb69"); return
        word=random.choice(remaining); self.score-=20; self.hint_letters=set(word); self.flash(f"راهنما: حروف «{word}» را پیدا کنید.","#ffd86a"); self.score_label.config(text=f"امتیاز {persian_number(self.score)}"); self.draw_letters()
    def next_level(self): self.order_pos+=1; self.load_level()
    def open_search(self): SearchWindow(self.root)

def run_tests():
    errors=[]; levels=validate_levels(LEVELS); words=sum(len(x["words"]) for x in levels)
    if len(levels)<100: errors.append("تعداد سطح کم است")
    for level in levels:
        if len(level["words"]) != len(set(level["words"])): errors.append("پاسخ تکراری")
        for word in level["words"]:
            if not valid_word(word,level["letters"]): errors.append(f"نامعتبر: {word}")
    if normal("ك ي ى") != "ک ی ی": errors.append("نرمال‌سازی")
    if [score_for(x) for x in ("تا", "مار", "مادر", "مدرسه")] != [10,10,15,20]: errors.append("امتیاز")
    print("آزمون بازی آمیرزا\n-----------------")
    print(f"سطوح: {len(levels)}\nکلمات معتبر: {words}\nفرهنگ کلمات: {len(DICTIONARY)}\nخطا: {len(errors)}")
    if errors: print("وضعیت: ناموفق\n"+"\n".join(errors)); return 1
    print("وضعیت: موفق"); return 0

if __name__ == "__main__":
    if "--test" in sys.argv: sys.exit(run_tests())
    root=tk.Tk(); AmirzaGame(root); root.mainloop()
