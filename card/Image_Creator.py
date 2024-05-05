import os
from PIL import Image, ImageFont, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import webbrowser

IMG_PATH = 'imgs/png/'
BLANK_PATH = os.path.join(IMG_PATH, 'Blank.png')
PDF_DIR = 'pdfs/'

# Load the blank image for the background of a card
background = Image.open(BLANK_PATH)


# TODO X4 X5 X6
# Load all images
images = {
    "Aventuriere": Image.open(os.path.join(IMG_PATH, 'Aventuriere.png')),
    "Baronne": Image.open(os.path.join(IMG_PATH, 'Baronne.png')),
    "Chauffeur": Image.open(os.path.join(IMG_PATH, 'Chauffeur.png')),
    "Detective": Image.open(os.path.join(IMG_PATH, 'Detective.png')),
    "Journaliste": Image.open(os.path.join(IMG_PATH, 'Journaliste.png')),
    "Servante": Image.open(os.path.join(IMG_PATH, 'Servante.png')),
    "Retry": Image.open(os.path.join(IMG_PATH, 'Retry.png')),
    "X0": Image.open(os.path.join(IMG_PATH, 'X0.png')),
    "X1": Image.open(os.path.join(IMG_PATH, 'X1.png')),
    "X2": Image.open(os.path.join(IMG_PATH, 'X2.png')),
    "X3": Image.open(os.path.join(IMG_PATH, 'X3.png')),
    #"X4": Image.open(os.path.join(IMG_PATH, 'X4.png')),
    #"X5": Image.open(os.path.join(IMG_PATH, 'X5.png')),
    #"X6": Image.open(os.path.join(IMG_PATH, 'X6.png')),
    "T1": Image.open(os.path.join(IMG_PATH, 'T1.png')),
    "T2": Image.open(os.path.join(IMG_PATH, 'T2.png')),
    "T3": Image.open(os.path.join(IMG_PATH, 'T3.png')),
    "T4": Image.open(os.path.join(IMG_PATH, 'T4.png')),
    "T5": Image.open(os.path.join(IMG_PATH, 'T5.png')),
    "T6": Image.open(os.path.join(IMG_PATH, 'T6.png')),
    "Stairs": Image.open(os.path.join(IMG_PATH, 'Stairs.png')),
    "Room": Image.open(os.path.join(IMG_PATH, 'Room.png')),
    "Hallway": Image.open(os.path.join(IMG_PATH, 'Hallway.png')),
    "Scene": Image.open(os.path.join(IMG_PATH, 'Scene.png')),
    "Sing Room": Image.open(os.path.join(IMG_PATH, 'Sing_Room.png')),
    "Dance Room": Image.open(os.path.join(IMG_PATH, 'Dance_Room.png')),
    "Txt_Scene": Image.open(os.path.join(IMG_PATH, 'Txt_Scene.png')),
    "Txt_Sing Room": Image.open(os.path.join(IMG_PATH, 'Txt_Sing.png')),
    "Txt_Dance Room": Image.open(os.path.join(IMG_PATH, 'Txt_Dance.png')),
    "Txt_Room": Image.open(os.path.join(IMG_PATH, 'Txt_Room.png')),
    "Txt_Hallway": Image.open(os.path.join(IMG_PATH, 'Txt_Hallway.png')),
    "Txt_Stairs": Image.open(os.path.join(IMG_PATH, 'Txt_Stairs.png')),
    "Part_1": Image.open(os.path.join(IMG_PATH, 'Txt_Part_1.png')),
    "Part_2": Image.open(os.path.join(IMG_PATH, 'Txt_Part_2.png')),
    "Map": Image.open(os.path.join(IMG_PATH, 'Map.png')),
}


def create_img_from_card(card):
    """
    Create an image from a card with the icons and the room's name
    :param card: The card to create the image from
    :return: The image of the card
    """
    img = background.copy()

    # Hint icons in the card
    for col in range(4):
        for lin in range(6):
            if card.icons[lin, col] is not None:
                icon = images[card.icons[lin, col]]
                img.paste(icon, get_hint_icon_img_coords(col, lin), icon)

    # Icon of the room
    room_icon = images[card.room.name]
    img.paste(room_icon, get_room_icon_coords(), room_icon)

    # Seed number
    if card.seed is not None:
        add_seed_number_to_img(img, card.seed)

    # Room's name
    room_txt_img = images[f"Txt_{card.room.name}"]
    img.paste(room_txt_img, (int(1550-room_txt_img.width/2), 500), room_txt_img)

    # Part's name
    part_txt_img = images[f"Part_{card.part}"]
    img.paste(part_txt_img, (int(1450-part_txt_img.width/2), -10), part_txt_img)

    return img


def create_pdf_from_cards(graph, cards, pdf_name="Kronologic.pdf", openPDF=True):
    """
    Create a pdf from a list of cards
    :param graph: The graph of the game
    :param cards: The list of cards to put in the pdf
    :param pdf_name: The name of the pdf
    :param openPDF: If True, open the pdf automatically after creation
    """
    pdf_file = os.path.join(PDF_DIR, pdf_name)
    can = canvas.Canvas(pdf_file, pagesize=A4)

    # Add the map to pdf if there is some information given at start
    if graph.given_information > 0:
        characters_with_information = [c for c in graph.characters.values() if c.information_given]
        map_img = get_given_information_img(characters_with_information, seed=graph.seed)
        add_img_to_pdf(can, map_img, 210, 680, real_coords=True, rotation=0, size_multiplier=0.65)

    # Add the cards images to the pdf
    x = 0
    y = 0
    for c in cards:
        img = create_img_from_card(c)
        add_img_to_pdf(can, img, x, y)
        x += 1
        if x == 2:
            x = 0
            y += 1

    # Save the pdf and open it if openPDF is True
    can.save()
    if openPDF:
        webbrowser.open(os.path.abspath(pdf_file))


