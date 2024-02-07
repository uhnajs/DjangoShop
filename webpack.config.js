const path = require('path');

module.exports = {
    entry: './src/index.js', // ścieżka do Twojego głównego pliku JavaScript
    output: {
        path: path.resolve(__dirname, 'static'), // katalog statyczny Django
        filename: 'bundle.js', // nazwa pliku wynikowego
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader'],
            },
        ],
    },
};
