import cv2
import numpy as np
from ultralytics import YOLO
from collections import defaultdict
from CentroidTracker import CentroidTracker
import config

def calculate_weight(distance, max_distance=config.WEIGHT_MAX_DISTANCE, min_weight=config.WEIGHT_MIN, max_weight=config.WEIGHT_MAX):
    weight = max_weight - ((distance / max_distance) * (max_weight - min_weight))
    return max(min_weight, min(weight, max_weight))

def smooth_activity_score(activity_scores, window_size=config.SMOOTHING_WINDOW_SIZE):
    if len(activity_scores) == 0:
        return 0  # Return a default value when no data points are available
    if len(activity_scores) < window_size:
        return np.mean(activity_scores)  # Average the available scores if less than window size
    return np.mean(activity_scores[-window_size:])

def is_point_in_trapezoid(point, vertices):
    contour = np.array(vertices, dtype=np.int32)
    return cv2.pointPolygonTest(contour, point, False) >= 0

def calculate_angle(vector1, vector2):
    unit_vector1 = vector1 / np.linalg.norm(vector1)
    unit_vector2 = vector2 / np.linalg.norm(vector2)
    dot_product = np.dot(unit_vector1, unit_vector2)
    angle = np.arccos(dot_product)
    return np.degrees(angle)


def calculate_activity(tracker, previous_positions, frame, activity_scores, direction_scores):
    activity_score = 0
    direction_score = 0
    current_positions = tracker.objects
    static_point = np.array(config.STATIC_POINT)
    print("Current positions:", current_positions)
    print("Previous positions:", previous_positions)
    for object_id, position in current_positions.items():
        position_tuple = tuple(map(int, position))  # Convert to a tuple of integers
        if is_point_in_trapezoid(position_tuple, config.TRAPEZOID_VERTICES):
            if object_id in previous_positions:
                previous_position = previous_positions[object_id]
                movement_vector = position - previous_position
                direction_vector = static_point - position
                distance = np.linalg.norm(movement_vector)
                weight = calculate_weight(np.linalg.norm(position - static_point))

                # Calculate angle and direction-based score
                angle = calculate_angle(movement_vector, direction_vector)
                direction_weight = 1 if angle < config.ATTRACTION_ANGLE else 0  #range that object can move towards centroid and still be considered moving towards centroid. 
                direction_score += distance * direction_weight
                activity_score += distance * weight * direction_weight
                tracker.update_activity_score(object_id, activity_score)
                print(f"Object ID {object_id} moved {distance:.2f} pixels with weight {weight:.2f} and direction weight {direction_weight:.2f} and score is {activity_score:.2f} and direction score is {direction_score:.2f}")
                
                cv2.line(frame, tuple(previous_position), position_tuple, config.LINE_COLOR, config.LINE_THICKNESS)
    
    activity_scores.append(activity_score)
    direction_scores.append(direction_score)
    
    smoothed_activity_score = smooth_activity_score(activity_scores)
    smoothed_direction_score = smooth_activity_score(direction_scores)
    
    return smoothed_activity_score, smoothed_direction_score, current_positions



def main():
    # Load YOLOv8 model
    model = YOLO(config.YOLO_MODEL_PATH)

    # Initialize video capture
    cap = cv2.VideoCapture(config.VIDEO_SOURCE)
    
    # Initialize centroid tracker
    tracker = CentroidTracker()
    previous_positions = {}

    # Initialize activity score history
    activity_scores = []
    direction_scores = []

    # Initialize a VideoWriter object to export the output video
    if(config.RECORD_RESULT):
        out = cv2.VideoWriter('output.mp4', -1, 20.0, (1280, 720))  # adjust FPS and frame size as needed


    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Skip every other frame to process at 30fps
        # frame_count += 1
        # if frame_count % 2 != 0:
        #     continue
        
        # Resize frame to 720p
        frame = cv2.resize(frame, (1280, 720))

        # Draw static point
        cv2.circle(frame, config.STATIC_POINT, 10, (0, 255, 255), -1)  # Yellow point

        # Draw trapezoid area
        cv2.polylines(frame, [np.array(config.TRAPEZOID_VERTICES, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)

        # Detect persons using YOLOv8
        results = model(frame, verbose=False)
        detections = results[0].boxes.data.cpu().numpy()
        person_detections = [d for d in detections if int(d[5]) == 0]  # Filter for person class (class ID 0)
        rects = [(int(d[0]), int(d[1]), int(d[2]), int(d[3])) for d in person_detections]

        # Update tracker with current detections
        tracker.update(rects)

        # Calculate activity score
        activity_score, direction_score, current_positions = calculate_activity(tracker, previous_positions, frame, activity_scores, direction_scores)

        # Update previous positions for the next frame
        previous_positions = current_positions.copy()

        # Display smoothed activity score
        cv2.putText(frame, f'Smoothed Activity Score: {activity_score:.2f}', (10, 30), config.FONT, config.FONT_SCALE, config.FONT_COLOR, config.FONT_THICKNESS)

        # Draw bounding boxes and centroids
        for rect in rects:
            cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), config.RECTANGLE_COLOR, config.RECTANGLE_THICKNESS)
        for object_id, centroid in tracker.objects.items():
            text = f'ID {object_id}, Activity: {tracker.activity_scores[object_id]:.2f}'  # Add activity score to text
            cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10), config.FONT, 0.5, config.CENTROID_COLOR, 2)
            cv2.circle(frame, tuple(centroid), config.CENTROID_RADIUS, config.CENTROID_COLOR, -1)

        # Write the frame to the output video file
        if(config.RECORD_RESULT):
            out.write(frame)

        # Display frames
        cv2.imshow('Frame', frame)

        # Break loop on quit key press
        if cv2.waitKey(config.FRAME_DELAY) & 0xFF == ord(config.QUIT_KEY):
            break

    # After the loop, release the video writer
    if(config.RECORD_RESULT):
        out.release()

    # Release video capture and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
