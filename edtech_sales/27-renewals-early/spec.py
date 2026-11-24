import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Renewals",
       "Your renewals are decided <em>long before the renewal call.</em>",
       "How to keep students for next year with what you do this year.",
       photo=ph("hook"), brief="Parent and student together")

c.side("The problem",
       "The renewal call <em>comes too late.</em>",
       "By the time you call about next year, the parent has already decided, based on the last 10 months.",
       "Renewals are won in monthly reports, not in the final pitch.",
       tags=("Retention", "Parents"),
       photo=ph("side"), brief="Parent reading a report")

c.steps("The framework",
        "A <em>renewal year</em> in 4 steps",
        [("Every month", "A short progress report: marks, attendance, one next step."),
         ("Mid-year", "A parent meeting with a plan for next year."),
         ("After a win", "A good test or result? That's when you ask."),
         ("Before the year ends", "An early-renewal benefit with a real deadline.")])

c.compare("The renewal call",
          "Pitch vs <em>review</em>",
          "Pitch", ["\"Next year's batch is starting. Shall I book a seat?\"", "A discount if they ask twice."],
          "Review", ["\"Let's look at how her scores moved this year, and what next year needs to focus on.\"", "The plan first, then the fee."])

c.script("After a win",
         "Ask <em>at the right moment</em>",
         [("You", "\"Congratulations! Aisha scored 82% in this month's test, up from 64% in June.\""),
          ("Parent", "\"Yes, we're really happy.\""),
          ("You", "\"Let's keep that going. Can we plan next year together this week, while it's fresh?\"")],
         "A parent who has just seen progress is ready to talk about what's next.")

c.bottom("Pro tip",
         "Make the early-renewal benefit <em>real.</em>",
         "A fee lock or a free test series, with a published end date that doesn't move.",
         "<strong>Rule:</strong> early renewers should never pay more than late ones.",
         photo=ph("bottom"), brief="Calendar")

c.save("Your renewal checklist",
       "Save this for <em>this academic year.</em>",
       ["<b>Send a progress report</b> every month.",
        "<b>Hold a mid-year meeting</b> with a next-year plan.",
        "<b>Ask after a win moment,</b> not at random.",
        "<b>Review before you pitch</b> on the renewal call.",
        "<b>Offer an early-renewal benefit</b> with a real deadline.",
        "<b>Never charge early renewers</b> more."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
