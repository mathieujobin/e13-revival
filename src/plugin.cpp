#include "plugin.h"
#include "decoration.h"

namespace E13
{

Plugin::Plugin(QObject *parent)
    : KDecoration2::DecorationFactory(parent)
{
}

Plugin::~Plugin() = default;

KDecoration2::Decoration *Plugin::create(KDecoration2::DecoratedClient *client, QObject *parent)
{
    return new Decoration(client, parent);
}

} // namespace E13
