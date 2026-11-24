import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Webinars",
       "Your free masterclass is teaching. <em>It should also be selling.</em>",
       "How to run a free webinar that fills a batch, not just a chat window.",
       photo=ph("hook"), brief="Presenter speaking to an audience")

c.side("The problem",
       "Great session. <em>Zero admissions.</em>",
       "Most free webinars end with \"Thanks for joining!\" and a link nobody clicks.",
       "The attendees liked you. Nobody told them what to do next.",
       tags=("Attention", "Next step"),
       photo=ph("side"), brief="Person watching a session on a laptop")

c.numbered("4 webinar <em>mistakes</em>",
           [("Teaching everything", "If they learn it all for free, why join?"),
            ("No interaction", "Passive viewers don't become students."),
            ("The pitch as an afterthought", "Rushed in the last 2 minutes, after half have left."),
            ("No same-night follow-up", "By tomorrow, the excitement is gone.")],
           photo=ph("band"), brief="Audience in a seminar")

c.steps("The framework",
        "The <em>webinar that sells</em> in 4 parts",
        [("Teach one thing", "One strategy they can use tomorrow. Not the whole syllabus."),
         ("Live mini-test", "5 questions in the chat. Everyone sees where they stand."),
         ("Show the gap", "\"Here's what the top scorers did differently.\""),
         ("Make the offer", "One clear next step, with a real deadline.")])

c.script("The offer moment",
         "Make the offer <em>sound like help</em>",
         [("You", "\"If you got 3 or fewer right today, you're not alone. That's exactly the gap our crash batch closes in 8 weeks.\""),
          ("You", "\"Type YES in the chat and a counsellor will call you tonight with the plan.\""),
          ("Attendee", "\"YES\"")],
         "Tie the offer to the result they just saw. Ask for one small action, not a payment.")

c.bottom("Pro tip",
         "Call the <em>YES list</em> the same night.",
         "Split the chat replies between counsellors before the webinar ends. Every YES gets a call within 2 hours.",
         "<strong>Open with:</strong> \"You were on tonight's session. How did the mini-test go?\"",
         photo=ph("bottom"), brief="Counsellor on a phone call")

c.save("Your webinar checklist",
       "Save this before your <em>next free webinar.</em>",
       ["<b>Teach one strategy</b>, not the syllabus.",
        "<b>Run a live mini-test</b> in the chat.",
        "<b>Show the gap</b> between them and top scorers.",
        "<b>Make one clear offer</b> with a real deadline.",
        "<b>Ask for a YES</b> in the chat, not a payment.",
        "<b>Call every YES</b> the same night."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
