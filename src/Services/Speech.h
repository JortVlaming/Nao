//
// Created by crystal on 8/2/25.
//

#ifndef SPEECH_H
#define SPEECH_H
#include <qi/session.hpp>

class Speech {
public:
	Speech(const qi::SessionPtr& session);

	void say(const std::string& text) const;
	void setVolume(float volume) const;
	float getVolume() const;
private:
	qi::AnyObject proxy;
};

#endif //SPEECH_H
