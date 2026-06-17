# This is to generate a "fake" image tensor and pass it through your untrained network just to ensure the plumbing works

import torch
from model import DashboardLightCNN

def test_architecture():
    print("Initializing DashboardLightCNN...")
    # Initialize the model for 4 categories
    model = DashboardLightCNN(num_classes=4)
    
    # Create a dummy image tensor matching PyTorch's format: [Batch Size, Channels, Height, Width]
    # We are simulating a single RGB image resized to 128x128
    dummy_image = torch.randn(1, 3, 128, 128)
    
    print(f"Input shape: {dummy_image.shape}")
    
    # Pass the dummy image through the network
    try:
        output = model(dummy_image)
        print(f"Output shape: {output.shape}")
        print("Success! The tensor dimensions are calculated correctly.")
        print(f"Raw output logits: {output.detach().numpy()}")
    except RuntimeError as e:
        print(f"Architecture Error: {e}")

if __name__ == "__main__":
    test_architecture()