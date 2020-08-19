import React, { Component } from 'react';
import { Terminal, ITerminalAddon } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';

const className = require('classnames');

export interface IXtermProps extends React.DOMAttributes<{}> {
    onChange?: (e) => void;
    onInput?: (e) => void;
    addons?: ITerminalAddon[];
    onScroll?: (e) => void;
    onContextMenu?: (e) => void;
    options?: any;
    path?: string;
    value?: string;
    className?: string;
    style?: React.CSSProperties;
}

export interface IXtermState {
    isFocused: boolean;
}

export default class XTerm extends Component<IXtermProps, IXtermState> {
    xterm: Terminal;
    container!: HTMLDivElement;

    constructor(props: IXtermProps, context?: any) {
        super(props, context);
        this.xterm = new Terminal(this.props.options);
        this.state = {
            isFocused: false
        };
    }

    applyAddon(addon: ITerminalAddon) {
        this.xterm.loadAddon(addon);
    }

    componentDidMount() {
        const fitAddon = new FitAddon();

        const addons = [fitAddon]

        addons.forEach(addon => {
            this.xterm.loadAddon(addon);
        });

        fitAddon.fit();
        this.xterm.open(this.container);

        if (this.props.onContextMenu) {
            if (this.xterm.element)
                this.xterm.element.addEventListener('contextmenu', this.onContextMenu.bind(this));
        }

        if (this.props.onInput) {
            this.xterm.onData(this.onInput);
        }

        if (this.props.value) {
            this.xterm.write(this.props.value);
        }
    }

    shouldComponentUpdate(nextProps, nextState) {
        if (nextProps.hasOwnProperty('value') && nextProps.value !== this.props.value) {
            if (this.xterm) {
                this.xterm.clear();
                setTimeout(() => {
                    this.xterm.write(nextProps.value);
                }, 0)
            }
        }
        return false;
    }

    getTerminal() {
        return this.xterm;
    }

    write(data: any) {
        this.xterm && this.xterm.write(data);
    }

    writeln(data: any) {
        this.xterm && this.xterm.writeln(data);
    }

    focus() {
        if (this.xterm) {
            this.xterm.focus();
        }
    }

    onInput = data => {
        this.props.onInput && this.props.onInput(data);
    };

    resize(cols: number, rows: number) {
        this.xterm && this.xterm.resize(Math.round(cols), Math.round(rows));
    }

    setOption(key: string, value: boolean) {
        this.xterm && this.xterm.setOption(key, value);
    }

    refresh() {
        this.xterm && this.xterm.refresh(0, this.xterm.rows - 1);
    }

    onContextMenu(e) {
        this.props.onContextMenu && this.props.onContextMenu(e);
    }

    render() {
        const terminalClassName = className('ReactXTerm', this.state.isFocused ? 'ReactXTerm--focused' : null, this.props.className);
        return <div ref={ref => (this.container = ref as HTMLDivElement)} className={terminalClassName} />;
    }
}
export { Terminal, XTerm };