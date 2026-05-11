# cliente_visual.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Panel de Control WebSocket</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; padding: 40px; }
        .container { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        #estado { padding: 10px; border-radius: 5px; margin-bottom: 20px; font-weight: bold; text-align: center; }
        .online { background: #d4edda; color: #155724; }
        .offline { background: #f8d7da; color: #721c24; }
        #log { height: 300px; border: 1px solid #ddd; background: #1e1e1e; color: #d4d4d4; overflow-y: scroll; padding: 10px; font-family: monospace; border-radius: 5px; }
        .input-group { margin-top: 20px; display: flex; gap: 10px; }
        input { flex-grow: 1; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .msg-in { color: #b5cea8; } /* Color para mensajes recibidos */
        .msg-out { color: #569cd6; } /* Color para mensajes enviados */
    </style>
</head>
<body>
    <div class="container">
        <h2>Visual WebSocket Client</h2>
        <div id="estado" class="offline">Estado: Desconectado</div>
        
        <div id="log"></div>

        <div class="input-group">
            <input type="text" id="mensaje" placeholder="Escribe un mensaje..." onkeypress="if(event.key==='Enter') enviar()">
            <button onclick="enviar()">Enviar</button>
        </div>
    </div>

    <script>
        const logDiv = document.getElementById('log');
        const estadoDiv = document.getElementById('estado');
        const inputMsg = document.getElementById('mensaje');

        // 1. Iniciar conexión WebSocket
        const socket = new WebSocket('ws://localhost:8080');

        // Evento: Conexión abierta
        socket.onopen = () => {
            estadoDiv.innerText = "Estado: Conectado a ws://localhost:8080";
            estadoDiv.className = "online";
            addLog("SISTEMA: Conexión establecida", "yellow");
        };

        // Evento: Mensaje recibido
        socket.onmessage = (event) => {
            addLog("SRV: " + event.data, "msg-in");
        };

        // Evento: Error
        socket.onerror = (error) => {
            addLog("ERROR: No se pudo conectar al servidor", "#ff5555");
        };

        // Evento: Conexión cerrada
        socket.onclose = () => {
            estadoDiv.innerText = "Estado: Desconectado";
            estadoDiv.className = "offline";
            addLog("SISTEMA: Conexión cerrada", "yellow");
        };

        function enviar() {
            const texto = inputMsg.value;
            if (texto.trim() !== "" && socket.readyState === WebSocket.OPEN) {
                socket.send(texto);
                addLog("YO: " + texto, "msg-out");
                inputMsg.value = "";
            }
        }

        function addLog(txt, clase) {
            const p = document.createElement('div');
            p.className = clase;
            p.style.color = (clase.includes('msg')) ? '' : clase;
            p.innerText = `[${new Date().toLocaleTimeString()}] ${txt}`;
            logDiv.appendChild(p);
            logDiv.scrollTop = logDiv.scrollHeight;
        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(port=5000)