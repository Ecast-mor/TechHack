import cv2
import mediapipe as mp
import time
import os
import math
import numpy as np
import queue
import pygame



def run_vision(target_queue, result_queue, frame_queue):

   
    aslDict = {"A": {
            4:  {'x': 0.728, 'y': -0.950, 'z': -0.146}, 
            8:  {'x': 0.377, 'y': -0.371, 'z': -0.232}, 
            12: {'x': 0.199, 'y': -0.319, 'z': -0.142}, 
            16: {'x': 0.073, 'y': -0.358, 'z': -0.072}, 
            20: {'x': -0.023, 'y': -0.514, 'z': -0.040}, 
            "error_threshold": 1.3
        }, "B": {
            4:  {'x': 0.055, 'y': -0.777, 'z': -0.272}, 
            8:  {'x': 0.256, 'y': -1.738, 'z': -0.320},
            12: {'x': 0.136, 'y': -1.885, 'z': -0.340}, 
            16: {'x': -0.014, 'y': -1.724, 'z': -0.363}, 
            20: {'x': -0.150, 'y': -1.422, 'z': -0.378}, 
            "error_threshold": 1.4
        }, "C": {
            4:  {'x': 0.876, 'y': -0.678, 'z': -0.138}, 
            8:  {'x': 0.852, 'y': -1.165, 'z': -0.142}, 
            12: {'x': 0.778, 'y': -1.252, 'z': -0.221}, 
            16: {'x': 0.730, 'y': -1.262, 'z': -0.247}, 
            20: {'x': 0.618, 'y': -1.292, 'z': -0.298},
            "error_threshold": 1.6
        }, "D": {
            4:  {'x': 0.875, 'y': -0.581, 'z': 0.054},  
            8:  {'x': 0.516, 'y': -1.688, 'z': 0.145}, 
            12: {'x': 0.842, 'y': -0.663, 'z': -0.098}, 
            16: {'x': 0.813, 'y': -0.617, 'z': -0.126}, 
            20: {'x': 0.776, 'y': -0.725, 'z': -0.195},
            "error_threshold": 2.6  ### FIX THIS BASED ON TESTING 
        }, "E": {
            4:  {'x': 0.231, 'y': -0.818, 'z': -0.222}, 
            8:  {'x': 0.395, 'y': -0.902, 'z': -0.264},
            12: {'x': 0.263, 'y': -0.957, 'z': -0.221}, 
            16: {'x': 0.134, 'y': -0.958, 'z': -0.181}, 
            20: {'x': -0.003, 'y': -0.985, 'z': -0.207},
            "error_threshold": 1.45
        }, "F": {
            4:  {'x': 0.278, 'y': -0.733, 'z': -0.434}, 
            8:  {'x': 0.214, 'y': -0.775, 'z': -0.482}, 
            12: {'x': 0.095, 'y': -1.819, 'z': -0.321}, 
            16: {'x': -0.111, 'y': -1.730, 'z': -0.307}, 
            20: {'x': -0.399, 'y': -1.433, 'z': -0.256},
            "error_threshold": 1.5 
        }, "G": {
            4:  {'x': 1.198, 'y': -1.465, 'z': -0.290}, 
            8:  {'x': 1.583, 'y': -1.275, 'z': -0.588}, 
            12: {'x': 0.856, 'y': -0.724, 'z': -0.486}, 
            16: {'x': 0.817, 'y': -0.396, 'z': -0.379}, 
            20: {'x': 0.795, 'y': -0.088, 'z': -0.468},
            'error_threshold': 2.5   ## FIX THIS BASED ON TESTING
        }, "H": {
            4:  {'x': 1.134, 'y': -0.548, 'z': 0.198}, 
            8:  {'x': 1.732, 'y': -0.767, 'z': 0.024}, 
            12: {'x': 1.869, 'y': -0.553, 'z': -0.037}, 
            16: {'x': 0.985, 'y': -0.228, 'z': 0.046}, 
            20: {'x': 0.923, 'y': 0.016, 'z': 0.093},
                "error_threshold": 1.9 ## Fix this based on testing
        }, "I": {
            4:  {'x': 0.191, 'y': -1.146, 'z': -0.222}, 
            8:  {'x': 0.340, 'y': -0.866, 'z': -0.218}, 
            12: {'x': 0.198, 'y': -0.748, 'z': -0.225}, 
            16: {'x': 0.057, 'y': -0.621, 'z': -0.166}, 
            20: {'x': -0.155, 'y': -1.611, 'z': -0.125},
            "error_threshold": 2.2

        }, "K": {
            4:  {'x': 0.375, 'y': -1.276, 'z': -0.010}, 
            8:  {'x': 0.475, 'y': -2.175, 'z': -0.297}, 
            12: {'x': 0.888, 'y': -1.926, 'z': -0.282}, 
            16: {'x': 0.481, 'y': -0.915, 'z': -0.106}, 
            20: {'x': 0.561, 'y': -0.682, 'z': -0.043},
            "error_threshold": 2.2 # rerecord this and adjust based on testing
        }, "L": {
            4:  {'x': 0.991, 'y': -0.523, 'z': -0.380}, 
            8:  {'x': 0.463, 'y': -1.865, 'z': -0.339}, 
            12: {'x': 0.258, 'y': -0.485, 'z': -0.266}, 
            16: {'x': 0.098, 'y': -0.457, 'z': -0.198}, 
            20: {'x': -0.046, 'y': -0.506, 'z': -0.165},
            "error_threshold": 1.4
        }, "M": {
            4:  {'x': 0.018, 'y': -0.984, 'z': -0.301}, 
            8:  {'x': 0.407, 'y': -0.482, 'z': -0.423}, 
            12: {'x': 0.288, 'y': -0.499, 'z': -0.318}, 
            16: {'x': 0.106, 'y': -0.597, 'z': -0.210}, 
            20: {'x': -0.138, 'y': -0.589, 'z': -0.237},
            "error_threshold": 1.4

        }, "N": {
            4:  {'x': 0.070, 'y': -1.130, 'z': -0.215}, 
            8:  {'x': 0.365, 'y': -0.660, 'z': -0.330}, 
            12: {'x': 0.250, 'y': -0.710, 'z': -0.265}, 
            16: {'x': 0.095, 'y': -0.510, 'z': -0.185}, 
            20: {'x': -0.040, 'y': -0.520, 'z': -0.170},
            "error_threshold": 1.4
        }, "O": {
            4:  {'x': 0.741, 'y': -0.753, 'z': 0.078}, 
            8:  {'x': 0.661, 'y': -0.990, 'z': 0.105}, 
            12: {'x': 0.674, 'y': -0.995, 'z': 0.005}, 
            16: {'x': 0.661, 'y': -0.935, 'z': -0.088}, 
            20: {'x': 0.598, 'y': -0.865, 'z': -0.158},
            "error_threshold": 1.4  
        }, "P": {
            4:  {'x': 0.771, 'y': -0.730, 'z': -0.345}, 
            8:  {'x': 1.150, 'y': -0.801, 'z': -0.575}, 
            12: {'x': 0.950, 'y': -0.098, 'z': -0.505}, 
            16: {'x': 0.405, 'y': -0.125, 'z': -0.325}, 
            20: {'x': 0.355, 'y': -0.055, 'z': -0.470},
            "error_threshold": 2.3 
        }, "Q": {
            4:  {'x': 1.125, 'y': -0.320, 'z': -0.125}, 
            8:  {'x': 1.285, 'y': -0.560, 'z': -0.230}, 
            12: {'x': 0.665, 'y': -0.340, 'z': -0.270}, 
            16: {'x': 0.580, 'y': -0.220, 'z': -0.230}, 
            20: {'x': 0.535, 'y': -0.140, 'z': -0.295},
            "error_threshold": 2.0
        }, "R": {
            4:  {'x': 0.193, 'y': -0.895, 'z': -0.332}, 
            8:  {'x': 0.191, 'y': -1.716, 'z': -0.336}, 
            12: {'x': 0.174, 'y': -1.920, 'z': -0.338}, 
            16: {'x': 0.106, 'y': -0.609, 'z': -0.298}, 
            20: {'x': 0.006, 'y': -0.486, 'z': -0.294},
            "error_threshold": 1.6
        }, "S": {
            4:  {'x': 0.432, 'y': -1.055, 'z': -0.225}, 
            8:  {'x': 0.315, 'y': -0.785, 'z': -0.160}, 
            12: {'x': 0.155, 'y': -0.772, 'z': -0.036}, 
            16: {'x': 0.016, 'y': -0.760, 'z': 0.040},  
            20: {'x': -0.110, 'y': -0.810, 'z': 0.018},
            "error_threshold": 1.5
        }, "T": {
            4:  {'x': 0.457, 'y': -1.144, 'z': -0.155}, 
            8:  {'x': 0.443, 'y': -0.771, 'z': -0.264}, 
            12: {'x': 0.229, 'y': -0.457, 'z': -0.203}, 
            16: {'x': 0.081, 'y': -0.392, 'z': -0.123}, 
            20: {'x': -0.035, 'y': -0.521, 'z': -0.117},
            "error_threshold": 1.7
        }, "U": {
            4:  {'x': 0.111, 'y': -0.672, 'z': -0.395}, 
            8:  {'x': 0.434, 'y': -1.803, 'z': -0.396}, 
            12: {'x': 0.350, 'y': -1.990, 'z': -0.423}, 
            16: {'x': 0.108, 'y': -0.513, 'z': -0.399},
            20: {'x': 0.027, 'y': -0.427, 'z': -0.356},
            "error_threshold": 1.5
        }, "V": {
            4:  {'x': 0.007, 'y': -0.826, 'z': -0.366}, 
            8:  {'x': 0.274, 'y': -1.869, 'z': -0.334}, 
            12: {'x': -0.264, 'y': -1.839, 'z': -0.355}, 
            16: {'x': 0.008, 'y': -0.523, 'z': -0.309}, 
            20: {'x': -0.076, 'y': -0.380, 'z': -0.294}, 
            "error_threshold": 1.6
        }, "W": {
            4:  {'x': 0.046, 'y': -0.588, 'z': -0.347}, 
            8:  {'x': 0.606, 'y': -1.755, 'z': -0.367}, 
            12: {'x': 0.174, 'y': -2.007, 'z': -0.400}, 
            16: {'x': -0.201, 'y': -1.716, 'z': -0.521},
            20: {'x': -0.041, 'y': -0.496, 'z': -0.419},
            "error_threshold": 1.75
        }, "X": {
            4:  {'x': 0.366, 'y': -0.669, 'z': -0.524}, 
            8:  {'x': 0.603, 'y': -1.364, 'z': -0.421}, 
            12: {'x': 0.316, 'y': -0.622, 'z': -0.198}, 
            16: {'x': 0.124, 'y': -0.650, 'z': -0.101}, 
            20: {'x': -0.038, 'y': -0.733, 'z': -0.169},
            "error_threshold": 1.7 # fix maybe?
        }, "Y": {
            4:  {'x': 0.571, 'y': -1.315, 'z': -0.198}, 
            8:  {'x': 0.183, 'y': -0.662, 'z': -0.238}, 
            12: {'x': 0.081, 'y': -0.476, 'z': -0.266}, 
            16: {'x': -0.071, 'y': -0.497, 'z': -0.196}, 
            20: {'x': -0.789, 'y': -1.418, 'z': -0.217},
            "error_threshold": 1.8

        }
    }

    j_buffer = []
    z_buffer = []
    MAX_BUFFER_SIZE = 30 # Tracks about 1 second of motion

    def detect_J_motion(current_pinky_pos):
        """
        Tracks pinky for a 'hook' shape.
        J starts as an 'I' shape moving down, then curving up/left.
        """
        j_buffer.append(current_pinky_pos)
        if len(j_buffer) > MAX_BUFFER_SIZE:
            j_buffer.pop(0)
        
        if len(j_buffer) < 10: return False
        
        # Logic: Start of buffer should be higher (lower y) than the middle.
        # End of buffer should be moving left (assuming mirrored, x decreases).
        start_y = j_buffer[0][1]
        lowest_p = max(j_buffer, key=lambda p: p[1]) # Screen y-down
        end_x = j_buffer[-1][0]
        
        # If pinky dropped significantly then hooked left
        if (lowest_p[1] - start_y > 0.1) and (j_buffer[-1][0] < lowest_p[0] - 0.05):
            j_buffer.clear() # Reset after success
            return True
        return False

    def detect_Z_motion(current_index_pos):
        """
        Tracks index for a zig-zag shape.
        Z moves: Right -> Diagonal Down-Left -> Right.
        """
        z_buffer.append(current_index_pos)
        if len(z_buffer) > MAX_BUFFER_SIZE:
            z_buffer.pop(0)

        if len(z_buffer) < 15: return False

        # Logic: Divide buffer into 3 parts to check the Z segments
        # Part 1: Moving Right (+x)
        # Part 2: Moving Down-Left (+y, -x)
        # Part 3: Moving Right (+x)
        # This is a simplified check for the 'feel' of a Z
        if z_buffer[-1][0] > z_buffer[0][0] + 0.1: # Moved overall right
            # Check if we dipped in the middle (the diagonal)
            mid_p = z_buffer[len(z_buffer)//2]
            if mid_p[1] > z_buffer[0][1] + 0.05:
                z_buffer.clear()
                return True
        return False


    def checkSign (asl_sign, current_rel_tips, hand):
        target_sign = asl_sign

        if target_sign == "J":
            # J uses the Pinky Tip (Landmark 20)
            pinky = (hand[20].x, hand[20].y)
            if detect_J_motion(pinky):
                return True
            return # Exit 

        if target_sign == "Z":
            # Z uses the Index Tip (Landmark 8)
            index = (hand[8].x, hand[8].y)
            if detect_Z_motion(index):
                return True
            return # Exit 


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
        error_threshold = aslDict[target_sign]["error_threshold"]  

        if total_error < error_threshold:
            print(f"Sign '{target_sign}' detected with total error: {total_error:.3f}")
            return True
        else:
            print(f"Total error for '{target_sign}': {total_error:.3f} (threshold: {error_threshold})")
            return False

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
        
        print("Camera started.")

        
        target_sign = None
        counter = 0
        waiting_for_new_target = False

        while cap.isOpened():
            try:
                target_sign = target_queue.get_nowait()
                counter = 0  # Reset counter for the new letter
                waiting_for_new_target = False
            except queue.Empty:
                pass    


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
            if result.hand_landmarks and not waiting_for_new_target and target_sign is not None:
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



                    ## 1. Create a dictionary of the current relative fingertip positions
                    current_rel_tips = {
                        4: {'x': rel_thumb_x, 'y': rel_thumb_y, 'z': rel_thumb_z},
                        8: {'x': rel_index_x, 'y': rel_index_y, 'z': rel_index_z},
                        12: {'x': rel_middle_x, 'y': rel_middle_y, 'z': rel_middle_z},
                        16: {'x': rel_ring_x, 'y': rel_ring_y, 'z': rel_ring_z},
                        20: {'x': rel_pinky_x, 'y': rel_pinky_y, 'z': rel_pinky_z}
                        }

                    # 2. Calculate the Euclidean distance for all 5 fingertips
                    is_sign_detected = checkSign(target_sign, current_rel_tips, hand)

                    if is_sign_detected:
                        if target_sign in ["J", "Z"]:
                            counter += 10
                        else:
                            counter += 1
                    else:
                        counter = 0

                    if counter >= 5:
                        print(f"Success '{target_sign}' Detected! Passing to Pygames")
                        result_queue.put(target_sign)
                        waiting_for_new_target = True
                        counter = 0              

                    '''
                    print(f"Relative Index Tip: ({rel_index_x:.3f}, {rel_index_y:.3f}, {rel_index_z:.3f})")
                    print(f"Relative Middle Tip: ({rel_middle_x:.3f}, {rel_middle_y:.3f}, {rel_middle_z:.3f})")
                    print(f"Relative Ring Tip: ({rel_ring_x:.3f}, {rel_ring_y:.3f}, {rel_ring_z:.3f})")
                    print(f"Relative Pinky Tip: ({rel_pinky_x:.3f}, {rel_pinky_y:.3f}, {rel_pinky_z:.3f})")
                    print(f"Relative Thumb Tip: ({rel_thumb_x:.3f}, {rel_thumb_y:.3f}, {rel_thumb_z:.3f})")
                    '''

                    
            small_frame = cv2.resize(rgb_frame, (320, 240))
            pygame_frame = np.swapaxes(small_frame, 0, 1)
            pygame_surface = pygame.surfarray.make_surface(pygame_frame) 

            pygame_surface = pygame.surfarray.make_surface(pygame_frame)
            # Clear the queue if it's getting full before putting the new frame
            if frame_queue.full():
                try:
                    frame_queue.get_nowait()
                except queue.Empty:
                    pass
            
            # We use put_nowait to prevent the vision thread from freezing if Pygame is slow
            try:
                frame_queue.put_nowait(pygame_surface)
            except queue.Full:
                pass


    cap.release()
    