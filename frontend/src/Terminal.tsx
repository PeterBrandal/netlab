import { useEffect, useRef } from 'react'
import { Terminal as Xterm } from '@xterm/xterm'
import '@xterm/xterm/css/xterm.css'

export function Terminal() {

    const containerRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        const container = containerRef.current
        if (!container) return

        const term = new Xterm()
        const ws = new WebSocket('ws://localhost:3000/')

        term.onData(data => ws.send(data))

        ws.onmessage = (event) => term.write(event.data)

        term.open(container)

        return () => {
            term.dispose()
            ws.close()
        }
    },[]) 

    return <div ref={containerRef}></div>
}