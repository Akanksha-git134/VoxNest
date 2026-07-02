from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import uuid

from services.translation_pipeline import TranslationPipeline
from services.elevenlabs_service import ElevenLabsService

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

    audio = request.files["audio"]

    target_language = request.form.get(
        "target_language",
        "English"
    )
    
    voice_id = request.form.get(
        "voice_id"
    )
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
            voice_id,
        )

        return jsonify(result)

    except Exception as e:
        import traceback
        
        print("ERROR:", e)
        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)