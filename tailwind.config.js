/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'dark-bg': '#0b1020',
        'dark-card': 'rgba(255,255,255,0.04)',
        'dark-border': 'rgba(255,255,255,0.06)',
        'accent-teal': '#6ee7b7',
        'accent-blue': '#60a5fa',
        'text-muted': 'rgba(255,255,255,0.6)',
      },
    },
  },
  plugins: [],
};
