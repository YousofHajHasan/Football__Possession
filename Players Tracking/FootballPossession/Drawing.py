import cv2
from Mask import *


def DrawPlayersRectangle(img, Player_class, coordinates, colors_class):

    if Player_class == "red":
        cv2.rectangle(img, (coordinates[0], coordinates[1]), (coordinates[2], coordinates[3]), color("red"), 3)
        cv2.putText(img, text=colors_class["red"], org=(coordinates[0] - 5, coordinates[1] - 5), fontFace=1, fontScale=1,
                    thickness=2, color=color("red"))
    elif Player_class == "green":
        cv2.rectangle(img, (coordinates[0], coordinates[1]), (coordinates[2], coordinates[3]), color("green"), 3)
        cv2.putText(img, text=colors_class["green"], org=(coordinates[0] - 5, coordinates[1] - 5), fontFace=1, fontScale=1,
                    thickness=2, color=color("green"))
    elif Player_class == "yellow":
        cv2.rectangle(img, (coordinates[0], coordinates[1]), (coordinates[2], coordinates[3]), color("yellow"), 3)
        cv2.putText(img, text=colors_class["yellow"], org=(coordinates[0] - 5, coordinates[1] - 5), fontFace=1, fontScale=1,
                    thickness=2, color=color("yellow"))
    elif Player_class == "black":
        cv2.rectangle(img, (coordinates[0], coordinates[1]), (coordinates[2], coordinates[3]), color("black"), 3)
        cv2.putText(img, text=colors_class["black"], org=(coordinates[0] - 5, coordinates[1] - 5), fontFace=1, fontScale=1,
                    thickness=2, color=color("black"))
    elif Player_class == "grey":
        cv2.rectangle(img, (coordinates[0], coordinates[1]), (coordinates[2], coordinates[3]), color("grey"), 3)
        cv2.putText(img, text=colors_class["grey"], org=(coordinates[0] - 5, coordinates[1] - 5), fontFace=1, fontScale=1,
                    thickness=2, color=color("grey"))
    elif Player_class == "white":
        cv2.rectangle(img, (coordinates[0], coordinates[1]), (coordinates[2], coordinates[3]), color("white"), 3)
        cv2.putText(img, text=colors_class["white"], org=(coordinates[0] - 5, coordinates[1] - 5), fontFace=1, fontScale=1,
                    thickness=2, color=color("white"))
    elif Player_class == "blue":
        cv2.rectangle(img, (coordinates[0], coordinates[1]), (coordinates[2], coordinates[3]), color("blue"), 3)
        cv2.putText(img, text=colors_class["blue"], org=(coordinates[0] - 5, coordinates[1] - 5), fontFace=1, fontScale=1,
                    thickness=2, color=color("blue"))

    return img

def get_teams_information(available_colors):

    Team1 = input("Enter Team1 Name: ")
    while True:
        Team1_color = input(f"Enter {Team1} color: ").lower()
        if Team1_color in available_colors:
            break
        else:
            print("Color unavailable...")
    while True:
        Team1_Keeper = input(f"Enter {Team1} Keeper color: ").lower()
        if Team1_Keeper.lower() in available_colors:
            break
        else:
            print("Color unavailable...")

    Team2 = input("Enter Team2 Name: ")
    while True:
        Team2_color = input(f"Enter {Team2} color: ").lower()
        if Team2_color in available_colors:
            break
        else:
            print("Color unavailable...")
    while True:
        Team2_Keeper = input(f"Enter {Team2} Keeper color: ").lower()
        if Team2_Keeper in available_colors:
            break
        else:
            print("Color unavailable...")

    while True:
        Referee = input(f"Enter referee color: ").lower()
        if Referee in available_colors:
            break
        else:
            print("Color unavailable...")
    return {Team1: [Team1_color, Team1_Keeper], Team2: [Team2_color, Team2_Keeper], "Referee": [Referee]}


def get_teams_color(Teamsinfo):
    """
    :param Teamsinfo: A dictionary with team name as key and players and the goalkeeper color as a values.
    Example:   {"Bayern":["red", "green"], "Dortmund":["yellow", "grey"], "Referee":["black"]}
    :return List of lists that contain the colors of each team as an index:
    Example: [["red", "green"], ["yellow", "grey"], ["black"]]
    """
    colors = []
    Teams_name = list(Teamsinfo.keys())
    for team in Teams_name:
        colors.append(Teamsinfo[team])
    return colors


def get_colors_class(Teamsinfo):
    """
    :param Teamsinfo: A dictionary with team name as key and players and the goalkeeper color as a values.
    Example:   {"Bayern":["red", "green"], "Dortmund":["yellow", "grey"], "Referee":["black"]}
    :return: A dictionary, each key represents a color and which team it describes as a value.
    Example: {'red': 'Bayern', 'green': 'Bayern Keeper', 'yellow': 'Dortmund', 'grey': 'Dortmund Keeper', 'black': 'Referee'}
    """
    color_representation = {}
    Teams_name = list(Teamsinfo.keys())

    for team in Teams_name:
        if team == "Referee":
            color_representation[Teamsinfo[team][0]] = "Referee"
            break
        color_representation[Teamsinfo[team][0]] = team
        color_representation[Teamsinfo[team][1]] = team + " Keeper"

    return color_representation

def Draw_ball(img, coordinates):
    cv2.rectangle(img, (coordinates[0] + 10, coordinates[1] + 20), (coordinates[2] - 10, coordinates[3] - 20), (0, 0, 0), 3)
