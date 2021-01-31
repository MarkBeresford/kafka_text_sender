module.exports = {
  mode: "development",
  devtool: "inline-source-map",
  entry: {
      main: "./static/typescript/main.ts",
      firstTopic: "./static/typescript/firstTopic.ts",
      secondTopic: "./static/typescript/secondTopic.ts"
  },
  output: {
    path: __dirname + '/static',
    filename: "[name]-bundle.js"
  },
  resolve: {
    // Add `.ts` and `.tsx` as a resolvable extension.
    extensions: [".ts", ".tsx", ".js"]
  },
  module: {
    rules: [
      // all files with a `.ts` or `.tsx` extension will be handled by `ts-loader`
      { test: /\.tsx?$/, loader: "ts-loader" }
    ]
  }
};