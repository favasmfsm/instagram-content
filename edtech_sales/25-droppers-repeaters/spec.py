import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Droppers and repeaters",
       "A dropper has already failed once. <em>Don't pitch like they haven't.</em>",
       "How to talk to students taking a second attempt, and to their parents.",
       photo=ph("hook"), brief="Serious student studying alone")

c.side("How they feel",
       "They're <em>scared of a second miss.</em>",
       "A dropper has heard every promise before. Their parents have already paid once.",
       "Generic pitches sound like last year. Specific plans sound like hope.",
       tags=("Trust", "Second attempt"),
       photo=ph("side"), brief="Student looking out of a window")

c.compare("The opening",
          "Generic vs <em>specific</em>",
          "Generic", ["\"Our results are the best in the city.\"", "\"Just join. You'll crack it this time.\""],
          "Specific", ["\"What happened in the last attempt? Which subject cost you the most marks?\"", "\"Let's look at your last scorecard together.\""])

c.script("The conversation",
         "Find <em>the real gap</em>",
         [("You", "\"Walk me through last year. Where do you think the marks went?\""),
          ("Student", "\"Physics. I knew the concepts, but I ran out of time.\""),
          ("You", "\"So it's speed and practice, not concepts. Then you need timed tests every week, with someone reviewing each one.\"")],
         "Pitch only to the gap they named. It shows you listened.")

c.numbered("What a dropper plan <em>needs to show</em>",
           [("A diagnosis", "Last year's score, broken down by subject."),
            ("A different method", "Not the same classes again."),
            ("Regular checkpoints", "Monthly tests with a progress call."),
            ("Proof from similar students", "A past dropper's story, shared with consent.")],
           photo=ph("band"), brief="Teacher reviewing a test with a student")

c.bottom("Pro tip",
         "Talk to the parent <em>about the money.</em>",
         "They paid once and it didn't work. Say it plainly, then show what will be different this time.",
         "<strong>Never say:</strong> \"This time it's guaranteed.\"",
         photo=ph("bottom"), brief="Parent and child talking")

c.save("Your dropper-call checklist",
       "Save this for <em>results season.</em>",
       ["<b>Ask what went wrong</b> in the last attempt.",
        "<b>Look at the scorecard</b> together.",
        "<b>Name the real gap:</b> concepts, speed or stress.",
        "<b>Show a different method,</b> not the same classes.",
        "<b>Share a past dropper's story</b> with consent.",
        "<b>Never promise</b> a selection."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
