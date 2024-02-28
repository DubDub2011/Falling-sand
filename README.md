# Falling Sand

Solution for https://www.youtube.com/watch?v=L4u7Zy_b868

Had a couple of annoying bugs with this one, but was a good project in the end:

Key takeaways:
- Python is really really nice to work with, I see why it's become a popular language
- Tried to do a bit of TDD with this one, and while it was good fun, very clear to see it doesn't suit programming on the fly, need to have a defined spec before you start, which probably isn't great for these 'figure it out as you go' style of challenges, will be much better for the challenges from John Crickett https://codingchallenges.fyi/ although it was really helpful at times, can see a lot of value in having a lot of tests that you can use to run test cases against.
- Figuring out bugs in graphical simulations aren't easy! Need to do things very iteratively else you can quickly write a lot of code, not test it and then be unclear where things went wrong. As it's a simulation, it's hard to recreate the exact situation and follow through the data structure in your debugger at a larger scale. (This is where I found TDD really helpful, before deciding to stop doing it haha)

## Setup
- Make sure you have pygame installed (see https://www.pygame.org/wiki/GettingStarted)
- Run in your terminal `python main.py`
- Enjoy falling sand! (you can increase the size of your brush by scrolling up or down)

## Future improvements
Don't plan on coming back to this one, really happy with the final outcome at the moment, but...
- Add a circle around the mouse to indicate the brush size, just a nicety
- Add a way to reset the simulation, maybe even a menu?
- Start to notice performance issues when filling up the screen, tested this and the functionality I've added for avoiding processing particles that are locked in place is working, meaning it's the pygame library that's starting to struggle, could probably improve this by not redrawing the static particles, but for now it's easily processing lot of particles so happy to leave it as is.
