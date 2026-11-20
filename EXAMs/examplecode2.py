import cv2
import numpy as np
import time
import os
import urllib.request
import threading
from collections import deque, Counter
from datetime import datetime

# ============================================================
#   MEDIAPIPE IMPORT
# ============================================================
try:
    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    print(f"✅ MediaPipe {mp.__version__} loaded!")
except Exception as e:
    print(f"❌ Error: {e}")
    print("👉 Fix: pip install mediapipe opencv-python numpy")
    exit()

# ============================================================
#   AUTO DOWNLOAD MODEL
# ============================================================
MODEL_PATH = "hand_landmarker.task"
MODEL_URL = ("https://storage.googleapis.com/mediapipe-models/"
             "hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task")

def download_model():
    if os.path.exists(MODEL_PATH) and os.path.getsize(MODEL_PATH) > 100_000:
        print(f"✅ Model found: {MODEL_PATH}")
        return True
    print(f"📥 Downloading hand model (~14MB)...")
    try:
        def progress(block, block_size, total):
            pct = min(block * block_size * 100 // total, 100) if total > 0 else 0
            bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
            print(f"\r   [{bar}] {pct}%", end="")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH, progress)
        print(f"\n✅ Downloaded: {MODEL_PATH}")
        return True
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        return False

# ============================================================
#   AUTO-DETECT SCREEN RESOLUTION
# ============================================================
def get_screen_resolution():
    """Get primary screen resolution automatically."""
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
        return width, height
    except:
        return 1920, 1080  # Default Full HD

SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_resolution()
print(f"🖥️  Screen Resolution: {SCREEN_WIDTH} x {SCREEN_HEIGHT}")

# ============================================================
#   RESPONSIVE SCALING SYSTEM
# ============================================================
class ScaleManager:
    """
    Automatically scales all UI elements based on screen resolution.
    Base design: 1920x1080 (Full HD)
    """
    def __init__(self, target_width, target_height):
        self.base_w = 1920
        self.base_h = 1080
        self.target_w = target_width
        self.target_h = target_height
        self.scale_x = target_width / self.base_w
        self.scale_y = target_height / self.base_h
        self.scale = min(self.scale_x, self.scale_y)  # Uniform scaling
    
    def x(self, val):
        """Scale X coordinate."""
        return int(val * self.scale_x)
    
    def y(self, val):
        """Scale Y coordinate."""
        return int(val * self.scale_y)
    
    def s(self, val):
        """Scale size (uniform)."""
        return int(val * self.scale)
    
    def font(self, val):
        """Scale font size."""
        return val * self.scale
    
    def rect(self, x, y, w, h):
        """Scale rectangle."""
        return self.x(x), self.y(y), self.x(w), self.y(h)

SM = ScaleManager(SCREEN_WIDTH, SCREEN_HEIGHT)

