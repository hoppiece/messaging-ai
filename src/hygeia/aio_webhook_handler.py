# type: ignore

# The async version of linebot.v3.webhook.WebhookHandler
# Most code is copied from https://github.com/line/line-bot-sdk-python/blob/master/linebot/v3/webhook.py
import inspect

from linebot.v3.utils import LOGGER, PY3
from linebot.v3.webhook import WebhookHandler
from linebot.v3.webhooks import MessageEvent


class AsyncWebhookHandler(WebhookHandler):
    async def handle(self, body: str, signature: str) -> None:
        """Handle webhook.

        :param str body: Webhook request body (as text)
        :param str signature: X-Line-Signature value (as text)
        """
        payload = self.parser.parse(body, signature, as_payload=True)

        for event in payload.events:
            func = None
            key = None

            if isinstance(event, MessageEvent):
                key = self.__get_handler_key(event.__class__, event.message.__class__)
                func = self._handlers.get(key, None)

            if func is None:
                key = self.__get_handler_key(event.__class__)
                func = self._handlers.get(key, None)

            if func is None:
                func = self._default

            if func is None:
                LOGGER.info("No handler of " + key + " and no default handler")
            else:
                await self.__invoke_func(func, event, payload)

    @classmethod
    async def __invoke_func(
        cls,
        func,
        event,
        payload,
    ) -> None:  # type: ignore
        (has_varargs, args_count) = cls.__get_args_count(func)
        if has_varargs or args_count == 2:
            await func(event, payload.destination)
        elif args_count == 1:
            await func(event)
        else:
            await func()

    def __add_handler(self, func, event, message=None):
        key = self.__get_handler_key(event, message=message)
        self._handlers[key] = func

    @staticmethod
    def __get_args_count(func):
        if PY3:
            arg_spec = inspect.getfullargspec(func)
            return (arg_spec.varargs is not None, len(arg_spec.args))
        else:
            arg_spec = inspect.getargspec(func)
            return (arg_spec.varargs is not None, len(arg_spec.args))

    @staticmethod
    def __get_handler_key(event, message=None):
        if message is None:
            return event.__name__
        else:
            return event.__name__ + "_" + message.__name__
