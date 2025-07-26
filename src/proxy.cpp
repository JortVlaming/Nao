// proxy.cpp

#include "proxy.h"
#include <algorithm>
#include <iostream>
#include <any>
#include <almemory/constants.hpp>

void Proxy::on(const std::string& name,
               std::function<void(std::vector<std::any>)> callback,
               const std::string& source)
{
    if (debug_mode) {
        std::cout << "Callback registered for " << name << " sourced from " << source << "s\n";
    }

    if (source == "event") {
        if (callbacks.find(name) == callbacks.end()) {
            std::string callback_method_name = "_memory_cb_" + name;
            std::replace(callback_method_name.begin(), callback_method_name.end(), '/', '_');

            std::string subscriber_name = "Proxy_" + callback_method_name;

            // get ALMemory service by value
            qi::AnyObject memory = robot->getService("ALMemory");

            // subscribeToEvent method signature depends on your ALMemory binding
            // assuming it accepts (const std::string&, const std::string&, std::function<void(std::any)>)
            memory.call<void>("subscribeToEvent", name, subscriber_name,
                [this, name](std::any value) {
                    this->dispatch(name, { value });
                });

            memory_subscriptions[name] = { subscriber_name, callback_method_name };
        }

        callbacks[name].push_back(callback);

    } else {
        // Signal handling via proxy AnyObject
        qi::FutureSync<qi::SignalLink> link = proxy.connect(name, [this, name](const qi::AnyValue& val) {
            this->dispatch(name, { std::any(val) });
        });

        signal_connections[name] = link.value();
        callbacks[name].push_back(callback);
    }
}

void Proxy::disconnect_all()
{
    for (const auto& [event_name, signal_link] : signal_connections) {
        proxy.disconnect(signal_link);
    }
    signal_connections.clear();

    // get ALMemory service again (by value)
    qi::AnyObject memory = robot->getService("ALMemory");
    for (const auto& [event_name, sub] : memory_subscriptions) {
        memory.call<void>("unsubscribeToEvent", event_name, sub.first /* subscriber_name */);
    }
    memory_subscriptions.clear();

    callbacks.clear();
}

void Proxy::dispatch(const std::string& event_name, std::vector<std::any> args)
{
    auto it = callbacks.find(event_name);
    if (it != callbacks.end()) {
        for (auto& cb : it->second) {
            cb(args);
        }
    }
}
