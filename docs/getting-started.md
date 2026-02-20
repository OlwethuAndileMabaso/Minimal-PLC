# Getting Started with Minimal-PLC

## Prerequisites

- **Node.js 20+** — [Download from nodejs.org](https://nodejs.org)
- **Git** — [Download from git-scm.com](https://git-scm.com)
- A modern browser (Chrome, Edge, Firefox)

---

## 1. Clone and Install

```bash
git clone https://github.com/OlwethuAndileMabaso/Minimal-PLC.git
cd Minimal-PLC
npm run install:all
```

This installs all dependencies for the root, client (Angular), and server (Node.js).

---

## 2. Running in Development

```bash
npm run dev
```

This starts both the Angular dev server and the Node.js API server concurrently:

| Service | URL |
|---|---|
| Angular Frontend | http://localhost:4200 |
| Node.js API | http://localhost:3000 |
| API Health Check | http://localhost:3000/api/health |

---

## 3. Opening the App

1. Open your browser at **http://localhost:4200**
2. You will see the **Minimal-PLC Welcome Screen**
3. Click **+ New Project** or navigate using the sidebar

---

## 4. Creating Your First Project

1. From the Welcome screen, click **+ New Project**
2. You will be taken to the Dashboard
3. Navigate to **Devices** and click **+ Add Device**
4. Enter your device details (IP address, protocol)
5. Once connected, go to **HMI Designer** and start building your screen

---

## 5. Building for Production

```bash
npm run build
```

The Angular app will be built into `client/dist/`. Set `NODE_ENV=production` and run the server to serve the built app.

```bash
NODE_ENV=production npm run server
```
