async function loadVoices() {

    const response = await fetch("/voices");

    const voices = await response.json();

    const select =
    document.getElementById("voice-id");

    select.innerHTML = "";

    voices.forEach(voice => {

        select.innerHTML += `
            <option value="${voice.voice_id}">
                ${voice.name}
            </option>
        `;

    });

}

loadVoices();

const speedSlider = document.getElementById("voice-speed");
const speedValue = document.getElementById("speed-value");

speedSlider.addEventListener("input", () => {
    speedValue.innerText = speedSlider.value + "x";
});