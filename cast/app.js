Terminal.applyAddon(fullscreen);
Terminal.applyAddon(fit);
Terminal.applyAddon(webLinks);
Terminal.applyAddon(search);
const term = new Terminal({
  cursorBlink: true,
  macOptionIsMeta: true,
  scrollback: true

});

const MAX_LINES = 9999999;

term.open(document.getElementById("terminal"));
term.fit();
console.log(`size: ${term.cols} columns, ${term.rows} rows`);

term.fit();
term.setOption("scrollback", MAX_LINES);
term.writeln("Welcome to cast.sh! - https://github.com/hericlesme/cast.sh - Press [Enter] to Start");
term.on("key", (key, ev) => {
  console.log("pressed key", key);
  console.log("event", ev);
  socket.emit("pty-input", { input: key });
});

const socket = io.connect("/pty");
const status = document.getElementById("status");

socket.on("pty-output", function(data) {
  console.log("new output", data);
  term.write(data.output);
});

socket.on("connect", () => {
  fitToscreen();
  status.innerHTML =
    '<span class="connected">connected</span>';
});

socket.on("disconnect", () => {
  status.innerHTML =
    '<span class="disconnected">disconnected</span>';
});

function fitToscreen() {
  term.fit();
  socket.emit("resize", { cols: term.cols, rows: term.rows });
}

function debounce(func, wait_ms) {
  let timeout;
  return function(...args) {
    const context = this;
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(context, args), wait_ms);
  };
}

const wait_ms = 50;
window.onresize = debounce(fitToscreen, wait_ms);
