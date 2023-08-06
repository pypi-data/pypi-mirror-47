# This centers the window on the screen
win-origin -2 -2

model-path $THIS_PRC_DIR/../models
model-path $THIS_PRC_DIR/../textures

# Note that setting threading model breaks shadows - see
# https://bugs.launchpad.net/panda3d/+bug/1212752
threading-model App/Cull/Draw

tk-main-loop false


# Debugging
want-directtools false
want-tk false
want-pstats false