#ifndef E13_DECORATION_H
#define E13_DECORATION_H

#include <KDecoration2/Decoration>
#include <KDecoration2/DecorationButtonGroup>
#include <QObject>
#include <QPalette>

namespace E13
{

class Decoration : public KDecoration2::Decoration
{
    Q_OBJECT

public:
    explicit Decoration(KDecoration2::DecoratedClient *client, QObject *parent = nullptr);
    ~Decoration() override;

    void paint(QPainter *painter, const QRect &repaintRegion) override;

public Q_SLOTS:
    void init() override;

private:
    void updateBorders();
    void updateTitleBar();
    void paintFrameBackground(QPainter *painter) const;
    void paintCaption(QPainter *painter) const;
    void paintButtons(QPainter *painter) const;

    int borderSize() const;
    int titleBarHeight() const;
    
    QColor getFrameColor(bool active) const;
    QColor getTitleBarColor(bool active) const;
    QColor getTextColor(bool active) const;

private:
    KDecoration2::DecorationButtonGroup *m_leftButtons = nullptr;
    KDecoration2::DecorationButtonGroup *m_rightButtons = nullptr;
    
    // E13 style properties
    int m_borderWidth = 4;
    int m_titleHeight = 24;
    bool m_shadowsEnabled = true;
};

} // namespace E13

#endif // E13_DECORATION_H
