
// ===============================
// ELEMENTS
// ===============================
let currentAudio = null;
const startBtn = document.getElementById("start-record");
const stopBtn = document.getElementById("stop-record");
const restartBtn = document.getElementById("restart-record");

const timer = document.getElementById("recording-time");

const audioPlayer = document.getElementById("audio-player");

const previewCard = document.getElementById("audio-preview-card");

const downloadBtn = document.getElementById("download-recording");

const deleteBtn = document.getElementById("delete-recording");

// ===============================
// VARIABLES
// ===============================

let mediaRecorder;
let audioChunks = [];
let recordingStream;

let seconds = 0;
let timerInterval;

// ===============================
// TIMER
// ===============================

function updateTimer(){

    seconds++;

    let mins = Math.floor(seconds / 60);

    let secs = seconds % 60;

    timer.textContent =
        String(mins).padStart(2,"0") +
        ":" +
        String(secs).padStart(2,"0");

}

function startTimer(){

    seconds = 0;

    timer.textContent = "00:00";

    timerInterval = setInterval(updateTimer,1000);

}

function stopTimer(){

    clearInterval(timerInterval);

}

// ===============================
// START RECORDING
// ===============================

startBtn.addEventListener("click", async ()=>{

    try{

        recordingStream =
            await navigator.mediaDevices.getUserMedia({

                audio:true

            });

        mediaRecorder = new MediaRecorder(recordingStream);

        audioChunks = [];

        mediaRecorder.ondataavailable = e=>{

            audioChunks.push(e.data);

        };
        mediaRecorder.onstop = ()=>{

            const audioBlob = new Blob(audioChunks,{

                type:"audio/webm"

            });

            const audioURL = URL.createObjectURL(audioBlob);

            audioPlayer.src = audioURL;

            downloadBtn.href = audioURL;

            previewCard.style.display = "block";

            currentAudio = audioBlob;

        };

        mediaRecorder.start();

        startTimer();

        startBtn.disabled = true;

    }

    catch(err){

        alert("Microphone permission denied.");

    }

});

// ===============================
// STOP RECORDING
// ===============================

stopBtn.addEventListener("click", ()=>{

    if(mediaRecorder){

        mediaRecorder.stop();

        stopTimer();

        recordingStream
        .getTracks()
        .forEach(track=>track.stop());

        startBtn.disabled = false;

    }

});

// ===============================
// RESTART
// ===============================

restartBtn.addEventListener("click", ()=>{

    stopTimer();

    seconds = 0;

    timer.textContent = "00:00";

    audioChunks = [];

});

deleteBtn.addEventListener("click", () => {

    audioPlayer.src = "";

    previewCard.style.display = "none";

    currentAudio = null;

});

const uploadInput = document.getElementById("audio-upload");

const dropZone = document.getElementById("drop-zone");

uploadInput.addEventListener("change", function(){

    const file = this.files[0];

    if(!file) return;

    const url = URL.createObjectURL(file);

    audioPlayer.src = url;

    downloadBtn.href = url;

    previewCard.style.display = "block";

    currentAudio = file;

});

dropZone.addEventListener("dragover", function(e){

    e.preventDefault();

    dropZone.style.background="#ECF39E";

});

dropZone.addEventListener("dragleave", function(){

    dropZone.style.background="";

});

dropZone.addEventListener("drop", function(e){

    e.preventDefault();

    dropZone.style.background="";

    const file = e.dataTransfer.files[0];

    if(!file) return;

    const url = URL.createObjectURL(file);

    audioPlayer.src = url;

    downloadBtn.href = url;

    previewCard.style.display="block";

    currentAudio = file;

});

// ===============================
// SEARCHABLE LANGUAGE DROPDOWNS
// ===============================

new TomSelect("#source-language", {
    create: false,
    sortField: {
        field: "text",
        direction: "asc"
    },
    placeholder: "Search source language..."
});

new TomSelect("#target-language", {
    create: false,
    sortField: {
        field: "text",
        direction: "asc"
    },
    placeholder: "Search target language..."
});



