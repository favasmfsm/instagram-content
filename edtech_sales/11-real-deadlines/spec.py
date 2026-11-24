import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Urgency",
       "Fake deadlines kill trust. <em>Real ones close admissions.</em>",
       "How to create urgency without lying to parents.",
       photo=ph("hook"), brief="Clock")

c.side("Why fake urgency backfires",
       "Parents <em>talk to each other.</em>",
       "\"Last 2 seats!\" works once. Then a parent sees the same batch advertised next month.",
       "After that, nothing you say about dates or seats is believed.",
       tags=("Trust", "Word of mouth"),
       photo=ph("side"), brief="Two parents talking")

c.compare("Same push",
          "Fake urgency vs <em>real urgency</em>",
          "Fake", ["\"Only 2 seats left!\" (when there are 40.)", "\"Offer ends tonight!\" (every night.)"],
          "Real", ["\"The batch starts on the 15th. Joining later means catching up on 3 weeks.\"", "\"The early-bird fee ends on Friday, as listed on our site.\""])

c.numbered("Real deadlines <em>you already have</em>",
           [("The batch start date", "Joining late means missed classes. That's a real cost."),
            ("A seat limit per batch", "Only if you actually cap it. Say the number."),
            ("Early-bird fee end", "A published date that doesn't move."),
            ("Scholarship test date", "A fixed day with a clear benefit.")],
           photo=ph("band"), brief="Classroom")

c.script("How to say it",
         "Give the date <em>and the reason</em>",
         [("Parent", "\"We'll probably join next month.\""),
          ("You", "\"That works. Just so you know, the batch starts on the 15th, so joining next month means 3 weeks of catching up. Would you like the recordings plan for late joiners?\""),
          ("Parent", "\"Oh. Maybe we should start now, then.\"")],
         "A real deadline with a real reason doesn't feel like pressure. It feels like information.")

c.bottom("Pro tip",
         "Put every deadline <em>in writing.</em>",
         "Same dates on your website, WhatsApp and every call. Consistent deadlines are believable deadlines.",
         "<strong>Rule:</strong> if you'd be embarrassed to see it screenshotted, don't say it.",
         photo=ph("bottom"), brief="Calendar or planner")

c.save("Your urgency checklist",
       "Save this before your <em>next batch launch.</em>",
       ["<b>Only use deadlines</b> that are true.",
        "<b>Give the reason</b> with every date.",
        "<b>Publish dates</b> and never move them quietly.",
        "<b>Say the real number</b> if seats are capped.",
        "<b>Offer a late-joiner plan</b> instead of pressure.",
        "<b>Never say</b> \"last 2 seats\" unless it's true."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
