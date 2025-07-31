# Tool Directories

## spyher_tools/
Contains build automation scripts for managing git uploads and building sphere files. These scripts automate the process of:
- Building compiled sphere artifacts
- Managing git commits and uploads
- Automating deployment workflows

**Note:** This directory is not required for running the game and can be safely deleted.

## game_engine_tools/
Development utilities for performance profiling and debugging:
- Performance monitoring tools
- Debug utilities for game state inspection
- Development-only testing helpers

**Note:** These tools are only needed during development. This directory can be safely deleted for production builds.

## Cleanup
Both `spyher_tools/` and `game_engine_tools/` directories are optional development utilities. If you want to reduce the project size or prepare a clean distribution, you can remove both directories without affecting the core game functionality.