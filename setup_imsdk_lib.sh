if [ ! -d "node_modules/im_electron_sdk" ]; then
    nodeenv -p
fi
npm i im_electron_sdk --registry=https://registry.npmmirror.com --no-save --ignore-scripts
mkdir -p timsdk/lib
case "$OSTYPE" in
  msys*)    cp -r node_modules/im_electron_sdk/lib/windows timsdk/lib ;;
  linux*)   cp -r node_modules/im_electron_sdk/lib/linux timsdk/lib ;;
  darwin*)  cp -r node_modules/im_electron_sdk/lib/mac timsdk/lib ;;
  *)        echo "unknown: $OSTYPE" ;;
esac
