import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel

# Filled in once photos are picked: slot -> "photos/<file>.jpg"
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Objection handling",
       "Stop dropping your fee the moment a parent <em>hesitates.</em>",
       "\"It's too expensive\" rarely means what you think. Here's how to handle it.",
       photo=ph("hook"), brief="Indian parent on a phone call at home, thoughtful expression, natural light")

c.side("Why it backfires",
       "The quick discount <em>costs you twice.</em>",
       "A discount offered in the first minute tells the parent your fee was never real.",
       "And the next parent in their WhatsApp group will ask for the same price.",
       tags=("Trust", "Margin"),
       photo=ph("side"), brief="Family budget on a table: calculator, notebook, bills")

c.numbered("\"Expensive\" usually means <em>one of 3 things</em>",
           [("Budget", "The money genuinely isn't there right now."),
            ("Comparison", "Another institute quoted less."),
            ("Doubt", "They're not yet sure it will work for their child.")],
           photo=ph("band"), brief="Parent and teenager talking at a table at home")

c.script("Objection · Budget",
         "When it's really <em>the budget</em>",
         [("Parent", "\"Honestly, this is more than we planned for this year.\""),
          ("You", "\"That's fair. Can I ask what you'd planned for? Let's see what we can make work.\""),
          ("Parent", "\"Around half of that.\"")],
         "Find the real number before you offer anything. Then talk EMI or a shorter plan, not a discount.")

c.script("Objection · Comparison",
         "When they're <em>comparing</em> you",
         [("Parent", "\"Another academy is offering the same course for less.\""),
          ("You", "\"Good that you're comparing. What did they include? Batch size, doubt sessions, mock tests?\""),
          ("Parent", "\"I didn't ask about all that.\"")],
         "Turn price into a comparison of what's included. Never criticise the other institute.",
         ground="")

c.steps("The framework",
        "4 steps before you <em>touch the price</em>",
        [("Ask", "\"Compared to what?\" Find out which of the 3 it is."),
         ("Isolate", "\"Apart from the fee, is anything else stopping you?\""),
         ("Reframe", "Cost per month, per class, per mark gained."),
         ("Offer", "Only now: EMI, a shorter plan or a scholarship test.")])

c.bottom("When to offer EMI",
         "EMI is a tool, <em>not a reflex.</em>",
         "Offer it once the parent is sold on the course but not on the lump sum. Earlier, it sounds like a discount in disguise.",
         "<strong>Ask first:</strong> \"If the fee were monthly, would you start this batch?\"",
         photo=ph("bottom"), brief="Hand holding a phone showing a payment screen")

c.save("Your price-objection checklist",
       "Save this for your <em>next price objection.</em>",
       ["<b>Never discount</b> on the first call.",
        "<b>Ask \"compared to what?\"</b> before anything else.",
        "<b>Find the real reason:</b> budget, comparison or doubt.",
        "<b>Compare what's included</b>, not just the fee.",
        "<b>Offer EMI only</b> after they're sold on the course.",
        "<b>Never criticise</b> another institute."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    if "--export" in sys.argv:
        print("exported", c.export(), "slides")
    else:
        print("built", c.build())
