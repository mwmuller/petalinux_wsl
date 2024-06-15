FROM mcr.microsoft.com/devcontainers/cpp:1-debian-11
RUN apt-get update

ARG REINSTALL_CMAKE_VERSION_FROM_SOURCE="3.21.5"
ARG USERNAME
ARG USER_UID
ARG USER_GID
# Optionally install the cmake for vcpkg
COPY ./reinstall-cmake.sh /tmp/
RUN echo "${USERNAME}"
RUN if [ "${REINSTALL_CMAKE_VERSION_FROM_SOURCE}" != "none" ]; then \
        chmod +x /tmp/reinstall-cmake.sh && /tmp/reinstall-cmake.sh ${REINSTALL_CMAKE_VERSION_FROM_SOURCE}; \
    fi \
    && rm -f /tmp/reinstall-cmake.sh

# [Optional] Uncomment this section to install additional vcpkg ports.
# RUN su vscode -c "${VCPKG_ROOT}/vcpkg install <your-port-name-here>"

# [Optional] Uncomment this section to install additional packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends \
     git \
     xdg-utils 


# Create the user
RUN if getent passwd ${USER_UID} > /dev/null; then userdel -r $(getent passwd ${USER_UID} | cut -d ':' -f 1); fi \ 
    && groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
