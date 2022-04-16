const path = require('path');

module.exports = {
    context: path.resolve(__dirname, './front-end'),
    entry: {
        novel: './index.js',
        reader: './reader.js'
    },
    output: {
        filename: '[name].js',
        path: path.resolve(__dirname, './static'),
        library: "[name]"
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
        ]
    },
    watch: true
}