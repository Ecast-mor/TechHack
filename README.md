# Echo Sign

Echo Sign is an interactive, real-time American Sign Language (ASL) recognition game. Players are tasked with recreating ASL letters shown on screen to serve animated customers in a tavern setting. The game uses computer vision to track hand landmarks in 3D space and verify the player's signs.

## Features
* **Real-Time ASL Recognition:** Detects static ASL alphabet signs using 3D spatial coordinate mapping.
* **Dynamic Motion Tracking:** Specialized logic to detect moving signs like 'J' (hook motion) and 'Z' (zig-zag motion).
* **Multithreaded Performance:** The computer vision pipeline and the game engine run on separate threads, communicating via thread-safe queues to ensure smooth, lag-free gameplay.
* **Gamified Interface:** Features animated sprites, a tavern background, and a scroll-based UI.

## Prerequisites
Ensure you have Python 3.13 installed. You will need the following libraries:

```bash
pip install pygame opencv-python mediapipe numpy
```
## Credits:

https://craftpix.net
https://eeveeexpo.com/resources/1609/
https://www.youtube.com/watch?v=LnmY5Rgpb1Y&list=RD4WIMyqBG9gs&index=11
https://www.pngegg.com/en/png-ebtas
https://glazermuseum.org/signlanguageabcs/