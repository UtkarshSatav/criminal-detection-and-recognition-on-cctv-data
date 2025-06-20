import cv2
import requests

video_path = "cctv_video.mp4"
cap = cv2.VideoCapture(video_path)
frame_num = 0
fps = int(cap.get(cv2.CAP_PROP_FPS))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if frame_num % fps == 0:  # one frame per second
        _, img_jpg = cv2.imencode('.jpg', frame)
        files = {'image': img_jpg.tobytes()}

        # Detect faces
        r = requests.post("http://localhost:18081/face/detect", files=files)
        detections = r.json().get('faces', [])

        for face in detections:
            x1, y1, x2, y2 = map(int, face['bbox'])
            crop = frame[y1:y2, x1:x2]
            _, crop_jpg = cv2.imencode('.jpg', crop)
            match_r = requests.post("http://localhost:18081/face/search", files={"image": crop_jpg.tobytes()})
            match = match_r.json().get('results', [])[0]  # best match

            print(f"Frame {frame_num}: {match['name']} - Score: {match['score']:.2f}")

    frame_num += 1

cap.release()
