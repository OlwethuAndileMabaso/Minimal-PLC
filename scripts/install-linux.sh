#!/bin/bash
echo "Installing Minimal-PLC..."
which node || (echo "Node.js not found. Install: https://nodejs.org" && exit 1)
npm run install:all
echo "Done! Run: npm run dev"
