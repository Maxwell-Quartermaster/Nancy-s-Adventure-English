# Watchman research generator. Writes RESEARCH.md only. No deletes, no /tmp.
import os
OUT = "/workspace/council-tools/watchman-ext/location-steps/RESEARCH.md"
P = "**Watchman:** "

# (location title, intro, steps, sources, notes)
# step = (title, [(kind, who, text)])
LOC = []

LOC.append(("1. Prenatal clinic visit", "Nancy has a routine visit, about 7 months along. Sam can come with her.", [
 ("Check in at the front desk", [
  ("SAY","", "I have an appointment."),
  ("SAY","", "My name is Nancy."),
  ("HEAR","receptionist", "What is your birthday?"),
  ("SAY","", "I need a Thai interpreter."),
  ("HEAR","receptionist", "Please have a seat."),
 ]),
 ("Weight and blood pressure", [
  ("HEAR","nurse", "Please step on the scale."),
  ("SAY","", "Is my weight okay?"),
  ("HEAR","nurse", "Roll up your sleeve, please."),
  ("HEAR","nurse", "Your blood pressure is good."),
 ]),
 ("Urine sample", [
  ("HEAR","nurse", "We need a urine sample."),
  ("HEAR","nurse", "Please use this cup."),
  ("SAY","", "Where is the bathroom?"),
  ("SAY","", "Here is my cup."),
 ]),
 ("Belly check, heartbeat, ultrasound (only on some visits)", [
  ("HEAR","nurse", "Please lie down here."),
  ("HEAR","nurse", "This gel is a little cold."),
  ("HEAR","nurse", "Let's listen to the heartbeat."),
  ("SAY","", "Is my baby okay?"),
  ("HEAR","nurse", "Your baby looks healthy."),
 ]),
 ("Talk with the doctor", [
  ("HEAR","doctor", "How are you feeling today?"),
  ("HEAR","doctor", "Is the baby moving a lot?"),
  ("SAY","", "The baby kicks a lot."),
  ("SAY","", "I have a question."),
  ("SAY","", "Please speak more slowly."),
 ]),
 ("Make the next appointment", [
  ("HEAR","receptionist", "Come back in two weeks."),
  ("SAY","", "Can I come Tuesday morning?"),
  ("HEAR","receptionist", "Here is your appointment card."),
  ("SAY","", "Thank you. See you soon."),
 ]),
], [
 ("https://www.nhs.uk/pregnancy/your-pregnancy-care/your-antenatal-appointments/",
  "28 week appointment: \"ask to check your blood pressure\", \"ask to test your pee\", \"ask to measure your bump\", \"discuss your baby's movements\". Also: \"If you have a partner, they can come to appointments if you would like them to.\""),
 ("https://www.mayoclinic.org/healthy-lifestyle/pregnancy-week-by-week/in-depth/prenatal-care/art-20044882",
  "\"your health care provider will measure your weight and height\"; \"you might be able to hear your baby's heartbeat with a small device, called a Doppler\"; \"Your prenatal appointments are an ideal time to discuss questions you have.\""),
 ("https://www.acog.org/womens-health/faqs/having-a-baby",
  "\"As your pregnancy continues, you may visit your ob-gyn more often. At your visits, you can ask any questions you may have.\" and \"You also may have a urine test\"."),
], [
 "Ultrasound is not every visit. NHS (UK) says: \"You'll be offered at least 10 antenatal appointments if this is your first baby, and 2 ultrasound scans.\" So step 4 is mostly the heartbeat and belly check; keep the ultrasound as an occasional scene.",
 "UK vs US: in the UK the visit is usually with a midwife (NHS: \"You'll usually see a midwife, and also a doctor if you need to.\"). US pages (ACOG, Mayo) talk about an ob-gyn or other provider. The game can keep \"doctor\" and \"nurse\".",
 "No source I opened covers Thailand practice, so no US vs Thailand note.",
 "Visits get closer together near the end (ACOG: \"you may visit your ob-gyn more often\"). \"Come back in two weeks\" is a sample line, not a medical schedule.",
]))

