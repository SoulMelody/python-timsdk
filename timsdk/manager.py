import json
import os
import time
import threading

from .callbacks import logger, login_callback, on_recv_new_msg, tim_log
from .enums import LoginStatus
from .library import module_dir, recv_msg_callback, tim_factory
from .utils import str2ptr


class TIMManager(threading.Thread):
    @property
    def sdk_config(self):
        return {
            "sdk_config_log_file_path": os.path.join(
                module_dir, "com_tencent_imsdk_log"
            ),
            "sdk_config_config_file_path": os.path.join(
                module_dir, "com_tencent_imsdk_data"
            ),
        }

    def __init__(
        self,
        sdk_appid: int,
        user_id: str,
        user_sig: str,
        metadata: dict,
    ):
        super().__init__()
        self.sdk_appid = sdk_appid
        self.user_id = user_id
        self.user_sig = user_sig
        self.metadata = metadata
        self.event = threading.Event()
        logger.add(
            os.path.join(module_dir, "com_tencent_imsdk_log/timsdk.log"), level="DEBUG"
        )

    def stop(self):
        self.event.set()

    def stopped(self):
        return self.event.is_set()

    def run(self):
        @recv_msg_callback
        def _on_recv_new_msg(json_msg_array, _):
            on_recv_new_msg(json_msg_array, self)

        with tim_factory() as tim_lib:
            tim_lib.TIMSetLogCallback(tim_log, str2ptr(""))
            tim_lib.TIMInit(self.sdk_appid, str2ptr(json.dumps(self.sdk_config)))
            tim_lib.TIMAddRecvNewMsgCallback(_on_recv_new_msg, str2ptr(""))
            tim_lib.TIMLogin(
                str2ptr(self.user_id),
                str2ptr(self.user_sig),
                login_callback,
                str2ptr(""),
            )
            logged_in = LoginStatus.LOGGED_OUT
            for _ in range(10):
                logged_in = tim_lib.TIMGetLoginStatus()
                if logged_in == LoginStatus.LOGGED_IN:
                    break
                time.sleep(1)
            else:
                if logged_in != LoginStatus.LOGGED_IN:
                    logger.warning("login failed!")
                    return
            while not self.stopped():
                time.sleep(0.1)
