/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "secondary-light": "#606D7B",
        "secondary-dark": "#FFFFFF99",
        cashback: "#B13430",
        discount: "#F19F44",
        black: "#171717",
      },
    },
  },
  plugins: [],
};
