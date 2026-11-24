import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_system"))
from esm import Carousel
P = json.load(open(os.path.join(HERE, "photos.json"))) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
ph = lambda k: P.get(k, {}).get("file")

c = Carousel(HERE)

c.hook("Instagram",
       "Someone commented \"fees?\" <em>Don't just reply \"DM sent.\"</em>",
       "How to turn comments and DMs into calls, not dead chats.",
       photo=ph("hook"), brief="Phone with social media")

c.compare("The reply",
          "Dead end vs <em>conversation</em>",
          "Dead end", ["\"DM sent.\"", "A fee-list PDF with no message."],
          "Conversation", ["\"Happy to help! Which exam and year are you preparing for? Sending details in DM.\"", "A question they can answer in one line."])

c.numbered("4 mistakes <em>in the DMs</em>",
           [("Replying hours later", "They've already messaged three other pages."),
            ("Fee dump first", "A number with no context gets compared."),
            ("No question", "A message with nothing to answer ends the chat."),
            ("Chatting forever", "Ten messages, no call, no decision.")],
           photo=ph("band"), brief="Person texting")

c.script("In the DM",
         "Ask, then <em>move it to a call</em>",
         [("Lead", "\"What's the fee for NEET?\""),
          ("You", "\"Hi Sneha! It depends on the batch. Are you in class 11 or 12?\""),
          ("Lead", "\"Class 11.\"")],
         "Then offer a 5-minute call to explain the options. Chats inform. Calls decide.")

c.steps("The framework",
        "Comment to call <em>in 4 steps</em>",
        [("Reply publicly", "A warm reply with one question, within the hour."),
         ("DM in 10 minutes", "Personal, with their name and the course."),
         ("Qualify", "Exam, year, and who decides."),
         ("Book a call", "A fixed time, today or tomorrow.")])

c.bottom("Pro tip",
         "Save <em>quick-reply templates.</em>",
         "Instagram lets you save replies. Write one for fees, one for batches and one for demos, each ending in a question.",
         "<strong>Rule:</strong> edit the name and course every time, so it doesn't read like a template.",
         photo=ph("bottom"), brief="Phone in hand")

c.save("Your Instagram-lead checklist",
       "Save this for your <em>social media desk.</em>",
       ["<b>Reply publicly</b> with a question.",
        "<b>DM within 10 minutes.</b>",
        "<b>Ask exam and year</b> before the fee.",
        "<b>Always end</b> with a question.",
        "<b>Move it to a call</b> at a fixed time.",
        "<b>Save quick-reply templates</b> and personalise them."])

c.follow()

if __name__ == "__main__":
    print("rule problems:", c.check_rules() or "none")
    print("exported", c.export(), "slides") if "--export" in sys.argv else print("built", c.build())
