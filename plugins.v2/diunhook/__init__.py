from typing import Any, List, Dict, Tuple
from app.log import logger
from app.plugins import _PluginBase
from app.schemas.types import NotificationType
from app import schemas


class DiunHook(_PluginBase):
    # 插件名称
    plugin_name = "Diun-webhook通知"
    # 插件描述
    plugin_desc = "接收Diun-webhook通知并推送"
    # 插件图标
    plugin_icon = "Ward_A.png"
    # 插件版本
    plugin_version = "0.0.2"
    # 插件作者
    plugin_author = "saitenasuk"
    # 作者主页
    author_url = "https://github.com/saitenasuk"
    # 插件配置项ID前缀
    plugin_config_prefix = "diun_notify_"
    # 加载顺序
    plugin_order = 30
    # 可使用的用户级别
    auth_level = 1

    # 私有属性
    _enabled = False
    _notify = False

    def init_plugin(self, config: dict = None):
        if config:
            self._enabled = config.get("enabled")
            self._notify = config.get("notify")

    def send_notify(self, content: dict):
        """
        发送通知
        """
        logger.info(f"收到webhook消息啦。。。  {content}")
        if self._enabled and self._notify:
            if content:
                self.post_message(
                    title="Diun通知",
                    mtype=NotificationType.SiteMessage,
                    text="收到Diun-webhook消息",
                )

        return schemas.Response(success=True, message="发送成功")

    def get_state(self) -> bool:
        return self._enabled

    @staticmethod
    def get_command() -> List[Dict[str, Any]]:
        pass

    def get_api(self) -> List[Dict[str, Any]]:
        return [
            {
                "path": "/webhook",  # API路径，必须以/开始
                "endpoint": self.send_notify,  # API响应方法
                "methods": ["POST"],  # 请求方式：GET/POST/PUT/DELETE
                "summary": "diun-webhook通知",  # API名称
                "description": "接收diun-webhook消息后推送",  # API描述
            }
        ]

    def get_form(self) -> Tuple[List[dict], Dict[str, Any]]:
        """
        拼装插件配置页面，需要返回两块数据：1、页面配置；2、数据结构
        """
        # 编历 NotificationType 枚举，生成消息类型选项
        MsgTypeOptions = []
        for item in NotificationType:
            MsgTypeOptions.append({"title": item.value, "value": item.name})
        return [
            {
                "component": "VForm",
                "content": [
                    {
                        "component": "VRow",
                        "content": [
                            {
                                "component": "VCol",
                                "props": {"cols": 12, "md": 6},
                                "content": [
                                    {
                                        "component": "VSwitch",
                                        "props": {
                                            "model": "enabled",
                                            "label": "启用插件",
                                        },
                                    }
                                ],
                            },
                            {
                                "component": "VCol",
                                "props": {"cols": 12, "md": 6},
                                "content": [
                                    {
                                        "component": "VSwitch",
                                        "props": {
                                            "model": "notify",
                                            "label": "开启通知",
                                        },
                                    }
                                ],
                            },
                        ],
                    },
                    {
                        "component": "VRow",
                        "content": [
                            {
                                "component": "VCol",
                                "props": {"cols": 12, "md": 12},
                                "content": [
                                    {
                                        "component": "VAlert",
                                        "props": {
                                            "type": "info",
                                            "variant": "tonal",
                                            "text": "接收消息地址：http://ip:port/api/v1/plugin/DiunHook/webhook",
                                        },
                                    }
                                ],
                            },
                        ],
                    },
                ],
            }
        ], {
            "enabled": False,
            "notify": False,
        }

    def get_page(self) -> List[dict]:
        pass

    def stop_service(self):
        """
        退出插件
        """
        pass
