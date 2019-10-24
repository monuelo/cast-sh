const $ = document.querySelector.bind(document);
var currentSsid = '';
var tabs = []
var close = []
var closedTabs = []
var sessions = [];
var TID = 0;
const MAX_LINES = 9999999;
let socket;

const generateSSID = () => (
  Math.random().toString(36).substring(2, 15)
  + Math.random().toString(36).substring(2, 15)
);

Terminal.applyAddon(fullscreen);
Terminal.applyAddon(fit);
Terminal.applyAddon(webLinks);
Terminal.applyAddon(search);




const termSetup = (term, ssid, newCurrentSession) => {

  term.open(document.getElementById(ssid));
  term.fit();
  term.setOption("scrollback", MAX_LINES);
  term.writeln("Welcome to cast.sh! - https://github.com/hericlesme/cast-sh - Press [Enter] to Start");

  term.on("key", (key, ev) => {
    // 'currentSsid' is global
    console.log(`client-input:: from: ${currentSsid})}`);
    socket.emit("client-input", { input: key, session_id: currentSsid });
  });

  getTabBySSID(ssid).session = newCurrentSession;
}

const Cast = (ssid, tid) => {

  let term = new Terminal({
    cursorBlink: true,
    macOptionIsMeta: true,
    scrollback: true
  });

  let newCurrentSession = { ssid: ssid, term: term, tid: tid };
  termSetup(term, ssid, newCurrentSession);
  return newCurrentSession;
}

const focusStyle = (tid) => {
  let i, tabcontent, tablinks, logger;
  let tab = getTabByTID(tid);
  logger = document.getElementById("downloadLog");
  tabcontent = document.getElementsByClassName("tabcontent");

  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  tablinks = document.getElementsByClassName("tab");

  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].classList.remove('active');
  }

  let tablink = document.getElementById(tid);
  if (closedTabs.includes(tid)) {
    tablink.style.backgroundColor = "red";
    tablink.style.color = "white";
    logger.style.display = "block";
    document.getElementById(tab.ssid).style.display = "none";
  }
  else {
    tablink.classList.add('active');
    logger.style.display = "none";
    document.getElementById(tab.ssid).style.display = "block";
  }
  console.log("Session ID:  " + getTabByTID(tid).ssid);
}

const openSession = (tid) => {
  let tab = getTabByTID(tid);
  focusStyle(tid);
  console.log(tab.ssid);
  // currentSession = tab.session;
  currentSsid = tab.session.ssid;
  // document.getElementById(tab.ssid).style.display = "block";
  console.log(`openSession:: ${JSON.stringify(currentSsid)}`)
  if (socket) {
    // To register new session on WebSocket server
    socket.emit("new-session", { session_id: currentSsid });

    // To mark current tab as the current session on WebSocket server
    socket.emit("client-input", { input: '', session_id: currentSsid })
  }
}

const closeSession = (tid) => {
  if (closedTabs.includes(tid)) {
    //pass
  }
  else {
    console.log("Closing the tab " + tid);

    let tablink = document.getElementById(tid);
    tablink.innerText = "[closed] " + tablink.innerText;
    tablink.contentEditable = false;
    let close = tablink.nextElementSibling;
    close.parentElement.removeChild(close);

    closedTabs.push(tid);
    focusStyle(tid);
  }

}



/*** HTML Elements ***/

const newTab = (ssid) => {
  let tab = document.createElement("div");
  tab.className = "tab";
  tab.contentEditable = true;
  tab.innerText = "tab " + (sessions.length + 1);
  tab.id = TID;
  tab.onkeydown = function(e) {
    console.log('keydown');
    if (!e) {
      e = window.event;
    }
    var keyCode = e.which || e.keyCode,
      target = e.target || e.srcElement;

    if (keyCode === 13 && !e.shiftKey) {
      console.log('Just enter');
      if (e.preventDefault) {
        e.preventDefault();
      } else {
        e.returnValue = false;
      }
      target.blur();
    }
  }


  tabs.push({ tid: TID, ssid: ssid, session: null });
  return tab;
}

const closeButton = (ssid) => {
  let close_button = document.createElement("div");
  close_button.className = "close";
  close_button.innerText = "X";
  close_button.id = TID;

  close.push({ tid: TID, ssid: ssid });
  return close_button
}

const appendTab = (ssid) => {
  let header = $(".header");
  let element = $("#create-tab");

  let tab = newTab(ssid);
  let close = closeButton(ssid);
  tab.addEventListener('click', (e) => {
    console.log(e.target.id);
    openSession(e.target.id);
    currentSsid = ssid;
  })

  close.addEventListener('click', (e) => {
    console.log(e.target.id);
    closeSession(e.target.id);
    currentSsid = ssid;
  })

  header.insertBefore(tab, element);
  header.insertBefore(close, element);
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
  return ssid;
}


/*** Utils ***/

const getTabByTID = (tid) => tabs.find(t => t.tid == tid);

const getTabBySSID = (ssid) => tabs.find(t => t.ssid == ssid);

currentSsid = createTab();

function downloadLog(ssid = currentSsid) {
  console.log(ssid);
  document.getElementById("downloadLog").href = "/download/" + ssid + ".txt";
}

/*** Socket Settings ***/


socket = io.connect("/cast", { query: `session_id=${currentSsid}` });
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
  getTabBySSID(currentSsid).session.term.fit();
});
