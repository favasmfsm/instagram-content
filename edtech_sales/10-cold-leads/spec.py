import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Lead re-engagement",
       "Last season's leads aren't dead. <em>They're waiting.</em>",
       "How to bring cold leads back for the new batch, without spamming them.",
       photo=ph("hook"), brief="Person on a laptop")

c.side("Why they still convert",
       "Cold leads <em>already know you.</em>",
       "Many just weren't ready last time: wrong timing, a board exam, a tight month.",
       "A new batch is a new reason to talk, not a reminder that they said no.",
       tags=("Timing", "Familiarity"),
       photo=ph("side"), brief="Notebook and planning")

c.numbered("Sort them <em>before you call</em>",
           [("Didn't attend the demo", "Invite them to a fresh demo."),
            ("Attended, didn't enrol", "Lead with what's new since then."),
            ("Said \"next year\"", "It's next year. Remind them, kindly."),
            ("Chose another institute", "Ask how it went. Some want a change.")],
           photo=ph("band"), brief="Office desk")

c.compare("The first message",
          "The <em>re-opener</em>",
          "Wrong way", ["\"Admissions open! Limited seats! Enrol now!\""],
          "Right way", ["\"Hi Mr. Joseph, last year you asked about JEE coaching for Anu. How did Class 11 go?\""])

c.script("When they reply",
         "Listen for <em>what changed</em>",
         [("Parent", "\"She's in Class 12 now. The boards are taking all her time.\""),
          ("You", "\"That's why we run a weekend batch for board-year students. Want me to share the schedule?\""),
          ("Parent", "\"Yes, send it.\"")],
         "Their new situation is your reason to talk. Fit the offer to it.")

c.steps("The framework",
        "The <em>re-engagement</em> sequence",
        [("Week 1", "A personal WhatsApp: ask how the year went."),
         ("Week 2", "Share one useful thing: a free mock or a revision plan."),
         ("Week 3", "Invite them to a fresh demo or a short call."),
         ("Then stop", "No reply after 3 tries? Leave them until next season.")])

c.save("Your cold-lead checklist",
       "Save this for your <em>cold-lead list.</em>",
       ["<b>Sort cold leads</b> by why they stopped.",
        "<b>Open with</b> their name and last year's question.",
        "<b>Ask what changed</b> before you pitch.",
        "<b>Offer something useful</b> first.",
        "<b>Invite them</b> to a fresh demo.",
        "<b>Stop after 3 tries</b> with no reply."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
