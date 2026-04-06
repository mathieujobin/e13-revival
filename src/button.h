#ifndef E13_BUTTON_H
#define E13_BUTTON_H

#include <KDecoration2/DecorationButton>
#include <QObject>

namespace E13
{

class Button : public KDecoration2::DecorationButton
{
    Q_OBJECT

public:
    explicit Button(KDecoration2::DecorationButtonType type, KDecoration2::Decoration *decoration, QObject *parent = nullptr);
    ~Button() override;

    static KDecoration2::DecorationButton *create(KDecoration2::DecorationButtonType type, KDecoration2::Decoration *decoration, QObject *parent);

    void paint(QPainter *painter, const QRect &repaintRegion) override;

private:
    void drawCloseButton(QPainter *painter) const;
    void drawMaximizeButton(QPainter *painter) const;
    void drawMinimizeButton(QPainter *painter) const;
    void drawMenuButton(QPainter *painter) const;
    void drawKeepAboveButton(QPainter *painter) const;
    void drawKeepBelowButton(QPainter *painter) const;
    void drawShadeButton(QPainter *painter) const;
    void drawOnAllDesktopsButton(QPainter *painter) const;
    
    QColor getButtonColor() const;
    QColor getIconColor() const;
};

} // namespace E13

#endif // E13_BUTTON_H
