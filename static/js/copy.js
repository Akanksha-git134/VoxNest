const copyOriginal =
document.getElementById("copy-original");

const copyTranslation =
document.getElementById("copy-translation");

copyOriginal.addEventListener("click", async ()=>{

    const text =
    document.getElementById(
        "original-text"
    ).innerText;

    await navigator.clipboard.writeText(text);

    copyOriginal.innerHTML =
    "✅ Copied";

    setTimeout(()=>{

        copyOriginal.innerHTML =
        '<i class="bi bi-copy"></i> Copy';

    },2000);

});

copyTranslation.addEventListener("click", async ()=>{

    const text =
    document.getElementById(
        "translated-text"
    ).innerText;

    await navigator.clipboard.writeText(text);

    copyTranslation.innerHTML =
    "✅ Copied";

    setTimeout(()=>{

        copyTranslation.innerHTML =
        '<i class="bi bi-copy"></i> Copy';

    },2000);

});