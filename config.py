import cv2
# config.py

# YOLO model path
YOLO_MODEL_PATH = 'yolov8n.pt'  # Update with the actual path to your YOLO model

RECORD_RESULT = False

# Maximum number of frames an object can be absent before deregistering
MAX_DISAPPEARED = 50

# Weight parameters
WEIGHT_MIN = 0.1  # Minimum weight assigned to objects far from the static point
WEIGHT_MAX = 1.0  # Maximum weight assigned to objects close to the static point
WEIGHT_MAX_DISTANCE = 600  # Maximum distance at which an object contributes to the activity score

# TRAPEZOID_VERTICES = [(960, 720), (320, 720), (200, 360), (1080, 360)] #small trapezoid
TRAPEZOID_VERTICES = [(960, 720), (320, 720), (200, 160), (1080, 160)] #big trapezoid
ATTRACTION_ANGLE = 45  # Angle in degrees within which an object is considered to be moving towards the centroid

# Static point coordinates (x, y)
STATIC_POINT = (650, 700)  # Adjust based on your frame size

# Drawing parameters
LINE_COLOR = (0, 255, 0)  # Green
LINE_THICKNESS = 2
RECTANGLE_COLOR = (255, 0, 0)  # Blue
RECTANGLE_THICKNESS = 2
CENTROID_COLOR = (0, 0, 255)  # Red
CENTROID_RADIUS = 5

# Font parameters
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 1
FONT_COLOR = (0, 255, 0)  # White
FONT_THICKNESS = 4

# Frame display parameters
FRAME_DELAY = 1
QUIT_KEY = 'q'

# Smoothing window size for activity score
SMOOTHING_WINDOW_SIZE = 20


# Video source
# VIDEO_SOURCE = 0  # 0 for webcam, or provide a path to a video file
# VIDEO_SOURCE = 'http://145.126.12.171:8080/video'
# VIDEO_SOURCE = 'Examples/Train_ns.mp4' 
#VIDEO_SOURCE = 'Examples/Train_instap.mp4' 
# VIDEO_SOURCE = 'Examples/Train_busy.mp4'
# VIDEO_SOURCE = 'Examples/Train_londen.mp4' 
# VIDEO_SOURCE = 'Examples/Train_tokio.mp4' 

VIDEO_SOURCE = 'Videos/GOPR_Drukte.mp4'
# VIDEO_SOURCE = 'Videos/GOPR_Wachten.mp4'
# VIDEO_SOURCE = 'Videos/GOPR_Instappen.mp4'
# VIDEO_SOURCE = 'Videos/GOPR_InUitStappen.mp4'
# VIDEO_SOURCE = 'Videos/GOPR_Sprinter.mp4'
# VIDEO_SOURCE = 'Videos/GOPR_Treuzelen.mp4'
# VIDEO_SOURCE = 'Videos/GOPR_Instappen2.mp4'
