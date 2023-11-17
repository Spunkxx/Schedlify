/** @type {import('tailwindcss').Config} */
import aspectRatioPlugin from "@tailwindcss/aspect-ratio";
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [aspectRatioPlugin],
};
