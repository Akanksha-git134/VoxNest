// ===============================
// LOADING ELEMENTS
// ===============================

const overlay = document.getElementById("loading-overlay");
const statusText = document.getElementById("loading-status");
const progressBar = document.getElementById("progress-bar");
const translateButton = document.getElementById("translate-btn");

// ===============================
// LOADING FUNCTIONS
// ===============================

function showLoading() {
    overlay.style.display = "flex";
    progressBar.style.width = "0%";
}

function hideLoading() {
    overlay.style.display = "none";
}

function updateLoading(text, percent) {
    statusText.innerHTML = text;
    progressBar.style.width = percent + "%";
}

// ===============================
// TRANSLATE BUTTON
// ===============================

translateButton.addEventListener("click", async () => {

    console.log("Translate button clicked!");

    if (!currentAudio) {
        alert("Please record or upload an audio file first.");
        return;
    }

    try {

        showLoading();

        updateLoading("🎤 Uploading Audio...", 25);

        const formData = new FormData();
        const targetLanguage =
        document.getElementById(
            "target-language"
        ).value;

        console.log("Target Language:", targetLanguage);

        formData.append(
            "target_language",
            targetLanguage
        );
        
        formData.append(
            "voice_id",
            document.getElementById("voice-id").value
        );

        formData.append(
            "audio",
            currentAudio,
            currentAudio.name || "recording.webm"
        );

        const response = await fetch("/upload-audio", {
        method: "POST",
        body: formData
        });
        
        const text = await response.text();

        console.log(text);

        if (!response.ok) {
            throw new Error(text);
        }

        const result = JSON.parse(text);

        updateLoading("📝 Transcribing Speech...", 70);

        updateLoading("🌍 Translating...", 90);

        hideLoading();
        if (!result.success) {

            alert("Translation failed.");

            return;

        }

        document.getElementById("translation-results").style.display = "block";

        document.getElementById("original-text").innerText =
         result.transcript;

        document.getElementById("translated-text").innerText =
        result.translated_text;

       

        document.getElementById("detected-language").innerText =
         result.detected_language;
        
        const audioPlayer =
        document.getElementById("translated-audio");

        audioPlayer.load();

        const aiAudio = document.getElementById("translated-audio");

        aiAudio.src = result.voice_url;
        aiAudio.load();

        document.getElementById        ("download-ai-audio").href =
        result.voice_url;
        
    } catch (error) {

        hideLoading();

        console.error("JavaScript Error:", error);

        alert(error.message);

    }

});