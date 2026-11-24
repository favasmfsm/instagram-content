import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("WhatsApp follow-up",
       "Your WhatsApp messages are being <em>muted.</em>",
       "5 mistakes that make parents ignore you, and what to send instead.",
       photo=ph("hook"), brief="Person reading WhatsApp on a phone")

c.numbered("5 messages parents <em>ignore</em>",
           [("The brochure dump", "Three PDFs and a fee chart, no context."),
            ("\"Dear Sir/Madam\"", "Copy-paste openers read as spam."),
            ("The 11 pm message", "Late messages feel pushy, not keen."),
            ("Five in a row", "Unanswered messages pile up into pressure."),
            ("No question at the end", "Nothing to reply to, so nobody replies.")],
           photo=ph("band"), brief="Phone with chat notifications")

c.compare("Mistake 1",
          "The <em>brochure dump</em>",
          "Wrong way", ["[Brochure.pdf] [Fees.pdf] [Timetable.pdf]", "\"Please check and revert.\""],
          "Right way", ["\"Hi Mrs. Nair, here's a 1-page plan for Arjun's NEET prep. Page 2 has the weekly test schedule you asked about.\""])

c.compare("Mistake 2",
          "The <em>copy-paste opener</em>",
          "Wrong way", ["\"Dear Sir/Madam, greetings from XYZ Academy!\""],
          "Right way", ["\"Hi Mrs. Nair, Arjun solved 4 of 5 in today's demo. Can I call at 6 to share where he lost marks?\""])

c.side("Mistakes 3 and 4",
       "Time it <em>like a person would.</em>",
       "Send between 10 am and 8 pm. A message at 11 pm reads as pressure, even when you mean well.",
       "No reply? Wait at least a day before the next message. Never send five in a row.",
       tags=("Timing", "Patience"),
       photo=ph("side"), brief="Phone on a table in the evening")

c.script("Mistake 5",
         "End with <em>an easy question</em>",
         [("You", "\"Hi Mrs. Nair, I've attached Arjun's demo test review.\""),
          ("You", "\"Would a quick call at 6 today or 11 tomorrow work better?\""),
          ("Parent", "\"6 today is fine.\"")],
         "Two time options are easy to answer. \"Let me know\" is easy to ignore.")

c.steps("The framework",
        "The <em>4-part</em> WhatsApp message",
        [("Names", "The parent's name and the student's name."),
         ("Context", "Why you're writing: the demo, their question."),
         ("Value", "One useful thing: a review, a plan, a clip."),
         ("Question", "An easy question with two options.")])

c.save("WhatsApp do's and don'ts",
       "Save these WhatsApp <em>rules.</em>",
       ["<b>Use names:</b> the parent's and the student's.",
        "<b>One attachment</b>, with a line about it.",
        "<b>Send between</b> 10 am and 8 pm.",
        "<b>Wait a day</b> before following up.",
        "<b>End with</b> an easy two-option question.",
        "<b>Never send</b> five messages in a row."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
