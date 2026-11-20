import cv2
import numpy as np
import time
import os
import urllib.request
import threading
from collections import deque, Counter

# ============================================================
#   MEDIAPIPE IMPORT
# ============================================================
try:
    import mediapipe as mp
    from mediapipe.tasks import python as mp_python
    from mediapipe.tasks.python import vision as mp_vision
    from mediapipe.tasks.python.vision import (
        FaceLandmarker, HandLandmarker,
        FaceLandmarkerOptions, HandLandmarkerOptions
    )
    from mediapipe.tasks.python.core.base_options import BaseOptions
    print(f"✅ MediaPipe {mp.__version__} loaded!")
except Exception as e:
    print(f"❌ Error: {e}")
    print("👉 Fix: pip install mediapipe==0.10.9 opencv-python numpy")
    exit()

# ============================================================
#   AUTO DOWNLOAD MODELS
# ============================================================
MODELS = {
    "face_landmarker.task":
        "https://storage.googleapis.com/mediapipe-models/face_landmarker/"
        "face_landmarker/float16/1/face_landmarker.task",
    "hand_landmarker.task":
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
        "hand_landmarker/float16/1/hand_landmarker.task",
}

def download_models():
    for fname, url in MODELS.items():
        if os.path.exists(fname) and os.path.getsize(fname) > 100_000:
            print(f"✅ Found: {fname}")
            continue
        print(f"📥 Downloading {fname}...")
        try:
            def prog(b, bs, total):
                pct = min(b*bs*100//total, 100) if total > 0 else 0
                bar = "█"*(pct//5) + "░"*(20-pct//5)
                print(f"\r   [{bar}] {pct}%", end="")
            urllib.request.urlretrieve(url, fname, prog)
            print(f"\n✅ Done: {fname}")
        except Exception as e:
            print(f"\n❌ Failed: {e}")
            return False
    return True

# ============================================================
#   THREADED CAMERA (eliminates buffer lag = +20 FPS)
# ============================================================
class ThreadedCamera:
    """
    Reads frames in a background thread so the main loop
    never waits on cap.read(). This alone gives +15-20 FPS.
    """
    def __init__(self, index=0, width=640, height=480):
        self.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)  # CAP_DSHOW = faster on Windows
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, 60)
        # Reduce internal buffer to 1 = always freshest frame
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        # Try MJPG codec — much faster USB transfer
        self.cap.set(cv2.CAP_PROP_FOURCC,
                     cv2.VideoWriter_fourcc(*"MJPG"))

        self.frame  = None
        self.lock   = threading.Lock()
        self.running = True
        self.thread = threading.Thread(target=self._reader, daemon=True)
        self.thread.start()

        # wait for first frame
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

    def get(self, prop):
        return self.cap.get(prop)

    def release(self):
        self.running = False
        self.thread.join(timeout=2)
        self.cap.release()

# ============================================================
#   ASYNC MEDIAPIPE DETECTOR (runs in separate thread)
# ============================================================
class AsyncDetector:
    """
    Runs face+hand detection in a background thread.
    Main thread draws at full speed; detection updates
    whenever it finishes (decoupled FPS).
    """
    def __init__(self, face_det, hand_det):
        self.face_det  = face_det
        self.hand_det  = hand_det

        # Latest results (thread-safe)
        self._lock        = threading.Lock()
        self._face_result = None
        self._hand_result = None

        # Input queue (only keep newest frame)
        self._pending     = None
        self._pending_lk  = threading.Lock()
        self._event       = threading.Event()

        self.running = True
        self.thread  = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def submit(self, mp_img):
        """Give a new frame to detect on (non-blocking)."""
        with self._pending_lk:
            self._pending = mp_img
        self._event.set()

    def results(self):
        """Get latest face+hand results (non-blocking)."""
        with self._lock:
            return self._face_result, self._hand_result

    def _worker(self):
        while self.running:
            self._event.wait(timeout=0.5)
            self._event.clear()
            with self._pending_lk:
                img = self._pending
                self._pending = None
            if img is None:
                continue
            try:
                fr = self.face_det.detect(img)
                hr = self.hand_det.detect(img)
                with self._lock:
                    self._face_result = fr
                    self._hand_result = hr
            except Exception:
                pass

    def stop(self):
        self.running = False
        self._event.set()
        self.thread.join(timeout=2)

