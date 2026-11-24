import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Discovery calls",
       "If you're doing most of the talking, <em>you're losing the call.</em>",
       "5 questions that get the parent selling your course to themselves.",
       photo=ph("hook"), brief="Student studying")

c.side("Discovery first",
       "Ask first. <em>Pitch later.</em>",
       "A pitch before questions is a guess. You don't yet know which part of your course matters to this family.",
       "Questions also show you care about the child, not just the admission.",
       tags=("Discovery", "Trust"),
       photo=ph("side"), brief="Two people in conversation")

c.numbered("5 questions that <em>sell for you</em>",
           [("What score are you aiming for?", "Sets the goal your course must reach."),
            ("What happened last exam?", "Shows the gap, in their words."),
            ("What have you tried so far?", "Tells you what not to repeat."),
            ("What's stopping progress?", "Names the problem you'll solve."),
            ("What if nothing changes?", "Makes the cost of waiting real.")],
           photo=ph("band"), brief="Open notebook with notes")

c.script("Use their answers",
         "Then repeat <em>their numbers</em> back",
         [("Parent", "\"He scored 410 in the mock. He needs 600 for a government seat.\""),
          ("You", "\"So the gap is about 190 marks, mostly in Physics, you said?\""),
          ("Parent", "\"Yes, Physics is the problem.\"")],
         "When you do pitch, pitch only to that gap.")

c.compare("Same course",
          "Two pitches. <em>One wins.</em>",
          "Feature dump", ["\"We have 40 faculty, 2,000 videos and an app.\"", "Every feature, for every parent."],
          "Gap pitch", ["\"Our weekly Physics mock reviews target exactly that 190-mark gap.\"", "One feature, tied to their goal."])

c.save("The 5 discovery questions",
       "Save these <em>5 questions.</em>",
       ["<b>What score</b> are you aiming for?",
        "<b>What happened</b> in the last exam?",
        "<b>What have you tried</b> so far?",
        "<b>What's stopping</b> progress right now?",
        "<b>What happens</b> if nothing changes?",
        "<b>Then pitch</b> only to the gap they named."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
