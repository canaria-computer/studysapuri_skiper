// ! 改行禁止
document.querySelector("video").volume = 0;
document.querySelector("video").playbackRate = 16;
document.querySelector("button[class*=bmpui]").click();
setInterval(() => { document.querySelector("video").volume = 0; document.querySelector("video").play(); }, 2000);
console.log("RUN");