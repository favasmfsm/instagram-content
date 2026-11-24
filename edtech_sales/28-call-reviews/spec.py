import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Sales coaching",
       "Your best sales training <em>is already recorded.</em>",
       "How to coach counsellors using their own calls.",
       photo=ph("hook"), brief="Headphones and laptop")

c.side("The problem",
       "One-day training <em>doesn't stick.</em>",
       "A workshop is forgotten by the next week. Real calls show what's actually happening.",
       "Short, regular reviews change habits.",
       tags=("Coaching", "Habits"),
       photo=ph("side"), brief="Manager and team member talking")

c.numbered("Score every call <em>on 4 things</em>",
           [("Opening", "Name, reason and permission in 30 seconds?"),
            ("Discovery", "Did they ask before they pitched?"),
            ("Objection", "Did they handle it, or drop the fee?"),
            ("Next step", "Did the call end with a fixed date and time?")],
           photo=ph("band"), brief="Team meeting")

c.steps("The framework",
        "A <em>weekly review</em> routine",
        [("Pick 3 calls", "One win, one loss, one random. Per counsellor."),
         ("Listen together", "20 minutes. The counsellor scores it first."),
         ("Find one moment", "The exact point where the call turned."),
         ("Role-play it", "Practise that moment twice. Then the next call.")])

c.compare("Feedback",
          "Vague vs <em>specific</em>",
          "Vague", ["\"Be more confident.\"", "\"Close better.\""],
          "Specific", ["\"At 3:40 she said 'expensive', and you offered EMI before asking 'compared to what?'\"", "One thing to try on the next call."])

c.bottom("Pro tip",
         "Start with <em>your best counsellor's calls.</em>",
         "Play one great call to the whole team every week. People copy what they hear.",
         "<strong>Note:</strong> tell leads that calls may be recorded, and follow local consent rules.",
         photo=ph("bottom"), brief="Microphone or headset")

c.save("Your call-review checklist",
       "Save this for your <em>Monday team meeting.</em>",
       ["<b>Review 3 calls</b> per counsellor every week.",
        "<b>Score 4 things:</b> opening, discovery, objection, next step.",
        "<b>Let them score</b> their own call first.",
        "<b>Find the one moment</b> the call turned.",
        "<b>Role-play it</b> twice.",
        "<b>Give one specific fix,</b> not \"be confident\"."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
