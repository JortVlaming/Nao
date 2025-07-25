//
// Created by crystal on 7/25/25.
//

#include "robot.h"

std::shared_ptr<qi::Session> Robot::_connect() const {
	auto session = std::make_shared<qi::Session>();
	try {
		session->connect("tcp://" + ip_ + ":" + std::to_string(port_));
	} catch (const std::runtime_error& e) {
		std::string msg = e.what();
		if (msg.find("The call request could not be handled") != std::string::npos) {
			return nullptr;
		}
		throw;
	}
	return session;
}

qi::AnyObject Robot::getService(const std::string& name) const {
	if (!session_ || !session_->isConnected()) {
		return {};
	}
	return session_->service(name).value();
}
