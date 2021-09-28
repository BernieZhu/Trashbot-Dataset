# Trashbot-Dataset

The annotation is in the csv format. Please use parse.py to parse the csv file.
```
python tools/parse_csv.py [--save_videos] [--HITId ID] > log.txt
--HITId ID: show annotations of specified HIT ID 
--save_videos: save the videos in folder videos when parsing
--vis_label: save the annotations of each video in srt format
```
Example:
```
python tools/parse_csv.py --HITId 308KJXFUK07J67W9762F6UYFDJNTAI --save_videos --vis_label 
cat all.log
Video: GH010299.mp4
Task ID: 308KJXFUK07J67W9762F6UYFDJNTAI
Low-quality: False
Rotated: False
|--Activity: 1
  |--Verb: open
  |--Object: refrigerator door
  |--Trial 1
    |--Start time: 0.6
    |--End time: 6.0
    |--Contact time: 3.5
    |--Successful: succ
|--Activity: 2
  |--Verb: take
  |--Object: paper cup
  |--Trial 1
    |--Start time: 10.2
    |--End time: 15.0
    |--Contact time: 10.6
    |--Successful: succ
|--Activity: 3
  |--Verb: close
  |--Object: refrigerator door
  |--Trial 1
    |--Start time: 20.3
    |--End time: 25.8
    |--Contact time: 21.0
    |--Successful: succ
```

If you find any problems with the annotations, please send me the Task IDs so I can reject the annotations (in a month) and re-publish the tasks (anytime).

# Annotation System
The interface might be useful to understand the structure of the annotations.  
Please check the annotation system at workersandbox.mturk.com, and search Trashbot-Temporal.  
It is a sandbox environment, where you can test the system and submit your results casually.  

# Trashbot Detector
I also have two models to detect the grabber and track two keypoints of the fingertip. Here are the video demos.  
Egocentric: https://youtu.be/B0zCNnd3Gec  
Vertical view: https://youtu.be/0xesy91Uplo  
The models and the datasets of these two are also available.  
