var currentSession;

Terminal.applyAddon(fullscreen);
Terminal.applyAddon(fit);
Terminal.applyAddon(webLinks);
Terminal.applyAddon(search);

const MAX_LINES = 9999999;

const generateSSID = () => (
  Math.random().toString(36).substring(2, 15)
  + Math.random().toString(36).substring(2, 15)
);

const termSetup = (term, ssid) => {
  currentSession.term.open(document.getElementById(ssid));
  currentSession.term.fit();
  currentSession.term.setOption("scrollback", MAX_LINES);
  currentSession.term.writeln("Welcome to cast.sh! - https://github.com/hericlesme/cast-sh - Press [Enter] to Start");
  getTabBySSID(ssid).session = currentSession;
  console.log(term);
  console.log(currentSession.ssid);
}

const Cast = (ssid, tid, term) => {
  this.tid = tid;
  this.term = term;
  this.ssid = ssid;

  term.on("key", (key, ev) => {
    socket.emit("client-input", { input: key, session_id: sessionId });
  });

  currentSession = { ssid: ssid, term: term };
  getTabBySSID(ssid).session = currentSession;
  termSetup(term, ssid);

  return this.ssid;
}

var tabs = []
var TID = 0;

// const term = new Terminal({
//   cursorBlink: true,
//   macOptionIsMeta: true,
//   scrollback: true
// });

// termSetup(term);


const openSession = (tid) => {
  let i, tabcontent, tablinks;

  tabcontent = document.getElementsByClassName("tabcontent");

  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  tablinks = document.getElementsByClassName("tab");

  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].style.backgroundColor = "";
    tablinks[i].style.color = "white";
  }

  let tablink = document.getElementById(tid);
  tablink.style.backgroundColor = "greenyellow";
  tablink.style.color = "black";

  let tab = getTabByTID(tid);
  console.log(tab);
  currentSession = tab.session;
  console.log(tab.ssid);
  document.getElementById(tab.ssid).style.display = "block";
}

const newTab = (ssid) => {
  let tab = document.createElement("div");
  tab.className = "tab";
  tab.innerText = ssid;
  tab.id = TID;

  tabs.push({ tid: TID, ssid: ssid, session: null });
  return tab;
}

const createTab = () => {
  let ssid = generateSSID();

  let termContainer = document.getElementById("term-container");
  let header = document.getElementsByClassName("header")[0];
  let element = document.getElementById("create-tab");
  let tab = newTab(ssid);
  tab.addEventListener('click', (e) => {
    console.log(e.target.id);
    openSession(e.target.id);
  })
  header.insertBefore(tab, element);

  let content = document.createElement("div");
  content.className = "tabcontent";
  content.id = ssid;
  termContainer.appendChild(content);


  Cast(ssid, ++TID, new Terminal({
    cursorBlink: true,
    macOptionIsMeta: true,
    scrollback: true
  }));

  openSession(TID - 1);
}



/*** Utils ***/

const getTabByTID = (tid) => tabs.find(t => t.tid == tid);

const getTabBySSID = (ssid) => tabs.find(t => t.ssid = ssid);

createTab();


/*** Socket Settings ***/


const socket = io.connect("/cast", { query: `session_id=${sessionId}` });
const status = document.getElementById("status");

socket.on("client-output", (data) => {
  let ssid = data.ssid;
  console.log("received: " + ssid);
  getTabBySSID(ssid).session.term.write(data.output);
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
  currentSession.term.fit();
});