import numpy as np
import random

cards_layout = [["Character_Journaliste_Share",   "Time5_Solo",       "Time4_Solo",       "Time6_Share"],
                ["Baronne_Solo",        "Time1_Share",      "Time3_Share",      "Servante_Share"],
                ["Aventuriere_Solo",    "Chauffeur_Solo",   "Time2_Share",      "Detective_Solo"],
                ["Time4_Share",         "Time6_Solo",       "Time5_Share",      "Aventuriere_Share"],
                ["Detective_Share",     "Journaliste_Solo", "Servante_Solo",    "Baronne_Share"],
                ["Time1_Solo",          "Time2_Solo",       "Chauffeur_Share",  "Time3_Solo"]]

layout = {
    "Characters": {
        "Shared": {
            "Coords": [(0, 0), (1, 3), (3, 3), (4, 0), (4, 3), (5, 2)],
            "Names": {
                "Journaliste": (0, 0),
                "Servante": (1,3),
                "Aventuriere": (3,3),
                "Detective": (4,0),
                "Baronne": (4,3),
                "Chauffeur": (5,2)
            }
        },
        "Solo": {
            "Coords": [(1, 0), (2, 0), (2, 1), (2, 3), (4, 1), (4, 2)],
            "Names": {
                "Baronne": (1, 0),
                "Aventuriere": (2, 0),
                "Chauffeur": (2, 1),
                "Detective": (2, 3),
                "Journaliste": (4, 1),
                "Servante": (4, 2)
            }
        }
    },
    "Times": {
        "Shared": {
            "Time1": (1, 1),
            "Time2": (2, 2),
            "Time3": (1, 2),
            "Time4": (3, 0),
            "Time5": (3, 2),
            "Time6": (0, 3)
        },
        "Solo": {
            "Time1": (5, 0),
            "Time2": (5, 1),
            "Time3": (5, 3),
            "Time4": (0, 2),
            "Time5": (0, 1),
            "Time6": (3, 1)
        }
    }

}


class Card:
    def __init__(self, room, characters, seed=None, part=1):
        self.room = room
        self.icons = np.empty((6, 4), dtype=object)
        self.seed = seed
        self.part = part

        # Fill characters share icons and retry icons
        characters_times = {character: [] for character in characters.values()}

        for time, characters in room.characters.items():
            for character in characters:
                #characters_times[character.name].append(time)
                characters_times.setdefault(character, []).append(time)

        for character, time in characters_times.items():
            self.icons[layout["Characters"]["Shared"]["Names"][character.name]] = f"X{len(time)}"
            if len(time) == 0 or (character.information_given and time == [1]):
                self.icons[layout["Characters"]["Solo"]["Names"][character.name]] = "Retry"
            else:
                time_displayed = random.choice([t for t in time if (not character.information_given or t != 1)])
                self.icons[layout["Characters"]["Solo"]["Names"][character.name]] = f"T{time_displayed}"

        # Fill time icons
        for time, characters in room.characters.items():
            self.icons[layout["Times"]["Shared"][f"Time{time}"]] = f"X{len(characters)}"
            if len(characters) == 0:
                self.icons[layout["Times"]["Solo"][f"Time{time}"]] = "Retry"
            else:
                character_displayed = random.choice(characters).name
                self.icons[layout["Times"]["Solo"][f"Time{time}"]] = character_displayed

    @staticmethod
    def create_cards(graph, show_seed=True, part=1):
        """
        Create the cards for each room
        :param graph: The graph
        :param seed: The seed of the game
        :return: a list of cards
        """
        cards = []
        for room in graph.rooms.values():
            if show_seed:
                cards.append(Card(room, graph.characters, seed=graph.seed, part=part))
            else:
                cards.append(Card(room, graph.characters, part=part))
        return cards

