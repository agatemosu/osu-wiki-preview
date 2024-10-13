// @ts-check

import path from "node:path";
import rspack from "@rspack/core";
import { RspackManifestPlugin } from "rspack-manifest-plugin";

/**
 * @param {string} name
 * @param {string} ext
 * @param {string} hashType
 */
function outputFilename(name, ext = "[ext]", hashType = "contenthash:8") {
	return `${name}.[${hashType}]${ext}`;
}

/** @type {rspack.Configuration} */
const config = {
	module: {
		rules: [
			{
				test: /\.ts$/,
				exclude: [/node_modules/],
				loader: "builtin:swc-loader",
				/** @type {rspack.SwcLoaderOptions} */
				options: {
					jsc: {
						target: "es2015",
					},
				},
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
					filename: outputFilename("images/[name]"),
				},
				test: /(\.(png|jpe?g|gif|webp)$|^((?!font).)*\.svg$)/,
				type: "asset/resource",
			},
			{
				generator: {
					filename: outputFilename("fonts/[name]"),
				},
				test: /(\.(woff2?|ttf|eot|otf)$|font.*\.svg$)/,
				type: "asset/resource",
			},
		],
	},
	entry: "./resources/js/index.ts",
	output: {
		filename: outputFilename("js/[name]", ".js"),
		path: path.resolve("./app/static"),
		publicPath: "/static/",
		clean: true,
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
			filename: outputFilename("css/[name]", ".css"),
		}),
		new RspackManifestPlugin({
			filter: (file) =>
				file.path.match(/^\/static\/(?:css|js)\/.*\.(?:css|js)$/) !== null,
			map: (file) => {
				const baseDir = file.path.match(/^\/static\/(css|js)\//)?.[1];
				if (baseDir !== null && !file.name.startsWith(`${baseDir}/`)) {
					file.name = `${baseDir}/${file.name}`;
				}

				return file;
			},
		}),
	],
};

export default config;
