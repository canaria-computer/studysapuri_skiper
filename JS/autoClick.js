function allRandomClick() {
  Array.from(document.querySelectorAll("[class*=TopicsPage__Main]  button"))
    .sort(() => Math.random() - Math.random())
    .forEach((each) => each.click());
}

function sendKeyClick() {
  document.querySelector("button[class*=RaisedButton]").click();
}

let click = setInterval(allRandomClick);
let send = setInterval(sendKeyClick, Math.random() * (10000 - 1000) + 1000);

function kill() {
  clearInterval(click);
  clearInterval(send);
}

function reStart() {
  return [setInterval(allRandomClick), setInterval(sendKeyClick, Math.random() * (10000 - 1000) + 1000)];
}

let count = 0;

document.addEventListener("keydown", (event) => {
  count++;

  if (event.code === "F8") {
    if (count % 2) {
      kill();
    } else {
      [click, send] = reStart();
    }
  }
  if (event.code === "F9") {
    kill();
    console.warn("Auto Click stop.");
    console.warn("To resume, call `reStat()` manually.");
  }
});
