import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Objection handling",
       "\"We'll join next year\" <em>often costs a student a year.</em>",
       "How to answer timing objections with the calendar, not pressure.",
       photo=ph("hook"), brief="Calendar pages")

c.side("What they mean",
       "\"Later\" <em>feels safe.</em>",
       "Parents want board exams to finish first, or think there's plenty of time. Often they haven't counted the weeks.",
       "Don't argue. Count them together.",
       tags=("Timing", "Planning"),
       photo=ph("side"), brief="Parent and teen at a table")

c.script("Count back",
         "Do the math <em>on the call</em>",
         [("Parent", "\"We'll start after his board exams.\""),
          ("You", "\"That makes sense. Can we count back together? If the entrance exam is in May and he starts in April, that's about 4 weeks. How long do you think the full syllabus needs?\""),
          ("Parent", "\"Hmm. That's not much time.\"")],
         "When the parent does the math, it's their conclusion, not your pressure.")

c.numbered("Options <em>between now and later</em>",
           [("Foundation batch", "A lighter pace that works alongside school."),
            ("Weekend batch", "Two days a week, so boards don't suffer."),
            ("Boards-plus-entrance plan", "One timetable for both exams."),
            ("A booked check-in", "If they still wait, fix a date to call back.")],
           photo=ph("band"), brief="Student studying at a desk")

c.compare("Same goal",
          "Pressure vs <em>planning</em>",
          "Pressure", ["\"If you don't join now, you'll regret it.\"", "\"Seats are filling fast!\""],
          "Planning", ["\"Let's look at the weeks left before the exam.\"", "\"Here's a lighter batch that fits around boards.\""])

c.bottom("Pro tip",
         "If they still say later, <em>fix the date.</em>",
         "\"Shall I call you on 20 March, the day after his last board paper?\" Put it in your CRM and keep it.",
         "<strong>Why:</strong> a booked call-back keeps the conversation alive.",
         photo=ph("bottom"), brief="Planner with dates")

c.save("Your timing-objection checklist",
       "Save this for the <em>next \"next year\".</em>",
       ["<b>Don't argue</b> with \"later\".",
        "<b>Count back</b> from the exam date together.",
        "<b>Show what the extra months</b> make possible.",
        "<b>Offer a foundation</b> or weekend batch.",
        "<b>No fake urgency</b>: use the real calendar.",
        "<b>Book a check-in date</b> if they still wait."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
