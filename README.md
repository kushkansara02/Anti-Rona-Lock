## ABOUT 

**Project Motivation**: 
COVID-19, Anti-maskers, People ignoring distancing regulations in public

**Function**: 
Our project takes pictures of people who wish to enter a building/room through a door. It determines whether masks are being worn and some distance is being maintained between individuals. If either of these conditions are not met, the door remains locked. Only when both conditions are satisfied is the door unlocked automatically.

**Approach**: 
We decided to use an Arduino as the microcontroller which would manipulate our lock, powered by a servo motor. The camera module we decided on had the ability to connect to the internet, which made sending images to our server (a computer) much easier. We decided to code in python, which allowed the use of the OpenCV library for image manipulation. We resolved that TensorFlow could be implemented for mask detection whereas Haar Cascades would suffice for distance detection, which only required detecting faces in an image.

## COLLABORATORS

*Aaditya Yadav* \
*David Xu* \
*Kevin Xu* \
*Kush Kansara* \
*William Xu*