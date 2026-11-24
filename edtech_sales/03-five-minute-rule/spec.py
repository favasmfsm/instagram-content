import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Speed to lead",
       "Your leads aren't cold. You're <em>calling too late.</em>",
       "The first call wins more admissions than the best script. Here's how to make it within 5 minutes.",
       photo=ph("hook"), brief="Counsellor with a headset on a call")

c.stat("The window",
       "5 min",
       "After that, the parent is already <em>filling in another institute's form.</em>",
       "Check yours: time from form fill to first call, this week")

c.side("Why speed wins",
       "The first caller <em>sets the frame.</em>",
       "A parent who just filled in your form is thinking about this decision right now. An hour later, they're cooking dinner.",
       "Call first and every other institute gets compared against your answers.",
       tags=("Intent", "Recall"),
       photo=ph("side"), brief="Student or parent picking up a phone call")

c.numbered("4 reasons leads <em>wait too long</em>",
           [("A shared inbox", "Everyone assumes someone else called."),
            ("Nobody owns the lead", "No name on it, so no one is accountable."),
            ("Counsellors stuck on long calls", "New leads queue up behind one conversation."),
            ("Leads after office hours", "Evening forms sit untouched until morning.")],
           photo=ph("band"), brief="Busy sales office")

c.steps("The framework",
        "Set up a <em>5-minute</em> lead flow",
        [("Route", "Every lead goes to one named counsellor, automatically."),
         ("Alert", "An instant WhatsApp or app alert, not an email."),
         ("Reply", "Auto-message: \"We'll call you in 5 minutes.\""),
         ("Call", "No answer? Retry at 15 minutes, then 2 hours.")])

c.script("The first 30 seconds",
         "Open with <em>a question</em>, not a pitch",
         [("You", "\"Hi, this is Anjali from Bright Path. You just asked about our NEET batch, so I called right away. Do you have 3 minutes?\""),
          ("Parent", "\"Yes, go ahead.\""),
          ("You", "\"Great. What made you start looking for coaching today?\"")],
         "Mention the form they filled, ask permission, then ask a question. The pitch comes later.")

c.save("Your lead-desk checklist",
       "Save this for your <em>lead desk.</em>",
       ["<b>Call every lead</b> within 5 minutes.",
        "<b>One named owner</b> for every lead.",
        "<b>Instant alerts</b>, not email.",
        "<b>Auto-reply</b> with a callback promise.",
        "<b>Retry</b> at 15 minutes and 2 hours.",
        "<b>Open with a question</b>, not a pitch."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
