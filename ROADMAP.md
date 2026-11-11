# Roadmap

A proposal, not a contract. The ordering principle: **every phase makes the
invisible visible, and nothing gets a visualization until I've seen the real bytes
behind it.** No animated cartoons of packets I never captured.

Each phase lists the React lesson it forces, because learning React by hand is a
goal in its own right and these problems get harder in a useful order.

---

## Phase 0 — A shell in the browser ✅

Done. Fastify + `@fastify/websocket` + `node-pty` on :3000, React + xterm.js on
:5173.

Already taught: the HTTP Upgrade handshake, why WebSocket exists at all, that a PTY
is a kernel object and not a program, and that `Origin` is a request header like any
other.

---

## Phase 1 — Make the terminal honest

The surface works but lies in several places. Fix it and the fixes teach protocol
design.

- Terminal resize. `cols: 80, rows: 24` is hardcoded, so `vim` and `htop` render
  wrong. Fixing it means sending a *resize* message over the same socket carrying
  keystrokes — so I have to invent a way to distinguish control from data. That is
  protocol design, and it is the same problem TCP solved with headers.
- The send-before-open race in `Terminal.tsx`.
- Bytes vs text. UTF-8 characters can split across chunk boundaries. What does that
  do to a WebSocket text frame, and whose job is reassembly?
- Real isolation. Right now a connection gets `bash` as me, with my environment.
  Replace the `Origin` check with something that actually constitutes a boundary.

**React lesson:** effects, refs, cleanup, and why `useEffect` runs twice in dev.

**Done when:** `vim` works, resize works, emoji survive, and the shell is no longer
my own account.

---

## Phase 2 — See the bytes

The most important phase. Capture real traffic and decode it **by hand** — no
dissector library, no Wireshark doing the thinking.

- Capture frames (`tcpdump -w`, then libpcap or raw `AF_PACKET` sockets).
- Write my own parsers: Ethernet → IPv4/IPv6 → TCP/UDP → application payload.
- Stream decoded frames to the browser; render a packet list and a byte-level
  header inspector.

**What it teaches:** that encapsulation is literally nested structs; network byte
order; why header fields are the widths they are; checksums; why the IPv4 header has
a length field *and* an options region.

**React lesson:** high-frequency streaming data. Hundreds of packets a second will
destroy a naive render. Virtualized lists, memoization, keeping state out of React
when it doesn't belong there.

**Done when:** I can point at any byte in a captured frame and say what it means
without looking it up.

---

## Phase 3 — Build the lab

This is where the name earns itself. Linux network namespaces let me build a lab of
hosts, switches and routers on one machine, for free.

- `ip netns`, `veth` pairs, a Linux bridge. Wire up two hosts that can ping each
  other, then a third that can't until I give it a route.
- A topology editor in the UI: define nodes and links, spawn the real namespaces
  behind them.
- A terminal per node (Phase 0 generalizes here — one PTY per namespace).
- Watch ARP happen. Watch a routing decision happen. Break them on purpose.

**Verified 2026-11-11:** WSL2 supports network namespaces — `net` is present in
`/proc/self/ns/` and `sudo ip netns add` succeeds. No Docker or VM required.

**What it teaches:** L2 vs L3 for real, ARP, routing tables, NAT, what a switch
actually does with a MAC table.

**React lesson:** graph editing, derived state, and many concurrent WebSockets.

**Done when:** I can draw a three-host network with a router in the browser and
ping across it.

---

## Phase 4 — Implement the protocols myself

Reading a protocol is not knowing it. Writing one is.

Pick in this order, each on raw sockets:

1. A DNS resolver — binary wire format, UDP, no connection state.
2. An HTTP/1.1 server on a bare TCP socket — parsing, framing, `Content-Length`,
   keep-alive.
3. Something TCP-shaped — handshake, sequence numbers, retransmission, a state
   machine that isn't a toy.

**What it teaches:** that protocols are state machines, and that the hard part is
never the happy path.

**Done when:** my DNS resolver answers correctly and my HTTP server serves the
frontend.

---

## Phase 5 — The teaching tool

Only now is there something worth handing to NTNU, because everything it shows is
backed by real captures from Phases 2–4.

- Step through a capture packet by packet. Scrub backwards.
- Generate sequence diagrams from real traffic — a TCP handshake drawn from the
  actual SYN.
- Layer view: peel encapsulation off one frame interactively.
- Guided scenarios: "break this route and watch what happens."

**React lesson:** animation, time-travel over a data set, routing, and the hardest
one — interface design for someone who doesn't already know the answer.

**Done when:** someone who doesn't know networking learns something from it without
me standing behind them.

---

## Deliberately not deciding yet

- Whether Phase 3 runs on namespaces, containers, or a VM. Phase 1 and 2 don't care.
- Persistence. No database until something genuinely needs to outlive a page reload.
- Deployment. This can stay localhost for a long time.