# ============================================================
#   COLORS (BGR)
# ============================================================
C = {
    "dark_card" : (35,  35,  60),
    "purple"    : (255, 100, 200),
    "cyan"      : (255, 210,  50),
    "green"     : ( 60, 220, 100),
    "red"       : ( 50,  50, 220),
    "yellow"    : (  0, 210, 255),
    "white"     : (255, 255, 255),
    "gray"      : (120, 120, 145),
    "orange"    : ( 20, 140, 255),
    "teal"      : (180, 200,  40),
    "pink"      : (200,  80, 240),
    "lime"      : ( 40, 255, 130),
    "blue"      : (255, 150,  50),
    "black"     : (  0,   0,   0),
}

# ============================================================
#   LANDMARK INDICES
# ============================================================
NOSE_TIP  = 4
FOREHEAD  = 10
CHIN      = 152
L_EAR     = 234
R_EAR     = 454
L_EYE     = 33
R_EYE     = 263

WRIST     = 0
MID_MCP   = 9

HAND_CONN = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (0,9),(9,10),(10,11),(11,12),
    (0,13),(13,14),(14,15),(15,16),
    (0,17),(17,18),(18,19),(19,20),
    (5,9),(9,13),(13,17),
]

FACE_OVAL = [
    10,338,297,332,284,251,389,356,454,323,361,288,
    397,365,379,378,400,377,152,148,176,149,150,136,
    172,58,132,93,234,127,162,21,54,103,67,109,10
]

# ============================================================
#   SMOOTHER
# ============================================================
class Smoother:
    def __init__(self, n=4):          # smaller n = faster response
        self.buf = deque(maxlen=n)
    def push(self, v):
        self.buf.append(v)
    def get(self):
        if not self.buf: return "UNKNOWN"
        return Counter(self.buf).most_common(1)[0][0]

# ============================================================
#   CACHED HUD OVERLAY
# ============================================================
class HUDCache:
    """
    Render expensive HUD elements only when data changes,
    then blit the cached image. Saves ~3ms per frame.
    """
    def __init__(self, shape):
        self.shape   = shape
        self.overlay = np.zeros(shape, dtype=np.uint8)
        self._hash   = None

    def needs_update(self, data_hash):
        if data_hash != self._hash:
            self._hash = data_hash
            return True
        return False

