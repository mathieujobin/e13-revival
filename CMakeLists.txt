cmake_minimum_required(VERSION 3.16)
project(e13-decoration VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# Find required packages
find_package(ECM REQUIRED NO_MODULE)
set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH})

include(FeatureSummary)
include(KDEInstallDirs)
include(KDECMakeSettings)
include(KDECompilerSettings NO_POLICY_SCOPE)

find_package(Qt5 REQUIRED COMPONENTS
    Core
    Gui
    Widgets
)

find_package(KF5 REQUIRED COMPONENTS
    Config
    CoreAddons
    GuiAddons
    I18n
)

find_package(KDecoration2 REQUIRED)

# Add subdirectories
add_subdirectory(src)

# Install metadata
install(FILES decoration/metadata.json DESTINATION ${PLUGIN_INSTALL_DIR}/org.kde.kdecoration2)

# Feature summary
feature_summary(WHAT ALL INCLUDE_QUIET_PACKAGES FATAL_ON_MISSING_REQUIRED_PACKAGES)
