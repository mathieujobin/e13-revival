#include "decoration.h"
#include "button.h"

#include <KDecoration2/DecoratedClient>
#include <KDecoration2/DecorationSettings>

#include <KConfigGroup>
#include <KSharedConfig>

#include <QPainter>
#include <QFontMetrics>
#include <QVariant>

namespace E13
{

Decoration::Decoration(KDecoration2::DecoratedClient *client, QObject *parent)
    : KDecoration2::Decoration(client, parent)
{
}

Decoration::~Decoration() = default;

void Decoration::init()
{
    // Load theme configuration
    auto config = KSharedConfig::openConfig("e13decorationrc");
    KConfigGroup generalGroup = config->group("General");
    
    m_borderWidth = generalGroup.readEntry("BorderWidth", 4);
    m_titleHeight = generalGroup.readEntry("TitleBarHeight", 24);
    m_shadowsEnabled = generalGroup.readEntry("EnableShadows", true);

    // Create button groups
    m_leftButtons = new KDecoration2::DecorationButtonGroup(
        KDecoration2::DecorationButtonGroup::Position::Left,
        this,
        &Button::create
    );
    
    m_rightButtons = new KDecoration2::DecorationButtonGroup(
        KDecoration2::DecorationButtonGroup::Position::Right,
        this,
        &Button::create
    );

    // Setup standard button layout (E13 style: icon on left, buttons on right)
    m_leftButtons->addButton(KDecoration2::DecorationButtonType::Menu);
    m_rightButtons->addButton(KDecoration2::DecorationButtonType::Minimize);
    m_rightButtons->addButton(KDecoration2::DecorationButtonType::Maximize);
    m_rightButtons->addButton(KDecoration2::DecorationButtonType::Close);

    // Connect signals for dynamic updates
    connect(client(), &KDecoration2::DecoratedClient::captionChanged, this, [this]() {
        update();
    });
    
    connect(client(), &KDecoration2::DecoratedClient::activeChanged, this, [this]() {
        update();
    });
    
    connect(client(), &KDecoration2::DecoratedClient::widthChanged, this, &Decoration::updateTitleBar);
    connect(client(), &KDecoration2::DecoratedClient::maximizedChanged, this, &Decoration::updateBorders);
    
    connect(settings().get(), &KDecoration2::DecorationSettings::borderSizeChanged, this, &Decoration::updateBorders);

    updateBorders();
    updateTitleBar();
}

void Decoration::updateBorders()
{
    QMargins borders;
    
    // No borders for maximized windows
    if (client()->isMaximized()) {
        borders = QMargins(0, titleBarHeight(), 0, 0);
    } else {
        const int border = borderSize();
        borders = QMargins(border, titleBarHeight(), border, border);
    }
    
    setBorders(borders);
}

void Decoration::updateTitleBar()
{
    // Position button groups
    const int buttonWidth = 24;
    const int buttonSpacing = 2;
    
    if (m_leftButtons) {
        m_leftButtons->setGeometry(QRect(
            m_borderWidth,
            0,
            buttonWidth,
            titleBarHeight()
        ));
    }
    
    if (m_rightButtons) {
        const int rightButtonsWidth = m_rightButtons->buttons().count() * (buttonWidth + buttonSpacing);
        m_rightButtons->setGeometry(QRect(
            size().width() - rightButtonsWidth - m_borderWidth,
            0,
            rightButtonsWidth,
            titleBarHeight()
        ));
    }
}

int Decoration::borderSize() const
{
    const int baseSize = settings()->smallSpacing();
    
    switch (settings()->borderSize()) {
        case KDecoration2::BorderSize::None:
            return 0;
        case KDecoration2::BorderSize::NoSides:
            return 0;
        case KDecoration2::BorderSize::Tiny:
            return qMax(2, baseSize);
        case KDecoration2::BorderSize::Normal:
            return m_borderWidth;
        case KDecoration2::BorderSize::Large:
            return m_borderWidth * 1.5;
        case KDecoration2::BorderSize::VeryLarge:
            return m_borderWidth * 2;
        case KDecoration2::BorderSize::Huge:
            return m_borderWidth * 2.5;
        case KDecoration2::BorderSize::VeryHuge:
            return m_borderWidth * 3;
        case KDecoration2::BorderSize::Oversized:
            return m_borderWidth * 4;
        default:
            return m_borderWidth;
    }
}

int Decoration::titleBarHeight() const
{
    return m_titleHeight;
}

QColor Decoration::getFrameColor(bool active) const
{
    // E13 classic style: darker frame
    if (active) {
        return QColor(40, 40, 45);
    } else {
        return QColor(60, 60, 65);
    }
}

QColor Decoration::getTitleBarColor(bool active) const
{
    // E13 style: gradient effect simulated with solid color
    if (active) {
        return QColor(50, 50, 55);
    } else {
        return QColor(70, 70, 75);
    }
}

QColor Decoration::getTextColor(bool active) const
{
    if (active) {
        return QColor(255, 255, 255);
    } else {
        return QColor(160, 160, 165);
    }
}

void Decoration::paint(QPainter *painter, const QRect &repaintRegion)
{
    Q_UNUSED(repaintRegion)
    
    painter->save();
    painter->setRenderHint(QPainter::Antialiasing);
    
    paintFrameBackground(painter);
    paintCaption(painter);
    
    painter->restore();
}

void Decoration::paintFrameBackground(QPainter *painter) const
{
    const bool active = client()->isActive();
    const QRect frameRect = rect();
    
    // Draw window border
    if (!client()->isMaximized() && borderSize() > 0) {
        painter->setPen(Qt::NoPen);
        painter->setBrush(getFrameColor(active));
        painter->drawRect(frameRect);
    }
    
    // Draw title bar
    const QRect titleBarRect(0, 0, frameRect.width(), titleBarHeight());
    painter->setPen(Qt::NoPen);
    painter->setBrush(getTitleBarColor(active));
    painter->drawRect(titleBarRect);
    
    // Draw subtle separator line
    painter->setPen(QPen(active ? QColor(70, 70, 75) : QColor(80, 80, 85), 1));
    painter->drawLine(
        titleBarRect.bottomLeft(),
        titleBarRect.bottomRight()
    );
}

void Decoration::paintCaption(QPainter *painter) const
{
    const bool active = client()->isActive();
    const QString caption = client()->caption();
    
    if (caption.isEmpty()) {
        return;
    }
    
    // Calculate text area (between button groups)
    int leftOffset = m_borderWidth + 30; // Menu button width
    int rightOffset = m_borderWidth + (m_rightButtons->buttons().count() * 26);
    
    QRect textRect(
        leftOffset,
        0,
        rect().width() - leftOffset - rightOffset,
        titleBarHeight()
    );
    
    // Draw caption text
    painter->setPen(getTextColor(active));
    
    QFont font = painter->font();
    font.setPointSize(10);
    font.setBold(false);
    painter->setFont(font);
    
    const QFontMetrics fm(font);
    QString elidedText = fm.elidedText(caption, Qt::ElideRight, textRect.width());
    
    painter->drawText(
        textRect,
        Qt::AlignVCenter | Qt::AlignLeft,
        elidedText
    );
}

} // namespace E13
