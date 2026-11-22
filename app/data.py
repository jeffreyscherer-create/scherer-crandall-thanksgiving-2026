"""Static event content: schedule, teams, Olympic events, scavenger hunt stops."""

TEAM_1 = ["Jess", "Sky", "Dash", "Kevin", "Lucy", "Sam", "Wayne", "Howard", "Carol"]
TEAM_2 = ["Bob", "Jeff", "Ellie", "Cassie", "Maisie", "Mona", "Rick", "Max", "Chayenne"]

SCHEDULE = [
    {
        "day": "Tuesday, Nov 24",
        "items": [
            {"time": "6:00pm", "title": "Dinner at home", "detail": "Family confirmed a fried clam happy hour would proceed as scheduled, adding that team assignments were final and any lobbying for a trade would be, in their words, \"noted and ignored.\""},
        ],
    },
    {
        "day": "Wednesday, Nov 25",
        "items": [
            {"time": "Morning", "title": "Happy Birthday to someone!", "detail": "Family confirmed one member is celebrating a birthday Wednesday, declining to specify who, citing a longstanding policy of making relatives figure it out themselves."},
            {"time": "Breakfast", "title": "Breakfast at our house", "detail": "Waffles, pancakes, yogurt bowls, granola, and mixed berries will reportedly be served to nine adults who, within hours, will be asked to pop balloons using only their faces."},
            {"time": "10:00am – 12:00pm", "title": "THE OLYMPICS", "detail": "At Jess's house. Attendees are advised to arrive with knee pads and, per one organizer, \"zero remaining dignity to lose.\"", "highlight": True},
            {"time": "12:00 / 12:30pm", "title": "Lunch", "detail": "A mandatory icing-of-injuries period will be observed at Jess's house."},
            {"time": "3:00pm – 5:30pm", "title": "SCAVENGER HUNT", "detail": "Downtown Boston and the North End will reportedly be introduced to this family for the first time, with limited advance warning.", "highlight": True},
            {"time": "5:30pm", "title": "Closing ceremonies + dinner", "detail": "Restaurant selected unilaterally by Wayne, who has asked that all complaints be directed to him in person: Piccolo Nido, 257 North St, Boston."},
        ],
    },
    {
        "day": "Thursday, Nov 26 — Thanksgiving",
        "items": [
            {"time": "All day", "title": "At Jess's house", "detail": ""},
            {"time": "Breakfast", "title": "Frittata and bagels", "detail": ""},
            {"time": "Daytime", "title": "Cooking together, white elephant gift exchange, football & family games", "detail": "Wayne and Dash confirmed they would once again fry the turkey themselves, with a fire extinguisher reportedly staged nearby \"just as a formality.\""},
            {"time": "4:00pm", "title": "Thanksgiving dinner", "detail": "Will proceed as planned, contingent on the structural integrity of both the turkey and the house."},
        ],
    },
]

OLYMPIC_EVENTS = [
    {
        "id": "pop-fast",
        "name": "Pop Fast",
        "tagline": "Local Family Confirms Balloon-Popping Can, In Fact, Be Done With Only Elbows",
        "rules": "3 people per team pop 20 balloons each — no hands or feet allowed. Fastest team to finish wins.",
        "team_size": "3 per team",
        "wins_by": "Fastest time",
    },
    {
        "id": "face-the-cookie",
        "name": "Face the Cookie",
        "tagline": "Area Adult Successfully Relocates Cookie Six Inches Using Only Facial Muscles",
        "rules": "5 people per team race a cookie from forehead down to the mouth, no hands. First team to get all 5 wins.",
        "team_size": "5 per team",
        "wins_by": "First team done",
    },
    {
        "id": "defying-gravity",
        "name": "Defying Gravity",
        "tagline": "Nine Adults To Spend Two Full Minutes Keeping Balloons Airborne For Unclear Reasons",
        "rules": "3 people per team keep balloons in the air as long as possible. Ends when one team's balloons all hit the ground, or at 2 minutes — whoever has more balloons still airborne wins.",
        "team_size": "3 per team",
        "wins_by": "Balloons down last, or most airborne at 2:00",
    },
    {
        "id": "iron-man",
        "name": "Iron Man",
        "tagline": "Grown Man Reportedly Reduced To Tears By Single Nut And One Chopstick",
        "rules": "3 people per team stack nuts using only chopsticks — no hands allowed. Fastest/most wins.",
        "team_size": "3 per team",
        "wins_by": "Fastest time",
    },
    {
        "id": "flip-cup-ttt",
        "name": "Flip Cup Tic-Tac-Toe",
        "tagline": "Bracket-Style Drinking Tournament Introduced To Settle Dispute No One Can Recall Starting",
        "rules": "4 people per team. Three 1-on-1 flip cup matches; the winners of each then face off until there's one champion.",
        "team_size": "4 per team",
        "wins_by": "Bracket winner",
    },
    {
        "id": "puzzle-race",
        "name": "Puzzle Race",
        "tagline": "Entire Team Confirms 500-Piece Puzzle Is, In Fact, Worth Fighting Over",
        "rules": "Entire team races to finish a puzzle first.",
        "team_size": "Whole team",
        "wins_by": "First team finished",
    },
]

