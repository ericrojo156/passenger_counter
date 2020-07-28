process.env.NODE_ENV = 'production';
var debug = true;
var webpack = require('webpack');

module.exports = {
    context: __dirname,
    devtool: debug ? "inline-sourcemap": false,
    entry: ["babel-polyfill", "./artifacts/client.js"],
    resolve: {
        extensions: [".ts", ".tsx", ".js", ".json"]
    },
    module: {
        loaders: [
            {
                test: /\.js?$/,
                exclude: /(node_modules|bower_components)/,
                loader: 'babel-loader',
                query: {
                    presets: ['react', 'es2015', 'stage-0'],
                    plugins: ['react-html-attrs', 'transform-class-properties', 'transform-decorators-legacy']
                }
            }
        ]
    },
    output: {
        path: __dirname + "/artifacts",
        filename: "client.min.js"
    },
    plugins: debug ? [] : [
            new webpack.optimize.OccurrenceOrderPlugin(),
            new webpack.optimize.UglifyJsPlugin({ mangle: false, sourcemap: false }),
        ]
};
