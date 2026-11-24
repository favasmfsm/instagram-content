import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Marketing planning",
       "Admissions follow exam season. <em>Your marketing should too.</em>",
       "A simple year plan for edtech marketing and sales teams.",
       photo=ph("hook"), brief="Planner and calendar on a desk")

c.side("The problem",
       "\"Admissions open\" <em>all year long.</em>",
       "The same post every month means it's right for nobody. Families think about different things in February and in June.",
       "Match the message to what's on their mind that month.",
       tags=("Timing", "Relevance"),
       photo=ph("side"), brief="Team planning on a whiteboard")

c.numbered("The <em>4 seasons</em> of edtech admissions",
           [("Board exam season", "Roughly Feb–Mar: revision help, stress tips, no hard selling."),
            ("Results season", "Roughly May–Jun: next-year plans, repeaters, new batches."),
            ("New academic year", "Roughly Jun–Jul: foundation batches, school-plus-coaching."),
            ("Mid-year reset", "Roughly Oct–Nov: crash courses, test series, last-mile prep.")],
           photo=ph("band"), brief="Wall calendar")

c.steps("The framework",
        "Plan each season <em>6 weeks ahead</em>",
        [("Week −6", "Pick the season's one message and offer."),
         ("Week −4", "Build the lead magnet: a mock, a planner, a guide."),
         ("Week −2", "Warm up: useful posts and a free webinar date."),
         ("Week 0", "Launch: ads, calls and WhatsApp follow-ups.")])

c.bottom("Biggest day of the year",
         "Be ready <em>on results day.</em>",
         "Students who missed their target are deciding what to do next, that same week. Have the repeater batch, the offer and the call team ready before results come out.",
         "<strong>Prep:</strong> a results-day post, a free counselling slot and extra counsellors.",
         photo=ph("bottom"), brief="Student checking results")

c.save("Your admissions-calendar checklist",
       "Save this for your <em>yearly plan.</em>",
       ["<b>Map your year</b> to exam and results dates.",
        "<b>One message</b> and one offer per season.",
        "<b>Plan 6 weeks</b> before each season.",
        "<b>No hard selling</b> during board exams.",
        "<b>Have repeater batches</b> ready before results.",
        "<b>Staff up</b> for results week."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
