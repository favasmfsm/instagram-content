import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Objection handling",
       "\"What if it doesn't work?\" <em>is a buying signal, not a no.</em>",
       "How to answer \"What if my child doesn't get selected?\" without promising a rank.",
       photo=ph("hook"), brief="Thoughtful parent")

c.side("Read the signal",
       "They're <em>picturing joining.</em>",
       "A parent who asks about failure is already imagining paying. They need a reason to trust you with the risk.",
       "Answer honestly and you move forward. Promise a rank and you lose trust.",
       tags=("Risk", "Honesty"),
       photo=ph("side"), brief="Parent thinking at home")

c.compare("Your answer",
          "Promise vs <em>proof</em>",
          "Promise", ["\"Don't worry, selection is guaranteed.\"", "\"All our students get through.\""],
          "Proof", ["\"No one can honestly promise a selection. Here's what we can promise.\"", "Show the plan, the tracking and the policy."])

c.numbered("What you <em>can</em> guarantee",
           [("Every class happens", "Schedule, faculty and hours in writing."),
            ("Regular tests", "With marks and feedback shared with you."),
            ("Mentoring", "A named mentor and monthly progress calls."),
            ("A clear refund policy", "Written, with dates. No surprises.")],
           photo=ph("band"), brief="Mentor with a student")

c.script("How to say it",
         "Honest <em>and confident</em>",
         [("Parent", "\"What if he doesn't get selected after all this?\""),
          ("You", "\"That's the right question. No one can honestly promise a selection. What I can promise is that you'll see his test scores every month, so if something isn't working, we'll know early and change the plan.\""),
          ("Parent", "\"So I'd know before the exam.\"")],
         "Parents don't need a guarantee. They need to know they won't be surprised.")

c.bottom("Pro tip",
         "Share the refund policy <em>in writing.</em>",
         "Send it on WhatsApp before they pay, even if they don't ask. The same policy for everyone.",
         "<strong>Why:</strong> a written policy shows you expect to keep your promises.",
         photo=ph("bottom"), brief="Signing a document")

c.save("Your \"what if\" checklist",
       "Save this for your <em>next worried parent.</em>",
       ["<b>Treat \"what if\"</b> as a buying signal.",
        "<b>Never promise</b> a rank or selection.",
        "<b>Say what you do guarantee:</b> classes, tests, mentoring.",
        "<b>Show monthly tracking</b> they'll see.",
        "<b>Explain how you'll change the plan</b> if scores dip.",
        "<b>Share the refund policy</b> in writing."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
