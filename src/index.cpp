#include "tray.h"

int main(int argc, char* argv[])
{
    Glib::RefPtr<Gtk::Application> ttray = Gtk::Application::create(argc, argv, "org.gtkmm.teatray", Gio::APPLICATION_HANDLES_OPEN);
    TeaTray tray(argc, argv);

    return ttray->run(tray);
}