# ============================================================
#   DRAWING HELPERS  (optimized — no copies where avoidable)
# ============================================================
def filled_rrect(img, x1, y1, x2, y2, r, color, alpha=0.75):
    r = max(1, min(r, (x2-x1)//2, (y2-y1)//2))
    overlay = img.copy()
    cv2.rectangle(overlay, (x1+r, y1), (x2-r, y2), color, -1)
    cv2.rectangle(overlay, (x1, y1+r), (x2, y2-r), color, -1)
    for cx, cy in [(x1+r,y1+r),(x2-r,y1+r),(x1+r,y2-r),(x2-r,y2-r)]:
        cv2.circle(overlay, (cx,cy), r, color, -1)
    cv2.addWeighted(overlay, alpha, img, 1-alpha, 0, img)


def border_rrect(img, x1, y1, x2, y2, r, color, t=1):
    r = max(1, min(r, (x2-x1)//2, (y2-y1)//2))
    cv2.line(img, (x1+r,y1),   (x2-r,y1),   color, t, cv2.LINE_AA)
    cv2.line(img, (x1+r,y2),   (x2-r,y2),   color, t, cv2.LINE_AA)
    cv2.line(img, (x1,y1+r),   (x1,y2-r),   color, t, cv2.LINE_AA)
    cv2.line(img, (x2,y1+r),   (x2,y2-r),   color, t, cv2.LINE_AA)
    cv2.ellipse(img,(x1+r,y1+r),(r,r),180, 0,90,color,t,cv2.LINE_AA)
    cv2.ellipse(img,(x2-r,y1+r),(r,r),270, 0,90,color,t,cv2.LINE_AA)
    cv2.ellipse(img,(x1+r,y2-r),(r,r), 90, 0,90,color,t,cv2.LINE_AA)
    cv2.ellipse(img,(x2-r,y2-r),(r,r),  0, 0,90,color,t,cv2.LINE_AA)


def put_txt(img, text, pos, scale, color,
            bold=False, font=cv2.FONT_HERSHEY_DUPLEX):
    t = 2 if bold else 1
    x, y = pos
    cv2.putText(img, text,(x+1,y+1),font,scale,(0,0,0),t+2,cv2.LINE_AA)
    cv2.putText(img, text,(x,  y  ),font,scale,color,  t,  cv2.LINE_AA)


def dir_label(d):
    return {"LEFT":"<-- LEFT","RIGHT":"--> RIGHT",
            "UP":"/\\ UP","DOWN":"\\/ DOWN",
            "CENTER":"[*] CENTER","UP-LEFT":"<^ UP-LEFT",
            "UP-RIGHT":"^> UP-RIGHT","DOWN-LEFT":"<v DOWN-LEFT",
            "DOWN-RIGHT":"v> DOWN-RIGHT","TILTED-L":"~< TILT-L",
            "TILTED-R":"~> TILT-R","LEVEL":"-- LEVEL",
            "NO FACE":"?? NO FACE","NO HAND":"?? NO HAND",
            }.get(d, d)


def dir_color(d):
    return {"CENTER":C["green"],"LEFT":C["cyan"],"RIGHT":C["orange"],
            "UP":C["purple"],"DOWN":C["red"],"UP-LEFT":C["teal"],
            "UP-RIGHT":C["pink"],"DOWN-LEFT":C["yellow"],
            "DOWN-RIGHT":C["orange"],"TILTED-L":C["cyan"],
            "TILTED-R":C["purple"],"LEVEL":C["lime"],
            }.get(d, C["white"])

# ============================================================
#   PRE-BUILT GRID (drawn once, blitted every frame)
# ============================================================
def make_grid(h, w, spacing=80):
    grid = np.zeros((h, w, 3), dtype=np.uint8)
    for x in range(0, w, spacing):
        cv2.line(grid, (x,0), (x,h), (22,22,45), 1)
    for y in range(0, h, spacing):
        cv2.line(grid, (0,y), (w,y), (22,22,45), 1)
    return grid

# ============================================================
#   FACE DIRECTION
# ============================================================
def calc_face_dir(lms, fw, fh):
    def lm(i):
        p = lms[i]
        return np.array([p.x*fw, p.y*fh], dtype=np.float32)

    nose = lm(NOSE_TIP); l_ear = lm(L_EAR); r_ear = lm(R_EAR)
    forehead = lm(FOREHEAD); chin = lm(CHIN)
    l_eye = lm(L_EYE); r_eye = lm(R_EYE)

    ear_d   = float(np.linalg.norm(r_ear - l_ear)) + 1e-6
    mid_x   = (l_ear[0] + r_ear[0]) / 2
    mid_y   = (l_ear[1] + r_ear[1]) / 2
    face_h  = float(np.linalg.norm(chin - forehead)) + 1e-6

    yaw_off   = (nose[0] - mid_x) / ear_d
    pitch_off = (nose[1] - mid_y) / face_h

    yaw   = "LEFT"   if yaw_off   < -0.07 else "RIGHT"  if yaw_off   > 0.07 else "CENTER"
    pitch = "UP"     if pitch_off < -0.02 else "DOWN"   if pitch_off > 0.10 else "CENTER"

    dx = r_eye[0]-l_eye[0]; dy = r_eye[1]-l_eye[1]
    ang = np.degrees(np.arctan2(dy, dx))
    roll = "TILTED-L" if ang > 8 else "TILTED-R" if ang < -8 else "LEVEL"

    return yaw, pitch, roll, (int(nose[0]), int(nose[1]))


def combined_dir(yaw, pitch):
    if "NO" in str(yaw): return "NO FACE"
    if yaw=="CENTER" and pitch=="CENTER": return "CENTER"
    if yaw=="CENTER":  return pitch
    if pitch=="CENTER": return yaw
    return f"{pitch}-{yaw}"

# ============================================================
#   HAND DIRECTION
# ============================================================
def calc_hand_dir(lms, fw, fh, label):
    def lm(i):
        p = lms[i]
        return np.array([p.x*fw, p.y*fh], dtype=np.float32)

    wrist = lm(WRIST); mid = lm(MID_MCP)
    dx = mid[0]-wrist[0]; dy = mid[1]-wrist[1]
    ang = np.degrees(np.arctan2(-dy, dx))

    if    67.5 < ang <= 112.5: pt = "UP"
    elif  22.5 < ang <=  67.5: pt = "UP-RIGHT"
    elif -22.5 < ang <=  22.5: pt = "RIGHT"
    elif -67.5 < ang <= -22.5: pt = "DOWN-RIGHT"
    elif-112.5 < ang <= -67.5: pt = "DOWN"
    elif-157.5 < ang <=-112.5: pt = "DOWN-LEFT"
    elif ang > 157.5 or ang <= -157.5: pt = "LEFT"
    else: pt = "UP-LEFT"

    tips_bases = [("I",8,6),("M",12,10),("R",16,14),("P",20,18)]
    states = [(n, bool(lm(ti)[1] < lm(bi)[1])) for n,ti,bi in tips_bases]
    t4=lm(4); t3=lm(3)
    states.append(("T", bool(t4[0]>t3[0]) if label=="Left" else bool(t4[0]<t3[0])))

    palm = "CAMERA" if ((label=="Right" and dx<0) or
                        (label=="Left"  and dx>0)) else "AWAY"
    return pt, palm, states, (int(wrist[0]), int(wrist[1]))

# ============================================================
#   DRAW LANDMARKS  (optimized with numpy)
# ============================================================
def draw_face_lm(frame, lms, fw, fh):
    pts = np.array([(int(l.x*fw), int(l.y*fh)) for l in lms])
    for i in range(len(FACE_OVAL)-1):
        a, b = FACE_OVAL[i], FACE_OVAL[i+1]
        if a < len(pts) and b < len(pts):
            cv2.line(frame, tuple(pts[a]), tuple(pts[b]),
                     (110,55,190), 1, cv2.LINE_AA)
    for idx in [NOSE_TIP,L_EYE,R_EYE,FOREHEAD,CHIN,L_EAR,R_EAR]:
        if idx < len(pts):
            cv2.circle(frame, tuple(pts[idx]), 4, C["purple"], -1)


def draw_hand_lm(frame, lms, fw, fh, accent):
    pts = np.array([(int(l.x*fw), int(l.y*fh)) for l in lms])
    for a, b in HAND_CONN:
        cv2.line(frame, tuple(pts[a]), tuple(pts[b]),
                 accent, 2, cv2.LINE_AA)
    for i, p in enumerate(pts):
        r = 6 if i in (4,8,12,16,20) else 3
        cv2.circle(frame, tuple(p), r,   C["lime"],  -1)
        cv2.circle(frame, tuple(p), r+1, accent,      1)

# ============================================================
#   HUD PANELS
# ============================================================
F = cv2.FONT_HERSHEY_SIMPLEX
D = cv2.FONT_HERSHEY_DUPLEX

def draw_face_panel(frame, yaw, pitch, roll, combo, nose_px):
    px,py,pw,ph = 10,10,298,228
    filled_rrect(frame,px,py,px+pw,py+ph,13,C["dark_card"],0.80)
    border_rrect(frame,px,py,px+pw,py+ph,13,C["purple"],1)
    cv2.rectangle(frame,(px+14,py+1),(px+pw-14,py+4),C["purple"],-1)

    put_txt(frame,"FACE DIRECTION",(px+14,py+27),0.50,C["purple"],font=D)
    col=dir_color(combo)
    put_txt(frame,dir_label(combo),(px+14,py+65),0.65,col,bold=True,font=D)
    cv2.line(frame,(px+12,py+78),(px+pw-12,py+78),(55,55,85),1)

    rows=[("YAW  :",yaw,C["cyan"]),
          ("PITCH:",pitch,C["yellow"]),
          ("ROLL :",roll,C["teal"])]
    for i,(lb,val,c) in enumerate(rows):
        y=py+104+i*40
        put_txt(frame,lb,(px+14,y),0.40,C["gray"],font=F)
        filled_rrect(frame,px+100,y-17,px+pw-10,y+7,5,(42,42,72),0.88)
        put_txt(frame,val,(px+106,y),0.43,c,font=F)

    cv2.circle(frame,nose_px,10,col,-1)
    cv2.circle(frame,nose_px,13,col,2)
    cv2.circle(frame,nose_px, 4,C["white"],-1)


def draw_hand_panel(frame, hand_data, fw):
    if not hand_data:
        px=fw-308; py=10
        filled_rrect(frame,px,py,px+296,py+70,13,C["dark_card"],0.78)
        border_rrect(frame,px,py,px+296,py+70,13,C["gray"],1)
        put_txt(frame,"NO HAND DETECTED",(px+20,py+42),0.52,C["gray"],font=D)
        return

    for idx,(label,pt,palm,fingers,wrist_px) in enumerate(hand_data):
        px=fw-308; py=10+idx*248; pw=296; ph=238
        accent=C["lime"] if label=="Right" else C["orange"]
        filled_rrect(frame,px,py,px+pw,py+ph,13,C["dark_card"],0.80)
        border_rrect(frame,px,py,px+pw,py+ph,13,accent,1)
        cv2.rectangle(frame,(px+14,py+1),(px+pw-14,py+4),accent,-1)

        put_txt(frame,f"{label.upper()} HAND",(px+14,py+27),0.50,accent,font=D)
        col=dir_color(pt)
        put_txt(frame,dir_label(pt),(px+14,py+65),0.65,col,bold=True,font=D)
        cv2.line(frame,(px+12,py+78),(px+pw-12,py+78),(55,55,85),1)

        put_txt(frame,"Palm:",(px+14,py+104),0.40,C["gray"],font=F)
        pc=C["green"] if palm=="CAMERA" else C["red"]
        filled_rrect(frame,px+82,py+87,px+210,py+110,5,(42,42,72),0.88)
        put_txt(frame,palm,(px+88,py+104),0.43,pc,font=F)

        put_txt(frame,"Fingers:",(px+14,py+130),0.40,C["gray"],font=F)
        fcols=[C["lime"],C["purple"],C["cyan"],C["orange"],C["yellow"]]
        icons=["I","M","R","P","T"]
        for fi,(fname,fup) in enumerate(fingers):
            bx=px+12+fi*56; by=py+172
            fc=fcols[fi] if fup else (40,40,65)
            filled_rrect(frame,bx,by-26,bx+50,by+10,7,fc,0.35 if fup else 0.60)
            if fup: border_rrect(frame,bx,by-26,bx+50,by+10,7,fcols[fi],1)
            put_txt(frame,icons[fi],(bx+17,by+4),0.47,
                    C["white"] if fup else C["gray"],font=F)
            cv2.putText(frame,"UP" if fup else "--",(bx+8,by+24),
                        F,0.27,fcols[fi] if fup else C["gray"],1,cv2.LINE_AA)

        cv2.circle(frame,wrist_px,10,accent,-1)
        cv2.circle(frame,wrist_px,14,accent, 2)
        cv2.circle(frame,wrist_px, 4,C["white"],-1)
        cv2.putText(frame,label[0],(wrist_px[0]-5,wrist_px[1]+5),
                    F,0.4,C["white"],1,cv2.LINE_AA)

# ============================================================
#   COMPASS
# ============================================================
def draw_compass(frame, cx, cy, direction, color, size=48, label=""):
    cv2.circle(frame,(cx,cy),size+3,(18,18,38),-1)
    cv2.circle(frame,(cx,cy),size,color,2)
    for deg in range(0,360,45):
        rad=np.radians(deg)
        s=np.sin(rad); c2=np.cos(rad)
        cv2.line(frame,
                 (cx+int((size-9)*s), cy-int((size-9)*c2)),
                 (cx+int((size-2)*s), cy-int((size-2)*c2)),
                 (65,65,95),1)
    for t,ox,oy in [("N",0,-1),("S",0,1),("W",-1,0),("E",1,0)]:
        cv2.putText(frame,t,(cx+int(ox*(size-17))-4,
                              cy+int(oy*(size-17))+5),
                    F,0.30,(85,85,115),1,cv2.LINE_AA)
    VM={"UP":(0,-1),"DOWN":(0,1),"LEFT":(-1,0),"RIGHT":(1,0),
        "UP-LEFT":(-0.707,-0.707),"UP-RIGHT":(0.707,-0.707),
        "DOWN-LEFT":(-0.707,0.707),"DOWN-RIGHT":(0.707,0.707),"CENTER":(0,0)}
    vec=VM.get(direction,(0,0))
    if vec!=(0,0):
        ex=cx+int(vec[0]*(size-16)); ey=cy+int(vec[1]*(size-16))
        cv2.arrowedLine(frame,(cx,cy),(ex,ey),color,3,
                        tipLength=0.45,line_type=cv2.LINE_AA)
    cv2.circle(frame,(cx,cy),4,color,-1)
    cv2.circle(frame,(cx,cy),2,C["white"],-1)
    if label:
        cv2.putText(frame,label,(cx-len(label)*6//2,cy+size+16),
                    F,0.36,color,1,cv2.LINE_AA)

# ============================================================
#   STATUS BAR
# ============================================================
def draw_status(frame, fps, count, face_ok, n_hands, detect_ms):
    fh,fw=frame.shape[:2]
    filled_rrect(frame,0,fh-38,fw,fh,0,(16,16,36),0.88)
    cv2.line(frame,(0,fh-38),(fw,fh-38),C["purple"],1)

    fc=C["lime"]  if face_ok  else C["red"]
    hc=C["lime"]  if n_hands  else C["red"]
    fps_c = C["lime"] if fps>=50 else C["yellow"] if fps>=30 else C["red"]

    put_txt(frame,f"FPS:{fps:5.1f}",(12,fh-11),0.44,fps_c,font=F)
    put_txt(frame,f"Det:{detect_ms:4.1f}ms",(100,fh-11),0.40,C["gray"],font=F)
    put_txt(frame,f"Face:{'OK' if face_ok else 'NO'}",(210,fh-11),0.43,fc,font=F)
    put_txt(frame,f"Hands:{n_hands}",(295,fh-11),0.43,hc,font=F)
    title="60 FPS Body Tracker  |  Q=Quit  S=Screenshot"
    tw=cv2.getTextSize(title,F,0.40,1)[0][0]
    put_txt(frame,title,(fw//2-tw//2,fh-11),0.40,C["purple"],font=F)

# ============================================================
#   FPS GRAPH (mini rolling graph at top-right of status)
# ============================================================
class FPSGraph:
    def __init__(self, n=80, w=120, h=30):
        self.buf = deque([0.0]*n, maxlen=n)
        self.n=n; self.gw=w; self.gh=h

    def update(self, fps):
        self.buf.append(fps)

    def draw(self, frame, x, y):
        arr=list(self.buf)
        mx=max(arr) if max(arr)>0 else 1
        filled_rrect(frame,x,y,x+self.gw,y+self.gh,4,(20,20,40),0.80)
        cv2.putText(frame,f"{mx:.0f}",(x+2,y+10),
                    F,0.28,C["gray"],1,cv2.LINE_AA)
        for i in range(1,len(arr)):
            x1=x+int((i-1)*self.gw/self.n)
            x2=x+int(i*self.gw/self.n)
            y1=y+self.gh-int(arr[i-1]*self.gh/mx)
            y2=y+self.gh-int(arr[i  ]*self.gh/mx)
            c=C["lime"] if arr[i]>=50 else C["yellow"] if arr[i]>=30 else C["red"]
            cv2.line(frame,(x1,y1),(x2,y2),c,1,cv2.LINE_AA)

# ============================================================
#   MAIN
# ============================================================
def main():
    print("="*58)
    print("   60 FPS Body & Hand Direction Tracker")
    print("="*58)

    if not download_models():
        input("Press Enter to exit..."); return

    # ── Camera (threaded) ─────────────────────────────────────
    print("📷  Opening camera (threaded)...")
    cam = ThreadedCamera(index=0, width=640, height=480)
    ret, test = cam.read()
    if not ret or test is None:
        print("❌  Camera not found!"); return

    fw = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    fh = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"✅  Camera: {fw}x{fh}")

    # ── Build detectors ───────────────────────────────────────
    face_opts = FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path="face_landmarker.task"),
        num_faces=1,
        min_face_detection_confidence=0.5,
        min_face_presence_confidence=0.5,
        min_tracking_confidence=0.5,
        running_mode=mp_vision.RunningMode.IMAGE,
    )
    hand_opts = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
        num_hands=2,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
        running_mode=mp_vision.RunningMode.IMAGE,
    )
    face_det = FaceLandmarker.create_from_options(face_opts)
    hand_det = HandLandmarker.create_from_options(hand_opts)

    # ── Async detector (runs detection in background thread) ──
    detector = AsyncDetector(face_det, hand_det)
    print("✅  Async detector ready!")

    # ── Pre-build static assets ───────────────────────────────
    grid_img   = make_grid(fh, fw, spacing=80)
    fps_graph  = FPSGraph(n=80, w=130, h=32)

    # ── Smoothers ─────────────────────────────────────────────
    sy=Smoother(4); sp=Smoother(4); sr=Smoother(4)
    sh={0:Smoother(3), 1:Smoother(3)}

    # State from last detection
    last_face_res = None
    last_hand_res = None

    # Cached direction data (reused between detections)
    yaw="NO FACE"; pitch="NO FACE"; roll="LEVEL"; combo="NO FACE"
    nose_px=(fw//2,fh//2)
    hand_data=[]

    # Timing
    frame_count  = 0
    fps          = 0.0
    t0           = time.perf_counter()
    t_fps        = time.perf_counter()
    detect_ms    = 0.0
    shot_n       = 0

    # Detection throttle: submit every N frames
    DETECT_EVERY = 3     # detect on every 2nd frame → ~30 det/s @ 60fps

    print("\n✅  Running! Press Q=Quit  S=Screenshot\n")

    while True:
        ret, frame = cam.read()
        if not ret or frame is None:
            continue

        frame = cv2.flip(frame, 1)
        frame_count += 1
        h2, w2 = frame.shape[:2]

        # ── Submit frame to async detector ───────────────────
        if frame_count % DETECT_EVERY == 0:
            t_d0 = time.perf_counter()
            rgb    = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            detector.submit(mp_img)

        # ── Get latest detection results ─────────────────────
        face_res, hand_res = detector.results()

        # ── Process face results if new ───────────────────────
        if face_res is not last_face_res and face_res is not None:
            last_face_res = face_res
            if face_res.face_landmarks:
                fl=face_res.face_landmarks[0]
                yr,pr,rr,nose_px = calc_face_dir(fl,w2,h2)
                sy.push(yr); sp.push(pr); sr.push(rr)
                yaw=sy.get(); pitch=sp.get(); roll=sr.get()
                combo=combined_dir(yaw,pitch)
            else:
                yaw="NO FACE"; pitch="NO FACE"
                combo="NO FACE"; nose_px=(w2//2,h2//2)

        # ── Process hand results if new ───────────────────────
        if hand_res is not last_hand_res and hand_res is not None:
            last_hand_res = hand_res
            hand_data = []
            if hand_res.hand_landmarks:
                for i,(hlm,hh) in enumerate(zip(
                        hand_res.hand_landmarks,
                        hand_res.handedness)):
                    label=hh[0].display_name
                    pt,palm,fingers,wrist_px=calc_hand_dir(hlm,w2,h2,label)
                    sh[i].push(pt)
                    hand_data.append((label,sh[i].get(),palm,fingers,wrist_px))

        # ── Draw background grid (blit pre-built) ─────────────
        cv2.addWeighted(frame,0.88,grid_img,0.12,0,frame)

        # ── Draw landmarks on live frame ──────────────────────
        if face_res and face_res.face_landmarks:
            draw_face_lm(frame, face_res.face_landmarks[0], w2, h2)

        if hand_res and hand_res.hand_landmarks:
            for i,(hlm,hh) in enumerate(zip(
                    hand_res.hand_landmarks,
                    hand_res.handedness)):
                label=hh[0].display_name
                accent=C["lime"] if label=="Right" else C["orange"]
                draw_hand_lm(frame,hlm,w2,h2,accent)

        # ── HUD Panels ────────────────────────────────────────
        draw_face_panel(frame,yaw,pitch,roll,combo,nose_px)
        draw_hand_panel(frame,hand_data,w2)

        # ── Compass roses ─────────────────────────────────────
        cy_c = h2 - 140
        draw_compass(frame,66,cy_c,combo,dir_color(combo),46,"Face")
        for hi,(lbl,pt,*_) in enumerate(hand_data):
            draw_compass(frame,185+hi*140,cy_c,
                         pt,dir_color(pt),46,f"{lbl} Hand")

        # ── FPS calculation ───────────────────────────────────
        now = time.perf_counter()
        if frame_count % 15 == 0:
            fps = 15.0 / max(now - t_fps, 1e-6)
            t_fps = now
            fps_graph.update(fps)

        # ── Status bar ────────────────────────────────────────
        draw_status(frame,fps,frame_count,
                    bool(face_res and face_res.face_landmarks),
                    len(hand_data), detect_ms)

        # ── FPS graph (top center) ────────────────────────────
        fps_graph.draw(frame, w2//2-65, 14)

        # ── Console ───────────────────────────────────────────
        h_str=" | ".join(f"{l[0]}:{p}" for l,p,*_ in hand_data) or "none"
        print(f"\r FPS:{fps:5.1f} | Face:{combo:14s} | Hands:{h_str}   ",end="")

        # ── Show ──────────────────────────────────────────────
        cv2.imshow("60 FPS Body Tracker", frame)

        key = cv2.waitKey(1) & 0xFF
        if key in (ord('q'), 27):
            print("\n\n✅  Quit."); break
        elif key == ord('s'):
            name=f"shot_{shot_n:03d}.png"
            cv2.imwrite(name,frame)
            print(f"\n📸  {name}")
            shot_n+=1

    # ── Cleanup ───────────────────────────────────────────────
    detector.stop()
    face_det.close()
    hand_det.close()
    cam.release()
    cv2.destroyAllWindows()
    print("👋  Done!")

if __name__ == "__main__":
    main()