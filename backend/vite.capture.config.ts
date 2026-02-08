import { resolve } from 'path';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
    root: 'src/renderer',
    resolve: {
        alias: {
            '@renderer': resolve(__dirname, 'src/renderer')
        }
    },
    plugins: [react()],
    server: {
        port: 5173,
        strictPort: true,
    }
});
