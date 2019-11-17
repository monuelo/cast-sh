const $ = document.querySelector.bind(document);
var notyf = new Notyf(); // Used for toast notifications
var currentSsid = '';
var tabs = []
var close = []
var closedTabs = []
var sessions = [];
var clickCount = 0;
var TID = 0;
const MAX_LINES = 9999999;
const status = document.getElementById("status");
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
  term.writeln("Welcome to cast.sh! - https://github.com/pod-cast/cast-sh - Press [Enter] to Start");

  term.on("key", (key, ev) => {
    // 'currentSsid' is global
    console.log(`client-input:: from: ${currentSsid})}`);
    socket.emit("client-input", { input: key, session_id: currentSsid });
    getTabBySSID(currentSsid).session.term.write(key);
    if(key.charCodeAt(0) == 13){
      getTabBySSID(currentSsid).session.term.write('\n');
    };
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
  currentSsid = tab.session.ssid;
  if(closedTabs.includes(tid)){
    console.log(socket);
    console.log("This session is closed");
  } else {
    console.log(`openSession:: ${JSON.stringify(currentSsid)}`)
    if (socket) {
      // To register new session on WebSocket server
      socket.emit("new-session", { session_id: currentSsid });
  
      // To mark current tab as the current session on WebSocket server
      socket.emit("client-input", { input: '', session_id: currentSsid })
    }
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
  tab.innerText = "tab " + (sessions.length + 1);
  tab.id = TID;
  tabs.push({ tid: TID, ssid: ssid, session: null });
  return tab;
}

const editTab = (tid) => {
  let tablink = document.getElementById(tid);
  tablink.contentEditable = true;
  tablink.focus();
  tablink.onkeydown = function(e) {
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
      tablink.contentEditable = false;
    }
  }
}

const closeButton = (ssid) => {
  let close_button = document.createElement("div");
  close_button.className = "close";
  close_button.innerText = "X";
  close_button.id = TID;

  close.push({ tid: TID, ssid: ssid });
  return close_button
}

const eventRegister = (tab, close) => {
  tab.addEventListener('click', (e) => {
    clickCount++;
    currentSsid = ssid;
    if (clickCount === 1) {
        singleClickTimer = setTimeout(function() {
            clickCount = 0;
            openSession(e.target.id);
        }, 150);
    } else if (clickCount === 2) {
        clearTimeout(singleClickTimer);
        clickCount = 0;
        if(closedTabs.includes(e.target.id)){
          //pass
        } else {
          focusStyle(e.target.id);
          editTab(e.target.id);
        }
    }
}, false);
  

  close.addEventListener('click', (e) => {
    console.log(e.target.id);
    closeSession(e.target.id);
    currentSsid = ssid;
  });
}

const appendTab = (ssid) => {
  let header = $(".header");
  let element = $("#create-tab");

  let tab = newTab(ssid);
  let close = closeButton(ssid);

  eventRegister(tab, close);

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
  console.log("Downloading log for " + ssid);
  fetch('/download/log_' + ssid + '.log')
    .then(function (response) {
      if (!response.ok) {
        throw Error(response.statusText);
      }
      response.blob().then(function (logBlob) {
        var blob = new Blob([logBlob], {
          type: 'application/octet-stream'
        });
        var link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = ssid + '.log';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      });
    })
    .catch(function (error) {
      console.log('Server error response: \n', error);
      notyf.error({
        message: 'No log available for download.',
        duration: 6000,
      });
    });
}

/*** Socket Settings ***/


socket = io.connect("/cast", { query: `session_id=${currentSsid}` });

socket.on("client-output", (data) => {
  let ssid = data.ssid;
  console.log("received: " + ssid);
  getTabBySSID(ssid).session.term.write(data.output);
});

socket.on("connect", () => {
  var addTab = document.getElementById("create-tab");
  addTab.style.display = "block";
  status.innerHTML =
    '<span class="connected">connected</span>';
});

socket.on("disconnect", () => {
  var addTab = document.getElementById("create-tab");
  addTab.style.display = "none";
  status.innerHTML =
    '<span class="disconnected">disconnected</span>';
  for(var i=0; i<tabs.length;i++){
    closeSession(String(i));
  };
});


window.addEventListener("resize", () => {
  getTabBySSID(currentSsid).session.term.fit();
});
