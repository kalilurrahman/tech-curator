# TechCurator Frontend

This is the frontend for the TechCurator application, built with [SvelteKit](https://kit.svelte.dev/) and styled with [Tailwind CSS](https://tailwindcss.com/). It functions as a Progressive Web App (PWA) to deliver a seamless news reading experience on both desktop and mobile devices.

## Features

- **Responsive Design**: Optimized for all screen sizes.
- **PWA Support**: Installable on devices, with offline capabilities via service workers.
- **Dynamic Content**: Fetches real-time news clusters from the backend API.
- **Zero-UI Philosophy**: Minimalist interface focused on content consumption.

## Project Structure

- `src/routes/`: Contains the application pages.
  - `+page.svelte`: The main landing page displaying the news feed.
  - `+layout.svelte`: The root layout component.
- `src/lib/`: Reusable components and utilities.
- `static/`: Static assets (images, icons, etc.).
- `service-worker.js`: Script for PWA functionality (caching, offline support).

## Prerequisites

- Node.js (v18 or later recommended)
- npm (or pnpm/yarn)

## Setup & Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Environment Variables:**
   The application expects the backend API URL. By default, it proxies requests in development or uses an environment variable.

   Create a `.env` file in the `frontend` directory:
   ```env
   PUBLIC_API_URL=http://localhost:8000
   ```

## Running the Application

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`.

## Building for Production

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with:

```bash
npm run preview
```

## PWA details

The application uses a service worker to cache assets and API responses, allowing it to load quickly and work offline. The manifest file is generated to allow installation on supported devices.
