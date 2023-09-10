 # Setup Instructions:
 * Clone the whole repository.
 * Make sure anaconda/miniconda is installed.
 * Create a custom conda virtual environmen: `conda env create -f env_setup\NEAT-venv.yml`.
 * Run game: `NEAT_FlappyBird.py`.

 # Configure Game (line 20-22):
 * Set maximum number of generations before terminating `MAX_GENERATIONS`.
 * Set `MODE` to change game behaviour:
    * `MODE = 'train'` → Train NEAT Networks & save best genome.
    * `MODE = 'restore_train'` → Restore training from a checkpoint.
    * `MODE = 'run'` → Run a saved genome from file.
    * `MODE = 'play'` → Play game with manual keyboard input.
 * Set `DRAW_LINES` to visualize NN's view of the pipes (off automatically in `run` & `play` configurations).

 # Configuring NEAT:
 * Modify contents of `NEAT_configs\config-feedforward.txt` to your requirements.
