# -*- coding: utf-8 -*-

from __future__ import print_function
from collections import defaultdict
import urllib2
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# -------------------------- Application constants -----------------------------

BE_API_HOST = "https://***/alexa"
en_US_locale = "en-US"
de_DE_locale = "de-DE"

intent_names = defaultdict()
intent_names["whats_new"] = "WhatsNewIntent"
intent_names["fashion_news"] = "FashionNewsIntent"
intent_names["read_article"] = "ReadArticleIntent"
intent_names["where_to_buy"] = "WhereToBuyIntent"
intent_names["help"] = "AMAZON.HelpIntent"
intent_names["cancel"] = "AMAZON.CancelIntent"
intent_names["stop"] = "AMAZON.StopIntent"
intent_names["repeat"] = "AMAZON.RepeatIntent"
intent_names["pause"] = "AMAZON.PauseIntent"
intent_names["yes"] = "AMAZON.YesIntent"
intent_names["no"] = "AMAZON.NoIntent"

speech_constants = defaultdict(dict)
speech_constants["welcome_response"][en_US_locale] = "Welcome to Fashion, the coolest news about Fashion and stores nearby"
speech_constants["welcome_response"][de_DE_locale] = "Willkommen in Fashion, die tollsten Nachrichten über die Mode und Geschäfte in der Nähe"
speech_constants["help_response"][en_US_locale] = "Ok, I will help. You can ask me the following questions: what's new on Fashion; tell me fashion news; read the article; where can I buy jeans nearby"
speech_constants["help_response"][de_DE_locale] = "Ok, ich werde helfen. Du kannst mir die folgenden Fragen stellen: was ist neu auf Fashion; sag mir mal die Mode Nachrichten; lies bitte den Artikel; wo kann ich jeans kaufen"
speech_constants["repeat_response"][en_US_locale] = "Could you please repeat your last phrase"
speech_constants["repeat_response"][de_DE_locale] = "Könnten Sie bitte Ihre letzte Phrase wiederholen"
speech_constants["yes_response"][en_US_locale] = "ok. Ask me something"
speech_constants["yes_response"][de_DE_locale] = "ok. Frag mich etwas"
speech_constants["no_response"][en_US_locale] = "Alexa applied your NO request. You could ask me something else."
speech_constants["no_response"][de_DE_locale] = "Alexa hat Ihre Kündigung beantragt. Sie könnten mich noch etwas fragen."
speech_constants["pause_response"][en_US_locale] = "Alexa paused your request"
speech_constants["pause_response"][de_DE_locale] = "Alexa hielt inne"
speech_constants["invalid_response"][en_US_locale] = "Invalid intent: %s. Alexa has not recognized your request. Please try again."
speech_constants["invalid_response"][de_DE_locale] = "Ungültige Absicht: %s. Alexa hat deine Anfrage nicht erkannt. Bitte versuche es erneut."
speech_constants["cancel_response"][en_US_locale] = "ok. Would you like to ask something else?"
speech_constants["cancel_response"][de_DE_locale] = "OK. Möchten Sie etwas anderes fragen?"
speech_constants["goodbye_response"][en_US_locale] = "Thank you for trying Fashion Alexa Skills Kit. Have a nice day!"
speech_constants["goodbye_response"][de_DE_locale] = "Vielen Dank für den Versuch der Fashion Alexa Skills Kit. Einen schönen Tag!"
speech_constants["want_to_read_article_response"][en_US_locale] = "Would you like me to read this article for you?"
speech_constants["want_to_read_article_response"][de_DE_locale] = "Möchten Sie, dass ich diesen Artikel für Sie lese?"
speech_constants["where_to_buy_not_found_query_response"][en_US_locale] = "I'm not sure what your requested query is. Please try again."
speech_constants["where_to_buy_not_found_query_response"][de_DE_locale] = "Ich bin mir nicht sicher, was Ihre angeforderte Abfrage ist. Bitte versuche es erneut."

