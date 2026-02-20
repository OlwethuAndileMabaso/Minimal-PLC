#!/bin/bash
echo "Installing Minimal-PLC on macOS..."
which node || (echo "Node.js not found. Install from https://nodejs.org or via Homebrew: brew install node" && exit 1)
npm run install:all
echo "Done! Run: npm run dev"
