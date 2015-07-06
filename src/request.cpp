#include "request.h"

#include <gtkmm.h>
#include <time.h>

#include <string>
#include <sstream>
#include <iostream>
#include <iomanip>

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/lexical_cast.hpp>

#include <libnotifymm.h>

namespace pt = boost::property_tree;

TeaTrayRequest::TeaTrayRequest(char* argv[])
{
    if(remove("/tmp/travis.json") != 0)
        std::cerr << "Error deleting file." << std::endl;
    else
        std::cout << "Deleted file." << std::endl;
    buffer = NULL;
    buffer = (char*)malloc(256*sizeof(char));
    bufSize = 0;

    std::list<std::string> headers;
    headers.push_back("Accept: application/vnd.travis-ci.2+json");
    std::string url = "https://api.travis-ci.org/repos/" + std::string(argv[1]);
    try
    {
        curlpp::Cleanup cleaner;
        curlpp::Easy request;

        using namespace curlpp::Options;
        request.setOpt(new HttpHeader(headers));
        request.setOpt(WriteFunction(curlpp::types::WriteFunctionFunctor(this, &TeaTrayRequest::getStatus)));
        request.setOpt(new Url(url));
        request.setOpt(new Verbose(false));

        request.perform();
        print();
    }
    catch (curlpp::LogicError &e)
    {
        std::cout << e.what() << std::endl;
    }
    catch (curlpp::RuntimeError &e)
    {
        std::cout << e.what() << std::endl;
    }
}

TeaTrayRequest::~TeaTrayRequest()
{
    if(buffer)
        free(buffer);
}

void* TeaTrayRequest::Realloc(void* data, size_t size)
{
    if(data)
        return realloc(data, size);
    else
        return malloc(size);
}

int TeaTrayRequest::getStatus(char* data, size_t size, size_t nmem)
{
    size_t realsize = size * nmem;
    buffer = (char*)Realloc(buffer, bufSize + realsize);
    if(buffer == NULL)
    {
        realsize = 0;
    }

    memcpy(&(buffer[bufSize]), data, realsize);
    bufSize += realsize;

    return realsize;
}

void TeaTrayRequest::print()
{
    pt::ptree status;
    std::ofstream tmp_json;
    try
    {
        tmp_json.open("/tmp/travis.json");
        tmp_json << buffer;
        tmp_json.close();

        pt::read_json("/tmp/travis.json", status);
        std::cout << "Write complete" << std::endl;;
        buildID = status.get<int>("repo.id");
        buildNumber = status.get<int>("repo.last_build_number");
        duration = status.get<time_t>("repo.last_build_duration");
        state = status.get<char *>("repo.last_build_state");
        tm* time = gmtime(&duration);
        std::stringstream statusStream;
        statusStream << "#" << buildNumber << " " << state << ". Took "<< time->tm_min << ":" << std::setfill('0') << std::setw(2) << time->tm_sec;
        state[0] = toupper(state[0]);

        Glib::RefPtr<Gdk::Pixbuf> icon = Gdk::Pixbuf::create_from_file("pass.svg");
        Notify::init("Tea Tray");
        Notify::Notification buildStatus(state, statusStream.str().c_str(), "dialog-warning");
        if(state == "Errored")
            buildStatus.set_urgency(Notify::URGENCY_CRITICAL);
        buildStatus.set_timeout(5000);
        buildStatus.show();
    }
    catch(std::exception& e)
    {
        std::cerr << e.what() << std::endl;
    }
}
