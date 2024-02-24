# **From Watching to Analyzing: Football Matches Possession with YOLOv8**


## **Description**
This project outlines my journey of fine-tuning the **YOLOv8** model to detect players in different football matches and categorize them into two teams to calculate the final **possession** result.
**Check out Tryolabs' helpful [blog](https://tryolabs.com/blog/2022/10/17/measuring-soccer-ball-possession-ai-video-analytics), which really helped me understand some key concepts and ideas for my project.** 

# Project's Output Sample
<p align="center">
   <img src="https://github.com/YousofHajHasan/Football_Possession/assets/161046637/c94584f8-54ad-4466-a26a-842a11e54abd" alt="Sample" width="600"/>
</p>

<p align="center">
    
</p>

## Installation Notes
An environment with a GPU can provide significantly faster processing.

**Don't forget to run pip install requirements.txt file**

## Table of Contents

* [Datasets](#datasets)
    * [Datasets links](#datasets-links)
    * [Players Dataset](#players-dataset)
    * [Ball Dataset](#ball-dataset)
* [Models](#models)
    * [All Models Weights](#all-models-weights)
* [Calculating Ball Possession](#calculating-ball-possession)
    * [Classify the Players](#classify-players)
    * [Hsv Filtering](#HSV)
    * [calculate distance and possession](#calculate-distance)
* [Final Results and A Few Notes to Consider](#final-results-and-a-few-notes-to-consider)


## **Datasets** <a id="datasets"></a>
For this project, I've created two different datasets. 
The first is for detecting the players, and the other is for detecting the ball.

### Datasets links <a id="datasets-links"></a> 

| Dataset  | # Images | Classes|
| ------------- | :-------------: | :-------------:|
| [Players and Ball Dataset](https://universe.roboflow.com/yousof-hajhasan-ndywi/full-players-data/dataset/3) | **1920** | Players Referee Keeper and Ball **-4 Classes-**
| [Ball Dataset **with** Augmentation](https://universe.roboflow.com/yousof-hajhasan-ndywi/football-detection-dataset/dataset/1) | **1770** | Ball-only **-1 class-**
| [Ball Dataset **without** Augmentation](https://universe.roboflow.com/yousof-hajhasan-ndywi/football-detection-dataset/dataset/2) | **650** | Ball-only **-1 class-**


**_Here is a brief explanation for each of these two datasets:_**

### **Players Dataset** <a id="players-dataset"></a>

<p align="center">
   <img src="https://github.com/YousofHajHasan/Football_Possession/assets/161046637/44d2b083-63d7-4c66-9952-52afcb7dd7c0" alt="Players" width="500"/> 
</p>

This dataset was imported from [Roboflow](https://roboflow.com/) website and then adjusted by adding some manually annotated images, and I am particularly grateful to my friends for their generous support in annotating these images.

This data contains **718** images in basic form, annotated for three classes: Ball, Player, goal Keeper, and Referee. For the final data version, I've combined the Referee, Keeper and the players into one class and done some augmentation techniques, such as hue and brightness adjustment, to get **1920** images in total resized to **640x640**.

Note: At the detecting phase I didn't use the Ball class using this dataset, due to its poor accuracy in detecting the ball, and I will introduce the ball-only dataset in the next section. So I only used the Players class from this dataset. 

### Ball Dataset <a id="ball-dataset"></a>


<p align="center">
   <img src="https://github.com/YousofHajHasan/Football_Possession/assets/161046637/865e4338-7508-4ff0-9797-5b138484fe42" alt="Ball" width="500"/> 
</p>


As the Players+Ball dataset performed poorly in ball detection, I started creating data from scratch. First, I collected videos of various football matches and annotated them using [Roboflow](https://roboflow.com/). This generated two versions of the Ball Dataset: one without augmentation techniques and one with. Each version comprises 650 and 1,770 images, respectively.

You can notice that the ball bounding box is relatively big compared to the ball size. This is because when I tried to train the model on a smaller bounding box, it didn't perform well. so for some reason, the bigger box learns and trains the model better.



## **Models** <a id="models"></a>
After preparing the data, I began with a single model to detect both players and the ball. However, it underperformed in detecting the ball. One potential reason could be the data class imbalance. Some images have significantly more annotations for the "Players" class compared to the ball class, leading the model to prioritize learning player detection and ignoring the ball class.

**My final work was as follows:**
### All Models Weights <a id="all-models-weights"></a>
| Model used Classes | Overfitting | Accuracy |
| --------------- | :-------------: | :-------------: |
| Players Model | Not overfitting the train data, can be used for any football match | Accurate in detecting the Players
| Ball Model **1** | Overfitted the train data, can be used to test the possession calculating technique | Perfectly detect the ball in the train data, but performing poorly on unseen data
| Ball Model **2** | Not overfitted, can be used for any match | May have lower accuracy on the training data, but it would be more generalized and applicable to any football matches.

These model were trained using the code on the file **Train the model.py**.

**Note:** The general ball model was trained on the [not augmented dataset](https://universe.roboflow.com/yousof-hajhasan-ndywi/football-detection-dataset/dataset/2), with freezing the first 8 layers of the Yolov8x version with 64 as the batch size.


## **Calculating Ball Possession** <a id="calculating-ball-possession"></a>
As you can see in the main.py file. I start with detecting only one ball in each frame, **'The ball with the highest confidence.'** Then, I use this ball in possession calculation.  

Calculating the ball possession was divided into two steps: 

**1-** Identifying the detected player class.

**2-** Determining the player that has the ball.

I will discuss these two steps further in the next sections.

### **Classify the Players** <a id="classify-players"></a>

**1. Find the player:**

I used the fine-tuned player model to find the players bounding boxes in the image.

**2. Focus on the shirt:**

I cropped the player image to get only the player's shirt

**3. Identify the shirt:**

Using the "classify_class" function, I got the player's team based on the HSV Filtering technique.

### **Hsv Filtering**: <a id="HSV"></a>

You can find the method to determine the thresholds for HSV filtering by running the **"HSV Filtering.py"** file.

You can find the values of the Hue Saturation Value of colors at the **"retrieve_color_values"** function in the **"Mask.py"** file.

### **Calculate distance and possession** <a id="calculate-distance"></a>
**- You can find the method to calculate the distance in Possession.py file**

#### Determining the team that has the ball

Now, I have the players and ball bounding boxes, so I need to start by calculating the distance between the bottom corners of the players and the center of the ball based on a specific threshold. The closest player to the ball will be classified as the player with the ball. 

**_For the next calculations, see the implementation of the CalPossession function in Possession.py file_** 

#### **My method is a points-based system to track possession over time.**



**Scenario:** (Team 1) has 7 points, and (Team 2) has 3 points.

**Calculation:**

Total Points = 7 + 3 = 10

Team 1 Possession = (7 / 10) * 100% = 70%

Team 2 Possession = (3 / 10) * 100% = 30%

### Now, How are the teams awarded points?


A team receives a point for every half-second (FPS/2) they maintain control of the ball without being intercepted.

The **interception** must be at least a quarter of a second (FPS/4) to be considered interception. 


## **Final Results and A Few Notes to Consider** <a id="final-results-and-a-few-notes-to-consider"></a>

### Some Notes To Be Considered

* I have created a simple scoreboard that appears on the top left of the video as you can see in the sample video. That has the possession percentage of the teams with colors representing their shirt color.

* I've added some videos for testing the model.

* The run.py file requires input based on the teams in your video. To see a sample output, there's a default input commented in the run.py file. Don't forget to adjust it if needed.

* Don't Forget to specify the model you want to use in the detection.

* All training and testing were performed locally on an NVIDIA RTX 2070 GPU utilizing PyTorch.

### Potential areas for improvement in the project

* Since there are some problems in ball detection accuracy, I think that making more Hyperparameter tuning will help in increasing the model accuracy, That is because I tried Roboflow API for training and I got amazing results.

* To effectively evaluate the capabilities of this project, I would require a video with a consistent camera angle throughout the entire 90 minutes. Additionally, the video should be pre-processed to exclude scenarios that the model isn't designed to handle, such as goal kicks, corner kicks, and throw-ins.

* I welcome any feedback or suggestions you may have regarding errors, bugs, or challenges encountered while using this project. As this is my first repository, your insights are highly appreciated.
