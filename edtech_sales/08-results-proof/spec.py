import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Marketing",
       "Stop writing better ads. <em>Start showing better proof.</em>",
       "Your last batch's results sell harder than any offer. Here's how to collect them and use them.",
       photo=ph("hook"), brief="Graduation celebration")

c.numbered("The <em>proof ladder</em>, weakest to strongest",
           [("Claims", "\"Best faculty in town.\" Nobody believes it."),
            ("Numbers", "Selections and score jumps, with names and consent."),
            ("Video stories", "A student explaining what changed for them."),
            ("Parent voice notes", "One parent telling another. The strongest of all.")],
           photo=ph("band"), brief="Students celebrating results")

c.steps("The framework",
        "Collect proof <em>while it's fresh</em>",
        [("Day 30", "Ask for a short voice note on what's improved."),
         ("Mock results", "Screenshot score jumps, with consent."),
         ("Results day", "Call every selected student. Record 60 seconds."),
         ("Every parent", "Ask: \"Can we share your words with other parents?\"")])

c.side("Where to use it",
       "Use it <em>where decisions happen.</em>",
       "Proof sitting on your website does little. Send it in the WhatsApp chat right after the demo.",
       "Match it: a NEET parent gets a NEET parent's voice note.",
       tags=("WhatsApp", "Calls", "Ads"),
       photo=ph("side"), brief="Phone in hand")

c.script("On the call",
         "Let <em>another parent</em> say it",
         [("Parent", "\"How do I know this will work for my son?\""),
          ("You", "\"Fair question. Can I send you a 40-second voice note from a parent whose son was in the same spot last year?\""),
          ("Parent", "\"Yes, please send it.\"")],
         "Don't argue that it works. Let someone they relate to say it.")

c.bottom("Always",
         "Ask before you <em>share anyone's results.</em>",
         "Written consent from the student and the parent, every time. Blur phone numbers and personal details.",
         "<strong>Keep it simple:</strong> a one-line WhatsApp consent message, saved.",
         photo=ph("bottom"), brief="Phone screen with a chat")

c.save("Your proof checklist",
       "Save this for <em>results season.</em>",
       ["<b>Ask for a voice note</b> at day 30.",
        "<b>Screenshot score jumps</b>, with consent.",
        "<b>Record 60 seconds</b> on results day.",
        "<b>Match the story</b> to the parent's exam.",
        "<b>Send proof</b> right after the demo.",
        "<b>Never share</b> without written consent."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
