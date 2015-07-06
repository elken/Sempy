#include <stdlib.h>
#include <gtkmm.h>

#include "request.h"

class TeaTray : public Gtk::Window
{
public:
    TeaTray(int, char*[]);
    ~TeaTray();
private:
    virtual void on_activated();
};
