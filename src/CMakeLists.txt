set(e13decoration_SRCS
    plugin.cpp
    decoration.cpp
    button.cpp
)

add_library(e13decoration MODULE ${e13decoration_SRCS})

target_link_libraries(e13decoration
    PUBLIC
        Qt5::Core
        Qt5::Gui
        Qt5::Widgets
        KF5::ConfigCore
        KF5::CoreAddons
        KF5::GuiAddons
        KF5::I18n
        KDecoration2::KDecoration2
)

install(TARGETS e13decoration DESTINATION ${PLUGIN_INSTALL_DIR}/org.kde.kdecoration2)
