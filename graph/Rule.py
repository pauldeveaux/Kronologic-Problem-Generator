import random

from graph.Character import Character
from enum import Enum


class RuleTag(Enum):
    """
    Enum to specify when the rule must be tested
    """
    MOVEMENT = 1
    END = 2
    START_ROOM = 3
    AFTER_A_TIME = 4


class Rule:
    """
    Class to represent a rule
    """

    def __init__(self, lambda_function=None, test_at=RuleTag.MOVEMENT, debug_id=None):
        self.lambda_function = lambda_function
        self.test_time = test_at
        self.debug_id = debug_id

    def is_respected(self):
        """
        Test if the rule is respected
        :return: True if the rule is respected, False otherwise
        """
        return self.lambda_function()

    @staticmethod
    def rules_for_part(part, graph):
        """
        Create the rules for the part 1 or 2 of Kronologic : The poisoning or The ghost
        :param graph: The graph
        :param part: The part of the game. 1 or 2
        :return: a list of rules
        """
        if part == 1:
            return Rule.rules_for_part_1(graph)
        elif part == 2:
            return Rule.rules_for_part_2(graph)
        else:
            return []

    @staticmethod
    def rules_for_part_1(graph):
        """
        Create the rules for the part 1 of Kronologic : The poisoning
        :param graph: The graph
        :return: a list of rules
        """
        rule1 = Rule.create_exactly_one_time_with_two_people(graph.characters["Detective"])
        rule2 = Rule.create_exactly_one_time_with_two_people_after_time(graph.characters["Detective"])
        rule3 = Rule.create_no_more_than_3_in_a_room(list(graph.characters.values()))
        return [rule1, rule2, rule3]

    @staticmethod
    def rules_for_part_2(graph, print_ghost=False):
        """
        Create the rules for the part 2 of Kronologic : The ghost
        :param graph: The graph
        :param print_ghost: If True, print the ghost's name. False by default
        :return: a list of rules
        """
        ghost = random.choice(list(graph.characters.values()))
        # Rule 1: The detective is always alone
        rule1 = Rule.create_is_always_alone(ghost)
        # Rule 2: Everyone is at least one time not alone (except the detective)
        rule2 = Rule.create_everyone_at_least_one_time_not_alone(
            [character for character in graph.characters.values() if
             character.name != ghost.name])
        rule3 = Rule.create_no_more_than_3_in_a_room(list(graph.characters.values()))

        return [rule1, rule2, rule3]

    @staticmethod
    def test_rules(rules, tag):
        """
        Test if all the rules are respected at a specific time
        :param rules: A list of rules
        :param tag: The tag of the rules to test
        :return: True if all the rules are respected, False otherwise
        """
        for rule in rules:
            if rule.test_time == tag:
                if rule.debug_id == 3:
                    pass
                if not rule.is_respected():
                    return False
        return True
        #return all(rule.is_respected() for rule in rules if rule.test_time == tag)

    @staticmethod
    def create_is_always_alone(character: Character):
        """
        Create a rule to test if a character is always alone
        :param character: The character that must be alone
        :return: a Rule
        """
        return Rule(lambda: all(len(room.characters[time]) <= 1 for time, room in character.times.items()),
                    test_at=RuleTag.MOVEMENT)

    @staticmethod
    def create_is_at_least_one_time_not_alone(character: Character):
        """
        Create a rule to test if a character is at least one time not alone
        :param character: The character that must be at least one time not alone
        :return: a Rule
        """
        return Rule(lambda: any(len(room.characters[time]) > 1 for time, room in character.times.items()),
                    test_at=RuleTag.END)

    @staticmethod
    def create_everyone_at_least_one_time_not_alone(characters: list):
        """
        Create a rule to test if everyone is at least one time not alone in the list of characters
        :param characters: The list of characters
        :return: a Rule
        """
        return Rule(lambda: all(any(len(room.characters[time]) > 1 for time, room in character.times.items())
                                for character in characters), test_at=RuleTag.END)

    @staticmethod
    def create_different_start_rooms(characters: list):
        # TODO
        pass

    @staticmethod
    def create_different_start_rooms_for(character: Character):
        # TODO
        pass
        return Rule(lambda: len(set(character.times.values())) == len(character.times), test_at=RuleTag.START_ROOM)

    @staticmethod
    def create_exactly_one_time_with_two_people_after_time(character: Character):
        """
        Create a rule to test if a character is exactly one time with two people
        This rule is tested at the end of a time
        :param character: The character that must be exactly one time with two people
        :return: a Rule
        """
        return Rule(lambda: sum(len(room.characters[time]) == 2 for time, room in character.times.items()) <= 1,
                    test_at=RuleTag.AFTER_A_TIME)

    @staticmethod
    def create_exactly_one_time_with_two_people(character: Character):
        """
        Create a rule to test if a character is exactly one time with two people
        This rule is tested at the end of the algorithm
        :param character: The character that must be exactly one time with two people
        :return: a Rule
        """
        return Rule(lambda: sum(len(room.characters[time]) == 2 for time, room in character.times.items()) == 1,
                    test_at=RuleTag.END)

    @staticmethod
    def create_no_more_than_3_in_a_room(characters: list):
        """
        Create a rule to test if there is no more than 3 characters in a room at any time
        :param characters: The list of characters
        :return: a Rule
        """

        def inner():
            rooms = [room for character in characters for room in character.times.values()]
            return all(len(room.characters[time]) <= 3 for room in rooms for time in room.characters)

        f = lambda: inner()
        return Rule(f, test_at=RuleTag.MOVEMENT, debug_id=3)


def nb_max_characters_in_starting_room(part):
    """
    Return the maximum number of characters in a starting room depending on the part of the game
    :param part: The part of the game
    :return: The maximum number of characters in a starting room
    """
    if part == 1:
        return 2
    elif part == 2:
        return 1
    elif part == 3:
        return 2