speech_constants["help_reprompt"][en_US_locale] = "Please ask by saying, what's new on Fashion."
speech_constants["help_reprompt"][de_DE_locale] = "Bitte fragen Sie mit den Worten: Was ist neu auf Fashion."
speech_constants["yes_reprompt"][en_US_locale] = "Your request has been confirmed. You could ask something else."
speech_constants["yes_reprompt"][de_DE_locale] = "Ihre Anfrage wurde bestätigt. Sie könnten etwas anderes fragen."
speech_constants["no_reprompt"][en_US_locale] = "Your request has been rejected. You could ask something else."
speech_constants["no_reprompt"][de_DE_locale] = "Ihre Anfrage wurde abgelehnt. Sie könnten etwas anderes fragen."
speech_constants["pause_reprompt"][en_US_locale] = "Your request has been paused. You could ask something else."
speech_constants["pause_reprompt"][de_DE_locale] = "Ihre Anfrage wurde angehalten. Sie könnten etwas anderes fragen."
speech_constants["invalid_reprompt"][en_US_locale] = "Your request has not been recognized. Please try again."
speech_constants["invalid_reprompt"][de_DE_locale] = "Ihre Anfrage wurde nicht erkannt. Bitte versuche es erneut."


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session, is_ssml=False):
    outputSpeech = {}

    if is_ssml:
        outputSpeech = {
           "type": "SSML",
           "ssml": output
        }
    else:
        outputSpeech = {
           "type": "PlainText",
           "text": output
        }

    return {
        "outputSpeech": outputSpeech,
        "card": {
            "type": "Simple",
            "title": "SessionSpeechlet - " + title,
            "content": "SessionSpeechlet - " + output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    print("build_response    session_attributes: " + str(session_attributes))
    print("build_response    speechlet_response: " + str(speechlet_response))

    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }


# ---------------------- Helpers for fetching data -----------------------------
def fetch_data_as_object(url):
    response_str = urllib2.urlopen(url).read()
    return json.loads(response_str)


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response(locale):
    print("get_welcome_response")

    card_title = "Welcome"
    speech_output = speech_constants["welcome_response"][locale]
    reprompt_text = speech_constants["help_reprompt"][locale]
    should_end_session = False

    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_help_intent(locale):
    print("handle_help_intent")

    card_title = "Help"
    speech_output = speech_constants["help_response"][locale]
    reprompt_text = speech_constants["help_reprompt"][locale]
    should_end_session = False

    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_repeat_intent(locale):
    print("handle_repeat_intent")

    card_title = "Repeat"
    speech_output = speech_constants["repeat_response"][locale]
    reprompt_text = speech_constants["help_reprompt"][locale]
    should_end_session = False

    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_yes_intent(intent, session, locale):
    print("handle_yes_intent")

    if session.get("attributes", {}) and "lastIntent" in session.get("attributes", {}) and session["attributes"]["lastIntent"] == intent_names["fashion_news"]:
        return get_read_article_response(intent, session, locale)

    card_title = "YES intent"
    speech_output = speech_constants["yes_response"][locale]
    reprompt_text = speech_constants["yes_reprompt"][locale]
    should_end_session = False

    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_no_intent(intent, session, locale):
    print("handle_no_intent")

    if session.get("attributes", {}) and "lastIntent" in session.get("attributes", {}):
        last_intent = session["attributes"]["lastIntent"]
        if last_intent == intent_names["fashion_news"] or last_intent == intent_names["cancel"] or last_intent == intent_names["stop"]:
            return handle_cancel_stop_intent(intent, session, locale)

    card_title = "NO intent"
    speech_output = speech_constants["no_response"][locale]
    reprompt_text = speech_constants["no_reprompt"][locale]
    should_end_session = False

    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_pause_intent(locale):
    print("handle_pause_intent")

    card_title = "PAUSE"
    speech_output = speech_constants["pause_response"][locale]
    reprompt_text = speech_constants["pause_reprompt"][locale]
    should_end_session = False

    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_invalid_intent(intent, session, locale):
    print("handle_invalid_intent")

    card_title = "INVALID: " + intent["name"]
    speech_output = speech_constants["invalid_response"][locale].replace("%s", intent["name"])
    reprompt_text = speech_constants["invalid_reprompt"][locale]
    should_end_session = False

    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_cancel_stop_intent(intent, session, locale):
    print("handle_cancel_stop_intent")

    if session.get("attributes", {}) and "lastIntent" in session.get("attributes", {}) and \
            session["attributes"]["lastIntent"] == intent_names["read_article"]:
        session_attributes = {"lastIntent": intent_names["stop"]}
        card_title = "StopIntent"
        speech_output = speech_constants["cancel_response"][locale]
        reprompt_text = None
        should_end_session = False

        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))

    return handle_session_end_request(locale)

