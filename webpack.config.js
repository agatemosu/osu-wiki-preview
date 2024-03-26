const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const Autoprefixer = require("autoprefixer");

function outputFilename(name, ext = "[ext]", hashType = "contenthash:8") {
	return `${name}.[${hashType}]${ext}`;
}

module.exports = {
	entry: "./resources/js/index.js",
	output: {
		filename: "main.js",
		path: path.resolve(__dirname, "static"),
	},
	module: {
		rules: [
			{
				test: /\.less$/,
				use: [
					MiniCssExtractPlugin.loader,
					{
						loader: "css-loader",
						options: {
							importLoaders: 1,
							sourceMap: true,
						},
					},
					{
						loader: "postcss-loader",
						options: {
							postcssOptions: {
								plugins: [Autoprefixer],
							},
						},
					},
					{
						loader: "less-loader",
						options: {
							sourceMap: true,
						},
					},
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
	plugins: [
		new MiniCssExtractPlugin({
			filename: "main.css",
		}),
	],
	resolve: {
		alias: {
			"@fonts": path.resolve(__dirname, "../osu-web/resources/fonts"),
			"@images": path.resolve(__dirname, "../osu-web/public/images"),
		},
	},
};
