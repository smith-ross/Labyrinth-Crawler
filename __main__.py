import random

class Item:
    def __init__(self, name, description):
        self.Name = name
        self.Description = description
        self.PickedUp = False
    
    def pickUp(self, inventory):
        self.PickedUp = True
        inventory.append(self)
        Rooms[Player["room"]].Items.remove(self)
        
    def drop(self, inventory):
        self.PickedUp = False,
        inventory.remove(self)
        Rooms[Player["room"]].Items.append(self)


class Room:
    def __init__(self, ID):
        self.ID = ID
        self.Temperature = random.choice(["cold", "average", "warm"])
        self.Darkness = random.choice(["dark", "average", "bright"])
        self.Material = random.choice(["stone", "wood", "brick"])
        self.Description = "You find yourself in a {dark} room. It's {temp}. The walls are made of {mat}.".format(dark=DESCRIPTIONS["DARKNESS"][self.Darkness], temp=DESCRIPTIONS["TEMPERATURE"][self.Temperature], mat=self.Material)
        self.Items = []
        self.Exits = {}
        

ENCOUNTERS = [
    ["You hear a noise... but from what?", 7],
    ["You thought you saw a man in the corner, but on second glance, there's no one there...", 15],
    ["There's fresh blood on the walls.", 30],
    ["The light is flickering... must be faulty.", 10],
    ["A dark figure can be seen in another room...", 25],
    ["You see a flash of white dash across the room.", 18]
    
]

DESCRIPTIONS = {
    "TEMPERATURE" : {
        "cold": "cold",
        "average": "not too cold, but not warm either",
        "warm": "noticeably warmer in here"
    },
    
    "DARKNESS" : {
        "dark": "pitch black",
        "average": "somewhat lit",
        "bright": "significantly bright"
    },
}

Items = [
    Item("Hood", "A worn hood made of coarse, greyish fabric."),
    Item("Quill", "An old-fashioned quill pen"),
    Item("Parchment", "A strangely-stained peace of paper."),
    Item("Carrot", "Why is there a fresh carrot here?"),
    Item("Torch", "A burnt out torch."),
    Item("Photograph", "A photograph of an old man and his dog."),
    Item("Vase", "Careful! You might smash it."),
    Item("Decapitated_Head", "Freaky..."),
    Item("Bloody_Knife", "Yikes."),
    Item("Butter_Knife", "I don't think anyone will die because of this."),
    Item("Shattered_Glass", "This will work as a makeshift weapon."),
    Item("Map", "Unfortunately for me, it's undecipherable.")
]

Player = {
    "room" : 0,
    "inventory": [],
    "playing": True,
    "insanity": 0,
}


        
Rooms = []

def generateRooms():
    
    def scatterItems():
        for item in Items:
            random.choice(Rooms).Items.append(item)
            Items.remove(item)
    
    def makeRoom(enteredFrom = None, previousRoom = None):
        possibleDirections = ["north", "east", "south", "west", "up", "down"]
        opposites = {
            "north" : "south",
            "south" : "north",
            "west" : "east",
            "east" : "west",
            "up" : "down",
            "down" : "up"
        }
        
        currentID = len(Rooms)
        Rooms.append(Room(currentID))
        currentRoom = Rooms[currentID]
        
        if enteredFrom:
            possibleDirections.remove(opposites[enteredFrom])
            currentRoom.Exits[opposites[enteredFrom]] = previousRoom
    
        for i in range(random.randint((0 if len(Rooms) > 4 else 1), 2) if currentID != 0 else random.randint(1, 2)):
            newDirection = random.choice(possibleDirections)
            possibleDirections.remove(newDirection)
            currentRoom.Exits[newDirection] = makeRoom(newDirection, currentRoom.ID)
            
        return currentID
   
    makeRoom()
    scatterItems()
    
    print("Total Rooms:", str(len(Rooms)))

def handleEncounter():
    scary_encounter = random.choice(ENCOUNTERS) if random.randint(1, 10) == 5 else False
    if scary_encounter:
        Player["insanity"] += scary_encounter[1]
        print(f"{scary_encounter[0]}\nYour Insanity Level has went up by {str(scary_encounter[1])} points.")
        if Player["insanity"] >= 100:
            print("You have been driven insane. It's not safe for you here anymore...\nGAME OVER!")
            Player["playing"] = False

      
    
def viewInventory(noun = None):
    print("You currently have:")
    for item in Player["inventory"]:
        print(item.Name)

def move(direction):
    currentRoom = Rooms[Player["room"]]
    if direction in currentRoom.Exits:
        Player["room"] = currentRoom.Exits[direction.lower()]
    
def examine(itemName):
    currentRoom = Rooms[Player["room"]]
    for item in (Player["inventory"] + currentRoom.Items):
        if item.Name.lower() == itemName.lower():
            print(f"{itemName} : {item.Description}")
            return
    print("No item found.")
    
def drop(itemName):
    currentRoom = Rooms[Player["room"]]
    for item in (Player["inventory"]):
        if item.Name.lower() == itemName.lower():
            item.drop(Player["inventory"])
            print("Dropped", itemName)
            return
    print("No item found.")

def take(itemName):
    currentRoom = Rooms[Player["room"]]
    for item in (currentRoom.Items):
        if item.Name.lower() == itemName.lower():
            item.pickUp(Player["inventory"])
            print("Picked up", itemName)
            return
    print("No item found.")

def exits(noun = None):
    currentRoom = Rooms[Player["room"]]
    print("Available Exits:")
    for key in currentRoom.Exits.keys():
        print(key)
        
def quit(noun = None):
    Player["playing"] = False
    print("You have quit the game.")
    
def check_items(noun = None):
    currentRoom = Rooms[Player["room"]]
    print("Items on the Ground:")
    if len(currentRoom.Items) == 0:
        print("None.")
    else:
        for x in currentRoom.Items:
            print(x.Name)
    
def look(noun = None):
    print(Rooms[Player["room"]].Description)

def calm(noun = None):
    Player["insanity"] -= (10 if Player["insanity"] >= 10 else Player["insanity"])
    print("You calmed down a bit.\n Your Insanity Level has reduced by 10 points.")
    
def check_insanity(noun = None):
    insanity = Player["insanity"]
    print(f"Insanity Level: {str(insanity)}%")

def handleInput(inpt):
    options = {
        "inventory": viewInventory,
        "go": move,
        "examine": examine,
        "drop":drop,
        "take":take,
        "exits":exits,
        "quit":quit,
        "look":look,
        "items": check_items,
        "calm": calm,
        "insanity": check_insanity
    }
    
    if inpt[0] in options:
        options[inpt[0]](inpt[1] if len(inpt) > 1 else "")
    

def game():
    generateRooms()
    prevRoom = -1
    while Player["playing"]:
        if prevRoom != Player["room"]:
            look()
            check_items()
            prevRoom = Player["room"]
            print("""
Options:
go [direction] - Travel to next room in given direction
examine [item] - Examine item in inventory or ground
drop [item] - Drop item
take [item] - Pick up item
inventory - View inventory
exits - View room exits
items - Check items on ground
look - View description of room
insanity - Check insanity level
calm - Calm yourself down
quit - Quit the game
""")
        handleEncounter()
        if Player["playing"] == False: break
        user_command = input("> ").split()
        if len(user_command) > 0:
            handleInput(user_command)
        
game()
