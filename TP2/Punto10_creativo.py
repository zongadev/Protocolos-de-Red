from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UCA WebSocket Monitor</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent: #38bdf8;
            --text-main: #f1f5f9;
            --success: #22c55e;
            --danger: #ef4444;
        }

        body { 
            font-family: 'Inter', system-ui, sans-serif; 
            background-color: var(--bg-color); 
            color: var(--text-main);
            display: flex; justify-content: center; align-items: center;
            min-height: 100vh; margin: 0;
        }

        .dashboard {
            width: 90%; max-width: 800px;
            background: var(--card-bg);
            padding: 30px; border-radius: 24px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.1);
        }

        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
        
        h2 { margin: 0; font-weight: 700; letter-spacing: -1px; background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

        #status-pill {
            padding: 6px 16px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;
            transition: all 0.3s ease; text-transform: uppercase;
        }

        .online { background: rgba(34, 197, 94, 0.2); color: var(--success); border: 1px solid var(--success); box-shadow: 0 0 15px rgba(34, 197, 94, 0.3); }
        .offline { background: rgba(239, 68, 68, 0.2); color: var(--danger); border: 1px solid var(--danger); }

        #console {
            height: 350px; background: #000; border-radius: 12px;
            padding: 15px; overflow-y: auto; font-family: 'Fira Code', monospace;
            font-size: 0.9rem; border: 1px solid #334155; margin-bottom: 20px;
        }

        .msg { margin-bottom: 8px; border-left: 3px solid transparent; padding-left: 10px; animation: fadeIn 0.3s ease; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }

        .tx { border-color: var(--accent); color: var(--accent); }
        .rx { border-color: var(--success); color: var(--success); }
        .sys { border-color: #94a3b8; color: #94a3b8; font-style: italic; }

        .input-area { display: flex; gap: 12px; }

        input {
            flex: 1; background: #0f172a; border: 1px solid #334155;
            padding: 14px; border-radius: 10px; color: white; outline: none;
            transition: border 0.3s;
        }
        input:focus { border-color: var(--accent); box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2); }

        button {
            background: var(--accent); color: #000; border: none;
            padding: 0 25px; border-radius: 10px; font-weight: 700;
            cursor: pointer; transition: transform 0.2s, background 0.2s;
        }
        button:hover { background: #7dd3fc; transform: translateY(-2px); }
        button:active { transform: translateY(0); }

        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
    </style>
</head>
<body>

<div class="dashboard">
    <div class="header">
        <h2>UCA WebSocket Monitor</h2>
        <div id="status-pill" class="offline">Desconectado</div>
    </div>

    <div id="console"></div>

    <div class="input-area">
        <input type="text" id="userInput" placeholder="Enviar comando al servidor..." autocomplete="off">
        <button onclick="send()">ENVIAR</button>
    </div>
</div>

<script>
    let ws;
    const consoleDiv = document.getElementById('console');
    const statusPill = document.getElementById('status-pill');
    const input = document.getElementById('userInput');

    function connect() {
        ws = new WebSocket('ws://localhost:8080');

        ws.onopen = () => {
            statusPill.innerText = "En línea";
            statusPill.className = "online";
            addLog("Sistema", "Conexión establecida con el servidor 8080", "sys");
        };

        ws.onmessage = (e) => addLog("Servidor", e.data, "rx");

        ws.onclose = () => {
            statusPill.innerText = "Desconectado";
            statusPill.className = "offline";
            addLog("Sistema", "Conexión perdida. Reintentando...", "sys");
            setTimeout(connect, 3000); // Intenta reconectar cada 3 seg
        };
    }

    function send() {
        const msg = input.value;
        if (msg && ws.readyState === WebSocket.OPEN) {
            ws.send(msg);
            addLog("Tú", msg, "tx");
            input.value = "";
        }
    }

    function addLog(user, text, type) {
        const div = document.createElement('div');
        div.className = `msg ${type}`;
        const time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', second:'2-digit'});
        div.innerHTML = `<strong>[${time}] ${user.toUpperCase()}:</strong> ${text}`;
        consoleDiv.appendChild(div);
        consoleDiv.scrollTop = consoleDiv.scrollHeight;
    }

    input.addEventListener("keypress", (e) => { if(e.key === "Enter") send(); });

    connect();
</script>

</body>
</html>
    """

if __name__ == "__main__":
    app.run(port=5011, debug=True)