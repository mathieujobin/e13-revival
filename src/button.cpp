#include "button.h"
#include "decoration.h"

#include <KDecoration2/DecoratedClient>

#include <QPainter>
#include <QPainterPath>

namespace E13
{

Button::Button(KDecoration2::DecorationButtonType type, KDecoration2::Decoration *decoration, QObject *parent)
    : KDecoration2::DecorationButton(type, decoration, parent)
{
    // Set button size
    const int buttonSize = 24;
    setGeometry(QRect(0, 0, buttonSize, buttonSize));
}

Button::~Button() = default;

KDecoration2::DecorationButton *Button::create(KDecoration2::DecorationButtonType type, KDecoration2::Decoration *decoration, QObject *parent)
{
    return new Button(type, decoration, parent);
}

QColor Button::getButtonColor() const
{
    const bool active = decoration()->client()->isActive();
    
    if (isPressed()) {
        return QColor(30, 30, 35);
    } else if (isHovered()) {
        return active ? QColor(70, 70, 75) : QColor(80, 80, 85);
    }
    
    return Qt::transparent;
}

QColor Button::getIconColor() const
{
    const bool active = decoration()->client()->isActive();
    
    if (type() == KDecoration2::DecorationButtonType::Close) {
        if (isHovered() || isPressed()) {
            return QColor(255, 255, 255);
        }
        return active ? QColor(220, 80, 80) : QColor(160, 160, 165);
    }
    
    if (isPressed()) {
        return active ? QColor(200, 200, 200) : QColor(140, 140, 145);
    } else if (isHovered()) {
        return active ? QColor(255, 255, 255) : QColor(180, 180, 185);
    }
    
    return active ? QColor(220, 220, 220) : QColor(160, 160, 165);
}

void Button::paint(QPainter *painter, const QRect &repaintRegion)
{
    Q_UNUSED(repaintRegion)
    
    painter->save();
    painter->setRenderHint(QPainter::Antialiasing);
    
    // Draw button background
    const QColor buttonColor = getButtonColor();
    if (buttonColor != Qt::transparent) {
        painter->setPen(Qt::NoPen);
        painter->setBrush(buttonColor);
        painter->drawRect(geometry());
    }
    
    // Draw button icon
    painter->translate(geometry().topLeft());
    
    switch (type()) {
        case KDecoration2::DecorationButtonType::Close:
            drawCloseButton(painter);
            break;
        case KDecoration2::DecorationButtonType::Maximize:
            drawMaximizeButton(painter);
            break;
        case KDecoration2::DecorationButtonType::Minimize:
            drawMinimizeButton(painter);
            break;
        case KDecoration2::DecorationButtonType::Menu:
            drawMenuButton(painter);
            break;
        case KDecoration2::DecorationButtonType::KeepAbove:
            drawKeepAboveButton(painter);
            break;
        case KDecoration2::DecorationButtonType::KeepBelow:
            drawKeepBelowButton(painter);
            break;
        case KDecoration2::DecorationButtonType::Shade:
            drawShadeButton(painter);
            break;
        case KDecoration2::DecorationButtonType::OnAllDesktops:
            drawOnAllDesktopsButton(painter);
            break;
        default:
            break;
    }
    
    painter->restore();
}

void Button::drawCloseButton(QPainter *painter) const
{
    painter->setPen(QPen(getIconColor(), 2, Qt::SolidLine, Qt::RoundCap));
    
    const int margin = 7;
    const int size = geometry().width() - 2 * margin;
    
    // Draw X
    painter->drawLine(margin, margin, margin + size, margin + size);
    painter->drawLine(margin + size, margin, margin, margin + size);
}

void Button::drawMaximizeButton(QPainter *painter) const
{
    painter->setPen(QPen(getIconColor(), 2, Qt::SolidLine, Qt::SquareCap));
    
    const int margin = 7;
    const int size = geometry().width() - 2 * margin;
    
    if (decoration()->client()->isMaximized()) {
        // Draw two overlapping squares for restore
        const int offset = 2;
        painter->drawRect(margin, margin + offset, size - offset, size - offset);
        painter->drawLine(margin + offset, margin, margin + size, margin);
        painter->drawLine(margin + size, margin, margin + size, margin + size - offset);
    } else {
        // Draw single square for maximize
        painter->drawRect(margin, margin, size, size);
    }
}

void Button::drawMinimizeButton(QPainter *painter) const
{
    painter->setPen(QPen(getIconColor(), 2, Qt::SolidLine, Qt::RoundCap));
    
    const int margin = 7;
    const int width = geometry().width() - 2 * margin;
    const int y = geometry().height() / 2 + 3;
    
    // Draw horizontal line
    painter->drawLine(margin, y, margin + width, y);
}

void Button::drawMenuButton(QPainter *painter) const
{
    painter->setPen(Qt::NoPen);
    painter->setBrush(getIconColor());
    
    const int margin = 6;
    const int size = geometry().width() - 2 * margin;
    
    // Draw application icon placeholder (simple square)
    painter->drawRect(margin, margin, size, size);
}

void Button::drawKeepAboveButton(QPainter *painter) const
{
    painter->setPen(QPen(getIconColor(), 2, Qt::SolidLine, Qt::RoundCap));
    
    const int margin = 7;
    const int size = geometry().width() - 2 * margin;
    const int centerY = geometry().height() / 2;
    
    // Draw up arrow
    QPainterPath path;
    path.moveTo(geometry().width() / 2, margin);
    path.lineTo(margin, centerY);
    path.moveTo(geometry().width() / 2, margin);
    path.lineTo(margin + size, centerY);
    
    painter->drawPath(path);
}

void Button::drawKeepBelowButton(QPainter *painter) const
{
    painter->setPen(QPen(getIconColor(), 2, Qt::SolidLine, Qt::RoundCap));
    
    const int margin = 7;
    const int size = geometry().width() - 2 * margin;
    const int centerY = geometry().height() / 2;
    
    // Draw down arrow
    QPainterPath path;
    path.moveTo(geometry().width() / 2, margin + size);
    path.lineTo(margin, centerY);
    path.moveTo(geometry().width() / 2, margin + size);
    path.lineTo(margin + size, centerY);
    
    painter->drawPath(path);
}

void Button::drawShadeButton(QPainter *painter) const
{
    painter->setPen(QPen(getIconColor(), 2, Qt::SolidLine, Qt::RoundCap));
    
    const int margin = 7;
    const int width = geometry().width() - 2 * margin;
    
    if (decoration()->client()->isShaded()) {
        // Draw down chevron when shaded
        const int y = geometry().height() / 2 + 2;
        painter->drawLine(margin, y - 2, geometry().width() / 2, y + 2);
        painter->drawLine(geometry().width() / 2, y + 2, margin + width, y - 2);
    } else {
        // Draw up chevron when not shaded
        const int y = geometry().height() / 2;
        painter->drawLine(margin, y + 2, geometry().width() / 2, y - 2);
        painter->drawLine(geometry().width() / 2, y - 2, margin + width, y + 2);
    }
}

void Button::drawOnAllDesktopsButton(QPainter *painter) const
{
    painter->setPen(Qt::NoPen);
    painter->setBrush(getIconColor());
    
    const int centerX = geometry().width() / 2;
    const int centerY = geometry().height() / 2;
    const int radius = decoration()->client()->isOnAllDesktops() ? 4 : 3;
    
    // Draw circle (filled if on all desktops, outline if not)
    if (decoration()->client()->isOnAllDesktops()) {
        painter->drawEllipse(QPoint(centerX, centerY), radius, radius);
    } else {
        painter->setPen(QPen(getIconColor(), 2));
        painter->setBrush(Qt::NoBrush);
        painter->drawEllipse(QPoint(centerX, centerY), radius, radius);
    }
}

} // namespace E13
