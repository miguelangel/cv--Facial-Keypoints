## TODO: define the convolutional neural network architecture

import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
# can use the below import should you choose to initialize the weights of your Net
import torch.nn.init as I


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        
        ## TODO: Define all the layers of this CNN, the only requirements are:
        ## 1. This network takes in a square (same width and height), grayscale image as input
        ## 2. It ends with a linear layer that represents the keypoints
        ## it's suggested that you make this last layer output 136 values, 2 for each of the 68 keypoint (x, y) pairs

        ## Note that among the layers to add, consider including:
        #    - maxpooling layers,
        #    - multiple conv layers,
        #    - fully-connected layers,
        #    - other layers (such as dropout or batch normalization)
        #      to avoid overfitting

        # As an example, you've been given a convolutional layer, which you may (but don't have to) change:
        
        # Input:
        #    - 1 input image channel (grayscale), 
        #      32 output channels/feature maps,
        #      5x5 square convolution kernel
        # Output:
        #    - size = (W-F)/S +1 = (224-5)/1 + 1 = 220
        #  the output Tensor for one image, will have the dimensions: (32, 220, 220)
        #  after one pool layer, this becomes (32, 110, 110)
        self.conv1 = nn.Conv2d(1, 32, 5)
                               
        # Input size: (32, 110, 110)
        # Output size: (W - F)/S + 1
        #              (110 - 5)/1 + 1 = 106 --> (64, 106, 106)
        # After a pool layer, it becomes (64, 53, 53)
        self.conv2 = nn.Conv2d(32, 64, 5)
                
        # Input size: (64, 53, 53)
        # Output size: (W - F)/S + 1        
        #              (53 - 5)/1 + 1 = 49 --> (128, 49, 49)
        # After a pool layer, it becomes (128, 24, 24)
        self.conv3 = nn.Conv2d(64, 128, 5)        
        
        # Input size: (128, 24, 24)
        # Output size: (W - F)/S + 1
        #              (24 - 5)/1 + 1 = 20 --> (256, 20, 20)
        # After another pool layer, this becomes (256, 10, 10)
        self.conv4 = nn.Conv2d(128, 256, 5)
                               
        # At this moment we will flatten: 256*10*10 = 12800        
        self.fc1 = nn.Linear(256*10*10, 6000)
        self.fc2 = nn.Linear(6000, 3000)
        self.fc3 = nn.Linear(3000, 1000)
        self.fc4 = nn.Linear(1000, 136)        

        # maxpool layer with kernel_size=2, stride=2
        self.pool = nn.MaxPool2d(2, 2)
        
        # Different dropouts
        self.drop1 = nn.Dropout(p=0.1)
        self.drop2 = nn.Dropout(p=0.2)
        
        
        
    def forward(self, x):
        ## TODO: Define the feedforward behavior of this model
        ## x is the input image and, as an example, here you may choose to include a pool/conv step:
        ## x = self.pool(F.relu(self.conv1(x)))
        
        # conv + activation + pool + drop
        x = self.drop1(self.pool(F.leaky_relu(self.conv1(x))))
        x = self.drop2(self.pool(F.leaky_relu(self.conv2(x))))
        x = self.drop2(self.pool(F.leaky_relu(self.conv3(x))))
        x = self.pool(F.leaky_relu(self.conv4(x)))
        
        
        # this line of code is the equivalent of Flatten in Keras
        x = x.view(x.size(0), -1)
        
        # linear layers
        x = self.drop2(F.leaky_relu(self.fc1(x)))
        x = self.drop2(F.leaky_relu(self.fc2(x)))
        x = self.drop2(F.leaky_relu(self.fc3(x)))
        x = F.leaky_relu(self.fc4(x))
        
        # a modified x, having gone through all the layers of your model, should be returned
        return x
