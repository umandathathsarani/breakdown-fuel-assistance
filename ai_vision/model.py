import torch
import torch.nn as nn
import torch.nn.functional as F

class DashboardLightCNN(nn.Module):
    def __init__(self, num_classes=4):
        super(DashboardLightCNN, self).__init__()
        
        # 1st Convolutional Layer
        # Input: 3 color channels (RGB). Output: 16 feature maps.
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, padding=1)
        
        # 2nd Convolutional Layer
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1)
        
        # 3rd Convolutional Layer
        self.conv3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
        
        # Pooling Layer (Halves the image dimensions each time it is used)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Fully Connected Layers
        # If we input a 128x128 image, after 3 pooling layers (128 -> 64 -> 32 -> 16), the dimensions become 16x16. 
        # Total flattened features = 64 channels * 16 width * 16 height = 16384
        self.fc1 = nn.Linear(64 * 16 * 16, 512)
        
        # Output layer matches the number of warning light categories
        self.fc2 = nn.Linear(512, num_classes)

    def forward(self, x):
        # Pass through Conv1 -> ReLU Activation -> MaxPool
        x = self.pool(F.relu(self.conv1(x)))
        
        # Pass through Conv2 -> ReLU -> MaxPool
        x = self.pool(F.relu(self.conv2(x)))
        
        # Pass through Conv3 -> ReLU -> MaxPool
        x = self.pool(F.relu(self.conv3(x)))
        
        # Flatten the 3D tensor into a 1D vector for the Dense layers
        x = x.view(-1, 64 * 16 * 16) 
        
        # Pass through Fully Connected Layers
        x = F.relu(self.fc1(x))
        x = self.fc2(x) # Final output probabilities
        
        return x