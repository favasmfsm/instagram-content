import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Demo classes",
       "Your demo bookings aren't showing up. <em>Here's why.</em>",
       "Small fixes between the booking and the class that get more students in the room.",
       photo=ph("hook"), brief="Empty classroom chairs")

c.compare("The booking call",
          "Booked vs <em>confirmed</em>",
          "Booked", ["\"I'll send you the link.\"", "A time you picked, not one they chose."],
          "Confirmed", ["\"Does Saturday 11 am work for both you and your father?\"", "They say the time back to you, and it goes in their calendar."])

c.numbered("Why <em>they don't show up</em>",
           [("They forgot", "No reminder, or one sent days too early."),
            ("The parent didn't know", "Family plans clashed with the class."),
            ("No reason to come", "\"Free class\" sounds optional."),
            ("The link didn't work", "Wrong app, no login, last-minute panic.")],
           photo=ph("band"), brief="Student on a laptop at home")

c.steps("The fix",
        "A <em>no-show-proof</em> booking",
        [("On the call", "Pick the time together. Add the parent to the WhatsApp."),
         ("24 hours before", "A reminder with the link and what to keep ready."),
         ("1 hour before", "\"See you at 11! Here's the link again.\""),
         ("15 minutes after", "Didn't join? Call now and offer the next slot.")])

c.side("Give them a reason",
       "Send a <em>small pre-demo task.</em>",
       "\"Try these 5 questions before Saturday. We'll solve the ones you got stuck on in class.\"",
       "A student with unfinished questions has a reason to show up.",
       tags=("Commitment", "Curiosity"),
       photo=ph("side"), brief="Student solving a worksheet")

c.bottom("Pro tip",
         "Call no-shows <em>within 15 minutes.</em>",
         "Something came up, and they feel a little guilty. That's the best moment to rebook.",
         "<strong>Say:</strong> \"No problem at all. Shall I book you into Sunday's 11 am demo?\"",
         photo=ph("bottom"), brief="Phone call")

c.save("Your demo show-up checklist",
       "Save this for your <em>demo desk.</em>",
       ["<b>Confirm the time</b> on the same call.",
        "<b>Add the parent</b> to the WhatsApp.",
        "<b>Remind 24 hours</b> and 1 hour before.",
        "<b>Send the link</b> again with the reminder.",
        "<b>Give a small task</b> to bring to class.",
        "<b>Call no-shows</b> within 15 minutes."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
