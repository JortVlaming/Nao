//
// Created by crystal on 8/3/25.
//

#ifndef MACROS_H
#define MACROS_H

// For calls that return void
#define PROXY_CALL_VOID(proxy, method, ...)       \
do {                                           \
if (!(proxy)) return;                     \
(proxy).call<void>(method, ##__VA_ARGS__); \
} while (0)

// For calls that return a value, with default fallback
#define PROXY_CALL(proxy, method, default_value, ...) \
([&]() -> decltype(default_value) {                                        \
if (!(proxy)) return default_value;                       \
return (proxy).call<decltype(default_value)>(method, ##__VA_ARGS__);   \
})()


#endif //MACROS_H
