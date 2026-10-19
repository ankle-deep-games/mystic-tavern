import { createServer } from "node:http";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { Server } from "colyseus";
import { WebSocketTransport } from "@colyseus/ws-transport";
import cors from "cors";
import express from "express";
import { GameRoom } from "./GameRoom.js";

const port = Number(process.env.PORT ?? 2567);
const app = express();

app.use(cors({ origin: true, credentials: true }));
app.use(express.json());
app.get("/health", (_request, response) => response.json({ ok: true, service: "ankle-deep-games" }));

const webDist = fileURLToPath(new URL("../../web/dist", import.meta.url));
app.use(express.static(webDist));
app.get(/.*/, (request, response, next) => {
  if (request.path.startsWith("/matchmake")) return next();
  response.sendFile(path.join(webDist, "index.html"));
});

const httpServer = createServer(app);
const gameServer = new Server({ transport: new WebSocketTransport({ server: httpServer }) });
gameServer
  .define("party", GameRoom)
  .filterBy(["partyCode"]);

await gameServer.listen(port);
console.log(`Ankle Deep Games realtime server listening on http://localhost:${port}`);
