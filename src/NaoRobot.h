//
// Created by crystal on 8/2/25.
//

#ifndef NAOROBOT_H
#define NAOROBOT_H

#include <string>
#include <qi/session.hpp>

#include "Services/Speech.h"

class NaoRobot {
public:
	NaoRobot(const std::string& ip, int port = 9559, bool dummy = false) {
		if (!dummy) {
			session = qi::makeSession();
			session->connect("tcp://" + ip + ":" + std::to_string(port));
		} else {
			session = nullptr;
		}

		speech = std::make_shared<Speech>(session);
	}

	std::shared_ptr<Speech> speech;
//	std::shared_ptr<Motion> motion;
//	std::shared_ptr<Camera> camera;
//	std::shared_ptr<Memory> memory;
//	std::shared_ptr<Posture> posture;
//	std::shared_ptr<Behavior> behavior;

private:
	qi::SessionPtr session;
};


#endif //NAOROBOT_H
