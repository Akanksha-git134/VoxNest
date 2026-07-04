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
    "m4a", 
    "ogg"
}

def allowed_file(filename):

    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )

pipeline = TranslationPipeline()
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
    print("=" * 60)
    print("Incoming filename:", audio.filename)
    print("=" * 60)

    if audio.filename == "":
        return jsonify({
            "success": False,
            "error": "No file selected."
        }), 400

    if not allowed_file(audio.filename):

        return jsonify({

            "success": False,
            "error":
            "Unsupported file type. Please upload a WEBM, WAV, MP3, or M4A file."

        }), 400

    filename = f"{uuid.uuid4().hex}_{secure_filename(audio.filename)}"
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    path = os.path.join(
       app.config["UPLOAD_FOLDER"],
       filename
    )

    audio.save(path)

    try:

        result = pipeline.process_audio(
            path,
            target_language,
            voice_id
        )

        return jsonify(result)

    except Exception as e:

        print("=" * 60)
        print("SERVER ERROR")
        print(type(e).__name__)
        print(e)
        print("=" * 60)

        message = str(e).strip()
        lower = message.lower()

        if "RESOURCE_EXHAUSTED" in lower:

            message = (
            "Gemini API quota exceeded. "
            "Please try again in about a minute."
            )
        elif "payment_required" in lower:
            message = (
            "Voice generation is temporarily unavailable."
            )


        elif "paid_plan_required" in lower:

            message = (
            "This AI voice requires a paid ElevenLabs plan."
            )

        elif "No audio received" in lower:

            message = (
            "No audio file was uploaded."
            )

        elif "ffmpeg" in lower:

            message = (
            "Unable to process the uploaded audio."
            )

        elif "timed out" in lower:
            message = (
                "The request took too long. Please try again."
            )

        return jsonify({

            "success": False,
            "error": message

        }), 500
    
    finally:

        if os.path.exists(path):
            os.remove(path)
if __name__ == "__main__":
    app.run(debug=True)