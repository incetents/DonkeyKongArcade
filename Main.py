
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Start location for game

from Engine.Engine import *

def main():
    engine.get_singleton().start()
    engine.get_singleton().m_loop()
    engine.get_singleton().exit()


# Run Main
if __name__ == "__main__":
    main()