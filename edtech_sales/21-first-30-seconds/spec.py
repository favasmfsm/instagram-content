import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Call openings",
       "You lose most sales calls <em>in the first 30 seconds.</em>",
       "What to say when the lead picks up, so they keep listening.",
       photo=ph("hook"), brief="Person answering a phone call")

c.compare("The opening",
          "Pitch first vs <em>permission first</em>",
          "Pitch first", ["\"Hi, I'm calling from ABC Academy. We have a great new batch with top faculty…\"", "Fee and features before they even know why you called."],
          "Permission first", ["\"Hi Priya, this is Rahul from ABC Academy. You asked about NEET coaching yesterday. Is this a good time for 2 minutes?\"", "Name, reason, permission. Then a question."])

c.numbered("The <em>4-part opening</em>",
           [("Their name", "Say it first. It tells them this call is for them."),
            ("Your name and institute", "One line. No titles, no taglines."),
            ("Why you're calling", "Link it to what they did: the form, the demo, the webinar."),
            ("Ask permission", "\"Is now a good time for 2 minutes?\" A no means book a time.")],
           photo=ph("band"), brief="Counsellor on a headset")

c.script("How it sounds",
         "Open, then <em>ask one easy question</em>",
         [("You", "\"Hi Priya, this is Rahul from ABC Academy. You filled in our NEET form yesterday. Is now a good time for 2 minutes?\""),
          ("Lead", "\"Yes, okay.\""),
          ("You", "\"Great. Which class are you in right now?\"")],
         "An easy first question gets them talking. Leads who talk stay on the call.")

c.side("If it's a bad time",
       "A no now <em>isn't a no.</em>",
       "If they're busy, don't squeeze the pitch in. Book a time: \"Shall I call at 7 pm today, or tomorrow morning?\"",
       "Then call at exactly that time. That alone builds trust.",
       tags=("Respect", "Callbacks"),
       photo=ph("side"), brief="Person checking a watch")

c.bottom("Pro tip",
         "Never open <em>with the fee.</em>",
         "If they ask the fee first, don't dodge it. Give a range and ask one question: \"It depends on the batch. Which exam and year are you aiming for?\"",
         "<strong>Why:</strong> a fee without context is just a number to compare.",
         photo=ph("bottom"), brief="Notebook and phone on a desk")

c.save("Your call-opening checklist",
       "Save this for your <em>next 50 calls.</em>",
       ["<b>Say their name</b> first.",
        "<b>One line</b> for your name and institute.",
        "<b>Say why you're calling:</b> link it to what they did.",
        "<b>Ask permission</b> for 2 minutes.",
        "<b>Ask one easy question</b> to start.",
        "<b>No fee, no pitch</b> in the first 30 seconds."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
