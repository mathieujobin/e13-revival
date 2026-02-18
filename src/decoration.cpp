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
    
    // General settings
    KConfigGroup generalGroup = config->group("General");
    m_borderWidth = generalGroup.readEntry("BorderWidth", 4);
    m_titleHeight = generalGroup.readEntry("TitleBarHeight", 24);
    m_shadowsEnabled = generalGroup.readEntry("EnableShadows", true);
    
    // Button settings
    KConfigGroup buttonGroup = config->group("Buttons");
    m_buttonSize = buttonGroup.readEntry("ButtonSize", 24);
    m_buttonSpacing = buttonGroup.readEntry("ButtonSpacing", 2);
    
    // Color settings
    KConfigGroup colorGroup = config->group("Colors");
    m_activeFrameColor = colorGroup.readEntry("ActiveFrameColor", QColor(40, 40, 45));
    m_activeTitleBarColor = colorGroup.readEntry("ActiveTitleBarColor", QColor(50, 50, 55));
    m_activeTextColor = colorGroup.readEntry("ActiveTextColor", QColor(255, 255, 255));
    m_inactiveFrameColor = colorGroup.readEntry("InactiveFrameColor", QColor(60, 60, 65));
    m_inactiveTitleBarColor = colorGroup.readEntry("InactiveTitleBarColor", QColor(70, 70, 75));
    m_inactiveTextColor = colorGroup.readEntry("InactiveTextColor", QColor(160, 160, 165));
    m_buttonHoverColor = colorGroup.readEntry("ButtonHoverColor", QColor(70, 70, 75));
    m_buttonPressColor = colorGroup.readEntry("ButtonPressColor", QColor(30, 30, 35));
    m_closeButtonColor = colorGroup.readEntry("CloseButtonColor", QColor(220, 80, 80));
    m_separatorColor = colorGroup.readEntry("SeparatorColor", QColor(70, 70, 75));
    
    // Advanced settings
    KConfigGroup advancedGroup = config->group("Advanced");
    m_titleFontSize = advancedGroup.readEntry("TitleFontSize", 10);
    m_titleBold = advancedGroup.readEntry("TitleBold", false);

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
    // Position button groups using theme button size
    if (m_leftButtons) {
        m_leftButtons->setGeometry(QRect(
            m_borderWidth,
            0,
            m_buttonSize,
            titleBarHeight()
        ));
    }
    
    if (m_rightButtons) {
        const int rightButtonsWidth = m_rightButtons->buttons().count() * (m_buttonSize + m_buttonSpacing);
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
    return active ? m_activeFrameColor : m_inactiveFrameColor;
}

QColor Decoration::getTitleBarColor(bool active) const
{
    return active ? m_activeTitleBarColor : m_inactiveTitleBarColor;
}

QColor Decoration::getTextColor(bool active) const
{
    return active ? m_activeTextColor : m_inactiveTextColor;
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
    painter->setPen(QPen(m_separatorColor, 1));
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
    int leftOffset = m_borderWidth + m_buttonSize + 6; // Menu button width + padding
    int rightOffset = m_borderWidth + (m_rightButtons->buttons().count() * (m_buttonSize + m_buttonSpacing));
    
    QRect textRect(
        leftOffset,
        0,
        rect().width() - leftOffset - rightOffset,
        titleBarHeight()
    );
    
    // Draw caption text using theme font settings
    painter->setPen(getTextColor(active));
    
    QFont font = painter->font();
    font.setPointSize(m_titleFontSize);
    font.setBold(m_titleBold);
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
