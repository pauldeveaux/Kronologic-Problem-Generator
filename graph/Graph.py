from graph.Room import Room
from graph.Character import Character
import random

from graph.Rule import RuleTag, Rule


class Graph:
    def __init__(self, nb_times=6, rooms=None, start_rooms=None, seed=None, given_information=0, nb_max_in_starting_room=1):
        if rooms is None:
            self.rooms = Room.create_rooms()
        else:
            self.rooms = rooms
        self.nb_times = nb_times
        if start_rooms is None:
            start_rooms = Graph.random_start_rooms(self.rooms.values())
        else:
            start_rooms = start_rooms

        self.characters = Character.create_characters(nb_times=nb_times, start_rooms=start_rooms)

        # Give starting information to some characters
        self.given_information = given_information
        state = random.getstate() # used to not change the seed because of the nb information given
        characters_copy = list(self.characters.keys())
        for i in range(given_information):
            character_given = random.choice(characters_copy)
            self.characters[character_given].information_given = True
            characters_copy.remove(character_given)
        random.setstate(state) # put the random state back to what it was before

        self.seed = seed


    def random_movements(self, time=6):
        """
        Generate random movements for the characters
        No rules are respected
        :param time:
        """
        for i in range(1, time):
            Character.random_move_characters(self.characters, i)

    @staticmethod
    def random_start_rooms(rooms, nb_characters_max=1):
        """
        Generate 6 random start rooms
        :param nb_characters_max: The maximum number of characters in a starting room
        :param rooms: the list of rooms
        :return: the list of start rooms
        """
        start_rooms = []
        available_rooms = {room: nb_characters_max for room in list(rooms)}
        for i in range(6):
            room = random.choice(list(available_rooms.keys()))
            start_rooms.append(room)
            available_rooms[room] -= 1
            if available_rooms[room] == 0:
                available_rooms.pop(room)
        return start_rooms

    def movements(self, rules: list = None, nb_times=6, nb_tests_max=5000):
        """
        Generate the movements of the characters
        :param rules: Rules the movements must respect
        :param nb_times: Number of times
        :param nb_tests_max: Maximum number of tests before giving up
        :return: None
        """
        if rules is None:
            rules = []

        def inner_movements(time):
            if time == nb_times:
                if Rule.test_rules(rules, RuleTag.END):
                    return True
                else:
                    return False
            nb_tests = 0
            error = False
            while nb_tests < nb_tests_max:
                for character in self.characters.values():
                    available_moves = character.times[time].adjacent_rooms.copy()
                    while True:
                        move = random.choice(available_moves)
                        available_moves.remove(move)
                        character.set_room(move, time + 1)
                        if Rule.test_rules(rules, RuleTag.MOVEMENT):
                            break
                        else:
                            character.remove_room(time + 1)
                        if len(available_moves) == 0:
                            error = True
                            break
                    if error:
                        break
                if not error and Rule.test_rules(rules, RuleTag.AFTER_A_TIME) and inner_movements(time + 1):
                    return True
                else:
                    nb_tests += 1
                    error = False
                    for character in self.characters.values():
                        character.remove_room(time + 1)

            return False

        solution_found = inner_movements(1)
        if solution_found:
            return
        else:
            raise Exception("No solution found")

    def show_matrix(self):
        """
        Print the matrix of the rooms for each time and each character
        :return:
        """
        s = ""
        # Column names
        s += "\t\t\t"

        for p in self.characters.values():
            s += f"{str(p.name).ljust(10)}\t\t"

        for t in range(1, self.nb_times + 1):
            s += f"\nTime {t}:\t\t"
            for p in self.characters.values():
                s += f"{str(p[t]).ljust(10)}\t\t"
        # Time number
        print(s)
        print("\n")

    def show_room_characters(self):
        """
        Print the time the characters are in each room
        :return:
        """
        for room in self.rooms.values():
            print(room)
            room.print_characters()
            print("\n")

    def show_time_characters(self):
        """
        Print the position of characters for each time
        """
        for time in range(1, self.nb_times + 1):
            print(f"Time {time}")
            for room in self.rooms.values():
                print(f"{room.name}: {room.characters[time]}")
            print("\n")

    def show_information_given(self):
        """
        Print the characters that have information given and the rooms they start in
        """
        for character in self.characters.values():
            if character.information_given:
                print(f"{character.name} starts in {character.times[1]} in time 1")
        print("\n")
