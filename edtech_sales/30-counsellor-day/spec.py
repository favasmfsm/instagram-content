import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Sales teams",
       "Your counsellors are busy all day. <em>Are they selling?</em>",
       "A daily routine that puts the best hours into the calls that matter.",
       photo=ph("hook"), brief="Office team on phones")

c.side("The problem",
       "Busy <em>isn't productive.</em>",
       "Reports, WhatsApp forwards, internal meetings. Many counsellors spend their best hours on everything except calls.",
       "Protect the hours when parents and students actually pick up.",
       tags=("Focus", "Time"),
       photo=ph("side"), brief="Person at a busy desk")

c.steps("The framework",
        "A day <em>that sells</em>",
        [("Morning", "New leads first, before anything else."),
         ("Midday", "Follow-ups and demo reminders."),
         ("Evening, 4–8 pm", "Often the best time to reach parents. Calls only, no admin."),
         ("End of day", "Update every lead's stage and next date.")])

c.compare("Same 8 hours",
          "Busy vs <em>selling</em>",
          "Busy", ["Reports at 5 pm, when parents pick up.", "Meetings in the middle of call time."],
          "Selling", ["Admin before 11 am or after 8 pm.", "Meetings only outside call blocks."])

c.numbered("Track <em>4 things daily</em>",
           [("New leads called", "How many within 5 minutes?"),
            ("Conversations", "Calls where you actually spoke."),
            ("Demos booked", "With a fixed date and time."),
            ("Next steps set", "Every lead has a next date.")],
           photo=ph("band"), brief="Whiteboard with notes")

c.bottom("Pro tip",
         "Block call time <em>on the calendar.</em>",
         "Put the call blocks in every counsellor's calendar, and yours, so no one books a meeting over them.",
         "<strong>Manager rule:</strong> you don't interrupt call blocks either.",
         photo=ph("bottom"), brief="Laptop with a calendar")

c.save("Your counsellor-day checklist",
       "Save this for your <em>sales floor.</em>",
       ["<b>Call new leads first,</b> every morning.",
        "<b>Fixed call blocks</b> on the calendar.",
        "<b>One follow-up hour</b> for reminders.",
        "<b>No admin</b> in peak hours (4–8 pm).",
        "<b>Track 4 numbers</b> every day.",
        "<b>Update the pipeline</b> before you log off."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
