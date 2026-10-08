import os
import cv2
import numpy as np
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import tempfile
import base64
import json

bp = Blueprint("vision", __name__)

def extract_features_from_video(video_path, sample_rate=2):
    \"\"\"
    Extract ORB features from video keyframes.
    sample_rate: number of frames per second to sample.
    \"\"\"
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps != fps: # Handle NaN
        fps = 30
        
    frame_interval = max(1, int(fps / sample_rate))
    
    orb = cv2.ORB_create(nfeatures=500)
    route_features = []
    
    frame_count = 0
    keyframe_index = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % frame_interval == 0:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Find keypoints and descriptors
            kp, des = orb.detectAndCompute(gray, None)
            
            if des is not None:
                # We need to serialize the descriptor (which is a numpy array) 
                # so it can be saved in the database as JSON.
                # Convert to lists for easier JSON storage
                des_list = des.tolist()
                
                # In a real app, we would store keypoint positions too, 
                # but let's keep it simple for now.
                
                route_features.append({
                    "keyframe_id": keyframe_index,
                    "timestamp_sec": frame_count / fps,
                    "descriptors": des_list
                })
                keyframe_index += 1
                
        frame_count += 1
        
    cap.release()
    return route_features

@bp.route("/vision/upload-route", methods=["POST"])
def upload_route_video():
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400
        
    video_file = request.files["video"]
    if video_file.filename == "":
        return jsonify({"error": "Empty filename"}), 400
        
    route_id = request.form.get("route_id", "default_route")
        
    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp:
        temp_path = temp.name
        video_file.save(temp_path)
        
    try:
        # Extract features
        features = extract_features_from_video(temp_path)
        
        # Here we would normally save 'features' to the database linked to 'route_id'
        # For example: mongo.db.routes.update_one({"route_id": route_id}, {"$set": {"vision_map": features}}, upsert=True)
        
        # Since we are using JsonDBAdapter, let's just return a summary
        return jsonify({
            "status": "success",
            "message": f"Successfully processed video for route {route_id}",
            "route_id": route_id,
            "keyframes_extracted": len(features)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
