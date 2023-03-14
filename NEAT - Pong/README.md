 # Setup Instructions:
 * Clone the whole repository.
 * Make sure anaconda/miniconda is installed.
 * Create a custom conda virtual environmen: `conda env create -f env_setup\NEAT-venv.yml`.
 * Run game: `NEAT_Pong.py`.

 # Configure Game (`NEAT_Pong.py`):
 * Set maximum number of generations before terminating `MAX_GENERATIONS`.
 * Set `MODE` to change game behaviour:
    * `MODE = 'pp'` → Player vs Player.
    * `MODE = 'ap'` → AI(left) vs Player(right).
    * `MODE = 'pa'` → Player(left) vs AI(right).
    * `MODE = 'aa'` → AI vs AI.
    * `MODE = 'train'` → AI training configuration.
    * `MODE = 'restore_train'` → Restore training from a checkpoint.
        * (changes to NEAT config won't take effect when restoring from a checkpoint)      

# Player Inputs:
 * RHS Player Up → `↑`
 * RHS Player Down → `↓`
 * LHS Player Up → `w`
 * LHS Player Down → `s`

 # Configuring NEAT:
 * Modify contents of `NEAT-configs\config-feedforward.txt` to your requirements.