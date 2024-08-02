const path = require("node:path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

function outputFilename(name, ext = "[ext]", hashType = "contenthash:8") {
	return `${name}.[${hashType}]${ext}`;
}

module.exports = {
	entry: "./resources/js/index.js",
	output: {
		filename: "main.js",
		path: path.resolve("./static"),
	},
	module: {
		rules: [
			{
				test: /\.less$/,
				use: [MiniCssExtractPlugin.loader, "css-loader", "less-loader"],
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
	plugins: [
		new MiniCssExtractPlugin({
			filename: "main.css",
		}),
	],
	resolve: {
		alias: {
			"@fonts": path.resolve("../osu-web/resources/fonts"),
			"@images": path.resolve("../osu-web/public/images"),
		},
	},
};
