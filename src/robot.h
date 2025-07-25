//
// Created by crystal on 7/25/25.
//

#ifndef ROBOT_H
#define ROBOT_H

#include <qi/session.hpp>
#include <qi/anyobject.hpp>
#include <memory>
#include <string>

class Robot {
public:
	explicit Robot(const std::string& ip, const int port = 9559)
		: ip_(ip), port_(port), session_(_connect()) {}

	qi::AnyObject getService(const std::string& name) const;

private:
	std::string ip_;
	int port_;
	std::shared_ptr<qi::Session> session_;

	std::shared_ptr<qi::Session> _connect() const;
};


#endif //ROBOT_H
