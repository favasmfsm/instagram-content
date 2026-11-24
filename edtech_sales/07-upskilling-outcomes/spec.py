import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Selling to professionals",
       "Working professionals don't want a certificate. <em>They want a raise.</em>",
       "3 pitch mistakes that lose upskilling leads, and what to say instead.",
       photo=ph("hook"), brief="Working professional at a desk")

c.side("What they're buying",
       "They're buying <em>an outcome.</em>",
       "A course means months of evenings and weekends. Nobody gives that up for a syllabus.",
       "They give it up for a new job, a promotion or a career switch.",
       tags=("New job", "Promotion", "Switch"),
       photo=ph("side"), brief="Person on a laptop in the evening")

c.compare("Mistake 1",
          "Pitching <em>the syllabus</em>",
          "Wrong way", ["\"12 modules, 80 hours: Python, SQL and Power BI.\""],
          "Right way", ["\"In 6 months you can apply for data analyst roles. Here's what that job looks like day to day.\""])

c.compare("Mistake 2",
          "Ignoring <em>their time</em>",
          "Wrong way", ["\"Classes run Monday to Friday, 7 to 9 pm.\""],
          "Right way", ["\"Plan for 45 minutes a day. Here's a week that fits around your shift.\""])

c.script("Mistake 3",
         "Telling <em>the wrong success story</em>",
         [("Prospect", "\"I'm 32 and in sales. Can someone like me really switch to data?\""),
          ("You", "\"Let me tell you about a learner from our last batch. Insurance sales at 34, analyst role a year later.\""),
          ("Prospect", "\"Okay, that's actually like me.\"")],
         "Match the story to their age, background and job. Use real learners from your own batches.")

c.steps("The framework",
        "The <em>outcome pitch</em> in 4 steps",
        [("Where now", "Current role, salary band, what frustrates them."),
         ("Where next", "The exact role they want in 12 months."),
         ("The bridge", "What they'll learn, mapped to that role."),
         ("The proof", "One learner who made the same move.")])

c.save("Your career-call checklist",
       "Save this before your <em>next career call.</em>",
       ["<b>Ask about</b> their current role first.",
        "<b>Name the job</b> they want, not the course.",
        "<b>Show a week</b> that fits their schedule.",
        "<b>Tell a success story</b> like theirs.",
        "<b>Talk outcomes</b> before modules.",
        "<b>Never promise</b> a salary you can't show."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
