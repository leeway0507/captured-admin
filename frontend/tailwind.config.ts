import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./node_modules/flowbite-react/**/*.js",
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            screens: {
                tb: "768px",
            },
            colors: {
                "main-black": "#323232",
                "sub-black": "#333D4B",
                "blue-black": "#6B7684",
                "deep-gray": "#D9D9D9",
                "light-gray": "#f5f5f5",
                "footer-gray": "#F9FAFB",
            },
            backgroundImage: {
                "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
                "gradient-conic": "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
            },
        },
    },
};
export default config;
