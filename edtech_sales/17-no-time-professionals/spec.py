import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Selling to professionals",
       "\"I don't have time\" means <em>\"I can't see where it fits.\"</em>",
       "How to answer the most common objection from working professionals.",
       photo=ph("hook"), brief="Busy professional")

c.side("What they mean",
       "They're not saying no. <em>They're saying how?</em>",
       "A professional with a job, a commute and a family can't picture adding a course to their week.",
       "Your job is to show them the week, not argue that it's possible.",
       tags=("Schedule", "Commitment"),
       photo=ph("side"), brief="Coffee and a laptop early in the morning")

c.compare("First reply",
          "Don't minimise. <em>Map it.</em>",
          "Wrong way", ["\"It's only 2 hours a day!\"", "\"Everyone manages somehow.\""],
          "Right way", ["\"Walk me through a normal weekday. Where's the quietest 45 minutes?\""])

c.script("The conversation",
         "Find the 45 minutes <em>together</em>",
         [("Prospect", "\"I leave at 8 and get back at 7. Then it's dinner and the kids.\""),
          ("You", "\"What about after the kids sleep, around 9:30? Or the train in the morning?\""),
          ("Prospect", "\"The train is 40 minutes. I just scroll my phone.\"")],
         "When they find the slot themselves, the objection is gone.")

c.steps("The framework",
        "The <em>busy-week plan</em>",
        [("Weekdays", "45 minutes: one lesson or one practice set."),
         ("Weekend", "One 2-hour live session or project block."),
         ("Missed a day", "Recordings and a catch-up plan. No guilt."),
         ("Monthly check-in", "A mentor call to adjust the plan.")])

c.save("Your no-time checklist",
       "Save this for your <em>next career call.</em>",
       ["<b>Don't say</b> \"it's only 2 hours\".",
        "<b>Ask them</b> to walk you through a weekday.",
        "<b>Find the 45 minutes</b> together.",
        "<b>Show a weekend block</b> for deeper work.",
        "<b>Explain the catch-up plan</b> for missed days.",
        "<b>Offer a mentor check-in</b> every month."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
