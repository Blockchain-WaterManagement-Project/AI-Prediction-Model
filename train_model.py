import pandas as pd
import torch
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Define the Transformer model (same as in app.py)
class TransformerModel(torch.nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers, nhead=3):
        super(TransformerModel, self).__init__()
        self.encoder_layer = torch.nn.TransformerEncoderLayer(d_model=input_size, nhead=nhead)
        self.transformer_encoder = torch.nn.TransformerEncoder(self.encoder_layer, num_layers=num_layers)
        self.fc = torch.nn.Linear(input_size, output_size)

    def forward(self, x):
        x = x.unsqueeze(1).transpose(0, 1)
        x = self.transformer_encoder(x)
        x = x[-1, :, :]
        return self.fc(x)

# Load data
print("Loading dataset...")
data = pd.read_csv("water_potability.csv")
data.fillna(data.median(), inplace=True)

# Prepare data
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
print("Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define and train model
print("Initializing model...")
model = TransformerModel(input_size=9, hidden_size=64, output_size=1, num_layers=4)
criterion = torch.nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Convert to tensors
print("Converting data to tensors...")
X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

# Training loop
print("Starting training...")
for epoch in range(100):
    model.train()
    optimizer.zero_grad()
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)
    loss.backward()
    optimizer.step()
    if (epoch+1) % 10 == 0:
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

# Save model and scaler
print("Saving model files...")
torch.save(model, 'water_quality_model.pth')
joblib.dump(scaler, 'scaler.pkl')

print("Model training complete! Files saved:")
print("- water_quality_model.pth")
print("- scaler.pkl")
