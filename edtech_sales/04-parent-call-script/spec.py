import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Parent calls",
       "The student says yes. <em>The parent pays.</em>",
       "A call script that speaks to both, without losing either.",
       photo=ph("hook"), brief="Parent with their child")

c.side("Who decides",
       "Two people, <em>two decisions.</em>",
       "The student decides if they want it. The parent decides if it's worth it.",
       "Pitch to only one of them and the other says no for both.",
       tags=("Student", "Parent"),
       photo=ph("side"), brief="Teenager studying")

c.numbered("What each one <em>needs to hear</em>",
           [("Student: it's doable", "A clear daily plan, not a mountain of syllabus."),
            ("Student: it's not boring", "Live classes, friends in the batch, quick doubt help."),
            ("Parent: it works", "Last batch's results and a teacher they can talk to."),
            ("Parent: it's safe", "Attendance updates, progress reports, no surprises.")],
           photo=ph("band"), brief="Family at home")

c.script("Step 1",
         "Bring the parent <em>into the call</em>",
         [("You", "\"This sounds like a great fit for you. Who usually decides on classes at home?\""),
          ("Student", "\"My mom.\""),
          ("You", "\"Could we get her on the call for 5 minutes? I'd like her to hear the plan too.\"")],
         "Ask early and naturally. A parent who hears it from you doesn't have to hear it second-hand.")

c.script("Step 2",
         "Then talk <em>to the parent</em>",
         [("You", "\"Meera is aiming for a top-500 rank. What worries you most about this year?\""),
          ("Parent", "\"She studies a lot, but her mock scores aren't improving.\""),
          ("You", "\"That's common. Can I show you how we track mock scores every week?\"")],
         "Lead with the child's goal, then the parent's worry. Your course answers both.",
         ground="")

c.steps("The framework",
        "The <em>joint call</em> in 4 moves",
        [("Student first", "Agree on the goal, in their words."),
         ("Invite the parent", "Ask who decides and bring them on."),
         ("The parent's worry", "Ask, listen, repeat it back."),
         ("One plan", "Show how the course answers both.")])

c.bottom("Pro tip",
         "Send the parent <em>their own summary.</em>",
         "After the call, WhatsApp the parent 3 lines: the goal, the worry and the plan.",
         "<strong>Try it:</strong> \"Goal: top 500. Concern: mock scores. Plan: weekly tracked tests.\"",
         photo=ph("bottom"), brief="Parent reading a message on their phone")

c.save("Your parent-call checklist",
       "Save this before your <em>next parent call.</em>",
       ["<b>Ask the student</b> who decides at home.",
        "<b>Get the parent on</b> during the first call.",
        "<b>Student:</b> the goal, in their words.",
        "<b>Parent:</b> ask what worries them.",
        "<b>Show one plan</b> that answers both.",
        "<b>Send the parent</b> a 3-line summary."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
