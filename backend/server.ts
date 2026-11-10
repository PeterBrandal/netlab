import Fastify from 'fastify'
import websocket from '@fastify/websocket'
import * as pty from 'node-pty'



const fastify = Fastify({
    logger: true
})

await fastify.register(websocket)

fastify.register(async function (fastify) {
    fastify.get('/', { websocket: true }, (socket, req) => {

        const shell = pty.spawn('bash', [], {
            name: 'xterm-256color',
            cols: 80,
            rows: 24,
            cwd: process.env.HOME,
            env: process.env,
        })

        socket.on('message', m => {
            shell.write(m.toString())
        })

        socket.on('close', () => {
            shell.kill()
        })

        shell.onData(data => socket.send(data))

        shell.onExit(() => socket.close())

    })
})

fastify.listen({ port: 3000 }, err => {
    if (err) {
        fastify.log.error(err)
        process.exit(1)
    }
})