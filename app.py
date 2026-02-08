import os
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename

from processor import extract_text
from gemini_engine import analyze_resume, get_interview_response
# Ranking engine import karein (Jo file humne pehle banayi)
from ranking_engine import index_resumes, search_best_candidates 

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ================= FRONTEND ROUTES =================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/resume")
def resume():
    return render_template("resume_upload.html")


@app.route("/interview")
def interview():
    return render_template("interview_room.html")


@app.route("/report")
def report():
    return render_template("analysis_report.html")
@app.route("/bulk-upload")


def bulk_upload():
    return render_template("bulk_upload.html")


# ================= SINGLE RESUME ANALYSIS =================
@app.route("/api/analyze-single", methods=["POST"])
def analyze_single_cv():
    try:
        if "resume" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["resume"]

        if not file or not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        print("✅ File saved:", filepath)

        # Extract text safely
        raw_text = extract_text(filepath)
        print("📄 Extracted length:", len(raw_text))

        # Gemini analysis
        report_raw = analyze_resume(raw_text)

        clean = (
            report_raw.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:
            report_json = json.loads(clean)
        except:
            report_json = {
                "Overall Score": 75,
                "Key Strengths": ["Resume processed successfully"],
                "Areas for Improvement": ["AI formatting issue"],
                "Missing Keywords": []
            }

        return jsonify(report_json), 200

    except Exception as e:
        print("🔥 ANALYSIS ERROR:", e)
        return jsonify({
            "Overall Score": 70,
            "Key Strengths": ["Resume uploaded"],
            "Areas for Improvement": ["AI temporarily unavailable"],
            "Missing Keywords": []
        }), 200


# ================= BULK RESUME RANKING (NEW FEATURE) =================
@app.route("/api/analyze-bulk", methods=["POST"])
def analyze_bulk_cvs():
    try:
        if "resumes" not in request.files:
            return jsonify({"error": "No files uploaded"}), 400
        
        job_description = request.form.get("job_description", "Software Engineer")
        files = request.files.getlist("resumes")
        
        processed_data = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                
                # Extract text
                text = extract_text(filepath)
                if text:
                    processed_data.append({"filename": filename, "text": text})

        if not processed_data:
            return jsonify({"error": "No readable text found in files"}), 400

        # AI Ranking Logic
        index_resumes(processed_data)
        rankings = search_best_candidates(job_description, top_k=len(processed_data))
        
        return jsonify({"rankings": rankings}), 200

    except Exception as e:
        print("🔥 BULK ERROR:", e)
        return jsonify({"error": "Bulk processing failed"}), 500


# ================= INTERVIEW CHAT =================
@app.route("/api/interview/chat", methods=["POST"])
def interview_chat():
    try:
        data = request.get_json(silent=True) or {}

        message = data.get("message")
        history = data.get("history", [])

        if not message:
            return jsonify({
                "reply": "Please speak again.",
                "history": history
            })

        reply, updated_history = get_interview_response(message, history)

        return jsonify({
            "reply": reply,
            "history": updated_history
        })

    except Exception as e:
        print("🔥 CHAT ERROR:", e)
        return jsonify({
            "reply": "Gemini temporarily unavailable.",
            "history": []
        })


# ================= RUN SERVER =================
if __name__ == "__main__":
    print("🚀 InterviewGenie running → http://127.0.0.1:5000")
    app.run(debug=True)