import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Objection handling",
       "\"I'll think about it\" usually means <em>\"I'm not sure yet.\"</em>",
       "Here's how to find out what they're unsure about, before you hang up.",
       photo=ph("hook"), brief="Person thinking, looking away")

c.numbered("What \"I'll think about it\" <em>really means</em>",
           [("Not sure it works", "They need proof, not time."),
            ("Need to ask family", "Someone else decides or pays."),
            ("The fee felt high", "They didn't want to say it out loud."),
            ("Not interested", "Better to know now than chase for weeks.")],
           photo=ph("band"), brief="Family talking at home")

c.compare("Same objection",
          "Two replies. <em>Two outcomes.</em>",
          "Wrong way", ["\"Sure, take your time. Call me back.\"", "\"Shall I send the brochure?\""],
          "Right way", ["\"Of course. Which part would you like to think over?\"", "\"Shall we talk tomorrow, after you've discussed it at home?\""])

c.script("Find the real reason",
         "Ask what's <em>left to decide</em>",
         [("Parent", "\"Let me think about it and get back to you.\""),
          ("You", "\"Of course. Is it more about the course, the timing or the fee?\""),
          ("Parent", "\"Honestly, the fee. And I need to ask my husband.\"")],
         "A gentle either-or question turns a vague no into a real objection you can handle.")

c.script("The family objection",
         "When it's <em>\"I'll discuss with family\"</em>",
         [("Parent", "\"I'll discuss it with my family and let you know.\""),
          ("You", "\"That makes sense. What do you think they'll ask?\""),
          ("Parent", "\"About results, and whether it fits her school timings.\"")],
         "Help them prepare for that conversation. Better still, offer a short call with the whole family.",
         ground="")

c.steps("The framework",
        "The <em>think-about-it</em> follow-up",
        [("Same call", "Ask what's left to decide. Name it together."),
         ("Book a time", "\"Can we speak tomorrow at 7, after you've talked?\""),
         ("Send answers", "WhatsApp answers to the questions the family will ask."),
         ("Call on time", "Exactly when you said. Start with their question.")])

c.bottom("Pro tip",
         "Never end a call <em>without a next time.</em>",
         "\"I'll call you back\" goes nowhere. A fixed day and time keeps the decision alive.",
         "<strong>Ask:</strong> \"Is tomorrow at 7 or Saturday morning better?\"",
         photo=ph("bottom"), brief="Calendar or planner")

c.save("Your think-about-it checklist",
       "Save this for every <em>\"let me think\".</em>",
       ["<b>Never just say</b> \"take your time\".",
        "<b>Ask:</b> the course, the timing or the fee?",
        "<b>Ask what the family</b> will want to know.",
        "<b>Offer a call</b> with the whole family.",
        "<b>Book a day and time</b> before you hang up.",
        "<b>Send answers</b> on WhatsApp the same day."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
