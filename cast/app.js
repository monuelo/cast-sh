Terminal.applyAddon(fullscreen);
Terminal.applyAddon(fit);
Terminal.applyAddon(webLinks);
Terminal.applyAddon(search);
const term = new Terminal({
  cursorBlink: true,
  macOptionIsMeta: true,
  scrollback: true
});
term.open(document.getElementById("terminal"));
term.fit();
term.resize(15, 50);
console.log(`size: ${term.cols} columns, ${term.rows} rows`);

term.fit();
term.write("Welcome to cast.sh!\nhttps://github.com/hericlesme/cast.sh\n");
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
    '<span style="background-color: lightgreen;">connected</span>';
});

socket.on("disconnect", () => {
  status.innerHTML =
    '<span style="background-color: #ff8383;">disconnected</span>';
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
