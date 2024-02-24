import cv2
import numpy as np
from Mask import *
from Drawing import *


def addScoreboard(scoreboard, img):
    scoreboard = cv2.resize(scoreboard, (345, 123))
    img[22:145, 55:400] = scoreboard
    return img


def scoreBoard(bars, team1_Name, team2_Name):
    scoreboard = cv2.imread("C:/Users/user/Downloads/Score.png")
    bars = cv2.resize(bars, (517, 57))
    scoreboard_height, scoreboard_width, _ = scoreboard.shape

    scoreboard[174:231, 24:541] = bars

    text_size, _ = cv2.getTextSize(f"{team2_Name}", cv2.FONT_HERSHEY_COMPLEX, 0.8, 2)
    # This is used to make specify the text location based on the bottom right pixel
    bottom_right_x = scoreboard_width - 23 - text_size[0] # Adjust according to your desired x position

    cv2.putText(scoreboard, f"{team1_Name}", (24, 157),
                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 2)
    cv2.putText(scoreboard, f"{team2_Name}", (bottom_right_x, 157),
                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 2)

    return scoreboard


def create_possession_widget(team1_percentage, team2_percentage, teams_info):

    """
    teams_info: Dictionary to store team names as keys and a list of associated colors as values in this format.:
    {"Bayern":["red", "green"], "Dortmund":["yellow", "grey"], "Referee":["black"]}
    """
    teams_name = list(teams_info.keys())
    # Set widget dimensions and font properties
    width = 500
    height = 80
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.9
    thickness = 4

    # Create background image
    bars = np.zeros((height, width, 3), dtype=np.uint8)

    # Set colors for each team's percentage
    team1_color = color(teams_info[teams_name[0]][0])
    team2_color = color(teams_info[teams_name[1]][0])

    # Calculate bar widths based on percentages
    team1_bar_width = int(width * team1_percentage / 100)
    team2_bar_width = int(width * team2_percentage / 100)

    # Draw team 1 bar
    bars[:, :team1_bar_width] = team1_color

    # Draw team 2 bar
    bars[:, team1_bar_width:] = team2_color

    # Add team labels and percentages
    cv2.putText(bars, f"{team1_percentage}%", (10, height // 2 + 5),
               font_face, font_scale, (0, 0, 0), thickness)
    cv2.putText(bars, f"{team2_percentage}%", (width - 55, height // 2 + 5),
               font_face, font_scale, (0, 0, 0), thickness)

    scoreboard = scoreBoard(bars, teams_name[0], teams_name[1])

    return scoreboard


def Percentage(t1_total, t2_total, teams_info):
    teams_name = list(teams_info.keys())
    Total = t1_total + t2_total
    team1Per = round(t1_total/Total*100)
    team2Per = round(t2_total/Total*100)
    print(f"{teams_name[0]} {team1Per}% --- {team2Per}% {teams_name[1]}")
    scoreboard = create_possession_widget(team1Per, team2Per, teams_info)
    if round(t1_total / Total * 100) + round(t2_total / Total * 100) != 100:
        print("No Way")

    return scoreboard


def CalPossession(FPS, team, t1_counter, t2_counter, img, t1_total, t2_total, teams_info, scoreboard):
    if team == 1:
        t1_counter += 1
        if t1_counter == int(FPS/4):
            t2_counter = 0
    else:
        t2_counter += 1
        if t2_counter == int(FPS/4):
            t1_counter = 0

    if t1_counter >= int(FPS/2):
        t1_total += 1
        scoreboard = Percentage(t1_total, t2_total, teams_info)
        t1_counter = 0  # Reset the counters
        t2_counter = 0  # Reset the counters

    elif t2_counter >= int(FPS/2):
        t2_total += 1
        scoreboard = Percentage(t1_total, t2_total, teams_info)
        t2_counter = 0  # Reset the counters
        t1_counter = 0  # Reset the counters

    return t1_counter, t2_counter, t1_total, t2_total, scoreboard


def CalculateDistance(Ball, Players, teams_info, img, FPS, t1_counter, t2_counter, t1_total, t2_total, scoreboard):
    BallCenter = (int((Ball[0] + Ball[2]) / 2), int((Ball[1] + Ball[3]) / 2))  # (x,y) of the center of the ball
    teams_color = get_teams_color(teams_info)
    team1 = teams_color[0]
    team2 = teams_color[1]
    closest_point = None
    Player_color = None
    min_distance = float('inf')

    for player in Players:

        bottom_right = (player[2], player[3])
        bottom_left = (player[0], player[3])

        # Calculate Euclidean distance for the bottom right and left for each player
        bottom_right_distance = np.sqrt(((bottom_right[0] - BallCenter[0]) ** 2) + ((bottom_right[1] - BallCenter[1]) ** 2))
        bottom_left_distance = np.sqrt(((bottom_left[0] - BallCenter[0]) ** 2) + ((bottom_left[1] - BallCenter[1]) ** 2))

        # Update the minimum distance and get the team of the player he was the closest
        if bottom_right_distance < min_distance:  # Checking if the player's bottom right corner is closer to the ball.
            closest_point = bottom_right
            Player_color = player[4]
            min_distance = bottom_right_distance

        if bottom_left_distance < min_distance:  # Checking if the player's bottom left corner is closer to the ball.
            closest_point = bottom_left
            Player_color = player[4]
            min_distance = bottom_left_distance

    if Players and min_distance <= 70:  # Checking if there are players detected before drawing the line
        cv2.line(img, closest_point, BallCenter, color(Player_color), 3)
        if Player_color in team1:
            t1_counter, t2_counter, t1_total, t2_total, scoreboard = CalPossession(FPS, 1, t1_counter, t2_counter, img, t1_total, t2_total, teams_info, scoreboard)
        elif Player_color in team2:
            t1_counter, t2_counter, t1_total, t2_total, scoreboard = CalPossession(FPS, 2, t1_counter, t2_counter, img, t1_total, t2_total, teams_info, scoreboard)
    return t1_counter, t2_counter, t1_total, t2_total, scoreboard
