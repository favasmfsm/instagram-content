import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Ad leads",
       "Not every Meta lead is a lead. <em>Find out in 2 questions.</em>",
       "How to qualify ad-form leads fast, so your counsellors call the right people first.",
       photo=ph("hook"), brief="Person scrolling on a phone")

c.side("The problem",
       "Ad leads are <em>curious, not committed.</em>",
       "One tap on an Instagram form isn't a decision. Many don't remember filling it in.",
       "Treat every one the same and your best counsellors spend their day on the least serious leads.",
       tags=("Intent", "Counsellor time"),
       photo=ph("side"), brief="Phone on a desk")

c.script("Question 1 and 2",
         "Two questions <em>sort almost everyone</em>",
         [("You", "\"Which exam are you preparing for, and which year are you appearing?\""),
          ("Student", "\"NEET, next May.\""),
          ("You", "\"Got it. And who will decide on coaching, you or your parents?\"")],
         "The exam and year tell you urgency. The decision-maker tells you who to talk to next.")

c.numbered("Score them <em>in 3 groups</em>",
           [("Hot", "Exam within a year, decision-maker on the call."),
            ("Warm", "Right exam, but later, or someone else decides."),
            ("Cold", "Just browsing, wrong course, or no clear exam.")],
           photo=ph("band"), brief="Office team at work")

c.steps("The framework",
        "What to do <em>with each group</em>",
        [("Hot", "Book a demo or counselling call on this call."),
         ("Warm", "Send one useful resource. Call again in 2 days."),
         ("Cold", "Add to a monthly newsletter. No more calls."),
         ("Wrong fit", "Thank them and close the lead. Keep the CRM clean.")])

c.save("Your ad-lead checklist",
       "Save this for your <em>ad-lead desk.</em>",
       ["<b>Ask the exam</b> and the year first.",
        "<b>Ask who decides</b> on coaching.",
        "<b>Tag every lead</b> hot, warm or cold.",
        "<b>Hot leads:</b> book a demo on the call.",
        "<b>Warm leads:</b> one resource, call in 2 days.",
        "<b>Cold leads:</b> newsletter, not calls."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
