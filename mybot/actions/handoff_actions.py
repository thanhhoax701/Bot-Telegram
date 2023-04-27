
from typing import (
    List,
    Text,
    Optional,
    Dict,
    Any,
    TYPE_CHECKING,
    Tuple,
    Set,
    cast,
)
from rasa.shared.core.events import Event, BotUttered
from typing_extensions import TypedDict
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, ConversationPaused

from rasa.shared.core.constants import (
    USER_INTENT_OUT_OF_SCOPE,
    ACTION_LISTEN_NAME,
    ACTION_RESTART_NAME,
    ACTION_SESSION_START_NAME,
    ACTION_DEFAULT_FALLBACK_NAME,
    ACTION_DEACTIVATE_LOOP_NAME,
    ACTION_REVERT_FALLBACK_EVENTS_NAME,
    ACTION_DEFAULT_ASK_AFFIRMATION_NAME,
    ACTION_DEFAULT_ASK_REPHRASE_NAME,
    ACTION_UNLIKELY_INTENT_NAME,
    ACTION_BACK_NAME,
    REQUESTED_SLOT,
    ACTION_EXTRACT_SLOTS,
    DEFAULT_SLOT_NAMES,
    MAPPING_CONDITIONS,
    ACTIVE_LOOP,
    ACTION_VALIDATE_SLOT_MAPPINGS,
    MAPPING_TYPE,
    SlotMappingType,
    
)
import rasa.core.actions.two_stage_fallback
from rasa.shared.nlu.constants import (
    INTENT_NAME_KEY,
    INTENT_RANKING_KEY,
    ENTITY_ATTRIBUTE_TYPE,
    ENTITY_ATTRIBUTE_ROLE,
    ENTITY_ATTRIBUTE_GROUP,
    PREDICTED_CONFIDENCE_KEY
)

import yaml
import logging
from telebot import TeleBot
logger = logging.getLogger(__name__)


MAP_INTENT_NAME = {}
TOKEN_SERVERBOT = ""
TOKEN_BOT = ""
ADMIN_ID = ""
with open("actions/config.yml") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    MAP_INTENT_NAME = data["map_intent_text"]
    TOKEN_SERVERBOT = data["token_serverbot"]
    TOKEN_BOT = data["token_bot"]
    ADMIN_ID = data["admin_idchat"]

teleServerBot = None
if TOKEN_SERVERBOT:
    teleServerBot = TeleBot(TOKEN_SERVERBOT)

teleBot = None
if TOKEN_BOT:
    teleBot = TeleBot(TOKEN_BOT)


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):

        message = "Chào bạn, Mình đang thực hiện kết nối đến tư vấn viên để giải đáp vấn đề của bạn. Bạn cần hỗ trợ thông tin gì ạ"
        dispatcher.utter_message(text=message)
        user = teleBot.get_chat(tracker.sender_id)
        name = ""
        if user.first_name:
            name += user.first_name
        if user.last_name:
            name += " " + user.last_name
        if ADMIN_ID:
            teleServerBot.send_message(ADMIN_ID, "THÔNG BÁO: Người dùng với ID {} và tên là {} đang cần bạn hỗ trợ".format(tracker.sender_id, name))
        return [UserUtteranceReverted(), ConversationPaused()]

class ActionDefaultAskAffirmation(Action):
    def name(self) -> Text:
        return "action_default_ask_affirmation"

    async def run(
        self,
        dispatcher,
        tracker,
        domain,
    ) -> List[Event]:
        latest_message = tracker.latest_message
        if latest_message is None:
            raise TypeError(
                "Cannot find last user message for detecting fallback affirmation."
            )   
        logger.error(latest_message)
        intent_to_affirm = latest_message["intent"]["name"]

        # FIXME: better type annotation for `parse_data` would require
        IntentPrediction = TypedDict(
            "IntentPrediction", {INTENT_NAME_KEY: Text, PREDICTED_CONFIDENCE_KEY: float}  # type: ignore[misc]  # noqa: E501
        )
        intent_ranking = cast(
            List["IntentPrediction"],
            latest_message.get(INTENT_RANKING_KEY) or [],
        )
        if (
            intent_to_affirm == "nlu_fallback"
            and len(intent_ranking) > 1
        ):
            intent_to_affirm = intent_ranking[1][INTENT_NAME_KEY]
        intent_to_affirm = MAP_INTENT_NAME.get(intent_to_affirm, intent_to_affirm)
        affirmation_message = f"Có phải ý của bạn là muốn '{intent_to_affirm}'?"

        message = {
            "text": affirmation_message,
            "buttons": [
                {"title": "Đúng", "payload": f"/{intent_to_affirm}"},
                {"title": "Sai", "payload": f"/{USER_INTENT_OUT_OF_SCOPE}"},
            ]
        }
        dispatcher.utter_message(**message)
        return []