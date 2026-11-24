import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Objection handling",
       "\"My child can't focus in online classes.\" <em>Here's how to answer.</em>",
       "The most common doubt parents have about online coaching, and how to turn it around.",
       photo=ph("hook"), brief="Child at a laptop")

c.numbered("What's <em>really behind it</em>",
           [("A bad past experience", "Lockdown classes left a mark."),
            ("Screen-time worry", "They fear more phone, not more learning."),
            ("Nobody checks", "No one notices if the child switches off."),
            ("Falling behind", "They fear online means less serious.")],
           photo=ph("band"), brief="Child doing homework at home")

c.compare("First reply",
          "Don't defend. <em>Ask.</em>",
          "Wrong way", ["\"Our classes are very interactive!\"", "\"Many students do really well online.\""],
          "Right way", ["\"That's a fair worry. What happened in the online classes before?\"", "Find the real reason first."])

c.script("The conversation",
         "Answer <em>the real worry</em>",
         [("Parent", "\"In lockdown he just kept the camera off and played games.\""),
          ("You", "\"That happens a lot when no one is watching. In our batches, attendance and camera-on are tracked, and you get a message if he misses a class.\""),
          ("Parent", "\"I'd get a message? That helps.\"")],
         "Most parents aren't against online learning. They're against not knowing what's happening.")

c.steps("The framework",
        "Prove it in <em>a trial week</em>",
        [("Live class", "Small batch, camera on, the teacher calls on him by name."),
         ("Doubt session", "One-on-one, so he sees help is real."),
         ("Parent check-in", "A call on day 4: what did he say about it?"),
         ("Progress report", "A short test and a written report on day 7.")])

c.bottom("Pro tip",
         "Show the parent <em>what they'll see.</em>",
         "Share a sample attendance alert and weekly report on WhatsApp before the trial starts.",
         "<strong>Why:</strong> visibility is what they're really buying.",
         photo=ph("bottom"), brief="Parent reading a phone message")

c.save("Your online-doubt checklist",
       "Save this for your <em>next doubtful parent.</em>",
       ["<b>Don't defend</b>; ask what happened before.",
        "<b>Name the real worry:</b> focus, screens or tracking.",
        "<b>Show attendance alerts</b> and weekly reports.",
        "<b>Offer a trial week</b> with a parent check-in.",
        "<b>Call on day 4</b> to ask how it's going.",
        "<b>Send a written report</b> at the end of the trial."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
