import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Referrals",
       "Your happiest parents are <em>your cheapest counsellors.</em>",
       "How to ask for referrals at the right moment, without sounding desperate.",
       photo=ph("hook"), brief="Happy mother")

c.side("Why referrals close faster",
       "A friend's word <em>beats any ad.</em>",
       "A referred parent arrives already trusting you. Half the selling is done before your first call.",
       "Yet most teams never ask, or ask once at admission and forget.",
       tags=("Trust", "Lower cost"),
       photo=ph("side"), brief="Two friends chatting")

c.steps("The framework",
        "Ask at the <em>4 win moments</em>",
        [("First good test", "The parent just saw progress. Ask then."),
         ("Parent meeting", "After you share a positive report."),
         ("Results day", "The happiest day of the year. Ask everyone."),
         ("Renewal", "They've chosen you twice. They'll recommend you.")])

c.compare("How to ask",
          "Same ask. <em>Different words.</em>",
          "Wrong way", ["\"Please refer your friends to us.\"", "Sent as a mass WhatsApp to every parent."],
          "Right way", ["\"Arjun's mock score went up again. Do you know another parent whose child is preparing for NEET this year?\"", "Asked personally, right after good news."])

c.script("The referral call",
         "Make it <em>easy to say yes</em>",
         [("Parent", "\"Yes, my neighbour's daughter is in Class 11.\""),
          ("You", "\"Would it be okay if I send you a short message you can forward to her? No pressure on her at all.\""),
          ("Parent", "\"Sure, send it.\"")],
         "Give them something to forward. Never ask for a phone number on the spot.")

c.bottom("What to give",
         "Thank them <em>for real.</em>",
         "A fee discount for both families, a free crash course or a personal thank-you call. Whatever you give, give it to both sides.",
         "<strong>Track it:</strong> one column in your CRM: \"Referred by\".",
         photo=ph("bottom"), brief="Small gift")

c.save("Your referral checklist",
       "Save this for your <em>referral plan.</em>",
       ["<b>Ask right after</b> a win moment.",
        "<b>Ask personally</b>, never as a mass message.",
        "<b>Name the kind of family</b> you're looking for.",
        "<b>Give a forwardable message</b>, not a form.",
        "<b>Reward both families</b>, not just one.",
        "<b>Track \"Referred by\"</b> in your CRM."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