LOC.append(("2. Hospital labor and delivery", "Nancy arrives in labor with Sam. Generic roles: registration clerk, nurse, doctor.", [
 ("Arrive and check in", [
  ("SAY","", "I think I am in labor."),
  ("SAY","", "My water broke."),
  ("HEAR","registration clerk", "Can I see your ID?"),
  ("HEAR","registration clerk", "This is your armband."),
 ]),
 ("Triage (the first check)", [
  ("HEAR","nurse", "Please put on this gown."),
  ("HEAR","nurse", "Why did you come in?"),
  ("SAY","", "My pains are close together."),
  ("HEAR","nurse", "This belt checks the baby."),
 ]),
 ("Admission to a labor room", [
  ("HEAR","nurse", "You are staying with us."),
  ("HEAR","nurse", "This is your room."),
  ("SAY","", "Can Sam stay with me?"),
  ("HEAR","nurse", "Press this button for help."),
 ]),
 ("Labor", [
  ("HEAR","nurse", "Breathe slowly with me."),
  ("SAY","", "It hurts a lot."),
  ("SAY","", "Can I have some water?"),
  ("HEAR","nurse", "Here are some ice chips."),
  ("SAY","", "I want to walk."),
 ]),
 ("The baby is born", [
  ("HEAR","doctor", "Push now. You can do it."),
  ("HEAR","doctor", "Your baby is here!"),
  ("SAY","", "Can I hold my baby?"),
  ("HEAR","nurse", "We will weigh the baby."),
 ]),
 ("Recovery and the mother-baby room", [
  ("SAY","", "I am very tired."),
  ("HEAR","nurse", "Let's try feeding the baby."),
  ("SAY","", "Thank you for your help."),
  ("HEAR","nurse", "Call me if you need me."),
 ]),
 ("Going home", [
  ("HEAR","nurse", "You can go home today."),
  ("HEAR","nurse", "Is the car seat ready?"),
  ("HEAR","nurse", "Here are your home instructions."),
  ("SAY","", "We are going home!"),
 ]),
], [
 ("https://www.kaweahhealth.org/our-services/family-birthing-center/labor-and-delivery-unit",
  "\"Here you will be registered and an armband applied.\" Triage: \"you will be asked to change into a gown and placed on a fetal monitor and asked about the reason you came to the hospital.\" Labor room: \"This is the room where you will labor, deliver, and recover. Once recovery is done, usually about two hours, you will be transferred to the Mother Baby Unit\"."),
 ("https://www.upmc.com/services/womens-health/services/obgyn/obstetrics/labor-delivery/birth-experience/hospital-stay",
  "\"When you have labor symptoms, call your obstetrician's main line\"; \"you may not be able to eat, but you can request water or ice chips\"; \"you can hold your baby right away\"; \"Your care team will weigh your baby\"; \"a hospital staff member will check that your baby is safely buckled in their car seat. Your nurse will give you a folder or booklet with information.\""),
], [
 "Visitor rules vary by hospital: Kaweah says \"Patients are allowed one (1) visitor in the triage room\"; UPMC says \"You can also have up to two support people, plus a doula\". So \"Can Sam stay with me?\" fits everywhere.",
 "Length of stay (UPMC): \"Two days if you have a vaginal birth. Three to four days if you have a cesarean section.\"",
 "Call first: UPMC says to call the obstetrician's line when labor starts. A game scene could open with Sam making that call.",
 "No source I opened covers Thailand practice, so no US vs Thailand note.",
]))

