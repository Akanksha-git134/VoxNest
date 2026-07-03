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

    if (currentAudio.size < 10000) {

        alert(
            "Recording is too short. Please record at least 1 second."
        );

        return;
    } 

    try {

        showLoading();

        translateButton.disabled = true;
        
        updateLoading("📤 Uploading audio...", 10);
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
        
        console.log(
            "Selected Voice ID:",
            document.getElementById("voice-id").value
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

        updateLoading("🎵 Preparing audio...", 25);

        const fetchPromise = fetch("/upload-audio", {
            method: "POST",
            body: formData
        });

        const loadingMessages = [
            ["🎤 Transcribing speech...", 40],
            ["🌍 Translating...", 65],
            ["🗣️ Generating AI Voice...", 90]
        ];

        let index = 0;

        const loadingInterval = setInterval(() => {

            if (index < loadingMessages.length) {

                updateLoading(
                    loadingMessages[index][0],
                    loadingMessages[index][1]
                );

                index++;

            }

        }, 2000);

        const response = await Promise.race([

            fetchPromise,

            new Promise((_, reject) =>

                setTimeout(() =>

                    reject(
                        new Error(
                            "Request timed out. Please try again."
                        )
                    ),

               90000)

            )

        ]);

        clearInterval(loadingInterval);

        const result = await response.json();

        updateLoading("✅ Finished!", 100);

        await new Promise(resolve => setTimeout(resolve, 500));
        hideLoading();
        translateButton.disabled = false;

        if (!response.ok || !result.success) {

            alert(`❌ ${result.error}`);
            return;
        }

        document.getElementById("translation-results").style.display = "block";

        document.getElementById("original-text").innerText =
         result.transcript;

        document.getElementById("translated-text").innerText =
        result.translated_text;

       

        document.getElementById("detected-language").innerText =
         result.detected_language;
        
        const aiAudio =
        document.getElementById("translated-audio");

        aiAudio.src = result.voice_url;
        aiAudio.load();

        document.getElementById("download-ai-audio").href =
        result.voice_url;

        // ===============================
        // RESET FOR NEXT TRANSLATION
        // ===============================

        currentAudio = null;

        document.getElementById("audio-upload").value = "";

        document.getElementById("audio-player").src = "";

        document.getElementById("audio-preview-card").style.display = "none";

        document.getElementById("start-record").disabled = false;

        resetRecorder();
        
    } catch (error) {

        hideLoading();
        translateButton.disabled = false;

        console.error("JavaScript Error:", error);

        alert(
            error.message || "Something went wrong."
        );

    }

});