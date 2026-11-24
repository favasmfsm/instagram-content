import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Marketing",
       "Stop collecting leads with <em>\"Download brochure\".</em>",
       "5 lead magnets that bring serious students, and how to follow up on each.",
       photo=ph("hook"), brief="Student taking a test")

c.compare("Brochure vs lead magnet",
          "What you offer <em>decides who signs up</em>",
          "Brochure", ["Attracts anyone mildly curious.", "Gives you nothing to talk about on the call."],
          "Lead magnet", ["Attracts students actively preparing.", "Gives you their score, goal or gap before you call."])

c.numbered("5 lead magnets <em>that work</em>",
           [("A free mock test", "Every result is a reason to call."),
            ("A rank or score predictor", "They tell you their marks and their target."),
            ("A previous-year question pack", "Pulls in students already revising."),
            ("A study planner", "Shows you how many weeks they have left."),
            ("A career-switch roadmap", "For professionals: their current role and goal.")],
           photo=ph("band"), brief="Exam paper and pencil")

c.side("The follow-up",
       "The magnet <em>is the opener.</em>",
       "Don't call to pitch. Call to talk about their result: the score, the plan, the gap.",
       "It's the most natural first call you'll ever make.",
       tags=("Mock test", "Predictor"),
       photo=ph("side"), brief="Student looking at results on a laptop")

c.script("The first call",
         "Open with <em>their result</em>",
         [("You", "\"Hi Riya, you took our free NEET mock yesterday. You scored 520. Do you want to know where the next 80 marks are hiding?\""),
          ("Student", "\"Yes, definitely.\""),
          ("You", "\"Most of what you dropped was in Organic Chemistry. Let me show you how we'd fix that in 6 weeks.\"")],
         "Their result is more interesting to them than your course. Start there.")

c.save("Your lead-magnet checklist",
       "Save this for your <em>next campaign.</em>",
       ["<b>Swap the brochure</b> for something useful.",
        "<b>Collect a score, goal or gap</b> with every sign-up.",
        "<b>Match the magnet</b> to the exam and the stage.",
        "<b>Call within the hour</b>, while they care.",
        "<b>Open with their result</b>, not your course.",
        "<b>Pitch only to the gap</b> the result shows."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