LOC.append(("3. Grocery store trip", "Nancy and Sam shop together. Generic roles: store employee, cashier.", [
 ("Make a list and get a cart", [
  ("SAY","", "Sam, let's make a list."),
  ("SAY","", "We need rice and eggs."),
  ("SAY","", "Can you get a cart?"),
  ("HEAR","Sam", "Do we need more milk?"),
 ]),
 ("Find things and ask for help", [
  ("HEAR","store employee", "Can I help you find something?"),
  ("SAY","", "Where is the rice?"),
  ("HEAR","store employee", "It's in aisle five."),
  ("SAY","", "Thank you so much."),
 ]),
 ("Choose fruit, vegetables and meat", [
  ("SAY","", "These apples look good."),
  ("SAY","", "How much is this?"),
  ("HEAR","store employee", "It's on sale this week."),
  ("SAY","", "Keep the meat separate, please."),
 ]),
 ("Checkout", [
  ("HEAR","cashier", "Did you find everything okay?"),
  ("SAY","", "Yes, thank you."),
  ("HEAR","cashier", "Do you have a rewards card?"),
  ("HEAR","cashier", "Paper or plastic?"),
  ("SAY","", "I brought my own bags."),
 ]),
 ("Pay", [
  ("HEAR","cashier", "Cash or card?"),
  ("SAY","", "I'll pay by card."),
  ("HEAR","cashier", "Here's your receipt."),
  ("HEAR","cashier", "Have a great day!"),
  ("SAY","", "You too, thanks."),
 ]),
 ("Put the food away at home", [
  ("SAY","", "Let's put the food away."),
  ("SAY","", "The milk goes in the fridge."),
  ("SAY","", "Put the eggs inside, please."),
  ("HEAR","Sam", "Where does the rice go?"),
 ]),
], [
 ("https://www.eslnote.com/conversation/at-the-grocery-store.html",
  "\"Joon is pushing a cart and looking at a shopping list on his phone.\" Employee: \"Can I help you find anything?\" / \"Brown rice is in aisle 5\". Cashier: \"Did you find everything you were looking for today?\" / \"Do you have a rewards or membership card with us?\" / \"Would you like paper bags, plastic bags, or do you have your own reusable bags?\" / \"Will you be paying with cash or card?\" / \"Here's your receipt.\""),
 ("https://www.mashaenglish.com/courses/english-for-daily-life/01-at-the-supermarket",
  "\"Excuse me, where is the milk?\" / \"It's in aisle 5.\" / \"How much is this?\" / cashier: \"Do you need a bag?\" / \"Would you like the receipt?\""),
 ("https://www.foodsafety.gov/keep-food-safe/4-steps-to-food-safety",
  "(food-safety steps) \"In your shopping cart, separate raw meat, poultry, seafood, and eggs from other foods\"; \"Refrigerate perishable foods within 2 hours\"; \"keep eggs in their original carton and store them in the main compartment—not in the door.\""),
], [
 "Masha's page notes (Canada): \"the price on the label often does not include tax. The price at the checkout will be a little higher.\" The same is true in most US stores, but I did not open a US source for that, so treat it as unverified for the US.",
 "\"Put the eggs inside, please\" stands for FoodSafety.gov's advice to keep eggs in the main part of the fridge, not the door. The game does not need to teach that rule.",
 "No source I opened covers Thailand practice, so no US vs Thailand note.",
]))

LOC.append(("4. Cooking at home", "Nancy and Sam cook dinner together. Only Sam and Nancy speak.", [
 ("Choose a meal and read the recipe", [
  ("SAY","", "What should we cook tonight?"),
  ("SAY","", "Let's make Thai fried rice."),
  ("SAY","", "Let's read the recipe first."),
  ("HEAR","Sam", "That sounds good to me."),
 ]),
 ("Wash hands and get things ready", [
  ("SAY","", "Wash your hands first."),
  ("SAY","", "Get the pan, please."),
  ("HEAR","Sam", "Where is the big pot?"),
  ("SAY","", "It's under the sink."),
 ]),
 ("Wash and cut the food", [
  ("SAY","", "Wash the vegetables, please."),
  ("SAY","", "Chop the onion, please."),
  ("SAY","", "Use the other cutting board."),
  ("HEAR","Sam", "Is this small enough?"),
 ]),
 ("Cook on the stove", [
  ("SAY","", "Turn on the stove."),
  ("SAY","", "Add a little oil."),
  ("SAY","", "Stir it slowly, please."),
  ("HEAR","Sam", "Be careful, it's hot."),
 ]),
 ("Taste and finish", [
  ("SAY","", "Taste it, please."),
  ("HEAR","Sam", "It needs more salt."),
  ("SAY","", "Turn off the stove."),
  ("SAY","", "Dinner is ready!"),
 ]),
 ("Clean up and save leftovers", [
  ("SAY","", "Put leftovers in the fridge."),
  ("SAY","", "I will wash the dishes."),
  ("HEAR","Sam", "Thank you for dinner."),
 ]),
], [
 ("https://thestudentchef.com/learn-to-cook/",
  "\"Read the entire recipe before turning on the stove. Gather ingredients, identify the equipment and complete the cutting and measuring that must happen before cooking begins.\" Also: \"Wash your hands before cooking\" and \"taste before serving.\""),
 ("https://www.foodsafety.gov/keep-food-safe/4-steps-to-food-safety",
  "\"four simple steps: clean, separate, cook and, chill.\" \"Wash your hands often, especially ... Before, during, and after preparing food\"; \"Rinse fruits and vegetables under running water\"; \"Use one cutting board for fresh produce ... and another for raw meat\"; \"Refrigerate perishable foods within 2 hours\"."),
], [
 "FoodSafety.gov: \"Don't wash meat, poultry, eggs, or seafood\". So the wash line is for vegetables only.",
 "No source I opened covers Thailand practice, so no US vs Thailand note. Thai fried rice is a sample dish, not from a source.",
]))

