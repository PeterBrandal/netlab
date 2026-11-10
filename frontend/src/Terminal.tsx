import { useEffect, useRef } from 'react'
import { Terminal as Xterm } from '@xterm/xterm'
import '@xterm/xterm/css/xterm.css'

export function Terminal() {

    const containerRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        const container = containerRef.current
        if (!container) return

        const term = new Xterm()
        term.open(container)
        term.write('hello from xterm\r\n')

        return () => {
            term.dispose()
        }
    },[]) 

    return <div ref={containerRef}></div>
}