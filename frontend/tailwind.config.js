/** @type {import('tailwindcss').Config} */
module.exports = {
  purge: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",

    // Or if using `src` directory:
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    fontFamily: {
      sans: ["Inter", "sans-serif"],
      serif: ["Lora", "serif"],
    },
    extend: {
      colors: {
        light: {
          100: "#8C909B",
          200: "#9A9DA7",
          300: "#A5A8B1",
          400: "#B0B2BA",
          500: "#B5B8BF",
          600: "#C6C8CD",
          700: "#D3D5D9",
          800: "#E1E2E5",
          900: "#EBEBED",
        },
        dark: {
          100: "#151619",
          200: "#212226",
          300: "#2B2C31",
          400: "#393B41",
          500: "#51535C",
          600: "#646672",
          700: "#7F828F",
          800: "#8D8F9B",
          900: "#989AA4",
        },
      },
    },
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
};