# --- Scavenger hunt -------------------------------------------------------

SCAVENGER_RULES = [
    "2.5 hours, hard stop. Both teams meet at Piccolo Nido. Late = minus 10 points per 5 minutes.",
    "Every photo or video needs at least 5 teammates in it unless the task says otherwise.",
    "Follow your own route in order. Pace yourselves and skip tasks when needed.",
    "Wildcards can be done anywhere, at any time, including while walking.",
    "Showdowns earn their base points when completed, plus +5 to the winning team, decided at dinner. The kids are the judges.",
    "Find-its require both an answer and a photo of the thing that gives the answer (sign, plaque, statue, carving). No photo, no points.",
    "Quiet zone: Copp's Hill Burying Ground is look-and-find only, so no silly stuff there.",
    "Always ask strangers first, accept “no” gracefully, and tip performers and guides who play along.",
]

# task: id, title, type (photo/video/find), flag (showdown/21+/italiano/None), points, description
def _t(id, title, type, points, description, flag=None):
    return {"id": id, "title": title, "type": type, "points": points, "description": description, "flag": flag}

STOPS = {
    "harbor": {
        "name": "Harbor",
        "location": "New England Aquarium · Central Wharf · Columbus Park",
        "tasks": [
            _t("seal-squad", "Seal Squad", "photo", 3, "The whole team does its best harbor-seal impression in front of the free outdoor seal tank."),
            _t("whose-roses", "Whose Roses?", "find", 3, "Christopher Columbus Park has a rose garden named after a famous North End–born mom. Who is it?"),
        ],
    },
    "old-state-house": {
        "name": "Old State House",
        "location": "State St & Washington St",
        "tasks": [
            _t("massacre-slowmo", "Massacre in Slow-Mo", "video", 5, "Find the cobblestone ring marking the Boston Massacre site and do a 15-second slow-motion reenactment beside it, not in traffic. Most realistic wins.", "showdown"),
            _t("lion-unicorn", "Lion & Unicorn", "photo", 3, "Two teammates copy the poses of the lion and unicorn on the roof's east side."),
            _t("bird-on-back", "Bird on the Back", "find", 2, "On the west side of the Old State House, what gilded bird sits on top?"),
        ],
    },
    "old-city-hall": {
        "name": "Old City Hall",
        "location": "45 School St",
        "tasks": [
            _t("be-ben", "Be Ben", "photo", 3, "Everyone copies Ben Franklin's pose at his statue."),
            _t("stand-in-what", "Stand in What?", "find", 3, "In front of the bronze donkey are bronze footprints. What three words are written there, and what animal is drawn on them?"),
            _t("schools-in", "School's In", "find", 3, "Find the colorful sidewalk mosaic near Ben. It marks the site of America's first public school. What is the school called?"),
        ],
    },
    "faneuil-hall": {
        "name": "Faneuil Hall & the Blackstone Block",
        "location": "Quincy Market · Union St · Marshall St",
        "tasks": [
            _t("bench-with-red", "Bench with Red", "photo", 3, "Squeeze as many teammates as possible onto the bench with the Red Auerbach statue, on the south side of Quincy Market."),
            _t("busker-shoutout", "Busker Shoutout", "video", 6, "Get a street performer to give your team a shoutout by name. Coolest shoutout wins.", "showdown"),
            _t("oldest-restaurant", "America's Oldest Restaurant", "find", 2, "What year did the Union Oyster House on Union St open?"),
            _t("boston-stone", "The Boston Stone", "find", 3, "Find the round stone set into a building wall on Marshall St. What year is carved under it?"),
            _t("last-call-news", "Last Call for the News", "find", 2, "Find the historic marker by the door of the Bell in Hand Tavern (45 Union St). What was the founder's job before he opened the tavern?"),
            _t("guinness-chugoff", "Guinness Chug-Off", "video", 8, "Inside the Bell in Hand, film two teammates chugging a Guinness at the same time. The time counts when the second person finishes. Fastest time wins.", "showdown"),
        ],
    },
    "hanover-north-sq": {
        "name": "Hanover St & North Square",
        "location": "Hanover St · North Sq · Paul Revere House",
        "tasks": [
            _t("midnight-ride", "The Midnight Ride", "video", 6, "One teammate “rides” past the Paul Revere House while the rest gallop behind yelling “The Regulars are coming out!” (what he actually said)."),
            _t("how-old", "How Old?", "find", 2, "The Paul Revere House is the oldest building in downtown Boston. About what year was it built?"),
            _t("ordina-italiano", "Ordina in Italiano", "video", 5, "Order something at a bakery or café entirely in Italian. +2 bonus if the staff answer back in Italian.", "italiano"),
            _t("pastry-hunt", "Pastry Hunt", "photo", 4, "Find the coolest, most unusual Italian pastry you can. Take a team photo with it and say what it's called. Coolest pastry wins.", "showdown"),
            _t("nonna-lesson", "Nonna Lesson", "video", 6, "Get a local to teach the team an Italian phrase on camera. Everyone repeats it.", "italiano"),
        ],
    },
    "old-north-copps": {
        "name": "Old North & Copp's Hill",
        "location": "Paul Revere Mall · Salem St · Hull St",
        "tasks": [
            _t("church-birthday", "Church Birthday", "find", 2, "Old North Church is Boston's oldest standing church. What year was it built?"),
            _t("who-made-horse", "Who Made the Horse?", "find", 3, "Who sculpted the bronze Paul Revere on horseback on the Prado? Give the last name (it's on the statue)."),
            _t("target-practice", "Target Practice", "find", 5, "In Copp's Hill Burying Ground, find the gravestone British soldiers are said to have shot musket balls at. Whose stone is it? Quiet zone: one person takes the photo."),
            _t("squeeze-play", "Squeeze Play", "photo", 4, "Everyone squeezes in front of the Skinny House at 44 Hull St, Boston's narrowest house. +2 if the team's guess of its width is within 1 foot."),
        ],
    },
}

