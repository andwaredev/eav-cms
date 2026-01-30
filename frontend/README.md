# EAV CMS Frontend

React frontend for the EAV CMS application, built with Vite and TypeScript.

## Setup

### 1. Use Correct Node Version

```bash
nvm use
```

This reads the `.nvmrc` file and switches to Node 22.

### 2. Install Dependencies

```bash
yarn
```

## Running the Dev Server

```bash
yarn dev
```

The app will be available at http://localhost:5173

## Building for Production

```bash
yarn build
```

Output will be in the `dist/` directory.

## Project Structure

```
frontend/
├── src/
│   ├── App.tsx          # Main component
│   ├── main.tsx         # Entry point
│   ├── App.css          # App styles
│   └── index.css        # Global styles
├── public/              # Static assets
├── .nvmrc               # Node version
├── package.json         # Dependencies
├── vite.config.ts       # Vite configuration
├── tsconfig.json        # TypeScript config
└── eslint.config.js     # ESLint config
```

## Backend API

The backend API runs at http://localhost:8000. CORS is pre-configured to allow requests from this frontend.
