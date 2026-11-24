import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Objection handling",
       "When a parent names another institute, <em>don't attack it.</em>",
       "How to answer \"The other place is cheaper\" without dropping your fee or badmouthing anyone.",
       photo=ph("hook"), brief="Parent comparing brochures")

c.side("Why it happens",
       "They're <em>comparing, not leaving.</em>",
       "A parent who mentions another institute is still on the phone with you. They want help deciding.",
       "Your job is to make the comparison fair, not to win an argument.",
       tags=("Comparison", "Trust"),
       photo=ph("side"), brief="Parent thinking over papers")

c.compare("First reply",
          "Defend vs <em>get curious</em>",
          "Defend", ["\"Their faculty isn't good.\"", "\"Okay, we can match that price.\""],
          "Get curious", ["\"That's a good option to look at. What did you like about them?\"", "\"What matters most to you in choosing?\""])

c.numbered("Compare on <em>what matters</em>",
           [("Batch size", "How many students per teacher?"),
            ("Doubt support", "Who answers doubts, and how fast?"),
            ("Tests and feedback", "How often, and does someone explain the mistakes?"),
            ("Similar students' results", "Students who started at the same level.")],
           photo=ph("band"), brief="Small classroom batch")

c.script("How to say it",
         "Make the comparison <em>fair</em>",
         [("Parent", "\"XYZ Classes is ₹15,000 cheaper.\""),
          ("You", "\"That's a real difference. Before you decide, ask them three things: batch size, who clears doubts, and how often tests are reviewed. Then compare us on the same three.\""),
          ("Parent", "\"Okay. I hadn't asked them that.\"")],
         "You're helping them choose well. Parents remember who helped, even if they don't join that day.")

c.bottom("Pro tip",
         "Send a <em>one-page comparison sheet.</em>",
         "Blank columns for any two institutes: fee, batch size, doubt support, tests and results. Share it on WhatsApp.",
         "<strong>Rule:</strong> never fill in the other institute's column yourself.",
         photo=ph("bottom"), brief="Checklist on a clipboard")

c.save("Your competitor-objection checklist",
       "Save this for the <em>next comparison call.</em>",
       ["<b>Never badmouth</b> the other institute.",
        "<b>Ask what they liked</b> about it.",
        "<b>Ask what matters most</b> to them.",
        "<b>Compare on 4 things:</b> batch, doubts, tests, results.",
        "<b>Don't drop your fee</b> to match.",
        "<b>Send a blank comparison sheet</b> on WhatsApp."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
