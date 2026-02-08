/** @type {import('tailwindcss').Config} */
export default {
    content: [
        './src/renderer/index.html',
        './src/renderer/**/*.{js,ts,jsx,tsx}',
    ],
    theme: {
        extend: {
            backdropBlur: {
                xs: '2px',
            },
            animation: {
                'fade-in': 'fadeIn 0.5s ease-out forwards',
                'slide-in-bottom': 'slideInBottom 0.5s ease-out forwards',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
                slideInBottom: {
                    '0%': { transform: 'translateY(20px)', opacity: '0' },
                    '100%': { transform: 'translateY(0)', opacity: '1' },
                },
            },
        },
    },
    plugins: [],
}