def get_given_information_img(characters, seed=None):
    """
    Create an image with information given at start
    :param characters: characters with information given at start
    :param seed: The seed number to add to the image
    :return: an image with the characters icons on the map
    """
    img = images["Map"]

    # Coordinates of the icons in the img map. The count is used to know which coordinate to use depending on
    # the number of characters in the room
    icon_in_rooms_coords = {
        "Scene": {'coords': [(170, 60), (170, 130), (170, 170), (170, 85), (170, 150), (195, 60)], 'count': 0},
        "Sing Room": {'coords': [(250, 100), (250, 80), (275, 100), (275, 80), (215, 100), (215, 80)], 'count': 0},
        "Dance Room": {'coords': [(250, 160), (250, 140), (275, 160), (275, 140), (215, 160), (215, 140)], 'count': 0},
        "Room": {'coords': [(120, 150), (120, 180), (120, 70), (120, 95), (120, 115), (120, 210)], 'count': 0},
        "Hallway": {'coords': [(15, 70), (15, 130), (15, 150), (15, 170), (15, 90), (15, 110)], 'count': 0},
        "Stairs": {'coords': [(50, 83), (50, 130), (80, 83), (50, 155), (80, 130), (80, 155)], 'count': 0},
    }

    # Add the characters icons to the image
    for c in characters:
        icon = images[c.name].copy()
        icon.thumbnail((30, 30))
        coords = icon_in_rooms_coords[c.times[1].name]
        img.paste(icon, coords['coords'][coords['count']], icon)
        coords['count'] += 1

    # Add the seed number to the image
    if seed is not None:
        add_seed_number_to_img(img, seed, x=0, y=40, rotation=0, size=14)

    return img


def add_seed_number_to_img(img, seed, x=95, y=500, rotation=90, size=100):
    """
    Add the seed number to a card image
    :param img: The image of the card
    :param seed: The seed number to add
    :param x: The x coordinate of the seed text, 95 by default
    :param y: The y coordinate of the seed text, 500 by default
    :param rotation: The rotation of the seed text, 90 by default
    :param size: The size of the seed text, 100 by default
    """
    # Draw seed number to another image
    text_img = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_img)
    font = ImageFont.truetype("ariali.ttf", size)
    draw.text((0, 0), f"Seed : {seed}", (51,44,44), font=font)

    # Rotate the text
    text_img = text_img.rotate(rotation, expand=True)

    # Create a new transparent image to keep the size of the original image
    new_img = Image.new('RGBA', img.size, (255, 255, 255, 0))
    new_img.paste(text_img, (0, 0))
    text_img = new_img

    # Paste the text image to the original image
    img.paste(Image.alpha_composite(img, text_img), (x, y), text_img)


def add_img_to_pdf(c, img, x, y, size_multiplier=0.5, real_coords=False, rotation=90):
    """
    Add an image to a pdf
    :param c: The canvas of the pdf
    :param img: The image to add
    :param x: The x coordinate
    :param y: The y coordinate
    :param size_multiplier: The size multiplier of the image in the pdf (0.5 by default)
    :param real_coords: If True, the x and y coordinates are the real coordinates in the pdf, if False, the x and y
    coordinates are the coordinates calculated for the grid of cards images in the pdf
    :param rotation: The rotation of the image (90 by default)
    """

    # Rotate
    img = img.rotate(rotation, expand=True)

    # Resize
    img.thumbnail((500, 500))

    # Transform transparent background to white
    white_background = Image.new("RGBA", img.size, (255, 255, 255))
    img = Image.alpha_composite(white_background, img)

    # Save the image to a temporary file, add it to the pdf and delete it
    img.save(f"temp{x}_{y}.png")
    if real_coords:
        coords = (x, y)
    else:
        coords = get_pdf_coords(x, y)
    c.drawImage(f"temp{x}_{y}.png", coords[0], coords[1], width=img.size[0] * size_multiplier,
                height=img.size[1] * size_multiplier)
    os.remove(f"temp{x}_{y}.png")


def get_hint_icon_img_coords(x, y):
    """
    Get the coordinates of an icon in a card image
    :param x: The x coordinate in the card (grid)
    :param y: The y coordinate in the card (grid)
    :return: The real coordinates of the icon in the card image
    """
    origin = (250, 875)
    odd_step = 180
    x_step = 480
    y_step = 400
    return origin[0] + x * x_step + odd_step * (y%2), origin[1] + y * y_step


def get_room_icon_coords():
    """
    Get the coordinates of the room icon in a card image
    :return: The real coordinates of the room icon in the card image
    """
    return 267, 170


def get_pdf_coords(x, y):
    """
    Get the real coordinates of a card in the pdf
    :param x: The x coordinate in the grid of cards
    :param y: The y coordinate in the grid of cards
    :return: The real coordinates of the card image in the pdf
    """
    origin = (25, 30)
    x_step = 300
    y_step = 230
    return origin[0] + x * x_step, origin[1] + y * y_step
