# AI-snake-game
## Getting Started

Clone the repo and enter the project directory:

```
git clone https://github.com/YourUser/ai-snake-game.git
cd ai-snake-game
```
Install the required Python packages:

```
pip install torch pygame numpy matplotlib
```
## Usage
1. Train the AI agent
```
python agent.py
```
This will open a Pygame window and start training. The training curve will display live, and the best model will be saved to model/model.pth.

2. (Optional) Headless training
If you want to train without rendering (faster), edit the instantiation in agent.py:

```
# in agent.py
game = SnakeGameAI(render=False)
```
Then re-run:
```
python agent.py
```
3. Play manually
```
python snake_game_human.py
```
Use the arrow keys to control the snake in the Pygame window.
