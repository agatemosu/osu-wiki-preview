// @ts-check

import path from "node:path";
import rspack from "@rspack/core";

/** @type {rspack.Configuration} */
const config = {
	entry: "./resources/js/index.ts",
	output: {
		filename: "main.js",
		path: path.resolve("./app/static"),
	},
	module: {
		rules: [
			{
				test: /\.ts$/,
				exclude: [/node_modules/],
				loader: "builtin:swc-loader"
			},
			{
				test: /\.less$/,
				use: [
					rspack.CssExtractRspackPlugin.loader,
					"css-loader",
					"less-loader",
				],
			},
			{
				generator: {
					filename: "images/[name].[contenthash:8][ext]",
				},
				test: /(\.(png|jpe?g|gif|webp)$|^((?!font).)*\.svg$)/,
				type: "asset/resource",
			},
			{
				generator: {
					filename: "fonts/[name].[contenthash:8][ext]",
				},
				test: /(\.(woff2?|ttf|eot|otf)$|font.*\.svg$)/,
				type: "asset/resource",
			},
		],
	},
	resolve: {
		tsConfig: {
			configFile: path.resolve("./tsconfig.json"),
		},
		alias: {
			"@fonts": path.resolve("../osu-web/resources/fonts"),
			"@images": path.resolve("../osu-web/public/images"),
		},
	},
	plugins: [
		new rspack.CssExtractRspackPlugin({
			filename: "main.css",
		}),
	],
	experiments: {
		css: false,
	},
};

export default config;
