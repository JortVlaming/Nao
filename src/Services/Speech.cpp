//
// Created by crystal on 8/2/25.
//

#include "Speech.h"

Speech::Speech(const qi::SessionPtr &session) {
	if (!session) return;
	this->proxy = session->service("ALTextToSpeech");
}

void Speech::say(const std::string &text) const {
	if (!this->proxy) return;
	this->proxy.call<void>("say", text);
}

void Speech::setVolume(float volume) const {
	if (!this->proxy) return;
	this->proxy.call<void>("setVolume", volume);
}

float Speech::getVolume() const {
	if (!this->proxy) return -1.0f;
	return this->proxy.call<float>("getVolume");
}
