/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./logic/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        background: "oklch(0.995 0.003 95)",
        foreground: "oklch(0.24 0.03 200)",
        card: "oklch(1.0 0 95)",
        primary: "#2a52be",
        "primary-foreground": "oklch(0.98 0.01 200)",
        secondary: "oklch(0.975 0.006 95)",
        muted: "oklch(0.975 0.006 95)",
        "muted-foreground": "oklch(0.24 0.03 200 / 0.62)",
        "muted-primary": "oklch(0.55 0.12 255)",
        border: "oklch(0.24 0.03 200 / 0.12)",
        input: "oklch(0.24 0.03 200 / 0.16)",
        ring: "#2a52be",
        destructive: "oklch(0.55 0.2 27)",
      },
      fontFamily: {
        sans: ['"Inter"', "system-ui", "sans-serif"],
        display: ['"Inter"', "system-ui", "sans-serif"],
        serif: ['"Inter"', "system-ui", "sans-serif"],
        mono: ['"Inter"', "system-ui", "sans-serif"],
        "nunito-sans": ['"Nunito Sans"', "system-ui", "sans-serif"],
      },
      borderRadius: { "3xl": "24px" },
    },
  },
  plugins: [],
};
