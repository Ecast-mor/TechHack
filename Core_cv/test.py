import cv2
import mediapipe as mp
import time
import os
import math

   
aslDict = {"A": {
        4:  {'x': 0.728, 'y': -0.950, 'z': -0.146}, # Thumb
        8:  {'x': 0.377, 'y': -0.371, 'z': -0.232}, # Index
        12: {'x': 0.199, 'y': -0.319, 'z': -0.142}, # Middle
        16: {'x': 0.073, 'y': -0.358, 'z': -0.072}, # Ring
        20: {'x': -0.023, 'y': -0.514, 'z': -0.040} # Pinky
    }, "B": {
        4:  {'x': 0.055, 'y': -0.777, 'z': -0.272}, # Thumb
        8:  {'x': 0.256, 'y': -1.738, 'z': -0.320}, # Index
        12: {'x': 0.136, 'y': -1.885, 'z': -0.340}, # Middle
        16: {'x': -0.014, 'y': -1.724, 'z': -0.363}, # Ring
        20: {'x': -0.150, 'y': -1.422, 'z': -0.378}  # Pinky
    }, "C": {
        4:  {'x': 0.876, 'y': -0.678, 'z': -0.138}, # Thumb
        8:  {'x': 0.852, 'y': -1.165, 'z': -0.142}, # Index
        12: {'x': 0.778, 'y': -1.252, 'z': -0.221}, # Middle
        16: {'x': 0.730, 'y': -1.262, 'z': -0.247}, # Ring
        20: {'x': 0.618, 'y': -1.292, 'z': -0.298}  # Pinky
    }, "D": {
        4:  {'x': 0.875, 'y': -0.581, 'z': 0.054},  # Thumb
        8:  {'x': 0.516, 'y': -1.688, 'z': 0.145},  # Index
        12: {'x': 0.842, 'y': -0.663, 'z': -0.098}, # Middle
        16: {'x': 0.813, 'y': -0.617, 'z': -0.126}, # Ring
        20: {'x': 0.776, 'y': -0.725, 'z': -0.195}  # Pinky
    }, "E": {
        4:  {'x': 0.231, 'y': -0.818, 'z': -0.222}, # Thumb
        8:  {'x': 0.395, 'y': -0.902, 'z': -0.264}, # Index
        12: {'x': 0.263, 'y': -0.957, 'z': -0.221}, # Middle
        16: {'x': 0.134, 'y': -0.958, 'z': -0.181}, # Ring
        20: {'x': -0.003, 'y': -0.985, 'z': -0.207} # Pinky
    }, "F": {
        4:  {'x': 0.278, 'y': -0.733, 'z': -0.434}, # Thumb
        8:  {'x': 0.214, 'y': -0.775, 'z': -0.482}, # Index
        12: {'x': 0.095, 'y': -1.819, 'z': -0.321}, # Middle
        16: {'x': -0.111, 'y': -1.730, 'z': -0.307}, # Ring
        20: {'x': -0.399, 'y': -1.433, 'z': -0.256}  # Pinky
    }

}

def checkSign (asl_sign, current_rel_tips):
    target_sign = asl_sign
    total_error = 0

    

    # 1. Calculate the Euclidean distance for all 5 fingertips
    for tip_id in [4, 8, 12, 16, 20]:
        dict_x = aslDict[target_sign][tip_id]['x']
        dict_y = aslDict[target_sign][tip_id]['y']
        dict_z = aslDict[target_sign][tip_id]['z']  
        
        curr_x = current_rel_tips[tip_id]['x']
        curr_y = current_rel_tips[tip_id]['y']
        curr_z = current_rel_tips[tip_id]['z']
        
        # Distance formula: sqrt((x2 - x1)^2 + (y2 - y1)^2 + (z2 - z1)^2)
        distance = math.sqrt((curr_x - dict_x)**2 + (curr_y - dict_y)**2 + (curr_z - dict_z)**2)
        total_error += distance

    # 2. Check against your threshold
    error_threshold = 1.50  # may need to adjust this based on testing

    if total_error < error_threshold:
        print(f"ASL '{target_sign}' Detected! (Error score: {total_error:.3f})")
    else:
        print(f"Not an '{target_sign}'. (Error score: {total_error:.3f})")

# 1. Setup the new Tasks API classes
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
model_path = os.path.join(os.path.dirname(__file__), 'hand_landmarker.task')

# 2. Configure the options
# The hand_landmarker.task file MUST be in the same folder as this script
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1)

