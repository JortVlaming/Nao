//
// Created by crystal on 8/2/25.
//

#include "Speech.h"
#include "macros.h"

Speech::Speech(const qi::SessionPtr &session) {
	if (!session) return;
	this->proxy = session->service("ALTextToSpeech");
}

void Speech::say(const std::string &text) const {
	PROXY_CALL_VOID(proxy, "say", text);
}

void Speech::setVolume(float volume) const {
	PROXY_CALL_VOID(proxy, "setVolume", volume);
}

float Speech::getVolume() const {
	return PROXY_CALL(proxy, "getVolume", -1.0f);
}
