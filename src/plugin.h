#ifndef E13_PLUGIN_H
#define E13_PLUGIN_H

#include <KDecoration2/DecorationFactory>
#include <QObject>

namespace E13
{

class Plugin : public KDecoration2::DecorationFactory
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.kde.kdecoration2" FILE "../decoration/metadata.json")
    Q_INTERFACES(KDecoration2::DecorationFactory)

public:
    explicit Plugin(QObject *parent = nullptr);
    ~Plugin() override;

    KDecoration2::Decoration *create(KDecoration2::DecoratedClient *client, QObject *parent) override;
};

} // namespace E13

#endif // E13_PLUGIN_H
