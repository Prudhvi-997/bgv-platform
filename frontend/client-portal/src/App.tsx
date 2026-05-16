import React from "react";

// Client Portal root shell. Per CLAUDE.md Part 4.1 each portal is an
// independently deployable React app. This shell will hold the
// portal's routes; routes for other portals never appear here.
export default function App() {
  return (
    <main>
      <h1>KCheck — Client Portal</h1>
      <p>Portal scaffold. Talks to <code>/api/client/</code>.</p>
    </main>
  );
}
