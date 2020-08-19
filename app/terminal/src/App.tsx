import React, { Component } from 'react';
import XTerm, { Terminal } from "./terminal";
import "xterm/css/xterm.css";
import './App.css';

interface IState {
}

interface IProps {
}

const MAX_LINES = 9999999;

class App extends Component<IProps, IState> {

  constructor(props: IProps, context?: any) {
    super(props, context);
    this.inputRef = React.createRef()
  }
  componentDidMount() {
    runFakeTerminal(this.inputRef.current!!);
  }

  private inputRef: React.RefObject<XTerm>;

  render() {
    return (
      <div className="App">
        <XTerm ref={this.inputRef}
          style={{
            overflow: 'hidden',
            position: 'relative',
            width: '100%',
            height: '100%'
          }} />
      </div>
    );
  }
}

function runFakeTerminal(xterm: XTerm) {
  const term: Terminal = xterm.getTerminal();
  var shellprompt = '$ ';

  function prompt() {
    xterm.write('\r\n' + shellprompt);
  }

  term.setOption("scrollback", MAX_LINES);
  term.writeln("Welcome to cast.sh! - https://github.com/tunl/cast-sh - Press [Enter] to Start");
  prompt();

  term.onKey(({ key, domEvent }) => {
    var printable = (
      !domEvent!!.altKey && !domEvent!!.ctrlKey && !domEvent!!.metaKey
    );

    if (domEvent!!.keyCode === 13) {
      prompt();
    } else if (printable) {
      xterm.write(key);
    }
  });

}

export default App;