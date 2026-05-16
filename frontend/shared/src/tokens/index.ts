// Design tokens — colours, spacing, typography — shared across portals.
// Tokens here are CSS-friendly primitives, not component definitions.

export const tokens = {
  color: {
    // Outcome colours per CLAUDE.md Part 6.1 (color-code matrix).
    outcomeGreen: "#1e8e3e",
    outcomeAmber: "#f9ab00",
    outcomeYellow: "#fbbc04",
    outcomeRed: "#d93025",
  },
  spacing: {
    unit: 4, // px — base spacing unit
  },
} as const;
