

class Room:
    def __init__(self, name, adjacent_rooms=None, nb_times=6):
        if adjacent_rooms is None:
            adjacent_rooms = []
        self.name = name
        self.adjacent_rooms = adjacent_rooms
        self.characters = {time: [] for time in range(1, nb_times + 1)}

    def add_character(self, character, time):
        """
        Add a character to the room at a specific time
        :param character: The character to add
        :param time: The time to add the character
        """
        self.characters[time].append(character)
        character.times[time] = self

    def remove_character(self, character, time):
        """
        Remove a character from the room at a specific time
        :param character: character to remove
        :param time: time to remove the character
        """
        self.characters[time].remove(character)
        character.times[time] = NULL_ROOM

    def add_adjacent_rooms(self, rooms: list):
        """
        Add adjacent rooms
        :param rooms: list of rooms
        """
        self.adjacent_rooms.extend(rooms)

    def print_characters(self):
        """
        Print the characters in the room at each time
        """
        for time, characters in self.characters.items():
            print(f"Time {time}: {characters}")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @staticmethod
    def create_rooms():
        """
        Create the rooms with their adjacent rooms
        :return: a dictionary of rooms
        """
        # Create rooms
        rooms = {}
        rooms["Sing Room"] = Room("Sing Room")
        rooms["Dance Room"] = Room("Dance Room")
        rooms["Scene"] = Room("Scene")
        rooms["Stairs"] = Room("Stairs")
        rooms["Room"] = Room("Room")
        rooms["Hallway"] = Room("Hallway")

        # Adjacent rooms
        rooms["Sing Room"].add_adjacent_rooms([rooms["Dance Room"], rooms["Scene"]])
        rooms["Dance Room"].add_adjacent_rooms([rooms["Sing Room"], rooms["Scene"]])
        rooms["Scene"].add_adjacent_rooms([rooms["Sing Room"], rooms["Dance Room"], rooms["Room"]])
        rooms["Stairs"].add_adjacent_rooms([rooms["Room"], rooms["Hallway"]])
        rooms["Room"].add_adjacent_rooms([rooms["Scene"], rooms["Stairs"], rooms["Hallway"]])
        rooms["Hallway"].add_adjacent_rooms([rooms["Stairs"], rooms["Room"]])
        return rooms


# Null room used to define a room not yet assigned to a character
NULL_ROOM = Room("Null Room")
