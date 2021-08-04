# MultiAgentHide-Seek
A multi-agent hide and seek game where the hider will learn to effectively hide from the seeker and the seeker will learn to catch the hider progressively using reinforcement learning algorithms.

An application which consists of a game arena that is the environment, few agents (just one hider and seeker for now, but the number can be easily increased).
Hiders and seekers have different set of policies on basis of which they are rewarded. The reward is a numerical value. For seeker, following are some example policies/ cases which decide his reward:
1) How much area has he covered till now?
2) How close is he to the hider?
3) Is he colliding with the wall?
4) Has he caught the hider? i.e. Is the hider in seeker’s vision radius?
For hider, following are some example policies/ cases which decide his reward:
1) How much area has he covered till now?
2) How close is he to the seeker?
3) Is he colliding with the wall?
4) Is he hiding successfully? i.e. Is he away from the seeker’s vision radius?

On basis these policies, the agent is granted a positive reward(incentive) is a negative reward(penalty), according to his present state in the environment.

Q-learning reinforcement learning algorithm is used, which seeks to find the best action to take given the current state. New actions can be explored or a old action can be reused (Exploration/ exploitation), which is decided by the Q-Learning algorithm at run-time.

Coming to the flexibility of movement, agent can move a single unit right/left/up/down and rotate by an angle in a single action. In exploration, every action that the agent performs is selected randomly. After random selection of an action, the action is validated. Checks are made to ensure that action is within the arena and the agents doesn’t overlap the walls. Wall collisions are taken care of. If everything is in place, then the action is performed and additions are made to the Q-Table.

A dashboard is added, in which current state of environment, rewards of the agents and selected agent’s vision to be displayed can be selected.
A version of our Q-Table is also included in the files.



https://user-images.githubusercontent.com/53032545/128169329-58ba3f80-7972-46e6-b657-c6805cc3b8d5.mp4

