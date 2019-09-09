const $ = document.querySelector.bind(document);
var currentSession;
var tabs = []
var sessions = [];
var TID = 0;
const MAX_LINES = 9999999;

const generateSSID = () => (
  Math.random().toString(36).substring(2, 15)
  + Math.random().toString(36).substring(2, 15)
);

Terminal.applyAddon(fullscreen);
Terminal.applyAddon(fit);
Terminal.applyAddon(webLinks);
Terminal.applyAddon(search);




const termSetup = (term, ssid) => {

  term.open(document.getElementById(ssid));
  term.fit();
  term.setOption("scrollback", MAX_LINES);
  term.writeln("Welcome to cast.sh! - https://github.com/hericlesme/cast-sh - Press [Enter] to Start");

  term.on("key", (key, ev) => {
    socket.emit("client-input", { input: key, session_id: ssid });
  });

  getTabBySSID(ssid).session = currentSession;
}

const Cast = (ssid, tid) => {

  term = new Terminal({
    cursorBlink: true,
    macOptionIsMeta: true,
    scrollback: true
  });

  currentSession = { ssid: ssid, term: term, tid: tid };
  termSetup(term, ssid);
  return currentSession;
}

const resetStyle = (tid) => {
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
  console.log("oii:  " + getTabByTID(tid).ssid);
}



const openSession = (tid) => {
  resetStyle(tid);
  let tab = getTabByTID(tid);
  console.log(tab.ssid);
  // currentSession = tab.session;
  document.getElementById(tab.ssid).style.display = "block";
}


/*** HTML Elements ***/

const newTab = (ssid) => {
  let tab = document.createElement("div");
  tab.className = "tab";
  tab.innerText = ssid;
  tab.id = TID;

  tabs.push({ tid: TID, ssid: ssid, session: null });
  return tab;
}

const appendTab = (ssid) => {
  let header = $(".header");
  let element = $("#create-tab");

  let tab = newTab(ssid);
  tab.addEventListener('click', (e) => {
    console.log(e.target.id);
    openSession(e.target.id);
  })

  header.insertBefore(tab, element);
}

const appendContent = (ssid) => {
  let termContainer = document.getElementById("term-container");
  let content = document.createElement("div");
  content.className = "tabcontent";
  content.id = ssid;
  termContainer.appendChild(content);
}


/*** Create Tab ***/

const createTab = () => {
  let ssid = generateSSID();

  appendTab(ssid);
  appendContent(ssid);

  let term = Cast(ssid, ++TID);

  sessions.push(term);
  console.log(sessions);

  openSession(TID - 1);
}


/*** Utils ***/

const getTabByTID = (tid) => tabs.find(t => t.tid == tid);

const getTabBySSID = (ssid) => tabs.find(t => t.ssid == ssid);

createTab();


/*** Socket Settings ***/


const socket = io.connect("/cast", { query: `session_id=${currentSession.ssid}` });
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