LOC.append(("5. Eating together (home or restaurant)", "Part A is at home with Sam. Part B is at a restaurant; generic roles are host and server.", [
 ("Home: set the table and sit down", [
  ("SAY","", "Please set the table."),
  ("SAY","", "Come and eat, Sam!"),
  ("SAY","", "Let's pray before we eat."),
  ("HEAR","Sam", "This looks so good."),
 ]),
 ("Restaurant: arrive and get a table", [
  ("HEAR","host", "How many in your party?"),
  ("SAY","", "Table for two, please."),
  ("HEAR","host", "Right this way."),
  ("HEAR","server", "Here are your menus."),
 ]),
 ("Order drinks and food", [
  ("HEAR","server", "Something to drink?"),
  ("SAY","", "Water for me, please."),
  ("HEAR","server", "Are you ready to order?"),
  ("SAY","", "I'd like the chicken, please."),
  ("SAY","", "Not too spicy, please."),
 ]),
 ("During the meal", [
  ("HEAR","server", "How is everything?"),
  ("SAY","", "Everything is great, thank you."),
  ("SAY","", "This is delicious!"),
  ("SAY","", "Could I have more water?"),
 ]),
 ("Finish and pay", [
  ("SAY","", "I am full, thank you."),
  ("HEAR","Sam", "Do you want dessert?"),
  ("SAY","", "Could we have the check?"),
  ("HEAR","server", "Cash or card?"),
 ]),
 ("Leave or clean up", [
  ("HEAR","server", "Have a nice night!"),
  ("SAY","", "Thank you. Good night!"),
  ("SAY","", "I'll clear the table."),
  ("SAY","", "Let's take this home."),
 ]),
], [
 ("https://learnesl.net/english-at-the-restaurant/",
  "Sections in order: \"1. Entering the Restaurant\" (\"Table for two?\"), \"2. Sitting Down and Reading the Menu\" (\"Here are your menus.\"), \"3. Ordering Drinks\", \"4. Ordering Food\" (\"I'd like the chicken, please.\"), \"6. During the Meal\" (\"How is everything?\" / \"Everything is great, thank you.\"), \"9. Paying the Bill\" (\"Could we have the check, please? (US English)\" / \"Cash or card?\")."),
 ("https://www.mashaenglish.com/lessons/a2-ordering-food-restaurant",
  "\"Step 1: Arriving\" ... \"Step 5: Paying\"; \"How spicy is this?\"; \"This is delicious, thank you!\"; \"Could we have the bill / check, please?\""),
], [
 "Tipping (learnesl.net): \"In the US, tipping is expected (15–20%). In many other countries, tipping is optional or already included.\"",
 "Word choice (Masha): bill (UK) / check (US). The game should use \"check\".",
 "Polite forms (learnesl.net): \"Direct requests like I want… may sound rude. Softer forms like Could I have… or I'd like… are standard.\"",
 "Praying before the meal is the game's faith thread, not from a source.",
]))