BATTLE_CRY_TASK = _t("battle-cry", "Battle Cry", "video", 5, "Before leaving your starting spot, perform a 10-second team battle cry for a stranger. On video, the stranger rates it 1 to 10. Higher rating wins.", "showdown")

WILDCARDS = [
    _t("revolutionary-selfie", "Revolutionary Selfie", "photo", 8, "A photo with someone in Revolutionary-era costume (a colonial guide, a redcoat, a town crier). The best bet is around Faneuil Hall. +3 bonus if they say “Huzzah!” on video."),
    _t("high-five-gauntlet", "High-Five Gauntlet", "video", 5, "High-five 10 different strangers in under 1 minute."),
    _t("sing-for-it", "Sing for It", "video", 6, "Get a stranger to sing “Sweet Caroline” with the team (just the “BUM BUM BUM” counts)."),
    _t("human-letters", "Human Letters", "photo", 4, "Spell B-O-S with your bodies (each person can be part of a letter)."),
]

# Each team runs the same 6 stops in a mirrored order.
TEAM_ROUTES = {
    "team1": {
        "start": "Central Wharf, in front of the New England Aquarium",
        "stops": ["harbor", "old-state-house", "old-city-hall", "faneuil-hall", "hanover-north-sq", "old-north-copps"],
        "hints": [
            "Walk up State St",
            "Walk to School St",
            "Walk to Faneuil Hall",
            "Walk up Hanover St",
            "Walk to the Prado",
            "Walk to Piccolo Nido",
        ],
    },
    "team2": {
        "start": "The Paul Revere statue on the Prado (Paul Revere Mall)",
        "stops": ["old-north-copps", "hanover-north-sq", "harbor", "old-state-house", "old-city-hall", "faneuil-hall"],
        "hints": [
            "Walk to North Square",
            "Walk to Columbus Park",
            "Walk up State St",
            "Walk to School St",
            "Walk to Faneuil Hall",
            "Walk up North St to Piccolo Nido",
        ],
    },
}

SHOWDOWNS = [
    {"id": "battle-cry", "title": "Battle Cry"},
    {"id": "massacre-slowmo", "title": "Massacre in Slow-Mo"},
    {"id": "busker-shoutout", "title": "Busker Shoutout"},
    {"id": "guinness-chugoff", "title": "Guinness Chug-Off"},
    {"id": "pastry-hunt", "title": "Pastry Hunt"},
]

ANSWER_KEY = {
    "whose-roses": "Rose Fitzgerald Kennedy (JFK's mother)",
    "bird-on-back": "An eagle",
    "stand-in-what": "“Stand in Opposition,” with elephants on the footprints",
    "schools-in": "Boston Latin School",
    "oldest-restaurant": "1826",
    "boston-stone": "1737",
    "last-call-news": "Town crier (Jimmy Wilson, Boston's last town crier)",
    "how-old": "About 1680",
    "church-birthday": "1723",
    "who-made-horse": "Cyrus Dallin",
    "target-practice": "Captain Daniel Malcolm",
    "squeeze-play": "About 10 feet (10.4 ft at its widest)",
}
