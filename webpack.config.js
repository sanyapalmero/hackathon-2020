const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");

const BundleTracker = require('./webpack-ext/bundler-tracker');

module.exports = {
    mode: "development",
    cache: false,
    entry: {
        'main': "./static/ts/main.ts",
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/
            },
            {
                test: /\.scss$|\.css$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: "[name]-[fullhash:16].css"
                        }
                    },
                    'extract-loader',
                    "css-loader",
                    "resolve-url-loader",
                    "sass-loader?sourceMap",
                ]
            },
            {
                test: /\.eot$|\.svg$|\.ttf$|\.woff$|\.woff2$|\.png$|\.gif$/,
                use: {
                    loader: 'file-loader',
                    options: {
                        name: "[name].[ext]"
                    }
                },
            }
        ]
    },
    optimization: {
        minimizer: [
            new OptimizeCSSAssetsPlugin({})
        ],
    },
    plugins: [
        new CleanWebpackPlugin(),
        new BundleTracker({ filename: './webpack-stats.json' }),
    ],
    resolve: {
        extensions: ['.ts', '.tsx', '.js', '.scss', '.css']
    },
    output: {
        filename: "[name]-[fullhash:16].js",
        path: __dirname + "/static/dist/",
        publicPath: '/static/dist/',
    }
};
