"use strict";

const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const webpack = require('webpack');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
  entry: {
    web: './js/web',
    styles: './css/main',
  },

  context: __dirname,

  // Include source maps for all compiled files
  devtool: 'source-map',

  // Put all output files at bundles
  output: {
    path: path.resolve('./bundles/'),
    filename: "[name].js",
  },

  plugins: [
    // BundleTracker lets Django know about the webpack build status, displaying errors if
    // they occur
    new BundleTracker({filename: './bundles/webpack-stats.json'}),

    // Separate out included CSS files
    new MiniCssExtractPlugin({filename: "[name].css"}),
  ],

  module: {
    rules: [{
      // Compile Sass into CSS, bundle into a single file
      test: /\.*css$/,
      use: ['style-loader', MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader']
    }, {
      // Stops Bootstrap from complaining
      test: /\.(png|woff|woff2|eot|ttf|svg|otf)$/,
      loader: 'url-loader?limit=100000'
    }, {
      // Compile JSX files to JS
      test: /\.jsx?$/,
      exclude: /node_modules/,
      use: [{
        loader: 'babel-loader',
        options: {
          plugins: ['transform-decorators-legacy'],
          presets: ['env', 'stage-0', 'react']
        }
      }]
    }, {
      test: /\.js$/,
      use: ["source-map-loader"],
      enforce: "pre"
    }]
  },

  // TODO: generic way to resolve aliases?
  resolve: {
    symlinks: false, // https://github.com/npm/npm/issues/5875
    modules: ['node_modules', 'src'],
    extensions: ['.js', '.jsx', '.scss', '.css']
  }
};
