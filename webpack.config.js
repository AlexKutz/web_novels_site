const path = require('path');

module.exports = {
    entry: './front-end/index.js',  // path to our input file
    output: {
        filename: 'index.js',  // output bundle file name
        path: path.resolve(__dirname, './static'),  // path to our Django static directory
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            // the react entry we addded above goes here
        ]
    },
    watch: true
}