import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel

P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Demo class · Conversion",
       "Your demo class isn't a free class. <em>It's a sales call.</em>",
       "Most demo attendees never enrol. Here's what the ones who do experienced.",
       photo=ph("hook"), brief="Student in an online class on a laptop at home, engaged, natural light")

c.stat("The problem",
       "Most",
       "demo-class attendees never enrol, and it's <em>rarely because of the teaching.</em>",
       "Check yours: admissions ÷ demo attendees, last 3 batches")

c.numbered("4 ways teams <em>waste</em> a demo class",
           [("No goal set", "Nobody asked what the student is aiming for."),
            ("Teaching only", "A great class, but no moment that shows the gap."),
            ("Parent not around", "The person who pays never saw anything."),
            ("Silence after", "No call the same day, so the excitement fades.")],
           photo=ph("band"), brief="Teacher taking an online class on a laptop with a headset")

c.steps("The framework",
        "Run the demo <em>like a sales call</em>",
        [("Before", "Call the parent. Agree on one goal for the demo."),
         ("During", "Plan one win moment the student will remember."),
         ("Last 10 min", "A short quiz, then: what's working, and the one gap."),
         ("Within 1 hour", "Call. Start with the win, then the plan.")])

c.side("The win moment",
       "Plan the <em>win moment</em>",
       "Every student should leave the demo having solved something they couldn't before.",
       "That's what they'll tell their parent at dinner. Not the teacher's name. The win.",
       tags=("Confidence", "Recall"),
       photo=ph("side"), brief="Happy student solving a problem in a notebook")

c.script("The last 10 minutes",
         "Then comes <em>the gap talk</em>",
         [("You", "\"Arjun got 4 of 5 today. That's real progress in Physics.\""),
          ("Parent", "\"Oh, good. So he's fine?\""),
          ("You", "\"He's strong on concepts. Where he loses marks is timing. That's exactly what the next 8 weeks fix.\"")],
         "Praise first, then name one specific gap your course closes.")

c.compare("Same demo",
          "Two teams. <em>Two mindsets.</em>",
          "Free-class mindset", ["Teach the full chapter and hope they like it.", "Send the fee PDF afterwards."],
          "Sales-call mindset", ["Teach one thing, build one win, show one gap.", "Call within the hour, starting with the win."])

c.bottom("Pro tip",
         "Send the <em>class clip</em>, not the brochure.",
         "Parents trust what they saw their child do. A short clip of the win beats any PDF.",
         "<strong>Try it:</strong> clip the best minute of every demo.",
         photo=ph("bottom"), brief="Hand holding a phone playing a short video")

c.save("Your demo-class checklist",
       "Save this before your <em>next demo class.</em>",
       ["<b>Agree one goal</b> with the parent beforehand.",
        "<b>Plan one win moment</b> for the student.",
        "<b>Get the parent</b> to watch the last 10 minutes.",
        "<b>Praise first</b>, then name one gap.",
        "<b>Call within the hour</b>, starting with the win.",
        "<b>Send the clip</b>, not the brochure."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    if "--export" in sys.argv:
        print("exported", c.export(), "slides")
    else:
        print("built", c.build())
