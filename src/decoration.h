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

public:
    // Accessors for theme properties (used by Button class)
    int buttonSize() const { return m_buttonSize; }
    int buttonSpacing() const { return m_buttonSpacing; }
    QColor buttonHoverColor() const { return m_buttonHoverColor; }
    QColor buttonPressColor() const { return m_buttonPressColor; }
    QColor closeButtonColor() const { return m_closeButtonColor; }
    QColor activeTextColor() const { return m_activeTextColor; }
    QColor inactiveTextColor() const { return m_inactiveTextColor; }

private:
    KDecoration2::DecorationButtonGroup *m_leftButtons = nullptr;
    KDecoration2::DecorationButtonGroup *m_rightButtons = nullptr;
    
    // E13 style properties - dimensions
    int m_borderWidth = 4;
    int m_titleHeight = 24;
    bool m_shadowsEnabled = true;
    int m_buttonSize = 24;
    int m_buttonSpacing = 2;
    
    // E13 style properties - colors
    QColor m_activeFrameColor;
    QColor m_activeTitleBarColor;
    QColor m_activeTextColor;
    QColor m_inactiveFrameColor;
    QColor m_inactiveTitleBarColor;
    QColor m_inactiveTextColor;
    QColor m_buttonHoverColor;
    QColor m_buttonPressColor;
    QColor m_closeButtonColor;
    
    // E13 style properties - fonts
    int m_titleFontSize = 10;
    bool m_titleBold = false;
};

} // namespace E13

#endif // E13_DECORATION_H
