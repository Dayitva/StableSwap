// tailwind.config.js
module.exports = {
  purge: [],
  purge: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        dark: "#060606",
      },
      fontSize: {
        xxs: "0.6rem",
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
