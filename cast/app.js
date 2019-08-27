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

term.setOption("scrollback", MAX_LINES);

term.writeln("Welcome to cast.sh! - https://github.com/hericlesme/cast.sh - Press [Enter] to Start");

term.on("key", (key, ev) => {
  socket.emit("client-input", { input: key });
});

const socket = io.connect("/cast");
const status = document.getElementById("status");

socket.on("client-output", function (data) {
  console.log("new output", data);
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
  console.log('fitting');
  term.fit();
});