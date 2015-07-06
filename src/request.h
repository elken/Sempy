#include <stdlib.h>

#include <curlpp/cURLpp.hpp>
#include <curlpp/Easy.hpp>
#include <curlpp/Options.hpp>
#include <curlpp/Exception.hpp>

class TeaTrayRequest
{
    int getStatus(char*, size_t, size_t);
    void* Realloc(void*, size_t);
    void print();
    int buildID;
    int buildNumber;
    char* state;
    time_t duration;
    size_t bufSize;
public:
    char* buffer;
    TeaTrayRequest(char* []);
    ~TeaTrayRequest();
};
