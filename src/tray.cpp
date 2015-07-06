#include "tray.h"
#include <sys/stat.h>

TeaTray::TeaTray(int argc, char* argv[])
{
    if(argc < 2)
    {
        std::cerr << "Wrong number of arguments.\n\t\t\t\t Usage: teatray user/repo" << std::endl;
    }
    else
    {
        struct stat buffer;
        std::string path = Glib::get_home_dir() + std::string("/.config/teatray.conf");
        std::cout << path << std::endl;
        if((stat(path.c_str(), &buffer) == 0))
        {
            std::cout << "File exists" << std::endl;
        }
        else
        {
            std::cout << "File doesn't exist" << std::endl;
        }
        while(true)
        {
            Glib::RefPtr<Gtk::StatusIcon> icon;
            icon = Gtk::StatusIcon::create_from_file("download.png");
            icon->signal_activate().connect(sigc::mem_fun(*this, &TeaTray::on_activated));
            icon->set_visible(true);
            TeaTrayRequest t(argv);
            sleep(5);
        }
    }
}

TeaTray::~TeaTray(){}

void TeaTray::on_activated()
{
    std::cout << "TODO: Put something here" << std::endl;
}