# ============================================================
#   THREADED CAMERA
# ============================================================
class ThreadedCamera:
    def __init__(self, index=0):
        self.cap = cv2.VideoCapture(index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.cap.set(cv2.CAP_PROP_FPS, 60)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        self.frame = None
        self.lock = threading.Lock()
        self.running = True
        self.thread = threading.Thread(target=self._reader, daemon=True)
        self.thread.start()
        
        timeout = time.time() + 5
        while self.frame is None and time.time() < timeout:
            time.sleep(0.01)
    
    def _reader(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.frame = frame
    
    def read(self):
        with self.lock:
            return self.frame is not None, (
                self.frame.copy() if self.frame is not None else None)
    
    def release(self):
        self.running = False
        self.thread.join(timeout=2)
        self.cap.release()

# ============================================================
#   ASYNC DETECTOR
# ============================================================
class AsyncHandDetector:
    def __init__(self, detector):
        self.detector = detector
        self._lock = threading.Lock()
        self._result = None
        self._pending = None
        self._pending_lock = threading.Lock()
        self._event = threading.Event()
        self.running = True
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()
    
    def submit(self, mp_img):
        with self._pending_lock:
            self._pending = mp_img
        self._event.set()
    
    def result(self):
        with self._lock:
            return self._result
    
    def _worker(self):
        while self.running:
            self._event.wait(timeout=0.5)
            self._event.clear()
            with self._pending_lock:
                img = self._pending
                self._pending = None
            if img is None:
                continue
            try:
                res = self.detector.detect(img)
                with self._lock:
                    self._result = res
            except:
                pass
    
    def stop(self):
        self.running = False
        self._event.set()
        self.thread.join(timeout=2)

# ============================================================
#   COLORS
# ============================================================
C = {
    "bg_dark"    : (12, 12, 28),
    "card_bg"    : (28, 28, 48),
    "card_dark"  : (18, 18, 35),
    "stop_red"   : (40, 40, 255),
    "go_green"   : (40, 255, 90),
    "slow_yellow": (0, 220, 255),
    "wait_orange": (0, 140, 255),
    "clear_cyan" : (255, 200, 40),
    "white"      : (255, 255, 255),
    "gray"       : (110, 110, 140),
    "light_gray" : (160, 160, 180),
    "purple"     : (255, 90, 200),
    "black"      : (0, 0, 0),
    "accent_blue": (255, 160, 60),
}

# ============================================================
#   GESTURE RECOGNITION
# ============================================================
def count_fingers(landmarks, label):
    def lm(i):
        return np.array([landmarks[i].x, landmarks[i].y])
    
    fingers_up = 0
    
    # Thumb
    thumb_tip = lm(4); thumb_ip = lm(3)
    if label == "Right":
        if thumb_tip[0] < thumb_ip[0]: fingers_up += 1
    else:
        if thumb_tip[0] > thumb_ip[0]: fingers_up += 1
    
    # Other fingers
    for tip, pip in [(8,6), (12,10), (16,14), (20,18)]:
        if lm(tip)[1] < lm(pip)[1]: fingers_up += 1
    
    return fingers_up

def detect_gesture(landmarks, label, finger_count):
    if finger_count == 5:
        return "STOP", C["stop_red"], "🛑"
    elif finger_count == 0:
        return "GO", C["go_green"], "✅"
    elif finger_count == 1:
        return "SLOW DOWN", C["slow_yellow"], "⚠️"
    elif finger_count == 2:
        return "WAIT", C["wait_orange"], "✋"
    elif finger_count == 3:
        def lm(i): return np.array([landmarks[i].x, landmarks[i].y])
        if np.linalg.norm(lm(4) - lm(8)) < 0.05:
            return "ALL CLEAR", C["clear_cyan"], "👌"
    return "UNKNOWN", C["gray"], "❓"

# ============================================================
#   SMOOTHER & LOG
# ============================================================
class GestureSmoother:
    def __init__(self, window=6):
        self.buffer = deque(maxlen=window)
    def update(self, gesture):
        self.buffer.append(gesture)
    def get(self):
        if not self.buffer: return "UNKNOWN"
        return Counter(self.buffer).most_common(1)[0][0]

class TrafficLog:
    def __init__(self, max_entries=15):
        self.log = deque(maxlen=max_entries)
    def add(self, gesture, timestamp):
        self.log.append((gesture, timestamp))
    def get_recent(self, n=10):
        return list(self.log)[-n:]

# ============================================================
#   DRAWING PRIMITIVES (Responsive)
# ============================================================
def filled_rrect(img, x1, y1, x2, y2, r, color, alpha=0.80):
    overlay = img.copy()
    r = max(1, min(r, (x2-x1)//2, (y2-y1)//2))
    cv2.rectangle(overlay, (x1+r, y1), (x2-r, y2), color, -1)
    cv2.rectangle(overlay, (x1, y1+r), (x2, y2-r), color, -1)
    for cx, cy in [(x1+r,y1+r),(x2-r,y1+r),(x1+r,y2-r),(x2-r,y2-r)]:
        cv2.circle(overlay, (cx,cy), r, color, -1)
    cv2.addWeighted(overlay, alpha, img, 1-alpha, 0, img)

def border_rrect(img, x1, y1, x2, y2, r, color, t=2):
    r = max(1, min(r, (x2-x1)//2, (y2-y1)//2))
    cv2.line(img, (x1+r,y1), (x2-r,y1), color, t, cv2.LINE_AA)
    cv2.line(img, (x1+r,y2), (x2-r,y2), color, t, cv2.LINE_AA)
    cv2.line(img, (x1,y1+r), (x1,y2-r), color, t, cv2.LINE_AA)
    cv2.line(img, (x2,y1+r), (x2,y2-r), color, t, cv2.LINE_AA)
    cv2.ellipse(img,(x1+r,y1+r),(r,r),180,0,90,color,t,cv2.LINE_AA)
    cv2.ellipse(img,(x2-r,y1+r),(r,r),270,0,90,color,t,cv2.LINE_AA)
    cv2.ellipse(img,(x1+r,y2-r),(r,r),90, 0,90,color,t,cv2.LINE_AA)
    cv2.ellipse(img,(x2-r,y2-r),(r,r),0,  0,90,color,t,cv2.LINE_AA)

def put_text(img, text, pos, scale, color, bold=False, font=cv2.FONT_HERSHEY_DUPLEX):
    t = 3 if bold else 2
    x, y = pos
    cv2.putText(img, text, (x+3, y+3), font, scale, (0,0,0), t+3, cv2.LINE_AA)
    cv2.putText(img, text, (x, y), font, scale, color, t, cv2.LINE_AA)

# ============================================================
#   DRAW HAND SKELETON
# ============================================================
HAND_CONN = [
    (0,1),(1,2),(2,3),(3,4), (0,5),(5,6),(6,7),(7,8),
    (0,9),(9,10),(10,11),(11,12), (0,13),(13,14),(14,15),(15,16),
    (0,17),(17,18),(18,19),(19,20), (5,9),(9,13),(13,17),
]

def draw_hand_skeleton(frame, landmarks, fw, fh, color):
    pts = np.array([(int(l.x*fw), int(l.y*fh)) for l in landmarks])
    thickness = SM.s(4)
    
    for a, b in HAND_CONN:
        cv2.line(frame, tuple(pts[a]), tuple(pts[b]), color, thickness, cv2.LINE_AA)
    
    for i, p in enumerate(pts):
        r = SM.s(12) if i in (4,8,12,16,20) else SM.s(7)
        cv2.circle(frame, tuple(p), r, C["go_green"], -1)
        cv2.circle(frame, tuple(p), r+SM.s(2), color, SM.s(2))

# ============================================================
#   GIANT COMMAND PANEL (Center)
# ============================================================
def draw_command_panel(frame, gesture, emoji, color, finger_count, label):
    h, w = frame.shape[:2]
    
    # Responsive panel size (40% of screen width)
    pw = SM.x(900)
    ph = SM.y(500)
    px = (w - pw) // 2
    py = SM.y(80)
    
    # Main card
    filled_rrect(frame, px, py, px+pw, py+ph, SM.s(30), C["card_bg"], 0.92)
    border_rrect(frame, px, py, px+pw, py+ph, SM.s(30), color, SM.s(5))
    
    # Top accent bar
    cv2.rectangle(frame, (px+SM.s(30), py+SM.s(5)), 
                  (px+pw-SM.s(30), py+SM.s(12)), color, -1)
    
    # Header
    header_y = py + SM.y(60)
    put_text(frame, "TRAFFIC CONTROL SYSTEM",
             (px + SM.x(210), header_y), 
             SM.font(1.2), C["white"], bold=True)
    
    # Divider
    cv2.line(frame, (px+SM.s(40), py+SM.y(85)), 
             (px+pw-SM.s(40), py+SM.y(85)), (55,55,85), SM.s(3))
    
    # Giant Emoji (with glow)
    emoji_y = py + SM.y(230)
    emoji_size = SM.font(10.0)
    
    # Emoji glow effect
    glow_center_x = px + pw//2
    glow_center_y = emoji_y - SM.y(50)
    for r in range(SM.s(100), 0, -SM.s(15)):
        cv2.circle(frame, (glow_center_x, glow_center_y), r,
                   color, -1, lineType=cv2.LINE_AA)
    
    # Draw emoji
    emoji_font = cv2.FONT_HERSHEY_PLAIN
    tw = cv2.getTextSize(emoji, emoji_font, emoji_size, SM.s(10))[0][0]
    emoji_x = px + (pw - tw) // 2
    cv2.putText(frame, emoji, (emoji_x, emoji_y),
                emoji_font, emoji_size, color, SM.s(12), cv2.LINE_AA)
    
    # Command text (giant)
    cmd_y = py + SM.y(350)
    cmd_scale = SM.font(3.5)
    cmd_tw = cv2.getTextSize(gesture, cv2.FONT_HERSHEY_DUPLEX, cmd_scale, SM.s(6))[0][0]
    cmd_x = px + (pw - cmd_tw) // 2
    put_text(frame, gesture, (cmd_x, cmd_y), cmd_scale, color, bold=True)
    
    # Info bar
    info_y = py + SM.y(430)
    info_text = f"Hand: {label}  |  Fingers: {finger_count}/5  |  Confidence: High"
    info_scale = SM.font(0.9)
    info_tw = cv2.getTextSize(info_text, cv2.FONT_HERSHEY_SIMPLEX, info_scale, SM.s(2))[0][0]
    put_text(frame, info_text, (px + (pw-info_tw)//2, info_y),
             info_scale, C["light_gray"], font=cv2.FONT_HERSHEY_SIMPLEX)
    
    # Animated pulse border
    pulse = int(abs(np.sin(time.time() * 3.5)) * SM.s(20))
    border_rrect(frame, px-pulse, py-pulse, px+pw+pulse, py+ph+pulse,
                 SM.s(30)+pulse, color, SM.s(2))

# ============================================================
#   TRAFFIC LOG (Left Panel)
# ============================================================
def draw_traffic_log(frame, log):
    h, w = frame.shape[:2]
    
    px = SM.x(30)
    py = h - SM.y(600)
    pw = SM.x(480)
    ph = SM.y(560)
    
    filled_rrect(frame, px, py, px+pw, py+ph, SM.s(20), C["card_bg"], 0.88)
    border_rrect(frame, px, py, px+pw, py+ph, SM.s(20), C["purple"], SM.s(3))
    
    # Header
    put_text(frame, "📋 COMMAND LOG", (px+SM.s(20), py+SM.y(45)),
             SM.font(0.95), C["purple"], bold=True)
    
    cv2.line(frame, (px+SM.s(20), py+SM.y(60)), 
             (px+pw-SM.s(20), py+SM.y(60)), (55,55,85), SM.s(2))
    
    # Recent commands
    recent = log.get_recent(12)
    for i, (cmd, timestamp) in enumerate(recent):
        y = py + SM.y(100) + i * SM.y(38)
        
        icons = {"STOP":"🛑", "GO":"✅", "SLOW DOWN":"⚠️", 
                 "WAIT":"✋", "ALL CLEAR":"👌"}
        icon = icons.get(cmd, "❓")
        
        colors_map = {
            "STOP": C["stop_red"], "GO": C["go_green"],
            "SLOW DOWN": C["slow_yellow"], "WAIT": C["wait_orange"],
            "ALL CLEAR": C["clear_cyan"]
        }
        col = colors_map.get(cmd, C["gray"])
        
        # Icon
        cv2.putText(frame, icon, (px+SM.s(25), y),
                    cv2.FONT_HERSHEY_PLAIN, SM.font(3.0), col, SM.s(3), cv2.LINE_AA)
        
        # Command name
        put_text(frame, cmd, (px+SM.s(90), y),
                 SM.font(0.65), col, font=cv2.FONT_HERSHEY_SIMPLEX)
        
        # Timestamp
        put_text(frame, timestamp, (px+SM.x(320), y),
                 SM.font(0.52), C["gray"], font=cv2.FONT_HERSHEY_SIMPLEX)

# ============================================================
#   GESTURE GUIDE (Right Panel)
# ============================================================
def draw_gesture_guide(frame):
    h, w = frame.shape[:2]
    
    px = w - SM.x(510)
    py = h - SM.y(600)
    pw = SM.x(480)
    ph = SM.y(560)
    
    filled_rrect(frame, px, py, px+pw, py+ph, SM.s(20), C["card_bg"], 0.88)
    border_rrect(frame, px, py, px+pw, py+ph, SM.s(20), C["clear_cyan"], SM.s(3))
    
    put_text(frame, "📖 GESTURE GUIDE", (px+SM.s(20), py+SM.y(45)),
             SM.font(0.95), C["clear_cyan"], bold=True)
    
    cv2.line(frame, (px+SM.s(20), py+SM.y(60)), 
             (px+pw-SM.s(20), py+SM.y(60)), (55,55,85), SM.s(2))
    
    guides = [
        ("🛑", "STOP",       "Spread all 5 fingers wide",  C["stop_red"]),
        ("✅", "GO",         "Close all fingers (fist)",   C["go_green"]),
        ("⚠️", "SLOW DOWN",  "Point 1 finger up (index)",  C["slow_yellow"]),
        ("✋", "WAIT",       "Show 2 fingers (peace)",     C["wait_orange"]),
        ("👌", "ALL CLEAR",  "Make OK circle sign",        C["clear_cyan"]),
    ]
    
    for i, (emoji, name, desc, col) in enumerate(guides):
        y = py + SM.y(110) + i * SM.y(85)
        
        # Emoji
        cv2.putText(frame, emoji, (px+SM.s(25), y),
                    cv2.FONT_HERSHEY_PLAIN, SM.font(3.2), col, SM.s(3), cv2.LINE_AA)
        
        # Name
        put_text(frame, name, (px+SM.s(95), y),
                 SM.font(0.75), col, bold=True, font=cv2.FONT_HERSHEY_SIMPLEX)
        
        # Description
        put_text(frame, desc, (px+SM.s(95), y+SM.y(25)),
                 SM.font(0.48), C["light_gray"], font=cv2.FONT_HERSHEY_SIMPLEX)

# ============================================================
#   HEADER BAR (Top)
# ============================================================
def draw_header_bar(frame):
    h, w = frame.shape[:2]
    
    bar_h = SM.y(70)
    filled_rrect(frame, 0, 0, w, bar_h, 0, (20,20,42), 0.90)
    cv2.line(frame, (0, bar_h), (w, bar_h), C["purple"], SM.s(3))
    
    # Logo
    put_text(frame, "🚦 TRAFFIC CONTROL AI", (SM.x(40), SM.y(48)),
             SM.font(1.1), C["purple"], bold=True)
    
    # Date & Time
    now_str = datetime.now().strftime("%A, %B %d, %Y  |  %I:%M:%S %p")
    time_tw = cv2.getTextSize(now_str, cv2.FONT_HERSHEY_SIMPLEX, 
                              SM.font(0.7), SM.s(2))[0][0]
    put_text(frame, now_str, (w - time_tw - SM.x(40), SM.y(48)),
             SM.font(0.7), C["light_gray"], font=cv2.FONT_HERSHEY_SIMPLEX)

# ============================================================
#   STATUS BAR (Bottom)
# ============================================================
def draw_status_bar(frame, fps, frame_count):
    h, w = frame.shape[:2]
    
    bar_h = SM.y(60)
    filled_rrect(frame, 0, h-bar_h, w, h, 0, (18,18,38), 0.92)
    cv2.line(frame, (0, h-bar_h), (w, h-bar_h), C["purple"], SM.s(3))
    
    # FPS indicator
    fps_c = C["go_green"] if fps >= 50 else C["slow_yellow"] if fps >= 30 else C["stop_red"]
    put_text(frame, f"FPS: {fps:5.1f}", (SM.x(30), h-SM.y(20)),
             SM.font(0.7), fps_c, font=cv2.FONT_HERSHEY_SIMPLEX, bold=True)
    
    # Frame count
    put_text(frame, f"Frame: {frame_count}", (SM.x(200), h-SM.y(20)),
             SM.font(0.6), C["gray"], font=cv2.FONT_HERSHEY_SIMPLEX)
    
    # Controls
    controls = "Q = Quit  |  S = Screenshot  |  F = Toggle Fullscreen  |  ESC = Exit"
    ctrl_tw = cv2.getTextSize(controls, cv2.FONT_HERSHEY_SIMPLEX, 
                              SM.font(0.65), SM.s(2))[0][0]
    put_text(frame, controls, (w//2 - ctrl_tw//2, h-SM.y(20)),
             SM.font(0.65), C["accent_blue"], font=cv2.FONT_HERSHEY_SIMPLEX)
    
    # System info
    put_text(frame, f"Resolution: {w}x{h}", (w - SM.x(300), h-SM.y(20)),
             SM.font(0.55), C["gray"], font=cv2.FONT_HERSHEY_SIMPLEX)

# ============================================================
#   MAIN
# ============================================================
def main():
    print("="*80)
    print("   🚦 FULL HD TRAFFIC HAND GESTURE CONTROL SYSTEM 🚦")
    print("="*80)
    print(f"\n   🖥️  Screen Resolution: {SCREEN_WIDTH} x {SCREEN_HEIGHT}")
    print(f"   📐  UI Scale Factor: {SM.scale:.2f}x")
    print("\n   Gestures:")
    print("   🛑  5 fingers open       → STOP")
    print("   ✅  Closed fist          → GO")
    print("   ⚠️  1 finger (index)     → SLOW DOWN")
    print("   ✋  2 fingers (peace)    → WAIT")
    print("   👌  OK sign (circle)     → ALL CLEAR")
    print("\n" + "="*80)
    
    if not download_model():
        input("\nPress Enter to exit...")
        return
    
    print("\n📷  Opening camera...")
    cam = ThreadedCamera(index=0)
    ret, test = cam.read()
    if not ret or test is None:
        print("❌  Camera not found!")
        return
    
    print("✅  Camera ready!")
    
    # Build detector
    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=1,
        min_hand_detection_confidence=0.7,
        min_hand_presence_confidence=0.7,
        min_tracking_confidence=0.7
    )
    detector_obj = vision.HandLandmarker.create_from_options(options)
    async_detector = AsyncHandDetector(detector_obj)
    print("✅  Hand detector ready!\n")
    
    # State
    smoother = GestureSmoother(window=6)
    traffic_log = TrafficLog(max_entries=15)
    
    current_gesture = "WAITING"
    current_color = C["gray"]
    current_emoji = "👋"
    finger_count = 0
    hand_label = ""
    last_logged_gesture = None
    
    frame_count = 0
    fps = 0.0
    t_fps = time.perf_counter()
    shot_n = 0
    
    is_fullscreen = False
    
    DETECT_EVERY = 2
    
    # Create window
    window_name = "Traffic Control System - Full HD"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Auto fullscreen on start
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    is_fullscreen = True
    
    print("✅  System ACTIVE! Show hand gestures...\n")
    print(f"   Window: {'FULLSCREEN' if is_fullscreen else 'WINDOWED'}")
    print("\n   Controls:")
    print("   - Q or ESC : Quit")
    print("   - S        : Screenshot")
    print("   - F        : Toggle Fullscreen\n")
    
    while True:
        ret, frame = cam.read()
        if not ret or frame is None:
            continue
        
        frame = cv2.flip(frame, 1)
        
        # Resize to screen resolution
        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        frame_count += 1
        h, w = frame.shape[:2]
        
        # Submit for detection
        if frame_count % DETECT_EVERY == 0:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            async_detector.submit(mp_img)
        
        # Get result
        result = async_detector.result()
        
        if result and result.hand_landmarks:
            hand_lms = result.hand_landmarks[0]
            hand_label = result.handedness[0][0].category_name
            
            draw_hand_skeleton(frame, hand_lms, w, h, C["clear_cyan"])
            
            finger_count = count_fingers(hand_lms, hand_label)
            gesture, color, emoji = detect_gesture(hand_lms, hand_label, finger_count)
            
            smoother.update(gesture)
            current_gesture = smoother.get()
            current_color = color
            current_emoji = emoji
            
            if current_gesture != last_logged_gesture and current_gesture != "UNKNOWN":
                timestamp = datetime.now().strftime("%H:%M:%S")
                traffic_log.add(current_gesture, timestamp)
                last_logged_gesture = current_gesture
                print(f"🚦  [{timestamp}] Command: {current_gesture}")
        
        else:
            current_gesture = "WAITING"
            current_color = C["gray"]
            current_emoji = "👋"
            finger_count = 0
            hand_label = ""
        
        # Background
        overlay = np.zeros_like(frame)
        cv2.rectangle(overlay, (0,0), (w,h), C["bg_dark"], -1)
        cv2.addWeighted(overlay, 0.18, frame, 0.82, 0, frame)
        
        # Draw UI
        draw_header_bar(frame)
        
        if current_gesture not in ["WAITING", "UNKNOWN"]:
            draw_command_panel(frame, current_gesture, current_emoji,
                               current_color, finger_count, hand_label)
        
        draw_traffic_log(frame, traffic_log)
        draw_gesture_guide(frame)
        
        # FPS
        if frame_count % 15 == 0:
            now = time.perf_counter()
            fps = 15.0 / max(now - t_fps, 1e-6)
            t_fps = now
        
        draw_status_bar(frame, fps, frame_count)
        
        # Display
        cv2.imshow(window_name, frame)
        
        # Handle keys
        key = cv2.waitKey(1) & 0xFF
        
        if key in (ord('q'), 27):  # Q or ESC
            print("\n\n✅  System shutdown initiated...")
            break
        
        elif key == ord('s'):  # Screenshot
            filename = f"traffic_control_{shot_n:04d}.png"
            cv2.imwrite(filename, frame)
            print(f"📸  Screenshot saved: {filename}")
            shot_n += 1
        
        elif key == ord('f'):  # Toggle fullscreen
            is_fullscreen = not is_fullscreen
            if is_fullscreen:
                cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, 
                                      cv2.WINDOW_FULLSCREEN)
                print("🖥️  Switched to FULLSCREEN mode")
            else:
                cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, 
                                      cv2.WINDOW_NORMAL)
                cv2.resizeWindow(window_name, 1280, 720)
                print("🪟  Switched to WINDOWED mode")
    
    # Cleanup
    async_detector.stop()
    detector_obj.close()
    cam.release()
    cv2.destroyAllWindows()
    print("\n👋  Traffic Control System stopped successfully.")
    print("="*80)


if __name__ == "__main__":
    main()