import os
import sys
import socket
import threading
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# Fetch environment parameters
NODE_ROLE = os.getenv("NODE_ROLE", "C_CONDUCTOR")
VERSION = os.getenv("PROTOCOL_VERSION", "5.0")
FEC_DELAY = os.getenv("FEC_DELAY_MS", "3")

# Global volatile telemetry tracking cache
latest_ingress_frames = []

def run_udp_sieve():
    """Background Sieve: Intercepts raw, high-velocity edge network telemetry loops"""
    print("[MSP/Kerbtap Sieve] Spawning network socket loop on port 9999/UDP...", flush=True)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind(('0.0.0.0', 9999))
        while True:
            data, addr = sock.recvfrom(1024)
            payload = data.decode('utf-8', errors='ignore').strip()
            
            log_line = f"Address: {addr[0]}:{addr[1]} | Payload: {payload}"
            print(f"[006 CHROMALON FORGE - RAW INGRESS] {log_line}", flush=True)
            
            # Push raw telemetry frames directly into memory pool
            global latest_ingress_frames
            latest_ingress_frames.append(log_line)
            if len(latest_ingress_frames) > 10:
                latest_ingress_frames.pop(0)
                
    except Exception as e:
        print(f"[MSP/Kerbtap Critical Error] Network loop failure: {e}", file=sys.stderr, flush=True)

@app.route('/api/telemetry')
def api_telemetry():
    return jsonify({
        "node_status": "INGRESS_SATIATION",
        "data_buffer": "PLENTY",
        "fec_shield_delay": f"{FEC_DELAY}ms",
        "memory_spool": "/tmp/kerbtap-spool",
        "active_frames": latest_ingress_frames
    })


@app.route('/api/provision_test_account', methods=['POST'])
def provision_test_account():
    """
    Enables the mobile phone webapp interface to pass temporary, short-lived 
    test tokens down to the FUSE driver layer for instant network verification loops.
    """
    from flask import request
    request_data = request.get_json() or {}
    
    temp_user = request_data.get("test_username", "anonymous")
    temp_group = request_data.get("test_group", "alt.test")
    
    # Dynamically inject the temporary runtime markers into the system context
    os.environ["USENET_USER"] = temp_user
    os.environ["USENET_GROUP"] = temp_group
    
    print(f"[006 CHROMALON FORGE] WebApp Handshake: Provisioned transient test group reference: {temp_group}", flush=True)
    return jsonify({
        "status": "PROVISION_SUCCESS",
        "active_mesh_target": temp_group,
        "mode": "DEMO_LOOPBACK_ACTIVE"
    })

@app.route('/')
def dashboard():
    # Embedding the client-side show-and-tell interface directly to keep the deployment completely self-contained
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>006 CHROMALON FORGE // MSP/Kerbtap Sandbox</title>
        <style>
            body { background-color: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 25px; }
            .box { border: 1px solid #ffb300; background-color: #161b22; padding: 20px; box-shadow: 0 0 15px rgba(255,179,0,0.1); }
            h1, h3 { color: #ffb300; margin-top: 0; }
            .badge { display: inline-block; padding: 4px 10px; font-size: 11px; font-weight: bold; background: #ffb300; color: #0d1117; margin-right: 5px; border-radius: 2px; }
            .entropy-monitor { font-size: 12px; background: #010409; padding: 12px; color: #39ff14; overflow-x: auto; margin-top: 15px; min-height: 24px; }
            .terminal { background: #010409; border: 1px solid #30363d; padding: 15px; font-size: 12px; color: #58a6ff; height: 150px; overflow-y: auto; }
            .story { border-left: 3px solid #ffb300; padding-left: 15px; font-style: italic; color: #8b949e; margin: 15px 0; }
        </style>
        <script>
            // Client-Side WebAssembly Simulation: Building crypto keyspaces directly out of thin air via browser interactions
            let streamBuffer = [];
            window.addEventListener('mousemove', (e) => {
                const tick = Date.now() % 1000;
                const mathematicalChaos = (e.clientX * e.clientY * tick) % 0xFFFFFF;
                if (streamBuffer.length > 4) streamBuffer.shift();
                streamBuffer.push("0x" + mathematicalChaos.toString(16).toUpperCase().padStart(6, '0'));
                document.getElementById('entropy').innerText = "STARLINK_ENTROPY_STREAM: " + streamBuffer.join(" <-> ");
            });

            // Poll the daemon API to update our container spool metrics live
            setInterval(async () => {
                try {
                    let response = await fetch('/api/telemetry');
                    let data = await response.json();
                    let logBox = document.getElementById('log-box');
                    if (data.active_frames.length === 0) {
                        logBox.innerHTML = "<i>Awaiting incoming UDP telemetry stream on port 9999...</i>";
                    } else {
                        logBox.innerHTML = data.active_frames.map(f => `<div>${f}</div>`).join('');
                    }
                } catch (err) { console.error("API link disrupted", err); }
            }, 1000);
        </script>
    </head>
    <body>
        <div class="box">
            <h1>⚓ 006 CHROMALON FORGE</h1>
            <div>
                <span class="badge">PROTOCOL: MSP/Kerbtap v{{ version }}</span>
                <span class="badge" style="background:#58a6ff; color:#0d1117;">ROLE: {{ role }}</span>
                <span class="badge" style="background:#238636; color:#ffffff;">SPOOL: tmpfs RAM</span>
            </div>
            
            <div class="story">
                "We are spinning up the volatile memory sandboxes. Once compiled as a raw WebAssembly asset, the client browser becomes an untouchable network point—shuffling metadata packets through the spool before an adversary's disk tracking can even register the frame footprint."
            </div>

            <h3>🌐 WebAssembly Client-Side Entropy (Move Mouse)</h3>
            <div id="entropy" class="entropy-monitor">STARLINK_ENTROPY_STREAM: INITIALIZING_LOCAL_HANDSHAKE_COORDINATES...</div>

            <h3 style="margin-top: 20px;">📥 Container Ingress Frame Cache (Port 9999/UDP)</h3>
            <div id="log-box" class="terminal">Loading streaming node frames...</div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, version=VERSION, role=NODE_ROLE)

if __name__ == '__main__':
    print("[006 CHROMALON FORGE] Initializing main system orchestration layers...", flush=True)
    
    # Run our background UDP loopback catcher thread
    net_thread = threading.Thread(target=run_udp_sieve, daemon=True)
    net_thread.start()
    
    # Launch user workspace server
    print("[006 CHROMALON FORGE] Firing up user-facing server on port 8080...", flush=True)
    app.run(host='0.0.0.0', port=8080, debug=False)
