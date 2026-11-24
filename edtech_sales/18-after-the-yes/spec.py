import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("After the sale",
       "The sale isn't done at \"yes\". <em>Week 1 decides if they stay.</em>",
       "How to close the payment and onboard new students so they don't ask for a refund.",
       photo=ph("hook"), brief="Student starting a class")

c.script("On the same call",
         "Close the payment <em>while they're sure</em>",
         [("Parent", "\"Okay, let's go ahead.\""),
          ("You", "\"Great. I'll send the payment link right now. Would you like the full fee or the 3-month EMI? I'll stay on the line while you check it.\""),
          ("Parent", "\"EMI, please.\"")],
         "\"I'll send the details later\" gives doubt a whole evening to grow.")

c.numbered("Why new students <em>drop out in week 1</em>",
           [("Confused by the app", "Couldn't log in, didn't ask."),
            ("Missed the first class", "Then felt too far behind."),
            ("Nobody called", "The counsellor moved on to new leads."),
            ("No early win", "A week in, nothing feels different yet.")],
           photo=ph("band"), brief="Student confused at a laptop")

c.steps("The framework",
        "The <em>first 7 days</em>",
        [("Day 0", "Welcome call: app set up together, first class booked."),
         ("Day 1", "Reminder an hour before the first class."),
         ("Day 3", "Check-in call: \"How was the first class?\""),
         ("Day 7", "One small win shared with the parent.")])

c.side("The handover",
       "Introduce the <em>mentor by name.</em>",
       "After payment, the counsellor shouldn't just disappear. Hand over to a named mentor on a short call.",
       "A face and a name stop the \"who do I even ask?\" feeling.",
       tags=("Mentor", "Handover"),
       photo=ph("side"), brief="Mentor talking with a student")

c.bottom("Pro tip",
         "Send the parent <em>a day-7 update.</em>",
         "Attendance, one thing their child did well and what's next. Three lines on WhatsApp.",
         "<strong>Why:</strong> a parent who sees progress in week 1 doesn't ask for a refund.",
         photo=ph("bottom"), brief="Parent smiling at a phone")

c.save("Your first-week checklist",
       "Save this for <em>every new admission.</em>",
       ["<b>Send the payment link</b> on the same call.",
        "<b>Set up the app together</b> on day 0.",
        "<b>Remind them</b> before the first class.",
        "<b>Call on day 3</b> to ask how it went.",
        "<b>Hand over</b> to a named mentor.",
        "<b>Send the parent</b> a day-7 update."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
