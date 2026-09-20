from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Inches, Pt
import pptx.oxml.ns as nsmap
from lxml import etree

prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(5.625)

# ── Palette ──────────────────────────────────────────────────────────────────
NAVY   = (27,  42,  74)
PURPLE = (108, 79,  212)
CORAL  = (240, 90,  91)
TEAL   = (0,   180, 166)
GOLD   = (247, 183, 49)
WHITE  = (255, 255, 255)
LIGHT  = (244, 241, 255)
MUTED  = (138, 143, 168)
DARK   = (27,  42,  74)
GREEN  = (39,  174, 96)
RED    = (231, 76,  60)

def rgb(t): return RGBColor(*t)

def rect(slide, l, t, w, h, color, alpha=None):
    from pptx.util import Inches
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(color)
    shape.line.fill.background()
    return shape

def oval(slide, l, t, w, h, color):
    shape = slide.shapes.add_shape(9, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(color)
    shape.line.fill.background()
    return shape

def tb(slide, text, l, t, w, h, size=14, bold=False, color=WHITE,
       align='left', italic=False, wrap=True):
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf  = txb.text_frame
    tf.word_wrap = wrap
    p   = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.size  = Pt(size)
    run.font.bold  = bold
    run.font.italic = italic
    run.font.color.rgb = rgb(color)
    run.font.name  = "Trebuchet MS"
    if align == 'center': p.alignment = PP_ALIGN.CENTER
    elif align == 'right': p.alignment = PP_ALIGN.RIGHT
    return txb

def tb_multi(slide, lines, l, t, w, h, size=13, color=WHITE, align='left',
             line_bold=None, line_color=None):
    """Multi-line textbox. lines = list of strings."""
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf  = txb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        run = p.add_run()
        run.text = line
        run.font.size  = Pt(size)
        run.font.name  = "Trebuchet MS"
        c = line_color[i] if line_color and i < len(line_color) else color
        b = line_bold[i]   if line_bold  and i < len(line_bold)  else False
        run.font.color.rgb = rgb(c)
        run.font.bold  = b
        if align == 'center': p.alignment = PP_ALIGN.CENTER
    return txb

def blank(): return prs.slides.add_slide(prs.slide_layouts[6])

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Title
# ═══════════════════════════════════════════════════════════════════════════════
s = blank()
rect(s, 0, 0, 10, 5.625, NAVY)
oval(s, 6.8, -0.6, 4.2, 4.2, (108, 79, 212))   # purple blob
oval(s, -0.8, 3.2, 3.0, 3.0, TEAL)             # teal blob

tb(s, "🧠", 0.5, 0.3, 1.0, 0.8, size=40)
tb(s, "WHAT IS", 0.5, 0.32, 9, 0.48, size=14, bold=True, color=GOLD, align='center')
tb(s, "Behavioral Health?", 0.5, 0.78, 9, 1.25, size=48, bold=True, color=WHITE, align='center')
tb(s, "A fun crash course for your public health brain 🎙️", 0.5, 2.1, 9, 0.55, size=17,
   color=MUTED, align='center', italic=True)

pills = ["Behavioral Health", "Neuroscience", "Brain Science"]
pxs   = [1.2, 3.85, 6.5]
for txt, px in zip(pills, pxs):
    rect(s, px, 3.0, 2.4, 0.42, PURPLE)
    tb(s, txt, px, 3.0, 2.4, 0.42, size=11, color=WHITE, align='center')

tb(s, "Module 1 · Lessons 1 & 2", 0.5, 5.1, 9, 0.3, size=10, color=MUTED, align='center')

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — The Big Question
# ═══════════════════════════════════════════════════════════════════════════════
s = blank()
rect(s, 0, 0, 10, 5.625, WHITE)
rect(s, 0, 0, 0.18, 5.625, CORAL)

tb(s, "THE BIG QUESTION", 0.4, 0.3, 9.2, 0.42, size=13, bold=True, color=CORAL)
tb(s, "Why do you do what you do?", 0.4, 0.65, 9.2, 0.95, size=36, bold=True, color=NAVY)

boxes = [
    ("📱", "Check your phone", "first thing every morning?"),
    ("🍩", "Snack when bored",  "even when not hungry?"),
    ("😴", "Skip your workout", "when you feel tired?"),
]
for i, (emo, lbl, sub) in enumerate(boxes):
    x = 0.4 + i * 3.1
    rect(s, x, 1.75, 2.88, 2.3, LIGHT)
    tb(s, emo,  x, 1.82, 2.88, 0.65, size=30, align='center')
    tb(s, lbl,  x, 2.5,  2.88, 0.42, size=14, bold=True,  color=NAVY,  align='center')
    tb(s, sub,  x, 2.9,  2.88, 0.42, size=11, color=MUTED, align='center')

rect(s, 0.4, 4.28, 9.2, 0.65, NAVY)
tb(s, "These are ALL behavioral health moments. Let's break them down. 🔍",
   0.4, 4.28, 9.2, 0.65, size=14, bold=True, color=WHITE, align='center')

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — What is Behavioral Health
# ═══════════════════════════════════════════════════════════════════════════════
s = blank()
rect(s, 0, 0, 10, 5.625, WHITE)
rect(s, 0, 0, 10, 1.1, PURPLE)

tb(s, "SO WHAT EXACTLY IS BEHAVIORAL HEALTH?",
   0.4, 0.0, 9.2, 1.1, size=20, bold=True, color=WHITE, align='center')

tb(s, '"The connection between your daily behaviors, habits,\nthoughts & emotions — and your overall health."',
   0.5, 1.2, 9, 0.9, size=16, color=NAVY, align='center', italic=True)

rows = [
    ("🧠", "Mental health",    "Depression, anxiety, bipolar, PTSD"),
    ("🍺", "Substance use",    "Alcohol, opioids, cannabis, stimulants"),
    ("🏃", "Health behaviors", "Sleep, diet, exercise, stress management"),
    ("💬", "Mind-body link",   "How emotions cause physical illness"),
]
for i, (emo, title, desc) in enumerate(rows):
    y   = 2.2 + i * 0.68
    bg  = LIGHT if i % 2 == 0 else WHITE
    rect(s, 0.4, y, 9.2, 0.6, bg)
    tb(s, emo,   0.5,  y, 0.6, 0.6, size=22, align='center')
    tb(s, title, 1.15, y, 2.8, 0.6, size=13, bold=True, color=PURPLE)
    tb(s, desc,  4.0,  y, 5.4, 0.6, size=13, color=NAVY)

rect(s, 0.4, 5.05, 9.2, 0.35, GOLD)
tb(s, "⚡ Behavior drives ~40% of premature deaths — it's the biggest lever we have.",
   0.4, 5.05, 9.2, 0.35, size=11, bold=True, color=DARK, align='center')

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — BH vs MH
# ═══════════════════════════════════════════════════════════════════════════════
s = blank()
rect(s, 0, 0, 10, 5.625, WHITE)

tb(s, "BEHAVIORAL HEALTH  vs.  MENTAL HEALTH",
   0.4, 0.22, 9.2, 0.42, size=13, bold=True, color=MUTED)
tb(s, "What's the real difference?",
   0.4, 0.6, 9.2, 0.72, size=32, bold=True, color=NAVY)

# Left — BH
rect(s, 0.4, 1.45, 4.3, 3.75, PURPLE)
tb(s, "🌐", 0.4, 1.52, 4.3, 0.65, size=30, align='center', color=WHITE)
tb(s, "BEHAVIORAL HEALTH", 0.4, 2.15, 4.3, 0.42, size=12, bold=True, color=GOLD, align='center')
tb(s, "The BIG umbrella", 0.4, 2.55, 4.3, 0.35, size=11, color=WHITE, align='center', italic=True)
bh_items = ["✓  Mental health", "✓  Substance use", "✓  Sleep & diet habits",
            "✓  Stress & coping", "✓  Medication adherence"]
for j, item in enumerate(bh_items):
    tb(s, item, 0.6, 2.92 + j * 0.43, 3.9, 0.4, size=12, color=WHITE)

# Right — MH
rect(s, 5.3, 1.45, 4.3, 3.75, LIGHT)
tb(s, "🧠", 5.3, 1.52, 4.3, 0.65, size=30, align='center', color=NAVY)
tb(s, "MENTAL HEALTH", 5.3, 2.15, 4.3, 0.42, size=12, bold=True, color=PURPLE, align='center')
tb(s, "A subset inside BH", 5.3, 2.55, 4.3, 0.35, size=11, color=MUTED, align='center', italic=True)
mh_items = ["→  Depression", "→  Anxiety disorders", "→  Bipolar disorder",
            "→  PTSD", "→  Schizophrenia"]
for j, item in enumerate(mh_items):
    tb(s, item, 5.5, 2.92 + j * 0.43, 3.9, 0.4, size=12, color=NAVY)

tb(s, "👉  Every mental health issue IS a behavioral health issue — but not vice versa!",
   0.4, 5.2, 9.2, 0.3, size=11, bold=True, color=CORAL, align='center')

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — The Core Formula
# ═══════════════════════════════════════════════════════════════════════════════
s = blank()
rect(s, 0, 0, 10, 5.625, NAVY)
oval(s, 7.0, -0.5, 4.0, 4.0, (108, 79, 212))

tb(s, "THE CORE FORMULA", 0.5, 0.28, 9, 0.42, size=13, bold=True, color=GOLD, align='center')
tb(s, "What shapes your behavioral health?",
   0.5, 0.65, 9, 0.65, size=26, bold=True, color=WHITE, align='center')

boxes = [
    ("🧠", "YOUR BRAIN",        "Biology & neuroscience\nGenes, chemistry, wiring"),
    ("🌍", "YOUR ENVIRONMENT",  "Social & situational\nFamily, stress, culture"),
    ("🔁", "YOUR HABITS",       "Repeated behaviors\nAutomatic daily loops"),
]
for i, (emo, label, sub) in enumerate(boxes):
    x = 0.3 + i * 3.1
    rect(s, x, 1.48, 2.82, 2.55, (80, 55, 170))
    tb(s, emo,   x, 1.55, 2.82, 0.62, size=28, align='center', color=WHITE)
    tb(s, label, x, 2.15, 2.82, 0.42, size=11, bold=True, color=GOLD, align='center')
    tb(s, sub,   x, 2.58, 2.82, 0.85, size=11, color=WHITE, align='center')
    if i < 2:
        tb(s, "+", x + 2.87, 1.9, 0.3, 1.6, size=26, bold=True, color=GOLD, align='center')

rect(s, 1.5, 4.2, 7.0, 0.88, CORAL)
tb(s, "=  YOUR BEHAVIORAL HEALTH  🎯",
   1.5, 4.2, 7.0, 0.88, size=20, bold=True, color=WHITE, align='center')

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — Automatic Behaviors
# ═══════════════════════════════════════════════════════════════════════════════
s = blank()
rect(s, 0, 0, 10, 5.625, WHITE)
rect(s, 0, 0, 0.18, 5.625, TEAL)

tb(s, "THE AUTOPILOT PROBLEM", 0.4, 0.25, 9.2, 0.42, size=13, bold=True, color=TEAL)
tb(s, "40–45% of your day runs on automatic habits",
   0.4, 0.62, 9.2, 0.72, size=28, bold=True, color=NAVY)

rect(s, 0.4, 1.45, 9.2, 0.65, LIGHT)
tb(s, "😰 Emotion  →  🔁 Automatic behavior  →  😌 Short-term relief  →  🔗 Loop reinforced",
   0.4, 1.45, 9.2, 0.65, size=14, bold=True, color=PURPLE, align='center')

examples = [
    ("😟 Anxiety",   "→  Check phone",   "floods brain with info before day starts"),
    ("😩 Boredom",   "→  Snack on junk",  "eating used to regulate emotion, not hunger"),
    ("😵 Overwhelm", "→  Skip exercise",  "avoidance of exercise increases fatigue over time"),
    ("😤 Stress",    "→  Smoke/drink",    "substance gives short relief, deepens the problem"),
]
for i, (trigger, beh, cost) in enumerate(examples):
    y  = 2.25 + i * 0.72
    bg = LIGHT if i % 2 == 0 else WHITE
    rect(s, 0.4, y, 9.2, 0.62, bg)
    tb(s, trigger, 0.5,  y, 1.9,  0.62, size=12, bold=True, color=CORAL)
    tb(s, beh,     2.45, y, 2.4,  0.62, size=12, bold=True, color=PURPLE)
    tb(s, cost,    4.95, y, 4.5,  0.62, size=11, color=MUTED, italic=True)

rect(s, 0.4, 5.1, 9.2, 0.32, NAVY)
tb(s, "This loop is the engine of most behavioral health problems — and the target of most interventions.",
   0.4, 5.1, 9.2, 0.32, size=10, bold=True, color=WHITE, align='center')

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — Case Study: Maria
# ═══════════════════════════════════════════════════════════════════════════════
s = blank()
rect(s, 0, 0, 10, 5.625, WHITE)
rect(s, 0, 0, 10, 1.05, CORAL)

tb(s, "REAL STORY: Meet Maria 👩  —  Chronic Insomnia",
   0.4, 0.0, 9.2, 1.05, size=24, bold=True, color=WHITE, align='center')

rect(s, 0.4, 1.15, 4.3, 0.88, (255, 243, 243))
tb(s, "💊  Old approach", 0.5, 1.2, 4.1, 0.38, size=12, bold=True, color=CORAL)
tb(s, "Prescribe sleep meds. Symptom treated.\nRoot cause? Still there.", 0.5, 1.55, 4.1, 0.42, size=11, color=NAVY)

rect(s, 5.3, 1.15, 4.3, 0.88, (232, 250, 245))
tb(s, "✅  BH approach", 5.4, 1.2, 4.1, 0.38, size=12, bold=True, color=TEAL)
tb(s, "Find & fix the behaviors driving\nthe insomnia. No meds needed.", 5.4, 1.55, 4.1, 0.42, size=11, color=NAVY)

fixes = [
    ("📱  Late-night scrolling",  "Phone-free bedroom · screen off by 10pm"),
    ("☕  Coffee at 4pm",          "No caffeine after 1pm (half-life is 5–6 hrs!)"),
    ("😰  Bedtime anxiety spiral", "Structured worry journal at 7pm"),
    ("🌡️  Warm, bright room",      "65°F + blackout curtains + bed = sleep only"),
]
for i, (issue, fix) in enumerate(fixes):
    y  = 2.18 + i * 0.68
    bg = LIGHT if i % 2 == 0 else WHITE
    rect(s, 0.4, y, 9.2, 0.6, bg)
    tb(s, issue, 0.5,  y, 4.3, 0.6, size=12, color=NAVY)
    tb(s, "→  " + fix, 4.85, y, 4.9, 0.6, size=12, bold=True, color=TEAL)

rect(s, 0.4, 5.06, 9.2, 0.36, TEAL)
tb(s, "Result: 6 weeks of CBT-I → sleeping great. Zero medication. This is behavioral health in action. 🎉",
   0.4, 5.06, 9.2, 0.36, size=11, bold=True, color=WHITE, align='center')

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — Lesson 2 Intro: Neuroscience
# ═══════════════════════════════════════════════════════════════════════════════
s = blank()
rect(s, 0, 0, 10, 5.625, NAVY)
oval(s, 6.2, 0.2, 4.5, 4.5, (0, 180, 166))   # teal blob

tb(s, "LESSON 2", 0.5, 0.35, 6, 0.42, size=13, bold=True, color=GOLD)
tb(s, "Your Brain on\nBehavioral Health",
   0.5, 0.72, 7, 1.75, size=40, bold=True, color=WHITE)
tb(s, "Neuroscience — made simple and interesting.",
   0.5, 2.52, 7, 0.5, size=16, color=MUTED, italic=True)

facts = [
    "🧠  86 billion neurons firing in your brain right now",
    "🔗  100 trillion connections between them",
    "🤖  40–45% of your day is pure autopilot habit",
]
for i, f in enumerate(facts):
    rect(s, 0.5, 3.2 + i * 0.58, 8.2, 0.5, (80, 55, 170))
    tb(s, f, 0.7, 3.2 + i * 0.58, 8.0, 0.5, size=13, color=WHITE)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — Neurons & Synapses
# ═══════════════════════════════════════════════════════════════════════════════
s = blank()
rect(s, 0, 0, 10, 5.625, WHITE)
rect(s, 0, 0, 0.18, 5.625, PURPLE)

tb(s, "HOW YOUR BRAIN ACTUALLY COMMUNICATES", 0.4, 0.22, 9.2, 0.42, size=13, bold=True, color=PURPLE)
tb(s, "Neurons, Synapses & Neurotransmitters",
   0.4, 0.6, 9.2, 0.65, size=26, bold=True, color=NAVY)

steps = [
    ("1️⃣", "Action potential fires", "Electrical signal travels down the neuron like a spark along a wire."),
    ("2️⃣", "Neurotransmitters released", "Chemical messengers flood into the synapse (the gap between neurons)."),
    ("3️⃣", "Receptors bind",          "Chemicals attach to the next neuron — exciting OR inhibiting it."),
    ("4️⃣", "Reuptake or breakdown",   "Leftover chemicals are recycled. Most meds work right here!"),
]
for i, (num, title, desc) in enumerate(steps):
    y  = 1.42 + i * 0.96
    bg = LIGHT if i % 2 == 0 else WHITE
    rect(s, 0.4, y, 9.2, 0.85, bg)
    tb(s, num,   0.5,  y, 0.7, 0.85, size=24, align='center')
    tb(s, title, 1.25, y, 3.0, 0.85, size=13, bold=True, color=PURPLE)
    tb(s, desc,  4.35, y, 5.1, 0.85, size=12, color=NAVY)

rect(s, 0.4, 5.3, 9.2, 0.2, LIGHT)
tb(s, "💡  Medications work by tweaking this system — blocking reuptake, mimicking chemicals, or boosting production.",
   0.4, 5.28, 9.2, 0.25, size=10, color=PURPLE, bold=True, align='center')

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — 5 Neurotransmitters
# ═══════════════════════════════════════════════════════════════════════════════
s = blank()
rect(s, 0, 0, 10, 5.625, WHITE)
rect(s, 0, 0, 10, 0.95, TEAL)
tb(s, "THE 5 BRAIN CHEMICALS YOU ABSOLUTELY NEED TO KNOW",
   0.3, 0.0, 9.4, 0.95, size=18, bold=True, color=WHITE, align='center')

nts = [
    ("🎯", "Dopamine",        "Reward & motivation",       "Spikes with ALL addictive substances",       (108, 79,  212), LIGHT),
    ("😊", "Serotonin",       "Mood, sleep, appetite",     "SSRIs keep more of this in your synapse",    (0,  180, 166), (232, 250, 245)),
    ("⚡", "Norepinephrine",  "Alertness & stress",        "Dysregulated in PTSD and panic disorder",    (247,183, 49),  (255, 251, 234)),
    ("😌", "GABA",            "Calm — brain's brake pedal","Benzodiazepines enhance this for anxiety",   (39, 174, 96),  (234, 250, 241)),
    ("🔑", "Glutamate",       "Learning & memory",         "Primary excitatory system in the brain",     (231, 76,  60), (254, 240, 239)),
]
for i, (emo, name, role, note, col, bg) in enumerate(nts):
    y = 1.06 + i * 0.88
    rect(s, 0.3, y, 9.4, 0.78, bg)
    tb(s, emo,  0.4,  y, 0.72, 0.78, size=24, align='center')
    tb(s, name, 1.18, y, 2.2,  0.78, size=14, bold=True, color=col)
    tb(s, role, 3.45, y, 2.9,  0.78, size=12, color=NAVY)
    tb(s, "→  " + note, 6.45, y, 3.35, 0.78, size=11, color=MUTED, italic=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — Brain Regions
# ═══════════════════════════════════════════════════════════════════════════════
s = blank()
rect(s, 0, 0, 10, 5.625, WHITE)
rect(s, 0, 0, 10, 1.0, PURPLE)
tb(s, "5 BRAIN REGIONS THAT RUN YOUR BEHAVIORAL HEALTH",
   0.3, 0.0, 9.4, 1.0, size=20, bold=True, color=WHITE, align='center')

regions = [
    ("🧭", "Prefrontal Cortex",  "Your CEO",               "Decision-making & impulse control. Not fully mature until mid-20s!"),
    ("🚨", "Amygdala",           "Your alarm bell",         "Fires at any threat — real or imagined. Hyperactive in PTSD & anxiety."),
    ("📚", "Hippocampus",        "Your librarian",          "Stores memories & context. Shrinks under chronic stress."),
    ("🎰", "Nucleus Accumbens",  "Your reward circuit",     "Dopamine central. Goes 'dark' in depression — causing anhedonia."),
    ("🕹️", "Hypothalamus",       "Your hormonal HQ",        "Launches the cortisol stress cascade when it senses danger."),
]
for i, (emo, name, role, desc) in enumerate(regions):
    col = 0 if i < 3 else 1
    row = i if i < 3 else i - 3
    x   = 0.3 + col * 5.05
    y   = 1.1 + row * 1.45
    rect(s, x, y, 4.6, 1.28, LIGHT)
    tb(s, emo,  x + 0.08, y + 0.08, 0.72, 1.1,  size=26, align='center')
    tb(s, name, x + 0.85, y + 0.08, 3.6,  0.38, size=13, bold=True, color=PURPLE)
    tb(s, role, x + 0.85, y + 0.44, 3.6,  0.28, size=11, color=CORAL, italic=True)
    tb(s, desc, x + 0.85, y + 0.7,  3.6,  0.48, size=10, color=MUTED)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — Neuroplasticity
# ═══════════════════════════════════════════════════════════════════════════════
s = blank()
rect(s, 0, 0, 10, 5.625, NAVY)
oval(s, -1.0, -0.8, 5.0, 5.0, (0, 180, 166))
oval(s,  7.5,  3.0, 4.0, 4.0, CORAL)

tb(s, "NEUROPLASTICITY", 0.5, 0.22, 9, 0.42, size=13, bold=True, color=GOLD, align='center')
tb(s, "Your brain can rewire itself at ANY age. 🌱",
   0.5, 0.6, 9, 0.88, size=32, bold=True, color=WHITE, align='center')

tb(s, '"Neurons that fire together, wire together."  — Hebb\'s Rule',
   0.5, 1.52, 9, 0.5, size=15, color=GOLD, italic=True, align='center')

points = [
    ("💬", "Therapy rewires fear responses — CBT literally changes amygdala activity"),
    ("🔄", "Recovery builds NEW competing neural pathways to replace old habits"),
    ("🧘", "Mindfulness strengthens PFC control over the amygdala — with practice"),
    ("🏋️", "New habits get easier every time — you're literally growing new neurons"),
]
for i, (emo, text) in enumerate(points):
    y = 2.22 + i * 0.72
    rect(s, 0.5, y, 9.0, 0.62, (80, 55, 170))
    tb(s, emo + "  " + text, 0.7, y, 8.6, 0.62, size=13, color=WHITE)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 13 — HPA Axis & Chronic Stress
# ═══════════════════════════════════════════════════════════════════════════════
s = blank()
rect(s, 0, 0, 10, 5.625, WHITE)
rect(s, 0, 0, 0.18, 5.625, CORAL)

tb(s, "THE STRESS RESPONSE & HPA AXIS", 0.4, 0.22, 9.2, 0.42, size=13, bold=True, color=CORAL)
tb(s, "Why chronic stress is slowly wrecking your health",
   0.4, 0.6, 9.2, 0.65, size=22, bold=True, color=NAVY)

# HPA cascade
chain = [
    ("🏔️  Hypothalamus", PURPLE, True),
    ("   ↓  releases CRH", MUTED, False),
    ("🫘  Pituitary gland", PURPLE, True),
    ("   ↓  releases ACTH", MUTED, False),
    ("⚡  Adrenal glands", PURPLE, True),
    ("   ↓  releases …", MUTED, False),
    ("💥  CORTISOL!", CORAL, True),
]
for i, (text, col, bold) in enumerate(chain):
    tb(s, text, 0.4, 1.38 + i * 0.46, 3.1, 0.42, size=12 if bold else 11,
       bold=bold, color=col)

# Damage box
rect(s, 3.75, 1.32, 5.9, 3.8, (255, 243, 243))
tb(s, "😬  What chronic cortisol does to you:",
   3.85, 1.38, 5.7, 0.42, size=12, bold=True, color=CORAL)
damage = [
    "🧩  Hippocampus shrinks → memory & context impaired",
    "🚨  Amygdala stuck ON → constant anxiety & hair-trigger",
    "🛡️  Immune system tanks → more illness & inflammation",
    "🧭  PFC degrades → poor decisions, less impulse control",
    "😞  Serotonin & dopamine drop → depression",
]
for i, d in enumerate(damage):
    tb(s, d, 3.85, 1.9 + i * 0.58, 5.6, 0.52, size=11, color=NAVY)

rect(s, 0.4, 5.1, 9.2, 0.38, TEAL)
tb(s, "🌿  The fix: Exercise · Sleep · Mindfulness · Social connection · Therapy",
   0.4, 5.1, 9.2, 0.38, size=12, bold=True, color=WHITE, align='center')

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 14 — Closing / Key Takeaways
# ═══════════════════════════════════════════════════════════════════════════════
s = blank()
rect(s, 0, 0, 10, 5.625, NAVY)
oval(s, 3.0, 0.3, 4.5, 4.5, (108, 79, 212))

tb(s, "🎓  KEY TAKEAWAYS", 0.5, 0.2, 9, 0.6, size=13, bold=True, color=GOLD, align='center')

takes = [
    (PURPLE, "01", "Behavioral health is BIGGER than mental health — habits, emotions & all behaviors that affect wellbeing."),
    (TEAL,   "02", "Neuroplasticity means your brain can rewire at any age — therapy, habits & exercise literally grow new pathways."),
    (CORAL,  "03", "Dopamine, serotonin, GABA & friends drive behavior — changed by meds AND lifestyle choices."),
    (GOLD,   "04", "Chronic stress (cortisol) shrinks your hippocampus & hijacks your amygdala. Sleep & exercise are medicine."),
]
for i, (col, num, text) in enumerate(takes):
    y = 0.92 + i * 1.0
    rect(s, 0.4, y, 0.65, 0.82, col)
    tb(s, num, 0.4, y, 0.65, 0.82, size=17, bold=True, color=WHITE, align='center')
    rect(s, 1.1, y, 8.5, 0.82, LIGHT)
    tb(s, text, 1.2, y, 8.3, 0.82, size=12, color=NAVY)

rect(s, 0.4, 5.05, 9.2, 0.4, CORAL)
tb(s, "🎙️  Share this episode with someone who needs to understand their brain a little better!  🧠✨",
   0.4, 5.05, 9.2, 0.4, size=12, bold=True, color=WHITE, align='center')


# ─── Save ─────────────────────────────────────────────────────────────────────
prs.save("behavioral_health_podcast.pptx")  # ← CHANGED THIS LINE
print("✅ 14-slide PowerPoint saved!")
print(f"📁 File location: {__import__('os').path.abspath('behavioral_health_podcast.pptx')}")