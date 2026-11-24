import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Sales calls",
       "5 phrases that make parents <em>stop trusting you.</em>",
       "Counsellors say them every day. Here's what to say instead.",
       photo=ph("hook"), brief="Person talking on the phone")

c.numbered("5 phrases <em>to drop today</em>",
           [("\"We guarantee a top rank.\"", "Nobody can. Parents know it."),
            ("\"Only 2 seats left!\"", "Unless it's true, it's a lie they'll catch."),
            ("\"Everyone joins us.\"", "Pressure, not proof."),
            ("\"Decide today or lose the offer.\"", "Rushing reads as desperation."),
            ("\"That other institute is useless.\"", "It makes you look small, not them.")],
           photo=ph("band"), brief="Two people talking")

c.compare("Phrase 1",
          "Instead of <em>promising a rank</em>",
          "Stop saying", ["\"Your child will definitely get a top-100 rank.\""],
          "Say instead", ["\"Here's what we'll work on each week, and how you'll see progress in the mock scores.\""])

c.compare("Phrases 2 and 3",
          "Instead of <em>pressure</em>",
          "Stop saying", ["\"Only 2 seats left!\"", "\"Everyone in your area joins us.\""],
          "Say instead", ["\"The batch starts on the 15th.\"", "\"Can I connect you with a parent from your area?\""])

c.compare("Phrases 4 and 5",
          "Instead of <em>rushing and attacking</em>",
          "Stop saying", ["\"Decide today or the offer is gone.\"", "\"That institute is useless.\""],
          "Say instead", ["\"Take tonight. Can I call you at 7 tomorrow?\"", "\"Good that you're comparing. Ask them about batch size and doubt support too.\""])

c.save("Your phrase swap list",
       "Save this and <em>share it with your team.</em>",
       ["<b>Never promise</b> a rank or a result.",
        "<b>Only state seat limits</b> that are real.",
        "<b>Offer a parent reference</b>, not \"everyone joins\".",
        "<b>Give time</b>, then book a follow-up.",
        "<b>Never criticise</b> another institute.",
        "<b>Show the weekly plan</b> instead of promises."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
