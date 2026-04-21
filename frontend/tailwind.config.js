/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#1a5c38',
          light: '#2d8a56',
          dark: '#0f3d24',
        },
      },
    },
  },
  plugins: [],
}
