import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from model import DashboardLightCNN
import os

def train_model():
    # 1. Define hyperparameters
    batch_size = 16
    learning_rate = 0.001
    num_epochs = 10
    
    # Setup path to your dataset (matches your current folder structure)
    dataset_path = os.path.join(os.path.dirname(__file__), 'dataset', 'train')
    
    # 2. Image Transformations
    # AI models need consistent data. We resize all images to 128x128 and convert them to Tensors.
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        # Normalize to help the network learn faster
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]) 
    ])

    # 3. Load the Dataset
    try:
        train_dataset = datasets.ImageFolder(root=dataset_path, transform=transform)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        print(f"Successfully loaded {len(train_dataset)} images from {len(train_dataset.classes)} classes.")
        print(f"Classes found: {train_dataset.class_to_idx}")
    except FileNotFoundError:
        print(f"Error: Could not find dataset at {dataset_path}. Please add images first.")
        return

    # 4. Initialize the Model, Loss Function, and Optimizer
    # We use 4 classes based on your folders: battery, engine, fuel, oil
    model = DashboardLightCNN(num_classes=len(train_dataset.classes))
    
    # CrossEntropyLoss is standard for multi-class classification
    criterion = nn.CrossEntropyLoss()
    
    # Adam optimizer is highly efficient for CNNs
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # 5. The Training Loop
    print("\nStarting training...")
    for epoch in range(num_epochs):
        running_loss = 0.0
        
        for images, labels in train_loader:
            # Zero the parameter gradients
            optimizer.zero_grad()

            # Forward pass: predict the classes
            outputs = model(images)
            
            # Calculate the loss (how wrong the predictions were)
            loss = criterion(outputs, labels)
            
            # Backward pass: compute the gradients
            loss.backward()
            
            # Optimize: adjust the weights
            optimizer.step()

            running_loss += loss.item()

        # Print statistics for this epoch
        avg_loss = running_loss / len(train_loader)
        print(f"Epoch [{epoch+1}/{num_epochs}] - Average Loss: {avg_loss:.4f}")

    # 6. Save the trained model
    save_path = os.path.join(os.path.dirname(__file__), 'dashboard_cnn.pt')
    torch.save(model.state_dict(), save_path)
    print(f"\nTraining complete! Model weights saved to {save_path}")

if __name__ == "__main__":
    train_model()