# 3. Initialize the Landmarker
with HandLandmarker.create_from_options(options) as landmarker:
    cap = cv2.VideoCapture(0)
    
    print("Press 'q' to quit.")
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
            
        # Flip frame for a mirror-like view and convert to RGB
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to MediaPipe Image object (required by the new API)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Calculate timestamp (required for VIDEO mode)
        timestamp_ms = int(time.time() * 1000)
        
        # Detect landmarks
        result = landmarker.detect_for_video(mp_image, timestamp_ms)
        
        # If hands are detected, extract the coordinates
        if result.hand_landmarks:
            for i, hand in enumerate(result.hand_landmarks):

                hand_label = result.handedness[i][0].category_name  # "Left" or "Right"


                wrist = hand[0]
                middle_mcp = hand[9]  # Middle Finger MCP joint (base of the middle finger)

                index_tip = hand[8]
                middle_tip = hand[12]
                ring_tip = hand[16]
                pinky_tip = hand[20]
                thumb_tip = hand[4]
                
                ref_dist = math.sqrt((middle_mcp.x - wrist.x)**2 + (middle_mcp.y - wrist.y)**2 + (middle_mcp.z - wrist.z)**2)

                if ref_dist == 0:
                    ref_dist = 1e-6

                flip_mult = -1 if hand_label == "Left" else 1

                # (Current X - Wrist X) / Ruler * Flip
                rel_index_x = ((index_tip.x - wrist.x) / ref_dist) * flip_mult
                rel_index_y = ((index_tip.y - wrist.y) / ref_dist) 
                rel_index_z = (index_tip.z - wrist.z) / ref_dist 

                
                rel_middle_x = ((middle_tip.x - wrist.x) / ref_dist) * flip_mult
                rel_middle_y = ((middle_tip.y - wrist.y) / ref_dist) 
                rel_middle_z = (middle_tip.z - wrist.z) / ref_dist 

                
                rel_ring_x = ((ring_tip.x - wrist.x) / ref_dist) * flip_mult
                rel_ring_y = (ring_tip.y - wrist.y) / ref_dist 
                rel_ring_z = (ring_tip.z - wrist.z) / ref_dist 
                
                rel_pinky_x = ((pinky_tip.x - wrist.x) / ref_dist) * flip_mult
                rel_pinky_y = (pinky_tip.y - wrist.y) / ref_dist 
                rel_pinky_z = (pinky_tip.z - wrist.z) / ref_dist 
                
                rel_thumb_x = ((thumb_tip.x - wrist.x) / ref_dist) * flip_mult
                rel_thumb_y = (thumb_tip.y - wrist.y) / ref_dist 
                rel_thumb_z = (thumb_tip.z - wrist.z) / ref_dist 


                target_sign = "F"

                ## 1. Create a dictionary of the current relative fingertip positions
                current_rel_tips = {
                    4: {'x': rel_thumb_x, 'y': rel_thumb_y, 'z': rel_thumb_z},
                    8: {'x': rel_index_x, 'y': rel_index_y, 'z': rel_index_z},
                    12: {'x': rel_middle_x, 'y': rel_middle_y, 'z': rel_middle_z},
                    16: {'x': rel_ring_x, 'y': rel_ring_y, 'z': rel_ring_z},
                    20: {'x': rel_pinky_x, 'y': rel_pinky_y, 'z': rel_pinky_z}
                    }

                # 2. Calculate the Euclidean distance for all 5 fingertips
                checkSign(target_sign, current_rel_tips)

                ''' 
                print(f"Relative Index Tip: ({rel_index_x:.3f}, {rel_index_y:.3f}, {rel_index_z:.3f})")
                print(f"Relative Middle Tip: ({rel_middle_x:.3f}, {rel_middle_y:.3f}, {rel_middle_z:.3f})")
                print(f"Relative Ring Tip: ({rel_ring_x:.3f}, {rel_ring_y:.3f}, {rel_ring_z:.3f})")
                print(f"Relative Pinky Tip: ({rel_pinky_x:.3f}, {rel_pinky_y:.3f}, {rel_pinky_z:.3f})")
                print(f"Relative Thumb Tip: ({rel_thumb_x:.3f}, {rel_thumb_y:.3f}, {rel_thumb_z:.3f})")
                '''
                


  


                
                # Get the pixel dimensions of your webcam frame
                h, w, c = frame.shape
                




                
        # Show the video feed
        cv2.imshow('Modern MediaPipe Demo', frame)
        
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()