LOC.append(("6. A day at home", "Nancy's day: morning, chores, going out, church (Sunday), evening, bedtime.", [
 ("Morning", [
  ("SAY","", "Good morning, Sam!"),
  ("SAY","", "I wake up at seven."),
  ("SAY","", "I brush my teeth."),
  ("SAY","", "Let's have breakfast together."),
 ]),
 ("Chores", [
  ("SAY","", "I do the laundry."),
  ("SAY","", "Can you help me, Sam?"),
  ("HEAR","Sam", "Please rest. I'll do it."),
  ("SAY","", "Thank you, my love."),
 ]),
 ("Going out", [
  ("SAY","", "I'm going to the store."),
  ("SAY","", "Where are my keys?"),
  ("HEAR","Sam", "Do you have your phone?"),
  ("SAY","", "I'll be back soon."),
 ]),
 ("Church (Sunday)", [
  ("HEAR","greeter", "Good morning! Welcome!"),
  ("SAY","", "This is my first time."),
  ("HEAR","greeter", "Here is a bulletin."),
  ("SAY","", "I like this song."),
  ("HEAR","pastor", "Let's pray together."),
 ]),
 ("Evening at home", [
  ("SAY","", "Let's have dinner now."),
  ("SAY","", "Let's watch TV."),
  ("SAY","", "I am tired tonight."),
 ]),
 ("Bedtime", [
  ("SAY","", "I take a shower."),
  ("SAY","", "Let's pray before bed."),
  ("SAY","", "Good night, Sam."),
  ("HEAR","Sam", "Sleep well, Nancy."),
 ]),
], [
 ("https://bostonenglishcenter.com/free-english-materials/a-day-in-my-life",
  "\"Wake up: stop sleeping.\" \"Brush my teeth\" \"Have breakfast\" \"Do chores: do jobs around the home.\" \"Go to bed: get into bed to sleep.\" \"In the morning, I brush my teeth. In the afternoon, I have lunch. In the evening, I watch TV.\""),
 ("https://findandvisitchurch.com/what-to-expect-at-church",
  "\"Most churches have greeters at the entrance who will welcome you, hand you a bulletin or program\"; \"Services typically begin with music\"; \"You can sing along, clap, or simply listen\"; \"The pastor or speaker will give a talk (usually 20–40 minutes) based on the Bible.\""),
], [
 "Church order varies (findandvisitchurch.com lists contemporary, traditional, liturgical and other styles). Music, sermon, offering and coffee after are common.",
 "Communion (findandvisitchurch.com): \"Policies vary — some welcome all attendees, others ask that only baptized believers participate. It is always okay to simply pass if you are not sure or not comfortable.\" Nancy is not baptized yet, so a game scene should not make her take communion.",
 "Offering (same source): \"As a visitor, you are never expected to contribute.\"",
 "\"Please rest. I'll do it\" is a gentle pregnancy line, not from a source.",
]))

def wc(s): return len(s.split())

lines = []
A = lines.append
A(P+"# Location step order and simple phrases for Nancy's Adventure English")
A(P+"Research only, not applied to the game.")
A(P+"Date: Monday Nov 2, 2026, 12:45 AM MST (Mountain time).")
A(P+"Based on: snap-r2h-0021MDT, pointer f6dac2d0, PASTE 317e91ce")
A("")
A(P+"Task: Maxwell t654u via Quartermaster. Each location follows real-world step order. Phrases are 3-6 words.")
A(P+"Key: SAY = Nancy says it. HEAR (role) = Nancy hears it from that person. Heroes are Sam and Nancy only. Other speakers are generic roles.")
A(P+"Every source below was opened with WebFetch this turn. Quotes are copied from the page. Lines marked \"not from a source\" are my content choices.")
A(P+"The hotel is skipped because Quartermaster already drafted it.")
A("")
counts = {}
allphr = []
for title, intro, steps, srcs, notes in LOC:
    A(P+"## "+title)
    A(P+intro)
    n=0
    for i,(st, phr) in enumerate(steps,1):
        A(P+"### Step %d: %s" % (i, st))
        for kind, who, text in phr:
            tag = "SAY" if kind=="SAY" else "HEAR (%s)" % who
            A(P+"- %s: \"%s\"" % (tag, text))
            n+=1; allphr.append((title, text, wc(text)))
    counts[title]=n
    A(P+"### Sources")
    for u,q in srcs:
        A(P+"- "+u)
        A(P+"  - Supports: "+q)
    A(P+"### What varies")
    for x in notes:
        A(P+"- "+x)
    A("")
A(P+"## Phrase counts")
for t,n in counts.items(): A(P+"- %s: %d phrases" % (t,n))
A(P+"- Total: %d phrases" % sum(counts.values()))
bad=[p for p in allphr if not (3<=p[2]<=6)]
A(P+"- Word-count exceptions (outside 3-6 words): %s" % ("none" if not bad else "; ".join('%s "%s" (%d)'%b for b in bad)))
A("")
A(P+"Ready to paste: none. CURRENT stays v5-37.")
open(OUT,"w",encoding="utf-8").write("\n".join(lines)+"\n")
print(counts, "bad:", bad)
