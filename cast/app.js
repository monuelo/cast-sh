Terminal.applyAddon(fullscreen);
Terminal.applyAddon(fit);
Terminal.applyAddon(webLinks);
Terminal.applyAddon(search);

const sessionId = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);

console.log("Session ID: " + sessionId);

const term = new Terminal({
  cursorBlink: true,
  macOptionIsMeta: true,
  scrollback: true
});

const MAX_LINES = 9999999;

term.open(document.getElementById("terminal"));

term.fit();

term.setOption("scrollback", MAX_LINES);

term.writeln("Welcome to cast.sh! - https://github.com/hericlesme/cast-sh - Press [Enter] to Start");

term.on("key", (key, ev) => {
  socket.emit("client-input", { input: key, session_id: sessionId });
});

const socket = io.connect("/cast", { query: `session_id=${sessionId}` });
const status = document.getElementById("status");

socket.on("client-output", function (data) {
  term.write(data.output);
});

socket.on("connect", () => {
  status.innerHTML =
    '<span class="connected">connected</span>';
});

socket.on("disconnect", () => {
  status.innerHTML =
    '<span class="disconnected">disconnected</span>';
});


window.addEventListener("resize", () => {
  term.fit();
});
