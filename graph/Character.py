from .Room import *
import random


class Character:
    """
    Class to represent a character
    """
    def __init__(self, name, start_room, nb_times=6):
        self.name = name
        self.times = {i: NULL_ROOM for i in range(1, nb_times + 1)}
        self.start_time = None
        self.set_start_room(start_room)
        self.information_given = False

    def set_start_room(self, room, time=1):
        """
        Set the start room of the character
        :param room: The room
        :param time: The first information about time. 1 by default
        """
        self.times[time] = room
        self.start_time = time
        room.characters[time].append(self)

    def set_room(self, room, time):
        """
        Set the room of the character at a specific time
        :param room: The room
        :param time: The time
        """
        self.times[time] = room
        room.characters[time].append(self)

    def remove_room(self, time):
        """
        Remove the room of the character at a specific time
        :param time: The time
        """
        if self.times[time] == NULL_ROOM:
            return
        self.times[time].characters[time].remove(self)
        self.times[time] = NULL_ROOM

    def random_move(self, start_time, next_time=None):
        """
        Move the character randomly
        :param start_time: The time the character start to move
        :param next_time: The time the character will be at the next room. start_time + 1 by default
        """
        if next_time is None:
            next_time = start_time + 1
        self.times[next_time] = random.choice(self.times[start_time].adjacent_rooms)

    def print_rooms(self):
        """
        Print the rooms of the character at each time
        """
        for time, room in self.times.items():
            print(f"Time {time}: {room}")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __getitem__(self, item):
        return self.times[item]


    @staticmethod
    def create_characters(start_rooms=None, nb_times=6):
        """
        Create the characters of the game
        :param start_rooms: The start rooms of the characters. NULL_ROOM by default
        :param nb_times: The number of times of the game
        :return: a dictionary of characters
        """
        if start_rooms is None:
            start_rooms = [NULL_ROOM for _ in range(6)]
        characters = {}
        characters["Aventuriere"] = Character("Aventuriere", start_rooms[0], nb_times=nb_times)
        characters["Baronne"] = Character("Baronne", start_rooms[1], nb_times=nb_times)
        characters["Chauffeur"] = Character("Chauffeur", start_rooms[2], nb_times=nb_times)
        characters["Detective"] = Character("Detective", start_rooms[3], nb_times=nb_times)
        characters["Journaliste"] = Character("Journaliste", start_rooms[4], nb_times=nb_times)
        characters["Servante"] = Character("Servante", start_rooms[5], nb_times=nb_times)
        return characters

    @staticmethod
    def random_move_characters(characters, time):
        """
        Move the characters randomly
        :param characters: The characters to move
        :param time: The time to move the characters
        :return: The characters moved
        """
        for character in characters.values():
            character.random_move(time)
        return characters