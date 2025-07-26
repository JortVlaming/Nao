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
	Proxy(Robot* robot, const std::string& name) : robot(robot), name(name) {};
	~Proxy();

	void on(const std::string& name,
			std::function<void(std::vector<std::any>)> callback,
			const std::string& source = "signal");

	void disconnect_all();

private:
	void dispatch(const std::string& event_name, std::vector<std::any> args);

	Robot* robot;
	std::string name;
	std::shared_ptr<AL::ALModule> proxy;

	std::unordered_map<std::string, int> signal_connections;
	std::unordered_map<std::string, std::vector<std::function<void(std::vector<std::any>)>>> callbacks;

	struct MemSub {
		std::string subscriber;
		std::string callback;
	};
	std::unordered_map<std::string, MemSub> memory_subscriptions;

	bool debug_mode = false;
};

#endif //PROXY_H