def handle_session_end_request(locale):
    print("handle_session_end_request")

    card_title = "Session Ended"
    speech_output = speech_constants["goodbye_response"][locale]
    # Setting should_end_session to true ends the session and exits the skill.
    should_end_session = True

    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def get_whats_new_response(intent, session, locale):
    print("get_whats_new_response")

    session_attributes = {"lastIntent": intent_names["whats_new"]}
    whats_new_response_object = fetch_data_as_object(BE_API_HOST + "/whatsNew?locale=" + locale)
    speech_output = whats_new_response_object["ssmlResult"]
    reprompt_text = None
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
            intent["name"], speech_output, reprompt_text, should_end_session, True))

def get_fashion_news_response(intent, session, locale):
    print("get_fashion_news_response")

    session_attributes = {"lastIntent": intent_names["fashion_news"]}
    fashion_news_response_object = fetch_data_as_object(BE_API_HOST + "/fashionNews?locale=" + locale)
    speech_output = fashion_news_response_object["result"] + speech_constants["want_to_read_article_response"][locale]
    reprompt_text = None
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
            intent["name"], speech_output, reprompt_text, should_end_session))

def get_read_article_response(intent, session, locale):
    print("get_read_article_response")

    session_attributes = {"lastIntent": intent_names["read_article"]}
    article_response_object = fetch_data_as_object(BE_API_HOST + "/lastArticleContent?locale=" + locale)
    speech_output = article_response_object["result"]
    reprompt_text = None
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
            intent["name"], speech_output, reprompt_text, should_end_session))

def get_where_to_buy_response(intent, session, locale):
    print("get_where_to_buy_response")

    if "Tag" in intent["slots"]:
        requested_tag = intent["slots"]["Tag"]["value"]
        where_to_buy_response_object = fetch_data_as_object(BE_API_HOST + "/whereToBuy?locale=" + locale + "&tag=" + requested_tag)
        speech_output = where_to_buy_response_object["ssmlResult"]
    else:
        speech_output = speech_constants["where_to_buy_not_found_query_response"][locale]

    session_attributes = {"lastIntent": intent_names["where_to_buy"]}
    reprompt_text = None
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
            intent["name"], speech_output, reprompt_text, should_end_session, True))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """
    print("on_session_started    requestId=" + session_started_request["requestId"]
          + ", sessionId=" + session["sessionId"])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want"""
    print("on_launch    requestId=" + launch_request["requestId"] +
          ", sessionId=" + session["sessionId"])
    # Dispatch to your skill's launch
    locale = launch_request["locale"]
    return get_welcome_response(locale)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    print("on_intent    requestId=" + intent_request["requestId"] + ", sessionId=" + session["sessionId"])

    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]
    locale = intent_request["locale"]

    # Dispatch to your skill's intent handlers
    if intent_name == intent_names["whats_new"]:
        return get_whats_new_response(intent, session, locale)
    elif intent_name == intent_names["fashion_news"]:
        return get_fashion_news_response(intent, session, locale)
    elif intent_name == intent_names["read_article"]:
        return get_read_article_response(intent, session, locale)
    elif intent_name == intent_names["where_to_buy"]:
        return get_where_to_buy_response(intent, session, locale)

    elif intent_name == intent_names["help"]:
        return handle_help_intent(locale)
    elif intent_name == intent_names["cancel"] or intent_name == intent_names["stop"]:
        return handle_cancel_stop_intent(intent, session, locale)
    elif intent_name == intent_names["repeat"]:
        return handle_repeat_intent(locale)
    elif intent_name == intent_names["yes"]:
        return handle_yes_intent(intent, session, locale)
    elif intent_name == intent_names["no"]:
        return handle_no_intent(intent, session, locale)
    elif intent_name == intent_names["pause"]:
        return handle_pause_intent(locale)
    else:
        return handle_invalid_intent(intent, session, locale)


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session. Is not called when the skill returns should_end_session=true"""
    print("on_session_ended    requestId=" + session_ended_request["requestId"] + ", sessionId=" + session["sessionId"])


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event['session']: " + str(event["session"]))
    print("event['request']: " + str(event["request"]))

    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])