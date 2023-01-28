import contextlib
import ctypes
import os
import platform


module_dir = os.path.dirname(__file__)
operating_system = platform.system()
cpu_bits, _ = platform.architecture()

if operating_system == "Windows":
    func_type = ctypes.WINFUNCTYPE
else:
    func_type = ctypes.CFUNCTYPE


tim_callback = func_type(
    None,
    ctypes.c_int32,
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_void_p,
)

log_callback = func_type(None, ctypes.c_int, ctypes.c_char_p, ctypes.c_void_p)
recv_msg_callback = func_type(None, ctypes.c_char_p, ctypes.c_void_p)


@contextlib.contextmanager
def tim_factory():
    tim_lib = None
    if operating_system == "Windows":
        if cpu_bits == "64bit":
            tim_lib = ctypes.WinDLL(
                os.path.join(module_dir, "lib/windows/lib/Win64/ImSDK.dll")
            )
        elif cpu_bits == "32bit":
            tim_lib = ctypes.WinDLL(
                os.path.join(module_dir, "lib/windows/lib/Win32/ImSDK.dll")
            )
    elif operating_system == "Linux":
        tim_lib = ctypes.CDLL(os.path.join(module_dir, "lib/linux/lib/libImSDK.so"))
    elif operating_system in {"MacOS", "Darwin"}:
        tim_lib = ctypes.CDLL(
            os.path.join(module_dir, "lib/mac/Versions/A/ImSDKForMac.dylib")
        )
    yield tim_lib
    if operating_system == "Windows":
        from ctypes import wintypes

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.FreeLibrary.argtypes = [wintypes.HMODULE]
        kernel32.FreeLibrary(tim_lib._handle)
    elif operating_system == "Linux":
        ctypes.CDLL("libdl.so").dlclose(tim_lib._handle)
    elif operating_system in {"MacOS", "Darwin"}:
        ctypes.CDLL("libdl.dylib").dlclose(tim_lib._handle)
