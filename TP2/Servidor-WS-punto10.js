const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

console.log("Servidor iniciado en ws://localhost:8080");

wss.on('connection', (ws) => {
    console.log("Cliente conectado");
    ws.send("Conexión exitosa con el servidor");

    ws.on('message', (data) => {
        console.log("Recibido:", data.toString());
        // Reenvía el mensaje al cliente (Eco)
        ws.send("Servidor dice: " + data);
    });
});