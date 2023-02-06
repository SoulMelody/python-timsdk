import platform
import shutil
import subprocess


def tim_lib_bootstrap():
    if platform.system() == "Windows":
        npm_cmd = "npm.cmd"
    else:
        npm_cmd = "npm"
    try:
        subprocess.check_call(
            [
                npm_cmd,
                "i",
                "im_electron_sdk",
                "--registry=https://registry.npmmirror.com",
                "--sass_binary_site=https://cdn.npmmirror.com/binaries/node-sass",
                "--electron_mirror=https://cdn.npmmirror.com/binaries/electron",
                "--no-save",
                "--ignore-scripts",
            ]
        )
    except subprocess.CalledProcessError:
        print("install im_electron_sdk failed")
        return
    shutil.copytree(
        "node_modules/im_electron_sdk/lib", "timsdk/lib", dirs_exist_ok=True
    )


if __name__ == "__main__":
    tim_lib_bootstrap()
