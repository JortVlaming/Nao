//
// Created by crystal on 7/26/25.
//

#ifndef PROXY_H
#define PROXY_H
#include <any>
#include <string>
#include <alcommon/almodule.h>
#include "robot.h"

class Proxy {
public:
	Proxy(Robot* robot, const std::string& name) : robot(robot), name(name), proxy(robot->getService(name)) {};
	~Proxy();
private:
	Robot* robot;
protected:
	std::string name;
	qi::AnyObject proxy;
};

#endif //PROXY_H
