/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        pixel: ['"Press Start 2P"', 'cursive'],
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        brand: {
          bg: '#0a0a0a',
          card: '#111111',
          purple: '#7c3aed',
          'purple-light': '#8b5cf6',
          'purple-dim': '#4c1d95',
          border: '#2d1b69',
        },
      },
      boxShadow: {
        glow: '0 0 20px rgba(139, 92, 246, 0.4)',
        'glow-lg': '0 0 40px rgba(139, 92, 246, 0.5)',
        'glow-sm': '0 0 10px rgba(139, 92, 246, 0.3)',
      },
      animation: {
        'ping-slow': 'ping 2s cubic-bezier(0, 0, 0.2, 1) infinite',
        'pulse-slow': 'pulse 3s ease-in-out infinite',
        'glow-pulse': 'glowPulse 2s ease-in-out infinite alternate',
        'float': 'float 3s ease-in-out infinite',
        'slide-up': 'slideUp 0.4s ease-out',
        'fade-in': 'fadeIn 0.5s ease-out',
      },
      keyframes: {
        glowPulse: {
          from: { boxShadow: '0 0 10px rgba(124,58,237,0.5), 0 0 20px rgba(124,58,237,0.3)' },
          to: { boxShadow: '0 0 25px rgba(139,92,246,0.8), 0 0 50px rgba(139,92,246,0.5)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-8px)' },
        },
        slideUp: {
          from: { opacity: '0', transform: 'translateY(20px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          from: { opacity: '0' },
          to: { opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
