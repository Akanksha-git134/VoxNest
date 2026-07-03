from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import uuid

from services.translation_pipeline import TranslationPipeline
from services.elevenlabs_service import ElevenLabsService

ALLOWED_EXTENSIONS = {
    "webm",
    "wav",
    "mp3",
    "m4a"
}

def allowed_file(filename):

    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/translator")
def translator():
    return render_template("translator.html")
@app.route("/voices")
def voices():

    service = ElevenLabsService()

    voices = service.get_all_voices()

    return jsonify([

        {

            "voice_id": voice.voice_id,

            "name": voice.name

        }

        for voice in voices

    ])
@app.route("/upload-audio", methods=["POST"])
def upload_audio():

    if "audio" not in request.files:
        return jsonify({
            "success": False,
            "message": "No audio received."
        }), 400

    target_language = request.form.get(
        "target_language",
        "English"
    )
    
    voice_id = request.form.get(
        "voice_id"
    )

    audio = request.files["audio"]

    if audio.filename == "":
        return jsonify({
            "success": False,
            "error": "No file selected."
        }), 400

    if not allowed_file(audio.filename):

        return jsonify({

            "success": False,
            "error":
            "Unsupported file type. Please upload a     WEBM, WAV, MP3, or M4A file."

        }), 400

    filename = f"{uuid.uuid4().hex}_{secure_filename(audio.filename)}"
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    path = os.path.join(
       app.config["UPLOAD_FOLDER"],
       filename
    )

    audio.save(path)

    pipeline = TranslationPipeline()

    try:

        result = pipeline.process_audio(
            path,
            target_language,
            voice_id
        )

        return jsonify(result)

    except Exception as e:

        print("ERROR:", e)

        message = str(e)

        if "RESOURCE_EXHAUSTED" in message:

            message = (
            "Gemini API quota exceeded. "
            "Please try again in about a minute."
            )
        elif "payment_required" in message:
            message = (
            "Voice generation is temporarily unavailable."
            )


        elif "paid_plan_required" in message:

            message = (
            "This AI voice requires a paid ElevenLabs plan."
            )

        elif "No audio received" in message:

            message = (
            "No audio file was uploaded."
            )

        elif "ffmpeg" in message.lower():

            message = (
            "Unable to process the uploaded audio."
            )

        elif "timed out" in message.lower():
            message = (
                "The request took too long. Please try again."
            )

        return jsonify({

            "success": False,
            "error": message

        }), 500

if __name__ == "__main__":
    app.run(debug=True)