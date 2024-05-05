import argparse
import math

from graph.Graph import *
from graph.Rule import *
from card.Card import *
from card.Image_Creator import *


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", type=int, default=1, help="Part of the game. 1, 2 or 3")
    parser.add_argument("--nb_information", type=int, default=6,
                        help="Number of information given about character's position in time 1. Between 0 and 6")
    parser.add_argument("--seed", type=int, default=None, help="Seed of the game")
    parser.add_argument("--solution", action='store_true', default=False, help="Show the solution of the problem")
    parser.add_argument("--debug", action='store_true', default=False, help="Print debug information")
    parser.add_argument("--no_pdf", action='store_true', default=False, help="Prevent the pdf from being created")
    return parser.parse_args()


def generate_problem(part, given_information, seed=None):
    # Creation of the graph
    rooms = Room.create_rooms()
    nb_max = nb_max_characters_in_starting_room(part)
    g = Graph(nb_times=6, given_information=given_information, rooms=rooms, seed=seed, nb_max_in_starting_room=nb_max)

    # Rules
    rules = Rule.rules_for_part(part, g)

    # Generate movements
    g.movements(rules=rules, nb_times=6)
    return g


def debug_print(g):
    g.show_information_given()
    g.show_matrix()
    g.show_room_characters()


if __name__ == "__main__":
    args = get_args()
    part = args.part
    seed = args.seed

    if seed:
        part = math.floor(seed / 10000000)
        if part not in [1, 2, 3]:
            raise ValueError("Wrong seed")

    print(f"\nCreation of a problem :\n\tPart : {part}\n\tSeed : {seed}\n"
          f"\tNumber of information given at start : {args.nb_information}\n\n")

    given_information = args.nb_information
    if not 0 <= given_information <= 6:
        raise ValueError("Number of information given must be between 0 and 6")

    if not seed:
        seed = random.randint(0, 10000000)
        seed += 10000000 * part
    random.seed(seed)

    succes = False
    while not succes:
        try:
            graph = generate_problem(part, given_information, seed)
            succes = True
        except Exception as e:
            continue

    if args.solution:
        if not seed:
            raise ValueError("Seed must be given to show the solution")
        graph.show_matrix()
    else:
        if not args.no_pdf:
            # Creation of cards and pdf
            cards = Card.create_cards(graph, part=part)
            create_pdf_from_cards(graph, cards, pdf_name=f"Kronologic_{graph.seed}.pdf", openPDF=True)
        if args.debug:
            debug_print(graph)
        print("Your seed is : ", graph.seed)

# TODO
# Create verso of cards
# Add a part for the solution
# Rules for part 3