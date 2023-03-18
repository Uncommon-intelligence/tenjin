/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },

  webpack: (config, { isServer }) => {
    // Fixes npm packages that depend on `fs` module
    if (!isServer) {
      config.resolve.fallback = {
        fs: false
      }
    }

    // Configure the 'file-loader' to handle binary files
    config.module.rules.push({
      test: /\.(pdf|node)$/,
      use: {
        loader: 'file-loader',
        options: {
          publicPath: '/_next/static',
          outputPath: 'static',
          name: '[name].[hash].[ext]',
        },
      },
    });

    return config;
  },
}

module.exports = nextConfig
