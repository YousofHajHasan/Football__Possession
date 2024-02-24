from ultralytics import YOLO
from Possession import *
from Drawing import *


PlayersModel = YOLO("Models/Players_Model/best.pt")
BallModel = YOLO("Models/Ball_Model2/best.pt")


cap = cv2.VideoCapture("Videos/BVB vs Bayern.mp4")
success, img = cap.read()

print("This is a default run. If you want to specify the video and the models, please adjust the run.py code.")

# Define some variables we need next
t1_counter = 0
t2_counter = 0
t1_total = 0
t2_total = 0
scoreboard = None

# TeamsInfo = get_teams_information(color("-", True))
TeamsInfo = {"Bayern": ["red", "green"], "Dortmund": ["yellow", "grey"], "Referee": ["black"]}  # Example input

Teams_name = list(TeamsInfo.keys())
Teams_color = get_teams_color(TeamsInfo)
colors_class = get_colors_class(TeamsInfo)
# Extract FPS value in the video
FPS = int(cap.get(cv2.CAP_PROP_FPS))
# Initialize the display image with the Scoreboard GUI
img = addScoreboard(create_possession_widget(0, 0, TeamsInfo), img)

while success:

    # Ball Model
    Prediction_img = img.copy()
    BallResults = BallModel(Prediction_img, stream=True, conf=0.4)
    BestBall = None

    for result in BallResults:
        # To extract the ball with the highest confidence in each frame.
        BallsConf = []
        boxes = result.boxes
        for box in boxes:
            confidence = box.conf.item()

            if BestBall is None or confidence > BestBall[0]:
                BestBall = (confidence, box)

        if BestBall:
            x1, y1, x2, y2 = BestBall[1].xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            Draw_ball(img, [x1, y1, x2, y2])
            BestBall = [x1+10, y1+20, x2-10, y2-20]

    # Players Model
    PlayerResults = PlayersModel(Prediction_img, stream=True, conf=0.45, iou=0.5)
    for result in PlayerResults:
        boxes = result.boxes
        PlayersInfo = []  # To store the team of each player
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # Each Player Image will be masked to be classified
            if box.cls == 1:  # Detect the players Only
                # Potential Error:
                if y1 >= y2-40 or x1 >= x2-5:
                    Cropped_img = Prediction_img[y1:y2, x1:x2]  # The value (40) is adjustable depending on the player's bounding box size
                else:
                    Cropped_img = Prediction_img[y1:y2-40, x1:x2-5]  # This makes the classification depend on the color of the shirt
                    # I exclude the shorts worn by the player

                Player_class = classify_class(Cropped_img, Teams_color)

                DrawPlayersRectangle(img, Player_class, [x1, y1, x2, y2], colors_class)

                if Player_class not in TeamsInfo[Teams_name[2]]:  # Exclude the referee class 'For possession calculation'
                    PlayersInfo.append([x1, y1, x2, y2, Player_class])

        if BestBall:  # if the ball is detected
            t1_counter, t2_counter, t1_total, t2_total, scoreboard = CalculateDistance(BestBall,
                                                                                       PlayersInfo,
                                                                                       TeamsInfo, img, FPS, t1_counter,
                                                                                       t2_counter, t1_total, t2_total,
                                                                                       scoreboard)
        if scoreboard is None:
            img = addScoreboard(create_possession_widget(0, 0, TeamsInfo), img)
        else:
            img = addScoreboard(scoreboard, img)

    # Display Frame
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    # out.write(img)
    success, img = cap.read()

# Print Final Possession
cv2.imshow("Final Result", scoreboard)
cap.release()
# out.release()
cv2.destroyAllWindows()

